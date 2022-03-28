#include <cstdlib>
#include <cstdio>
#include <vector>
#include <cmath>
#include <stdexcept>

using namespace std;

const int N = 1000; // grid dimension
const int DMAX = (N - 1) / 2;

const double PI = 3.141592654;

// macro to simplify the access to the grid Point3Ds
#define IDX(i, j, k) (i + j * N + k * N * N)

class Point3D
{
public:
    int m_x;
    int m_y;
    int m_z;
    int m_uid;

    Point3D(int uid, int x, int y, int z)
    {
        m_uid = uid;
        m_x = x;
        m_y = y;
        m_z = z;
    }

    void show()
    {
        printf("x: %d, y: %d, z: %d\n", m_x, m_y, m_z);
    }
};

// class Rod
// {
// public:
//     int m_uid; // unique id
//     Point3D *m_u;

//     Rod() {}

//     void random_walk(Point3D *u, int ts)
//     {
//         bool done = false;
//         while (done == false)
//         {
//             const int uid = rand() % u->m_V.size();
//             u = u->m_V[uid];
//             if (u->m_border)
//                 return;
//             if (u->aggregate())
//             {
//                 rolling_surface(u, ts);
//                 return;
//             }
//         }
//     }

//     void rolling_surface(Point3D *u, int ts)
//     {
//         Point3D *uMax = u; // max degree
//         int degMax = 0;
//         for (auto &v : u->m_C)
//             if (v->m_r != nullptr)
//                 ++degMax;

//         for( int i = 0; i < ts; ++i )    
//         {
//             const int uid = rand() % u->m_V.size();
//             Point3D *uNew = u->m_V[uid];
//             if (u->aggregate() == false)
//                 continue;
            
//             u = uNew;

//             // calc deg(u)
//             int deg = 0;
//             for (auto &v : u->m_C)
//                 if (v->m_r != nullptr)
//                     ++deg;
//             if (deg > degMax)
//             {
//                 degMax = deg;
//                 uMax = u;
//             }
//         }

//         uMax->m_r = this;
//         m_u = uMax;
//     }

//     void show()
//     {
//         printf("uid: %d\n", m_uid);
//     }
// };

// class KDTree
// {
// public:
//     vector<KDTree*> m_children;
//     int m_xMin;
//     int m_yMin;
//     int m_zMin;
//     int m_edgeSize;
//     int m_n; // number of objects
//     vector<int> m_V;
//     vector<KDTree *> m_children;
//     bool m_leaf;

//     KDTree(int edgeSize, int edgeSizeMax, int xmin, int ymin, int zmin )
//     {
//         m_edgeSize = edgeSize;
//         m_xMin = xmin;
//         m_yMin = ymin;
//         m_zMin = zmin;

//         m_leaf = edgeSize <= edgeSizeMax;

//         if( m_leaf == false )
//         {
//             edgeSize = edgeSizeMax / 2;
//             KDTree *u = nullptr;
//             // z = zmin
//             u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin, zmin);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin, zmin);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin + edgeSize, zmin);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin + edgeSize, zmin);
//             m_children.push_back(u);
//             // z == zmin + edgeSize
//             u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin, zmin + edgeSize);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin, zmin + edgeSize);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin + edgeSize, zmin + edgeSize);
//             m_children.push_back(u);
//             u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin + edgeSize, zmin + edgeSize);
//             m_children.push_back(u);
//         }
//     }

//     void add(int pid, Point3D &p)
//     {
//         if ((m_xMin <= p.m_x && p.m_x <= m_xMin + m_edgeSize) &&
//             (m_yMin <= p.m_y && p.m_y <= m_yMin + m_edgeSize) &&
//             (m_zMin <= p.m_z && p.m_z <= m_zMin + m_edgeSize))
//         {
//             ++m_n;            
//             for (auto &v : m_children)
//                 v->add(pid, p);
//             if (m_leaf)
//                 m_V.push_back(pid);
//         }
//     }

//     int locate( int x, int y, int z )
//     {

//     }

//     void aggregate(Point3D &p, int &n, vector<int> &V)
//     {
//         const int x = p.m_x;
//         const int y = p.m_y;
//         const int z = p.m_z;

