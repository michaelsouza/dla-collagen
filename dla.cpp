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
    bool verbose = false;
    for (int i = 0; i < argc; ++i)
    {
        if (strcmp(argv[i], "-verbose"))
            verbose = true;
    }

    N = 1000;
    int DMAX = N / 2;
    int ts = 10;
    vector<int> grid(N * N * N, -1);
    vector<Point3D> cluster;
    char bind_mode = 'n';
    
    // add first rod
    Point3D origin(0, N / 2, N / 2, N / 2);
    grid[IDX(origin.m_x, origin.m_y, origin.m_z)] = 0; // grid of possible locations
    cluster.push_back(origin); // cluster is the aggregate of the rods
    BBox bbox(origin); // bound box containing the cluster

    const int xmin = 0;
    const int xmax = N - 18;
    
    FILE* fid = nullptr; 
    
    if(verbose) fid = fopen("dla.dat", "w");

    cmd_add(fid, origin.m_uid, origin.m_x, origin.m_y, origin.m_z, 18 );
    cmd_bind(fid, origin.m_uid);

    // random walk
    srand(1);
    const int num_rods = 100; // number of rods
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

        cmd_add(fid, uid, x, y, z, 18);

        vector<int> p;
        p.push_back(x);
        p.push_back(y);
        p.push_back(z);

        bool done = false;
        bool is_bound = bind(bind_mode, bbox, grid, x, y, z);
        while (done == false)
        {
            bool updXYZ = random_walk(bbox, grid, x, y, z);
            p.push_back(x);
            p.push_back(y);
            p.push_back(z);
            if ( updXYZ == false )
                continue;

            const int dist = dist_origin(x, y, z);
            
            done = is_bound || dist >= DMAX;

            if (x < xmin || x > xmax || y < xmin || y > xmax || z < xmin || z > xmax)
                done = true;
        }
        
        for(int i = 3; i < p.size(); i+=3)
            cmd_move(fid, uid, p[i], p[i+1], p[i+2]);

        if( is_bound )
        {
            if (verbose) printf("surface_rolling\n");
            cmd_bind(fid, uid);         
            surface_rolling(bbox, grid, ts, bind_mode, x, y, z);
            cmd_move(fid, uid, x, y, z);
            cluster.push_back(Point3D(uid, x, y, z));
            bbox.add(x, y, z);
            printf("bind %d %d %d\n", x, y, z);
        }
    }

    if(fid) fclose(fid);
    return EXIT_SUCCESS;
}