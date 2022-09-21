#include "fast_dla.h"
#include <chrono>
#include <cstring>
#include <iostream>
#include <sys/resource.h>

void read_args(int argc, char const *argv[], int &tmax, char &mode, int &num_bind, unsigned int &seed)
{
  for (int i = 0; i < argc; ++i)
  {
    if (strcmp(argv[i], "-ts") == 0)
    {
      tmax = atoi(argv[i + 1]);
    }
    else if (strcmp(argv[i], "-mode") == 0)
      mode = argv[i + 1][0];
    else if (strcmp(argv[i], "-num_bind") == 0)
      num_bind = atoi(argv[i + 1]);
    else if (strcmp(argv[i], "-seed") == 0)
    {
      seed = atoi(argv[i + 1]);
      if (seed < 1)
      {
        printf("The parameter seed must greater than zero.\n");
        exit(EXIT_FAILURE);
      }
    }
  }
}

int main(int argc, char const *argv[])
{
  // tests **************************
  // test_overlap_mode_s();
  // return test_kdt()
  // std::chrono::steady_clock::time_point tic = std::chrono::steady_clock::now();

  const rlim_t kStackSize = 16 * 1024 * 1024; // min stack size = 16 MB
  struct rlimit rl;
  int result;

  result = getrlimit(RLIMIT_STACK, &rl);
  if (result == 0)
  {
    if (rl.rlim_cur < kStackSize)
    {
      rl.rlim_cur = kStackSize;
      result = setrlimit(RLIMIT_STACK, &rl);
      if (result != 0)
        fprintf(stderr, "setrlimit returned (result = %d)\n", result);
      //printf("change stack size\n");
    }
  }

  // default arguments
  char mode = 'n';
  int num_bind = 10000;
  int tmax = 1000;
  unsigned int seed = 1024;

  // read arguments
  read_args(argc, argv, tmax, mode, num_bind, seed);

  run_dla(tmax, num_bind, mode, seed);

  // std::chrono::steady_clock::time_point toc = std::chrono::steady_clock::now();
  // std::cout << "   Elapsed time " << std::chrono::duration_cast<std::chrono::seconds>(toc - tic).count() << " secs" << std::endl;
  return EXIT_SUCCESS;
}
