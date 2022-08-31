#include "fast_dla.h"
#include <chrono> 
#include <cstring>
#include <iostream>

int main(int argc, char const *argv[])
{
  std::chrono::steady_clock::time_point tic = std::chrono::steady_clock::now();    
  // return test_kdt()
  const char mode = 's';
  const int tmax = 20;
  const int num_bind = 100;
  run_dla(tmax, num_bind, mode);

  std::chrono::steady_clock::time_point toc = std::chrono::steady_clock::now();    
  std::cout << "   Elapsed time " << std::chrono::duration_cast<std::chrono::seconds>(toc - tic).count() << " secs" << std::endl;
}