//         // neighs on XY plane
//         n = 0;
//         int uid = -1;
//         for (int i = 1; i <= 17; ++i)
//         {
//             uid = locate(x - 1, y - i, z);
//             if (uid >= 0)
//                 V[n++] = uid;
//             uid = locate(x + 1, y - i, z);
//             if (uid >= 0)
//                 V[n++] = uid;
//         }

//     }
// };

// generate random number for the range (min, max)
double irand(int imin, int imax)
{
    return ((double)rand() / ((double)RAND_MAX + 1.0)) * (imax - imin) + imin;
}

int dist_origin( int x, int y, int z )
{
    int dx = (N / 2 - x);
    int dy = (N / 2 - y);
    int dz = (N / 2 - z);
    return sqrt(dx * dx + dy * dy + dz * dz);
}

class BBox
{
public:
    int m_xmin;
    int m_xmax;
    int m_ymin;
    int m_ymax;
    int m_zmin;
    int m_zmax;   
    int m_diameter;

    BBox(Point3D& p)
    {
        m_xmin = p.m_x - 1;
        m_ymin = p.m_y - 1;
        m_zmin = p.m_z - 1;
        m_xmax = p.m_x + 1;
        m_ymax = p.m_y + 19;
        m_zmax = p.m_z + 1;
        update_diameter();
    }

    void add(int x, int y, int z)
    {   
        bool update = false;
        if (m_xmin >= x)
            {m_xmin = x - 1;
            update = true;}
        if (m_xmax <= x)
            {m_xmax = x + 1;update = true;}
        if (m_ymin >= y)
            {m_ymin = y - 1;update = true;}
        if (m_ymax <= y + 19)
            {m_ymax = y + 19;update = true;}
        if (m_zmin >= z)
            {m_zmin = z - 1;update = true;}
        if (m_zmax <= z)
            {m_zmax = z + 1;update = true;}

        if( update ) update_diameter();
    }

    bool touch(int x, int y, int z) const
    {
        if( m_xmin <= x && x <= m_xmax )
            return true;
        if( m_ymin <= y && y <= m_ymax )
            return true;
        if( m_zmin <= z && z <= m_zmax )
            return true;
        return false;
    }

    void update_diameter()
    {
        int dx = m_xmax - m_xmin;        
        int dy = m_ymax - m_ymin;
        int dz = m_zmax - m_zmin;
        m_diameter = sqrt(dx * dx + dy * dy + dz * dz);
    }

    int diameter() const
    {
        return m_diameter;
    }
};

bool random_walk(const BBox& bbox, const vector<int> &grid, int &x, int &y, int &z)
{
    const int xOld = x;
    const int yOld = y;
    const int zOld = z;

    const int imove = rand() % 8;
    if (imove == 0)
        ++x;
    else if (imove == 1)
        --x;
    else if (imove == 2)
        ++y;
    else if (imove == 3)
        --y;
    else if (imove == 4)
    {
        ++z;
        ++y;
    }
    else if (imove == 5)
    {
        ++z;
        --y;
    }
    else if (imove == 6)
    {
        --z;
        ++y;
    }
    else if (imove == 7)
    {
        --z;
        --y;
    }

    // collision
    if ( bbox.touch(x, y, z) == false)
        return true;
    
    for (int i = 0; i < 17; ++i)
        if (grid[IDX(x, y + i, z)] > -1)
        {
            x = xOld;
            y = yOld;
            z = zOld;
            return false;
        }
    return true;
}

bool bind_specific(const BBox& bbox, const vector<int>& grid, const int x, const int y, const int z)
{
    return false;
}

bool bind_non_specific(const BBox& bbox, const vector<int> &grid, const int x, const int y, const int z)
{
    //     .+------+
    //   .' | N  .'|
    //  +---+--+'  |
    //  | W |  | E |
    //  |  ,+--+---+
    //  |.'  S| .' 
    //  +------+'     

    // TODO improve memory localization
    if( bbox.touch(x,y,z) == false )
        return false;
    
    for (int i = -17; i <= 17; ++i)
    {
        // face W
        if (grid[IDX(x - 1, y + i, z)] > -1)
            return true;
        // face E
        if (grid[IDX(x + 1, y + i, z)] > -1)
            return true;        
        // face S
        if (grid[IDX(x - 1, y + i, z - 1)] > -1)
            return true;
        // fase N
        if (grid[IDX(x + 1, y + i, z + 1)] > -1)
            return true;
    }
    return false;
}

