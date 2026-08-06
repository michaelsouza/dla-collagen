#include "fast_dla.h"

#include <cassert>
#include <fstream>
#include <iterator>
#include <string>

void test_degenerate_split() {
  constexpr int height = 18;
  constexpr int max_node_size = 100;

  std::vector<fiber_t> fibers;
  kdt_t kdt(max_node_size, height);

  for (int uid = 0; uid <= max_node_size; ++uid) {
    fibers.emplace_back(uid, height, 0, 0, 0);
    kdt.add(uid, fibers);
  }

  assert(kdt.m_lft != nullptr);
  assert(kdt.m_rht != nullptr);
  assert(!kdt.m_lft->m_uids.empty());
  assert(!kdt.m_rht->m_uids.empty());

  std::vector<int> neighbors;
  kdt.get_node_neighs(fibers.front(), neighbors);
  assert(neighbors.size() == fibers.size());
}

void test_resume_discards_incomplete_trailing_record() {
  const char *filename = "/tmp/test_fast_dla_resume.dat";
  {
    std::ofstream output(filename, std::ios::binary);
    output << "uid: 0 0 -9 0\n";
    output << "uid: 1 1 -5 0\n";
    output << "uid: 2 ";
  }

  std::vector<fiber_t> fibers;
  const int last_uid = load_fibers_for_resume(filename, 18, fibers);

  assert(last_uid == 1);
  assert(fibers.size() == 2);
  assert(fibers[0].m_uid == 0);
  assert(fibers[1].m_uid == 1);

  std::ifstream input(filename, std::ios::binary);
  const std::string contents(
      (std::istreambuf_iterator<char>(input)),
      std::istreambuf_iterator<char>());
  assert(contents == "uid: 0 0 -9 0\nuid: 1 1 -5 0\n");

  std::remove(filename);
}

int main() {
  test_degenerate_split();
  test_resume_discards_incomplete_trailing_record();
}
