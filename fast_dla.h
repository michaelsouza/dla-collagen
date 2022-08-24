#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <math.h>
#include <stdexcept>
#include <vector>

#define MAX(a, b) (((a) > (b)) ? (a) : (b))

const double PI = 3.141592654;

// generate random number for the range (min, max)
double irand(int imin, int imax) {
  return (rand() / ((double)RAND_MAX)) * (imax - imin) + imin;
}

enum fiber_state_t { OVERLAP, FREE, BIND };

class fiber_t {
public:
  int m_uid;
  int m_x[3];
  int m_height;
  fiber_state_t m_state;

  fiber_t(int uid, int h, double radius) {
    m_uid = uid;
    m_height = h;
    random_reset(radius);
  }

  fiber_t(int uid, int h, int x, int y, int z) {
    m_uid = uid;
    m_height = h;
    m_x[0] = x;
    m_x[1] = y;
    m_x[2] = z;
    m_state = fiber_state_t::FREE;
  }

  void random_reset(double radius) {
    const double theta = irand(0, 2 * PI);
    const double phi = acos(irand(-1, 1));
    m_x[0] = radius * cos(theta) * sin(phi);
    m_x[1] = radius * sin(theta) * sin(phi);
    m_x[2] = radius * cos(phi);
    m_state = fiber_state_t::FREE;
  }

  void random_walk() {
    int &x = m_x[0];
    int &y = m_x[1];
    int &z = m_x[2];

    const int imove = rand() % 8;
    // (1, 0, 0)
    if (imove == 0)
      ++x;
    else if (imove == 1)
      --x;
    // (0, 1, 0)
    else if (imove == 2)
      ++y;
    else if (imove == 3)
      --y;
    // (0, 1, 1)
    else if (imove == 4) {
      ++z;
      ++y;
    } else if (imove == 5) {
      --z;
      --y;
    }
    // (0, 1, -1)
    else if (imove == 6) {
      ++y;
      --z;
    } else if (imove == 7) {
      --y;
      ++z;
    }
  }

  /**
 * @brief Retorna true se houver ao menos uma face compartilhada e false em caso
 *        contrário.
 *
 * @param umin
 * @param umax
 * @param p
 * @return true
 * @return false
 */
inline int num_shared_faces(fiber_t& u) {
  // verificação/identificação da face em contato com a fxmin ou ftop
  //           (1,0,1) +-------------------------+ (1,h,1) = umax
  //                 / |z                       /|
  //        (0,0,1) +--------------------------+ |
  //                |  +-----------------------|-+ (1,h,0)
  //                | /x                       |/
  // umin = (0,0,0) +--------------------------+ (0,h,0)
  //                             y
  const int umin_x = u.m_x[0];
  const int umin_y = u.m_x[1];
  const int umin_z = u.m_x[2];

  const int umax_x = u.m_x[0] + 1;
  const int umax_y = u.m_x[1] + m_height;
  const int umax_z = u.m_x[2] + 1;

  const int pmin_x = m_x[0];
  const int pmin_y = m_x[1];
  const int pmin_z = m_x[2];

  const int pmax_x = m_x[0] + 1;
  const int pmax_y = m_x[1] + m_height;
  const int pmax_z = m_x[2] + 1;

  // não compartilha qualquer face
  const bool pmin_inside = umin_y <= pmin_y && pmin_y < umax_y;
  const bool pmax_inside = umin_y < pmax_y && pmax_y <= umax_y;
  if (!pmin_inside && !pmax_inside)
    return 0;

  if (pmin_x == umin_x && pmin_z == umin_z)
  {
    m_state = OVERLAP;
    return 0;
  }

  int num_faces = 0;
  if( pmin_inside )
    num_faces = umax_y - pmin_y;
  else // pmax_inside == true
    num_faces = pmax_y - umin_y;

  // compartilha a face da frente
  if ((umin_x - 1) == pmin_x && umin_z == pmin_z)
    return num_faces;

  // compartilha a face de cima
  if (umin_x == pmin_x && umax_z == pmin_z)
    return num_faces;

  // compartilha a face de trás
  if (umax_x == pmin_x && umin_z == pmin_z)
    return num_faces;

  // compartilha a face de baixo
  if (umin_x == pmin_x && (umin_z - 1) == pmin_z)
    return num_faces;

  return 0;
}

  void show()
  {
    printf("uid: %d, x:(%d,%d,%d)\n", m_uid, m_x[0], m_x[1], m_x[2]);
  }
};

