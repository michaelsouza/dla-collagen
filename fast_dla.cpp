#include "fast_dla.h"
#include <chrono>
#include <cstring>
#include <iostream>

int main(int argc, char const *argv[]) {
  const int num_bind = 10;
  const char mode = 'n';
  const int tmax = 10;

  const int height = 18;
  int max_num_uids = 10;
  int max_dist = 10;
  std::vector<fiber_t> fibers;

  // first fiber
  int uid = 0;
  int x = 0;
  int y = -height / 2;
  int z = 0;
  fibers.push_back(fiber_t(uid, height, x, y, z));

  kdt_t kdt(max_num_uids, height);
  kdt.add(uid, fibers);

  int num_neighs = 0;
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

      // check out of simulation?
      if (check_out_sim(f, max_dist, radius)) {
        reset_fiber = true;
        continue;
      }

      // get possible neighs
      kdt.get_neighs(f, neighs);

      if (neighs.size() == 0)
        continue;

      // check bind
      if (check_bind(f, neighs, fibers, mode)) {
        rolling_surface(f, kdt, fibers, mode, tmax);
        kdt.add(uid, fibers);
        break;
      }

      // check overlap
      if (f.m_state == OVERLAP) {
        // restore x
        for (int i = 0; i < 3; ++i)
          f.m_x[i] = xold[i];
        f.m_state = FREE;
        continue;
      }
    }
  }
}
