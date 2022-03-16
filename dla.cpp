#include <cstdlib>
#include <cstdio>
#include <vector>

using namespace std;

class Rod
{
public:
    int m_uid; // unique id
    int m_x;
    int m_y;
    int m_z;

    Rod(){}

    Rod(int uid, int x, int y, int z)
    {
        m_uid = uid;
        m_x = x;
        m_y = y;
        m_z = z;
    }

    void show()
    {
        printf("uid: %d, x: %d, y: %d, z: %d\n", m_uid, m_x, m_y, m_z);
    }
};

class Node
{
public:
    Rod *m_rod;
    Node()
    {
        m_rod = nullptr;
    };
};

int main(int argc, char *argv[])
{
    vector<Rod> rods(45000);
    
    // define uid
    int uid = 0;
    for (auto &rod : rods)
        rod.m_uid = uid++;

    const int N = 100;
    vector<Node> grid(N * N * N);
    printf("Hello!\n");
    return EXIT_SUCCESS;
}