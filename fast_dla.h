#include <vector>

class fiber_t
{
public:
    int m_uid;
    int m_x;
    int m_y;
    int m_z;
    int m_h;

    fiber_t(int uid, int x, int y, int z, int h)
    {
        m_uid = uid;
        m_x = x;
        m_y = y;
        m_z = z;
        m_h = h;
    }
};

class kdt_t
{
public:

    int m_x;        
    int m_y;
    int m_z;
    int m_dx;
    int m_dy;
    int m_dz;
    int m_max_num_uids;
    kdt_t *m_lft;
    kdt_t *m_rht;
    std::vector<int> m_uids;

    kdt_t(int x, int y , int z, int dx, int dy, int dz, int max_num_uids)
    {
        m_lft = nullptr;
        m_rht = nullptr;
        m_max_num_uids = max_num_uids;
    }

    ~kdt_t(){
        delete m_lft;
        delete m_rht;
    }

    /**
     * @brief 
     * 
     * @param f 
     */
    void add(int uid, std::vector<fiber_t> &fibers)
    {
        m_uids.push_back(uid);
        if (m_uids.size() > m_max_num_uids)
            split(fibers);
    }

    /**
     * @brief 
     * 
     */
    void split(std::vector<fiber_t> &fibers){
        // aloca os filhos
        m_lft = new kdt_t(x,y,z,dx,dy,dz);
        m_rht = new kdt_t(x,y,z,dx,dy,dz);

        // move as fibras para os filhos
        for (auto &&i : fibers)
        {
            
        }

        // libera as fibras
        m_uids.clear();
    }

    void get_neighs(int &n, int *neighs)
    {
        // checa se está em contato com o kdt

        if (m_lft)
            m_lft->get_neighs(n, neighs);
        if (m_rht)
            m_rht->get_neighs(n, neighs);
    }
};


bool test_kdt()
{
    const int h = 18;
    int max_num_uids = 10;
    int num_bind = 10;
    std::vector<fiber_t> fibers;

    int uid = 0;
    int x = 0;
    int y = -h / 2;
    int z = 0;
    fibers.push_back(fiber_t(uid, x, y, z, h));

    int dx = 1;
    int dy = h;
    int dz = 1;

    fiber_t &f = fibers[uid];
    kdt_t kdt(f.m_x, f.m_y, f.m_z, dx, dy, dz, max_num_uids);

    bool new_fiber = true;
    while(uid < num_bind)
    {        
        int x = 0; // rand
        int y = -h / 2; // rand
        int z = 0; // rand
        if(new_fiber)
            fibers.push_back(fiber_t(++uid, x, y, z, h));
        else
        {
            fibers[uid].m_x = x;
            fibers[uid].m_y = y;
            fibers[uid].m_z = z;
        }

        kdt.add(uid, fibers);
    }
}