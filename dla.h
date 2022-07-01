#include <cmath>
#include <cstdio>
#include <vector>
#include <cstdlib>
#include <stdexcept>
#include <algorithm>

using namespace std;

const double PI = 3.141592654;
int N = 3000; // grid dimension

// macro to simplify the access to the Point3D grid
#define IDX(i, j, k) ((i) + (j)*N + (k)*N * N)

int idx(int i, int j, int k)
{
    return IDX(i, j, k);
}

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

// generate random number for the range (min, max)
double irand(int imin, int imax)
{
    return (rand() / ((double)RAND_MAX)) * (imax - imin) + imin;

}

int dist_origin(int x, int y, int z)
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
    int m_height;

    BBox(int x, int y, int z, int height)
    {
        m_height = height;
        m_xmin = x - 1;
        m_ymin = y - 1;
        m_zmin = z - 1;
        m_xmax = x + 1;
        m_ymax = y + height + 1;
        m_zmax = z + 1;
        update_diameter();
    }

    void add(int x, int y, int z)
    {
        bool update = false;
        if (m_xmin >= x)
        {
            m_xmin = x - 1;
            update = true;
        }
        if (m_xmax <= x)
        {
            m_xmax = x + 1;
            update = true;
        }
        if (m_ymin >= y)
        {
            m_ymin = y - 1;
            update = true;
        }
        if (m_ymax <= y + m_height + 1)
        {
            m_ymax = y + m_height + 1;
            update = true;
        }
        if (m_zmin >= z)
        {
            m_zmin = z - 1;
            update = true;
        }
        if (m_zmax <= z)
        {
            m_zmax = z + 1;
            update = true;
        }

        if (update) update_diameter();
    }

    bool touch(int x, int y, int z) const
    {
        if (x < m_xmin || x > m_xmax)
            return false;
        if (y < (m_ymin - m_height) || y > m_ymax)
            return false;
        if (z < m_zmin || z > m_zmax)
            return false;
        return true;
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

bool random_single_step(const vector<char> &grid, int &x, int &y, int &z, int height, int xmin, int xmax)
{
    bool overlap = true;
    int xold = x, yold = y, zold = z;

    while (overlap)
    {
        x = xold;
        y = yold;
        z = zold;
        const int imove = rand() % 8;
        // (1, 0, 0 )
        if (imove == 0)
            ++x;
        else if (imove == 1)
            --x;
        // (0, 1, 0)
        else if (imove == 2)
            ++y;
        else if (imove == 3)
            --y;
        // (0, 1, 1)
        else if (imove == 4)
        {
            ++z;
            ++y;
        }
        else if (imove == 5)
        {
            --z;
            --y;
        }
        // (0, 1, -1)
        else if (imove == 6)
        {
            ++y;
            --z;
        }
        else if (imove == 7)
        {
            --y;
            ++z;
        }

        // out of the grid?
        if (x < xmin || x > xmax || y < xmin || y > xmax || z < xmin || z > xmax)
            return false;

        overlap = grid[IDX(x, y, z)] > 0 || grid[IDX(x, y + height - 1, z)] > 0;
    }
    return true;
}

inline bool bind_specific(const BBox &bbox, const vector<char> &grid,
                          const int x, const int y, const int z)
{
    throw new std::invalid_argument("NotImplemented.");
    return false;
}

inline bool bind_non_specific(const BBox &bbox, const vector<char> &grid, int height,
                              const int x, const int y, const int z)
{
    //       .+------+
    //   y .' | N  .'|
    //    +------+'  |
    //    | W |  | E |
    //  x |  ,+--|---+
    //    |.'  S | .'
    //    +------+'
    //        z
    for (int i = -(height - 1); i <= (height - 1); ++i)
    {
        // face W (XY)
        if (grid[IDX(x - 1, y + i, z)] > -1)
            return true;
        // face E
        if (grid[IDX(x + 1, y + i, z)] > -1)
            return true;
        // face S
        int iloc = IDX(x, y + i, z - 1);
        if (grid[iloc] > -1)
            return true;
        // fase N
        if (grid[IDX(x, y + i, z + 1)] > -1)
            return true;
    }
    return false;
}

inline bool bind(char bind_mode, const BBox &bbox, const vector<char> &grid, const int x, const int y, const int z, int height)
{
    //       .+------+
    //   y .' | N  .'|
    //    +------+'  |
    //    | W |  | E |
    //  x |  ,+--|---+
    //    |.'  S | .'
    //    +------+'
    //        z
    if(bbox.touch(x, y, z) == false)
        return false;
    
    // check bind    
    if (grid[IDX(x - 1, y, z)] == 1 || grid[IDX(x - 1, y + height - 1, z)] == 1)
        return true;
    // face E
    if (grid[IDX(x + 1, y, z)] == 1 || grid[IDX(x + 1, y + height - 1, z)] == 1)
            return true;
    // face S
    if (grid[IDX(x, y, z - 1)] == 1 || grid[IDX(x, y + height - 1, z - 1)] == 1)
        return true;
    // fase N
    if (grid[IDX(x, y, z + 1)] == 1 || grid[IDX(x, y + height - 1, z + 1)] == 1)
        return true;
    
    return false;
}

int energy_surface(const vector<char> &grid, int height, int &x, int &y, int &z)
{
    //     .+------+
    //   .' | N  .'|
    //  +------+'  |
    //  | W |  | E |
    //  |  ,+--|---+
    //  |.'  S | .'
    //  +------+'
    int E = 4 * height + 2; // max possible energy surface
    for (int i = 0; i < height; i++)
    {
        // face W (XY)
        if (grid[IDX(x - 1, y + i, z)] > 0)
            --E;
        // face E
        if (grid[IDX(x + 1, y + i, z)] > 0)
            --E;
        // face S
        if (grid[IDX(x, y + i, z - 1)] > 0)
            --E;
        // fase N
        if (grid[IDX(x, y + i, z + 1)] > 0)
            --E;
    }
    return E;
}

/**
 * @brief
 *
 * @param bbox
 * @param grid
 * @param ts
 * @param bind_mode
 * @param x
 * @param y
 * @param z
 */

void cmd_rolling(FILE *fid, int uid, int x, int y, int z, int accepted, int E)
{
    if (fid == nullptr)
        return;
    fprintf(fid, "rolling %03d %d %d %d %d %d\n", uid, x, y, z, accepted, E);
}

void surface_rolling(FILE *fid, int uid, const BBox &bbox, const vector<char> &grid, int height,
                     const int ts, const char bind_mode, int &x, int &y, int &z, int xmin, int xmax)
{    
    int xopt = x, yopt = y, zopt = z;
    int Emin = energy_surface(grid, height, x, y, z); // number of different neighs
    int E = Emin;

    // new data of rolling
    cmd_rolling(fid, uid, x, y, z, 1, E);

    int xold = x, yold = y, zold = z;
    for (int i = 0; i < ts; ++i)
    {
        random_single_step(grid, x, y, z, height, xmin, xmax);

        // rejected direction: the rod left the aggregate surface
        if (bind(bind_mode, bbox, grid, x, y, z, height) == false)
        {
            cmd_rolling(fid, uid, x, y, z, 0, E);
            x = xold;
            y = yold;
            z = zold;
            continue;
        }
        xold = x;
        yold = y;
        zold = z;

        // energy surface
        E = energy_surface(grid, height, x, y, z);
        
        // new data of rolling
        cmd_rolling(fid, uid, x, y, z, 1, E);

        // update minimal energy site
        if (E < Emin)
        {            
            xopt = x;
            yopt = y;
            zopt = z;
            Emin = E;
            if (Emin == 0) break;
        }
    }
    x = xopt;
    y = yopt;
    z = zopt;
}

void cmd_add(FILE *fid, int uid, int x, int y, int z, int h)
{
    if (fid == nullptr)
        return;

    fprintf(fid, "add %03d %d %d %d %d\n", uid, x, y, z, h);
}

void cmd_move(FILE *fid, int uid, int x, int y, int z)
{
    if (fid == nullptr)
        return;

    fprintf(fid, "move %03d %d %d %d\n", uid, x, y, z);
}

void cmd_bind(FILE *fid, int uid, int x, int y, int z)
{
    if (fid == nullptr)
        return;
    fprintf(fid, "bind %03d %d %d %d\n", uid, x, y, z);
}

void cmd_del(FILE *fid, int uid)
{
    if (fid == nullptr)
        return;
    fprintf(fid, "del %03d\n", uid);
}

void bind_rod(vector<char> &grid, vector<Point3D> &cluster, BBox &bbox, char bind_mode, int uid, int x, int y, int z, int height)
{
    if (bind_mode == 'n')
    {
        for (int i = 0; i < height; ++i)
            grid[IDX(x, y + i, z)] = 1;
    }
    else if (bind_mode == 's')
    {
        for (int i = 0; i < height; ++i)
            grid[IDX(x, y + i, z)] = (i % 4) ? 2 : 1;
    }
    else
    {
        printf("Error: non-supported bind_mode.\n");
        exit(EXIT_FAILURE);
    }
    cluster.push_back(Point3D(uid, x, y, z));
    bbox.add(x, y, z);
}
