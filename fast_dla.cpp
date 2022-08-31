#include "fast_dla.h"
#include <chrono> 
#include <cstring>
#include <iostream>

void read_args(int argc, char const *argv[], int &tmax, char &mode, int &num_bind, unsigned int &seed)
{
  for (int i = 0; i < argc; ++i)
  {
    if(strcmp(argv[i], "-tmax") == 0)
      tmax = atoi(argv[i+1]);
    else if(strcmp(argv[i], "-mode") == 0)
      mode = argv[i+1][0];    
    else if(strcmp(argv[i], "-num_bind") == 0)
      num_bind = atoi(argv[i+1]);
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
  // test_overlap_mode_s();
  // return test_kdt()  
  std::chrono::steady_clock::time_point tic = std::chrono::steady_clock::now();      

  // default arguments
  char mode = 's';
  int tmax = 20;
  int num_bind = 100;
  unsigned int seed = 0;

  // read arguments
  read_args(argc, argv, tmax, mode, num_bind, seed);
  
  run_dla(tmax, num_bind, mode, seed);

  std::chrono::steady_clock::time_point toc = std::chrono::steady_clock::now();    
  std::cout << "   Elapsed time " << std::chrono::duration_cast<std::chrono::seconds>(toc - tic).count() << " secs" << std::endl;
}
