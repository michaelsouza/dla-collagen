// fast_dla2: optimized DLA fibril generator.
//
// Drop-in replacement for fast_dla with the same CLI and output format.
//
// Default mode is BIT-IDENTICAL to the original: it consumes the libc rand()
// stream in exactly the same order and takes exactly the same decisions, so
// the .dat output must match byte for byte.  The k-d tree is replaced by a
// hash map from (x,z) columns to y-sorted rod lists, which answers the exact
// contact/overlap query in O(log column) instead of a tree traversal, without
// touching the random stream.
//
// Optional accelerators (each changes the random-number consumption, so the
// output is statistically equivalent instead of bit-identical):
//   -rng fast    xoshiro256++ instead of libc rand(); also fixes the launch
//                angle truncation bug (irand(0, 2*PI) truncates 2*PI to 6).
//   -jumps 1     long jumps across empty space: while the walker is farther
//                than JUMP_TRIGGER from the (safety-expanded) cluster bounding
//                box, replace n = gap-1 unit steps by one Gaussian jump with
//                the walk's exact per-step covariance diag(0.6, 0.2, 0.6),
//                clipped to |d|<=n so the walker provably cannot touch the
//                cluster mid-jump.  CLT-exact for large n.
//   -coverstop 1 stop the surface-diffusion walk as soon as every position of
//                the reachable bound component has been visited; additional
//                steps can change neither the argmin nor the first-reached
//                tie-break, so the placement law is exactly the original one.
//
#include "fast_dla.h"
#include <chrono>
#include <cstdint>
#include <unordered_map>
#include <unordered_set>
#include <deque>

// ---------------------------------------------------------------- RNG layer
static int g_rng_fast = 0;
static uint64_t g_xs[4];

