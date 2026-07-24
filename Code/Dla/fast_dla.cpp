#include "fast_dla.h"
//#include "fast_dla_2d.h"
//#include "dla_teste.h"
#include <chrono>
#include <cstring>
#include <iostream>
#include <string>
#include <sys/resource.h>

void read_args(
  int argc,
  char const *argv[],
  int &tmax,
  char &mode,
  int &num_bind,
  unsigned int &seed,
  std::string &output_dir)
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
    else if (strcmp(argv[i], "-output_dir") == 0)
    {
      output_dir = argv[i + 1];
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
  int num_bind = 3600;
  int tmax = 1; 
  unsigned int seed = 36;
  std::string output_dir = ".";


  // read arguments
  read_args(argc, argv, tmax, mode, num_bind, seed, output_dir);

  run_dla(tmax, num_bind, mode, seed, output_dir.c_str());

  // std::chrono::steady_clock::time_point toc = std::chrono::steady_clock::now();
  // std::cout << "   Elapsed time " << std::chrono::duration_cast<std::chrono::seconds>(toc - tic).count() << " secs" << std::endl;
  return EXIT_SUCCESS;
}