class kdt_t {
public:
  int m_level;
  int m_xmin[3];
  int m_xmax[3];
  int m_dx[3];
  int m_height;
  int m_max_node_size;
  kdt_t *m_lft;
  kdt_t *m_rht;
  std::vector<int> m_uids;
  int m_id;
  static int m_k; // number of created kdt entities

  kdt_t(int max_num_uids, int height) {
    m_level = 0;
    m_lft = nullptr;
    m_rht = nullptr;
    m_max_node_size = max_num_uids;
    m_height = height;
    m_dx[0] = 1;
    m_dx[1] = height;
    m_dx[2] = 1;
    m_id = kdt_t::m_k++;
  }

  ~kdt_t() {
    if(m_lft != nullptr)
      m_lft->~kdt_t();
    if(m_rht != nullptr)
      m_rht->~kdt_t();    
    delete m_rht;
    delete m_lft;
  }

  /**
   * @brief
   *
   * @param uid
   * @param fibers
   */
  void add(int uid, std::vector<fiber_t> &fibers) {
    fiber_t &f = fibers[uid];    
    // primeira fibra
    if (m_uids.size() == 0 && m_lft == nullptr) {
      // inicializa o bounding box
      for (int i = 0; i < 3; ++i) {
        m_xmin[i] = f.m_x[i];
        m_xmax[i] = f.m_x[i] + m_dx[i];
      }
    } else {
      // atualiza o bounding box
      for (int i = 0; i < 3; ++i) {
        if (m_xmin[i] > f.m_x[i])
          m_xmin[i] = f.m_x[i];
        if (m_xmax[i] < f.m_x[i] + m_dx[i])
          m_xmax[i] = f.m_x[i] + m_dx[i];
      }
    }

    // sem filhos
    if (m_lft == nullptr) {
      m_uids.push_back(uid);
      if (m_uids.size() > m_max_node_size)
        split(fibers);
    } else {
      // adiciona ao filho que menos é afetado pela entrada da nova fibra
      int d, d_lft = 0, d_rht = 0;
      for (int i = 0; i < 3; ++i) {
        d = MAX(m_lft->m_xmin[i] - f.m_x[i],
                f.m_x[i] + m_dx[i] - m_lft->m_xmax[i]);
        if (d_lft < d)
          d_lft = d;
      }
      for (int i = 0; i < 3; ++i) {
        d = MAX(m_rht->m_xmin[i] - f.m_x[i],
                f.m_x[i] + m_dx[i] - m_rht->m_xmax[i]);
        if (d_rht < d)
          d_rht = d;
      }

      if (d_lft < d_rht)
        m_lft->add(uid, fibers);
      else
        m_rht->add(uid, fibers);
    }
  }

  /**
   * @brief
   *
   * @param fibers
   */
  void split(std::vector<fiber_t> &fibers) {
    // aloca os filhos
    m_lft = new kdt_t(m_max_node_size, m_height);
    m_rht = new kdt_t(m_max_node_size, m_height);
    m_lft->m_level = m_level + 1;
    m_rht->m_level = m_level + 1;

    // identifica a direção do corte como sendo a mais longa
    int d[3] = {m_xmax[0] - m_xmin[0] - m_dx[0],
                m_xmax[1] - m_xmin[1] - m_dx[1],
                m_xmax[2] - m_xmin[2] - m_dx[2]};

    int imax = 0;
    for (int i = 0; i < 3; ++i)
      if (d[i] > d[imax])
        imax = i;

    std::vector<int> v;
    for (auto &&uid : m_uids)
      v.push_back(fibers[uid].m_x[imax]);
    std::sort(v.begin(), v.end());
    int x = v[v.size() / 2]; // mediana

    // divide os filhos pela mediana
    for (auto &&uid : m_uids)
      fibers[uid].m_x[imax] < x ? m_lft->add(uid, fibers)
                                : m_rht->add(uid, fibers);

    if (m_lft->m_uids.size() == 0 || m_rht->m_uids.size() == 0) {
      printf("split failed (empty child)\n");
      exit(EXIT_FAILURE);
    }

    // libera as fibras
    m_uids.clear();
  }

  /**
   * @brief Retorna os índices das fibras no kdtree que podem 
   *        estar em contato com a fibra f.
   *
   * @param neighs lista dos uids do vizinhos
   */
  void get_node_neighs(const fiber_t &f, std::vector<int> &neighs) {
    // inicializacao do n
    if (m_level == 0)
      neighs.clear();

    bool touch = true;
    for (int i = 0; i < 3 && touch; ++i)
      if ((f.m_x[i] < (m_xmin[i] - m_dx[i])) ||
          (m_xmax[i] < f.m_x[i]))
      {
        touch == false;
        return;
      }

    if (m_uids.size() == 0) {
      m_lft->get_node_neighs(f, neighs);
      m_rht->get_node_neighs(f, neighs);
      return;
    }

    // add to neighs all uids
    for (auto &&uid : m_uids)
      neighs.push_back(uid);
  }