static inline uint64_t splitmix64(uint64_t &x) {
  uint64_t z = (x += 0x9e3779b97f4a7c15ULL);
  z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
  z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
  return z ^ (z >> 31);
}
static inline uint64_t rotl64(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t xnext() {
  const uint64_t r = rotl64(g_xs[0] + g_xs[3], 23) + g_xs[0];
  const uint64_t t = g_xs[1] << 17;
  g_xs[2] ^= g_xs[0]; g_xs[3] ^= g_xs[1]; g_xs[1] ^= g_xs[2]; g_xs[0] ^= g_xs[3];
  g_xs[2] ^= t; g_xs[3] = rotl64(g_xs[3], 45);
  return r;
}
static void rng_seed(unsigned int seed) {
  srand(seed);                       // libc path, identical to the original
  uint64_t s = seed;
  for (int i = 0; i < 4; ++i) g_xs[i] = splitmix64(s);
}
static inline int rnd_mod(int m) {
  return g_rng_fast ? (int)(xnext() % (uint64_t)m) : rand() % m;
}
static inline double rnd_unit() {   // uniform in [0,1]
  return g_rng_fast ? (xnext() >> 11) * 0x1.0p-53
                    : rand() / ((double)RAND_MAX);
}
static inline double rnd_normal() { // Box-Muller
  double u1 = rnd_unit(), u2 = rnd_unit();
  if (u1 < 1e-300) u1 = 1e-300;
  return std::sqrt(-2.0 * std::log(u1)) * std::cos(2.0 * M_PI * u2);
}

// Walk moves: copies of fiber_t::random_walk / rolling_random_walk that go
// through the RNG layer.  In libc mode the rand() calls happen in exactly the
// original order.
static inline void walk_volume(fiber_t &f) {
  int &x = f.m_x[0]; int &y = f.m_x[1]; int &z = f.m_x[2];
  const int imove = rnd_mod(10);
  if      (imove == 0) ++x;
  else if (imove == 1) --x;
  else if (imove == 2) ++z;
  else if (imove == 3) --z;
  else if (imove == 4) { ++x; ++z; }
  else if (imove == 5) { ++x; --z; }
  else if (imove == 6) { --x; --z; }
  else if (imove == 7) { --x; ++z; }
  else if (imove == 8) --y;
  else if (imove == 9) ++y;
}
static inline void walk_rolling(fiber_t &f) {
  int &x = f.m_x[0]; int &z = f.m_x[2];
  const int imove = rnd_mod(8);
  if      (imove == 0) ++x;
  else if (imove == 1) --x;
  else if (imove == 2) ++z;
  else if (imove == 3) --z;
  else if (imove == 4) { ++x; ++z; }
  else if (imove == 5) { ++x; --z; }
  else if (imove == 6) { --x; --z; }
  else if (imove == 7) { --x; ++z; }
}
static inline void launch_on_sphere(fiber_t &f, double radius) {
  if (!g_rng_fast) {
    // exactly the original irand-based reset, truncation bug included:
    // irand(0, 2*PI) receives imax = (int)(2*PI) = 6.
    const double theta = irand(0, 2 * PI);
    const double phi = acos(irand(-1, 1));
    f.m_x[0] = radius * cos(theta) * sin(phi);
    f.m_x[1] = radius * sin(theta) * sin(phi);
    f.m_x[2] = radius * cos(phi);
  } else {
    const double theta = rnd_unit() * 2.0 * M_PI;       // bug fixed
    const double phi = acos(2.0 * rnd_unit() - 1.0);
    f.m_x[0] = radius * cos(theta) * sin(phi);
    f.m_x[1] = radius * sin(theta) * sin(phi);
    f.m_x[2] = radius * cos(phi);
  }
  f.m_state = fiber_state_t::FREE;
}

// ------------------------------------------------------------- column store
class colmap_t {
public:
  int m_height;
  int m_xmin[3], m_xmax[3];
  bool m_empty = true;
  std::unordered_map<uint64_t, std::vector<std::pair<int,int>>> m_cols; // (y,uid)

  explicit colmap_t(int height) : m_height(height) {
    m_cols.reserve(1 << 14);
  }
  static inline uint64_t key(int x, int z) {
    return ((uint64_t)(uint32_t)x << 32) | (uint32_t)z;
  }
  void add(int uid, std::vector<fiber_t> &fibers) {
    const fiber_t &f = fibers[uid];
    const int dx[3] = {1, m_height, 1};
    if (m_empty) {
      for (int i = 0; i < 3; ++i) { m_xmin[i] = f.m_x[i]; m_xmax[i] = f.m_x[i] + dx[i]; }
      m_empty = false;
    } else {
      for (int i = 0; i < 3; ++i) {
        if (m_xmin[i] > f.m_x[i]) m_xmin[i] = f.m_x[i];
        if (m_xmax[i] < f.m_x[i] + dx[i]) m_xmax[i] = f.m_x[i] + dx[i];
      }
    }
    auto &v = m_cols[key(f.m_x[0], f.m_x[2])];
    auto it = std::lower_bound(v.begin(), v.end(), std::make_pair(f.m_x[1], -1));
    v.insert(it, {f.m_x[1], uid});
  }
  int diameter() const {                      // same formula as kdt_t
    int diam = 0;
    for (int i = 0; i < 3; ++i) { int d = m_xmax[i] - m_xmin[i]; diam += d * d; }
    return int(std::sqrt((double)diam)) + 1;
  }
  // uids in column (x,z) whose y-range shares at least one level with [y, y+h)
  inline void column_hits(int x, int z, int y, std::vector<int> &out) const {
    auto it = m_cols.find(key(x, z));
    if (it == m_cols.end()) return;
    const auto &v = it->second;
    const int lo = y - (m_height - 1);
    auto p = std::lower_bound(v.begin(), v.end(), std::make_pair(lo, INT32_MIN));
    for (; p != v.end() && p->first <= y + (m_height - 1); ++p)
      out.push_back(p->second);
  }
  // Exact contact/overlap query: neighs receives the uids of rods sharing at
  // least one face with f (the exact set filter_shared_faces would keep);
  // overlap is true when a rod occupies the same column with y-range overlap.
  void query(const fiber_t &f, std::vector<int> &neighs, bool &overlap) const {
    neighs.clear();
    overlap = false;
    // same O(1) rejection the kdt root performed: a walker outside the global
    // bounding box (with the contact margins) can touch nothing.
    const int dx[3] = {1, m_height, 1};
    for (int i = 0; i < 3; ++i)
      if (f.m_x[i] < m_xmin[i] - dx[i] || m_xmax[i] < f.m_x[i]) return;
    const int x = f.m_x[0], y = f.m_x[1], z = f.m_x[2];
    auto it = m_cols.find(key(x, z));
    if (it != m_cols.end()) {
      const auto &v = it->second;
      const int lo = y - (m_height - 1);
      auto p = std::lower_bound(v.begin(), v.end(), std::make_pair(lo, INT32_MIN));
      if (p != v.end() && p->first <= y + (m_height - 1)) { overlap = true; return; }
    }
    column_hits(x - 1, z, y, neighs);
    column_hits(x + 1, z, y, neighs);
    column_hits(x, z - 1, y, neighs);
    column_hits(x, z + 1, y, neighs);
  }
};

static inline bool bind_registry(const fiber_t &f, const std::vector<int> &neighs,
                                 std::vector<fiber_t> &fibers, char mode) {
  if (neighs.empty()) return false;
  if (mode == 's') {
    for (int uid : neighs)
      if ((f.m_x[1] - fibers[uid].m_x[1]) % 4 == 0) return true;
    return false;
  }
  // mode 'n': any face-sharing contact binds (the y-overlap condition of the
  // original check_bind is implied by face sharing between equal-height rods)
  return true;
}

static inline int energy2(fiber_t &f, const std::vector<int> &neighs,
                          std::vector<fiber_t> &fibers) {
  int energy = 4 * f.m_height;
  for (int uid : neighs) energy -= f.num_shared_faces(fibers[uid]);
  return energy;
}

// ------------------------------------------------------- surface relaxation
static void rolling2(fiber_t &f, std::vector<int> &neighs, std::vector<fiber_t> &fibers,
                     char mode, int tmax, const colmap_t &cm, int coverstop) {
  int xold[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int xopt[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int Emin = energy2(f, neighs, fibers);

  // Reachable bound component (8-connectivity in the x-z plane, y fixed).
  // Once every component position has been visited, later steps can change
  // neither the minimum nor the first-reached tie-break: stop early.
  size_t comp_size = SIZE_MAX;
  std::unordered_set<uint64_t> visited;
  if (coverstop) {
    const size_t cap = (size_t)std::min(tmax, 4096);
    std::unordered_set<uint64_t> comp;
    std::deque<std::pair<int,int>> bfs;
    fiber_t probe = f;
    comp.insert(colmap_t::key(f.m_x[0], f.m_x[2]));
    bfs.push_back({f.m_x[0], f.m_x[2]});
    std::vector<int> pn;
    bool capped = false;
    static const int DX[8] = {1,-1,0,0,1,1,-1,-1};
    static const int DZ[8] = {0,0,1,-1,1,-1,-1,1};
    while (!bfs.empty()) {
      auto [cx, cz] = bfs.front(); bfs.pop_front();
      for (int k = 0; k < 8; ++k) {
        const int nx = cx + DX[k], nz = cz + DZ[k];
        const uint64_t kk = colmap_t::key(nx, nz);
        if (comp.count(kk)) continue;
        probe.m_x[0] = nx; probe.m_x[2] = nz;
        bool ovl; cm.query(probe, pn, ovl);
        if (ovl || !bind_registry(probe, pn, fibers, mode)) continue;
        comp.insert(kk);
        if (comp.size() > cap) { capped = true; break; }
        bfs.push_back({nx, nz});
      }
      if (capped) break;
    }
    if (!capped) comp_size = comp.size();
    visited.reserve(comp.size() * 2);
    visited.insert(colmap_t::key(f.m_x[0], f.m_x[2]));
    if (visited.size() >= comp_size) {          // single-position component
      return;                                    // placement already optimal
    }
  }

  for (int ts = 0; ts < tmax; ++ts) {
    walk_rolling(f);                             // one RNG draw, as original
    bool ovl;
    cm.query(f, neighs, ovl);
    if (!ovl && neighs.empty()) {                // detached: reject move
      f.m_state = BIND;
      for (int i = 0; i < 3; ++i) f.m_x[i] = xold[i];
      continue;
    }
    if (!ovl && bind_registry(f, neighs, fibers, mode)) {
      const int E = energy2(f, neighs, fibers);
      if (E < Emin) { Emin = E; for (int i = 0; i < 3; ++i) xopt[i] = f.m_x[i]; }
      for (int i = 0; i < 3; ++i) xold[i] = f.m_x[i];
      if (coverstop) {
        visited.insert(colmap_t::key(f.m_x[0], f.m_x[2]));
        if (visited.size() >= comp_size) break;  // full coverage: done
      }
      continue;
    }
    for (int i = 0; i < 3; ++i) f.m_x[i] = xold[i];   // overlap or no registry
  }
  for (int i = 0; i < 3; ++i) f.m_x[i] = xopt[i];
}

// ------------------------------------------------------------- long jumps
static const int JUMP_TRIGGER = 24;   // minimum axis gap before jumping

// Largest per-axis gap between the walker and the cluster bounding box
// expanded by the rod height (a safety margin larger than any contact reach).
static inline int bbox_gap(const fiber_t &f, const colmap_t &cm) {
  int gap = 0;
  for (int i = 0; i < 3; ++i) {
    const int lo = cm.m_xmin[i] - cm.m_height;
    const int hi = cm.m_xmax[i] + cm.m_height;
    int g = 0;
    if (f.m_x[i] < lo) g = lo - f.m_x[i];
    else if (f.m_x[i] > hi) g = f.m_x[i] - hi;
    if (g > gap) gap = g;
  }
  return gap;
}

// Replace n unit steps by one sampled displacement.  Per-step variances of the
// volume walk: Var(dx)=Var(dz)=0.6, Var(dy)=0.2, zero covariances.  The
// displacement after n steps is bounded by n in each axis, so with n = gap-1
// the walker provably cannot touch the cluster inside the jump.
static inline void long_jump(fiber_t &f, int n) {
  const double sx = std::sqrt(0.6 * n), sy = std::sqrt(0.2 * n);
  for (int i = 0; i < 3; ++i) {
    const double s = (i == 1) ? sy : sx;
    long d = std::lround(rnd_normal() * s);
    if (d > n) d = n;
    if (d < -n) d = -n;
    f.m_x[i] += (int)d;
  }
}

// ------------------------------------------------------------------ driver
static void run_dla2(int tmax, int num_bind, char mode, unsigned int seed,
                     const char *output_dir, bool resume,
                     unsigned int continuation_seed, int jumps, int coverstop) {
  printf("mode ....... %c\n", mode);
  printf("tmax ....... %d\n", tmax);
  printf("num_bind ... %d\n", num_bind);
  printf("seed ....... %d\n", seed);
  printf("rng ........ %s\n", g_rng_fast ? "fast(xoshiro256++)" : "libc");
  printf("jumps ...... %d\n", jumps);
  printf("coverstop .. %d\n", coverstop);

  const unsigned int active_seed = resume ? continuation_seed : seed;
  printf("rng seed ... %d%s\n", active_seed, resume ? " (continuation)" : "");
  rng_seed(active_seed);

  const int height = 18;
  char arquivo[1024];
  const int len = snprintf(arquivo, sizeof(arquivo),
                           "%s/dla_mode_%c_ts_%d_nb_%d_seed_%d_.dat",
                           output_dir, mode, tmax, num_bind, seed);
  if (len < 0 || len >= (int)sizeof(arquivo)) {
    printf("The output filename is too long.\n");
    exit(EXIT_FAILURE);
  }

  const int max_dist = 2;
  std::vector<fiber_t> fibers;
  colmap_t cm(height);
  FILE *fid = nullptr;
  int uid;

  if (resume) {
    try { uid = load_fibers_for_resume(arquivo, height, fibers); }
    catch (const std::exception &e) {
      fprintf(stderr, "Could not resume %s: %s\n", arquivo, e.what());
      exit(EXIT_FAILURE);
    }
    for (auto &fb : fibers) cm.add(fb.m_uid, fibers);
    fid = fopen(arquivo, "a");
    if (!fid) { printf("The file %s could not be opened for appending.\n", arquivo); exit(EXIT_FAILURE); }
    printf("resuming ... uid %d\n", uid);
  } else {
    fid = fopen(arquivo, "w");
    if (!fid) { printf("The file %s could not be opened.\n", arquivo); exit(EXIT_FAILURE); }
    uid = 0;
    fibers.push_back(fiber_t(uid, height, 0, -height / 2, 0));
    cm.add(uid, fibers);
    fprintf(fid, "uid: %d %d %d %d\n", uid, 0, -height / 2, 0);
  }

  std::vector<int> neighs;
  int xold[3];

  while (uid < num_bind) {
    const int radius = cm.diameter();
    fibers.push_back(fiber_t(++uid, height, 0, 0, 0));
    fiber_t &f = fibers[uid];
    launch_on_sphere(f, radius);
    bool reset_fiber = false;

    while (true) {
      if (reset_fiber) { launch_on_sphere(f, radius); reset_fiber = false; }

      if (jumps) {
        const int gap = bbox_gap(f, cm);
        if (gap >= JUMP_TRIGGER) {
          long_jump(f, gap - 1);
          if (check_out_sim(f, max_dist, radius)) reset_fiber = true;
          continue;
        }
      }

      for (int i = 0; i < 3; ++i) xold[i] = f.m_x[i];
      walk_volume(f);

      if (check_out_sim(f, max_dist, radius)) { reset_fiber = true; continue; }

      bool ovl;
      cm.query(f, neighs, ovl);

      if (!ovl && neighs.empty()) continue;             // far from cluster

      if (!ovl && bind_registry(f, neighs, fibers, mode)) {
        rolling2(f, neighs, fibers, mode, tmax, cm, coverstop);
        f.save(fid);
        cm.add(uid, fibers);
        break;
      }

      if (ovl) {                                        // overlap: reject move
        for (int i = 0; i < 3; ++i) f.m_x[i] = xold[i];
        f.m_state = FREE;
        continue;
      }
      // touching but no registry: keep position (as original)
    }
  }
  fclose(fid);
}

int main(int argc, char const *argv[]) {
  int tmax = 100, num_bind = 1000, jumps = 0, coverstop = 0;
  char mode = 's';
  unsigned int seed = 1, continuation_seed = 1;
  bool resume = false;
  std::string output_dir = ".";

  for (int i = 1; i < argc; ++i) {
    if      (!strcmp(argv[i], "-ts")) tmax = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-mode")) mode = argv[++i][0];
    else if (!strcmp(argv[i], "-num_bind")) num_bind = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-seed")) seed = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-output_dir")) output_dir = argv[++i];
    else if (!strcmp(argv[i], "-resume")) resume = true;
    else if (!strcmp(argv[i], "-continuation_seed")) continuation_seed = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-rng")) g_rng_fast = !strcmp(argv[++i], "fast");
    else if (!strcmp(argv[i], "-jumps")) jumps = atoi(argv[++i]);
    else if (!strcmp(argv[i], "-coverstop")) coverstop = atoi(argv[++i]);
  }
  if (seed < 1) { printf("The parameter seed must greater than zero.\n"); return EXIT_FAILURE; }

  auto t0 = std::chrono::steady_clock::now();
  run_dla2(tmax, num_bind, mode, seed, output_dir.c_str(), resume, continuation_seed,
           jumps, coverstop);
  const double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  printf("elapsed .... %.2f s\n", secs);
  return EXIT_SUCCESS;
}
