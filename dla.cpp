/**
 * @file dla.cpp
 * @author Michael Souza (michael@ufc.br)
 * @brief 
 * @version 0.1
 * @date 2022-04-04
 * @cite Parkinson94, Trinket 
 * @copyright Copyright (c) 2022
 * 
 */
#include <chrono>
#include <cstring>
#include <iostream>
#include "dla.h"


int main(int argc, char *argv[])
{
    std::chrono::steady_clock::time_point tic = std::chrono::steady_clock::now();    

    // read input 
    int NUM_BINDS = 3; // number of binds
    bool VERBOSE = false;
    for (int i = 0; i < argc; ++i)
    {
        if (strcmp(argv[i], "-verbose") == 0)
            VERBOSE = true;
        if (strcmp(argv[i], "-num_binds") == 0)
            NUM_BINDS = atoi(argv[i+1]);
    }    

    N = 1000;
    int DMAX = N / 2;
    int ts = 10;
    vector<int> grid(N * N * N, 0);
    vector<Point3D> cluster;
    char bind_mode = 'n';

    printf("Parameters\n");
    printf("N ........... %d\n", N);
    printf("ts .......... %d\n", ts);
    printf("num_binds ... %d\n", NUM_BINDS);
    printf("bind_mode ... %c\n", bind_mode);
    
    // 0: empty
    // 1: bind
    // 2: non_bind

    // add first rod
    int uid = 0;
    int x = N/2, y=N/2, z=N/2;
    const int height = 18;
    const int xmin = 0;
    const int xmax = N - height;

    add_rod(grid, x, y, z, height, bind_mode);
    
    // bound box containing the cluster
    BBox bbox(x, y, z, height); 
    
    FILE* fid = nullptr; 

    if(VERBOSE) fid = fopen("dla.dat", "w");
 
    cmd_add(fid, uid, x, y, z, height );
    cmd_bind(fid, uid, x, y, z);

    // random walk
    srand(1);    
    int num_binds = 1;
    while( num_binds <= NUM_BINDS )
    {
        ++uid;

        // uniform distribution over sphere
        // see: https://www.bogotobogo.com/Algorithms/uniform_distribution_sphere.php
        
        const int radius = min(bbox.diameter(), 200);
        const double theta = 2 * PI * irand(0, 1);
        const double phi = acos(2 * irand(0, 1) - 1.0);
        int x = N / 2 + radius * cos(theta) * sin(phi);
        int y = N / 2 + radius * sin(theta) * sin(phi);
        int z = N / 2 + radius * cos(phi);

        cmd_add(fid, uid, x, y, z, height);

        vector<int> p;
        p.push_back(x);
        p.push_back(y);
        p.push_back(z);

        bool cluster_add = bind(bind_mode, bbox, grid, x, y, z, height);
        while (cluster_add == false)
        {
            random_walk(x, y, z);
            p.push_back(x);
            p.push_back(y);
            p.push_back(z);
            
            // out of the grid?
            if (x < xmin || x > xmax || y < xmin || y > xmax || z < xmin || z > xmax)
                break;

            // touch the bound box?
            if( bbox.touch(x, y, z) == false )
                continue;

            // check bind
            cluster_add = bind(bind_mode, bbox, grid, x, y, z, height);                        
        }
        
        for(int i = 3; i < p.size(); i+=3)
            cmd_move(fid, uid, p[i], p[i+1], p[i+2]);

        if( cluster_add )
        {
            ++num_binds;                                    
            if (VERBOSE) printf("surface_rolling\n");
            cmd_bind(fid, uid, x, y, z);         
            surface_rolling(bbox, grid, height, ts, bind_mode, x, y, z);
            cmd_move(fid, uid, x, y, z);
            cluster.push_back(Point3D(uid, x, y, z));
            bbox.add(x, y, z);
            printf("bind num %d\n", num_binds);
            printf("   uid ........ %d\n", uid);
            printf("   (x, y,z) ... %d %d %d\n", x, y, z);
 


            std::chrono::steady_clock::time_point toc = std::chrono::steady_clock::now();    
            std::cout << "   Elapsed time " << std::chrono::duration_cast<std::chrono::seconds>(toc - tic).count() << " secs" << std::endl;
        }
    }

    if(fid) fclose(fid);
    return EXIT_SUCCESS;
}