  // calc diametro entre xmin e xmax
  int diameter() {
    int diam = 0;
    for (int i = 0; i < 3; ++i) {
      auto d = m_xmax[i] - m_xmin[i];
      diam += d * d;
    }
    return int(std::sqrt(diam)) + 1;
  }
};
int kdt_t::m_k = 0;


/**
 * @brief      Se f estiver em overlap com alguma fibra, seu estado é alterado
 * para OVERLAP, caso contrário, uids é atualizado para os índices das fibras em
 * contato com f.
 *
 * @param f    Fibra a ser avaliada.
 * @param uids Na entrata, é o vetor de índices das fibras que podem estar em
 * contato com a fibra f. Na saída, é atualizado para os índices que estão
 * efetivamente em contato com f.
 * @param fibers vetor de todas as fibras do cluster.
 */
void filter_shared_faces(fiber_t &f, std::vector<int>& uids, std::vector<fiber_t> &fibers) {
  // verificação/identificação da face em contato com a fxmin ou ftop
  //           (1,0,1) +-------------------+------+ (1,h,1) = umax
  //                 / |z                 /|     /|
  //        (0,0,1) +--------------------+-|----+ |
  //                |  |-----------------|-+----|-+ (1,h,0)
  //                | /x                 |/     |/
  // umin = (0,0,0) +--------------------+-----+ (0,h,0)
  //                             y       utop = (0,h-1,0)

  f.m_state = FREE;
  int k = 0; // número de fibras do cluster em contato com a fibra f
  for (int i = 0; i < uids.size(); ++i)
  {
    int uid = uids[i];
    fiber_t &u = fibers[uid];
    int num_faces = f.num_shared_faces(u);
    if (f.m_state == OVERLAP)
    {
      k = 0;
      break;
    }
    if (num_faces > 0)
      uids[k++] = uid;
  }
  uids.resize(k);
}

/**
 * @brief
 *
 * @param f
 * @param max_dist
 * @param radius
 * @return true
 * @return false
 */
inline bool check_out_sim(fiber_t &f, int max_dist, int radius) {

  for (int i = 0; i < 3; ++i)
    if (std::abs(f.m_x[i]) > max_dist * radius)
      return true;
  return false;
}

/**
 * @brief Verifica se a fibra está em bind com o cluster.
 *
 * @param f
 * @param n
 * @param uids
 * @param fibers
 * @param mode
 * @return true
 * @return false
 * @remark Se a fibra estiver em overlap, seu estado é alterado para OVERLAP.
 */
inline bool check_bind(fiber_t &f, std::vector<int> &uids,
                       std::vector<fiber_t> &fibers, char mode) {
  filter_shared_faces(f, uids, fibers);
  if (f.m_state == OVERLAP || uids.size() == 0)
    return false;

  if (mode == 's') {
    for (auto &&uid : uids) {
      fiber_t &u = fibers[uid];
      // checa se a base de u está em bind com f
      for (int i = 0; i <= 4; ++i)
        if (u.m_x[1] == (f.m_x[1] + 4 * i))
          return true;

      // checa se a base de f está em bind com u
      for (int i = 0; i <= 4; ++i)
        if (f.m_x[1] == (u.m_x[1] + 4 * i))
          return true;
    }
  } else if (mode == 'n') {
    for (auto &&uid : uids) {
      fiber_t &u = fibers[uid];

      // checa se a base de u está em bind com f
      if (f.m_x[1] <= u.m_x[1] && u.m_x[1] < (f.m_x[1] + f.m_height))
        return true;

      // checa se a base de f está em bind com u
      if (u.m_x[1] <= f.m_x[1] && f.m_x[1] < (u.m_x[1] + f.m_height))
        return true;
    }
  }
  return false;
}

/**
 * @brief Retorna o número de faces expostas.
 *
 * @param f
 * @param kdt
 * @param fibers
 * @return int
 * @remark O número máximo de faces expostas é 4 * f.m_height.
 */
