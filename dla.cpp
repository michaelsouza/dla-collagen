#include <cstdlib>
#include <cstdio>
#include <vector>

using namespace std;

// macro to simplify the access to the grid nodes
#define IDX(i, j, k) (i + j * N + k * N * N);

class Point3D
{
public:
    int m_x;
    int m_y;
    int m_z;

    void show()
    {
        printf("x: %d, y: %d, z: %d\n", m_x, m_y, m_z);
    }
};

class Rod
{
public:
    int m_uid; // unique id
    Node *m_u;

    Rod() {}

    void random_walk(Node *u, int ts)
    {
        bool done = false;
        while (done == false)
        {
            const int uid = rand() % u->m_V.size();
            u = u->m_V[uid];
            if (u->m_border)
                return;
            if (u->aggregate())
            {
                rolling_surface(u, ts);
                return;
            }
        }
    }

    void rolling_surface(Node *u, int ts)
    {
        Node *uMax = u; // max degree
        int degMax = 0;
        for (auto &v : u->m_C)
            if (v->m_r != nullptr)
                ++degMax;

        for( int i = 0; i < ts; ++i )    
        {
            const int uid = rand() % u->m_V.size();
            Node *uNew = u->m_V[uid];
            if (u->aggregate() == false)
                continue;
            
            u = uNew;

            // calc deg(u)
            int deg = 0;
            for (auto &v : u->m_C)
                if (v->m_r != nullptr)
                    ++deg;
            if (deg > degMax)
            {
                degMax = deg;
                uMax = u;
            }
        }

        uMax->m_r = this;
        m_u = uMax;
    }

    void show()
    {
        printf("uid: %d\n", m_uid);
    }
};

class KDTree
{
public:
    vector<KDTree*> m_children;
    int m_xMin;
    int m_yMin;
    int m_zMin;
    int m_edgeSize;
    int m_n; // number of objects
    vector<int> m_V;
    vector<KDTree *> m_children;
    bool m_leaf;

    KDTree(int edgeSize, int edgeSizeMax, int xmin, int ymin, int zmin )
    {
        m_edgeSize = edgeSize;
        m_xMin = xmin;
        m_yMin = ymin;
        m_zMin = zmin;

        m_leaf = edgeSize <= edgeSizeMax;

        if( m_leaf == false )
        {
            edgeSize = edgeSizeMax / 2;
            KDTree *u = nullptr;
            // z = zmin
            u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin, zmin);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin, zmin);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin + edgeSize, zmin);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin + edgeSize, zmin);
            m_children.push_back(u);
            // z == zmin + edgeSize
            u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin, zmin + edgeSize);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin, zmin + edgeSize);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin, ymin + edgeSize, zmin + edgeSize);
            m_children.push_back(u);
            u = new KDTree(edgeSize, edgeSizeMax, xmin + edgeSize, ymin + edgeSize, zmin + edgeSize);
            m_children.push_back(u);
        }
    }

    void add(int pid, Point3D &p)
    {
        if ((m_xMin <= p.m_x && p.m_x <= m_xMin + m_edgeSize) &&
            (m_yMin <= p.m_y && p.m_y <= m_yMin + m_edgeSize) &&
            (m_zMin <= p.m_z && p.m_z <= m_zMin + m_edgeSize))
        {
            ++m_n;            
            for (auto &v : m_children)
                v->add(pid, p);
            if (m_leaf)
                m_V.push_back(pid);
        }
    }

    void collision(Point3D &p, int &n, vector<int>& V)
    {

    }
};

int main(int argc, char *argv[])
{
    srand(1);
    
    vector<Rod> rods;
    while( )    

    // define uid
    int uid = 0;
    for (auto &rod : rods)
        rod.m_uid = uid++;

    const int N = 100;
    vector<Node> grid(N * N * N);

    printf("Hello!\n");
    return EXIT_SUCCESS;
}