int energy_surface( const vector<int>&grid, const char bind_mode, int &x, int &y, int &z )
{
    //     .+------+
    //   .' | N  .'|
    //  +---+--+'  |
    //  | W |  | E |
    //  |  ,+--+---+
    //  |.'  S| .' 
    //  +------+'     
    int E = 4 * 18; // energy surface
    if( bind_mode == 'n' ) // non-specific
    {
        // face W
        for (int i = -17; i <= 17; ++i)
            if ( grid[IDX(x - 1, y + i, z)] > -1)
            { 
                E -= (i < 0) ? i + 18: 18 - i;
                // jump to the rod corner
                i += 17;
            }
        // face W
        for (int i = -17; i <= 17; ++i)
            if ( grid[IDX(x + 1, y + i, z)] > -1)
            { 
                E -= (i < 0) ? i + 18: 18 - i;
                // jump to the rod corner
                i += 17;
            }
        // face S
        for (int i = -17; i <= 17; ++i)
            if ( grid[IDX(x, y + i, z - 1)] > -1)
            { 
                E -= (i < 0) ? i + 18: 18 - i;
                // jump to the rod corner
                i += 17;
            }
        // face S
        for (int i = -17; i <= 17; ++i)
            if ( grid[IDX(x, y + i, z + 1)] > -1)
            { 
                E -= (i < 0) ? i + 18: 18 - i;
                // jump to the rod corner
                i += 17;
            }
    }
    else
    {
        throw runtime_error("not implemented");
    }
    return E;
}

void surface_rolling( const BBox& bbox, const vector<int>&grid, const int ts, const char bind_mode, int &x, int &y, int &z )
{
    int xopt = x, yopt = y, zopt = z;
    int Emin = energy_surface(grid, bind_mode, x, y, z); // number of different neighs

    int xold = x, yold = y, zold = z;
    for(int i = 0; i < ts; ++i)   
    {
        const bool updXYZ = random_walk(bbox, grid, x, y, z);

        // rejected direction: the rod left the aggregate surface
        if( bind_non_specific(bbox, grid, x, y, z) == false )
        {
            x = xold,
            y = yold;
            z = zold;
            continue;
        }
        // energy surface 
        const int E = energy_surface(grid, bind_mode, x, y, z);
        // update minimal energy site
        if( E < Emin )
        {
            xopt = x;
            yopt = y;
            zopt = z;
            Emin = E;
            if( Emin = 0 ) break;
        }
    }
}

int main(int argc, char *argv[])
{
    srand(1);
    vector<int> grid(N * N * N, -1);
    vector<Point3D> cluster;
    
    // add first rod
    Point3D origin(0, N / 2, N / 2, N / 2);
    grid[IDX(origin.m_x, origin.m_y, origin.m_z)] = 0;
    cluster.push_back(origin);
    BBox bbox(origin);

    const int xmin = 0;
    const int xmax = N - 18;    

    // random walk
    const int num_rods = 10000; // number of rods
    for( int uid = 1; uid <= num_rods; ++uid )
    {
        // uniform distribution over sphere
        // see: https://www.bogotobogo.com/Algorithms/uniform_distribution_sphere.php
        
        const int radius = 2 * bbox.diameter();
        const double theta = 2 * PI * irand(0, 1);
        const double phi = acos(2 * irand(0, 1) - 1.0);
        int x = N / 2 + radius * cos(theta) * sin(phi);
        int y = N / 2 + radius * sin(theta) * sin(phi);
        int z = N / 2 + radius * cos(phi);

        bool done = false;
        bool bind = bind_non_specific(bbox, grid, x, y, z);
        while (done == false)
        {
            bool updXYZ = random_walk(bbox, grid, x, y, z);
            if ( updXYZ == false )
                continue;

            const int dist = dist_origin(x, y, z);
            
            done = bind || dist >= DMAX;

            if (x < xmin || x > xmax || y < xmin || y > xmax || z < xmin || z > xmax)
                throw runtime_error("out of grid");
        }

        if( bind )
        {
            // roll_surface()
            cluster.push_back(Point3D(uid, x, y, z));
            bbox.add(x, y, z);
        }
    }
    return EXIT_SUCCESS;
}