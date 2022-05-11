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
#include <cstring>
#include "dla.h"

int main(int argc, char *argv[])
{
    // read input 
    int num_rods = 100; // number of rods
    bool verbose = false;
    for (int i = 0; i < argc; ++i)
    {
        if (strcmp(argv[i], "-verbose") == 0)
            verbose = true;
        if (strcmp(argv[i], "-num_rods") == 0)
            num_rods = atoi(argv[i+1]);
    }    

    N = 1000;
    int DMAX = N / 2;
    int ts = 10;
    vector<int> grid(N * N * N, 0);
    vector<Point3D> cluster;
    char bind_mode = 'n';

    printf("Parameters\n");
    printf("N .......... %d\n", N);
    printf("ts ......... %d\n", ts);
    printf("num_rods ... %d\n", num_rods);
    printf("bind_mode .. %c\n", bind_mode);
    
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
    
    BBox bbox(x, y, z, height); // bound box containing the cluster
    
    FILE* fid = nullptr; 
    
    if(verbose) fid = fopen("dla.dat", "w");

    cmd_add(fid, uid, x, y, z, height );
    cmd_bind(fid, uid);

    // random walk
    srand(1);
    for( int uid = 1; uid <= num_rods; ++uid )
    {
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
            if (verbose) printf("surface_rolling\n");
            cmd_bind(fid, uid);         
            surface_rolling(bbox, grid, height, ts, bind_mode, x, y, z);
            cmd_move(fid, uid, x, y, z);
            cluster.push_back(Point3D(uid, x, y, z));
            bbox.add(x, y, z);
            printf("bind %d %d %d\n", x, y, z);
        }
    }

    if(fid) fclose(fid);
    return EXIT_SUCCESS;
}