int energy_surface(fiber_t &f, std::vector<int> &neighs, std::vector<fiber_t> &fibers, kdt_t &kdt) {
  //     .+------+
  //   .' | N  .'|
  //  +------+'  |
  //  | W |  | E |
  //  |  ,+--|---+
  //  |.'  S | .'
  //  +------+'
  
  int energy = 4 * f.m_height;
  for (auto &&uid : neighs) {
    fiber_t &u = fibers[uid];
    energy -= f.num_shared_faces(u);
  }
  return energy;
}

void rolling_surface(fiber_t &f, std::vector<int>& neighs, std::vector<fiber_t> &fibers,
                     char mode, int tmax, kdt_t &kdt) {
  int xold[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int xopt[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int Emin = energy_surface(f, neighs, fibers, kdt);
  // printf(">> Emin: %d " , Emin); f.show();
  int E = 0;
  for (int ts = 0; ts < tmax; ++ts) {    
    f.random_walk();
    // printf("rolling_walk:"); f.show();
    
    kdt.get_node_neighs(f, neighs);    
    if (neighs.size() == 0){
      // restaura a solução anterior
      f.m_state = BIND;
      for (auto i = 0; i < 3; ++i)
        f.m_x[i] = xold[i];
      continue;
    }

    if(check_bind(f, neighs, fibers, mode)){
      E = energy_surface(f, neighs, fibers, kdt);
      // printf(">> E: %d\n" , E);
      if(E < Emin){
        Emin = E;
        for (auto i = 0; i < 3; ++i)
          xopt[i] = f.m_x[i];
        // printf(">> Emin: %d " , Emin); f.show();
      }
      for (auto i = 0; i < 3; ++i)
        xold[i] = f.m_x[i];
      continue;
    }

    f.m_x[0] = xold[0];
    f.m_x[1] = xold[1];
    f.m_x[2] = xold[2];    
  }
  for (auto i = 0; i < 3; ++i)
    f.m_x[i] = xopt[i];
  // printf(">> Emin: %d " , Emin); f.show();
}


int test_kdt()
{
  const int height = 18;
  int max_node_size = 5;
  std::vector<fiber_t> fibers;

  // first fiber
  int uid = 0;
  int x = 0;
  int y = -height / 2;
  int z = 0;
  fibers.push_back(fiber_t(uid, height, x, y, z));

  kdt_t kdt(max_node_size, height);
  kdt.add(uid, fibers);
  fibers[uid].show();

  std::vector<int> neighs;

  for(int i = 1; i < 15; ++i){
    ++uid;
    fibers.push_back(fiber_t(uid, height, x + i, y, z));
    fiber_t& f = fibers[uid];
    kdt.get_node_neighs(f, neighs);
    kdt.add(uid, fibers);
  }
  return EXIT_SUCCESS;
}

int run_dla(int argc, char const *argv[]) {
  const int num_bind = 15;
  const char mode = 'n';
  const int tmax = 10;

  const int height = 18;
  int max_kdt_node_size = 15;
  int max_dist = 10;
  std::vector<fiber_t> fibers;

  // first fiber
  int uid = 0;
  int x = 0;
  int y = -height / 2;
  int z = 0;
  fibers.push_back(fiber_t(uid, height, x, y, z));

  kdt_t kdt(max_kdt_node_size, height);
  kdt.add(uid, fibers);
  fibers[uid].show();

  std::vector<int> neighs;
  int xold[3];

  while (uid < num_bind) {
    const int radius = kdt.diameter();

    fibers.push_back(fiber_t(++uid, height, radius));
    fiber_t &f = fibers[uid];
    bool reset_fiber = false;

    while (true) {
      if (reset_fiber) {
        f.random_reset(radius);
        reset_fiber = false;
      }

      // save current position
      for (int i = 0; i < 3; ++i)
        xold[i] = f.m_x[i];

      // random walk
      f.random_walk();
      // printf(">> random_walk:"); f.show();

      // check out of simulation?
      if (check_out_sim(f, max_dist, radius)) {
        // printf(">> out_sim:"); f.show();
        reset_fiber = true;
        continue;
      }

      // get possible neighs
      kdt.get_node_neighs(f, neighs);

      if (neighs.size() == 0)
        continue;

      // check bind
      if (check_bind(f, neighs, fibers, mode)) {
        printf(">> bind:");
        rolling_surface(f, neighs, fibers, mode, tmax, kdt);
        printf(">> rolling:"); f.show();
        kdt.add(uid, fibers);
        break;
      }

      // check overlap
      if (f.m_state == OVERLAP) {
        printf(">> overlap:"); f.show();
        // restore x
        for (int i = 0; i < 3; ++i)
          f.m_x[i] = xold[i];
        f.m_state = FREE;
        continue;
      }
    }
  }
}
