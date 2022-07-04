#include <vector>
#include <algorithm>

#define MAX(a, b) ((a) > (b) ? (a) : b)

class fiber_t
{
public:
    int m_uid;
    int m_x[3];
    int m_h;

    fiber_t(int uid, int x, int y, int z, int h)
    {
        m_uid = uid;
        m_x[0] = x;
        m_x[1] = y;
        m_x[2] = z;
        m_h = h;
    }
};

class kdt_t
{
public:

    int m_xmin[3];        
    int m_xmax[3];    
    int m_height;
    int m_max_num_uids;
    kdt_t *m_lft;
    kdt_t *m_rht;
    std::vector<int> m_uids;
    bool m_splitted;

    kdt_t(int max_num_uids, int height)
    {
        m_lft = nullptr;
        m_rht = nullptr;
        m_max_num_uids = max_num_uids;
        m_height = height;
        m_splitted = false;
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
        fiber_t &f = fibers[uid];
        if (m_splitted == false && m_uids.size() == 0)
        {
            // inicializa o bounding box
            for(int i = 0; i < 3; ++i)
                m_xmin[i] = f.m_x[i];
            m_xmax[0] = m_xmin[0] + 1;
            m_xmax[1] = m_xmin[1] + m_height;
            m_xmax[2] = m_xmin[2] + 1;
        }
        else
        {
            // atualiza o bounding box
            for (int i = 0; i < 3; ++i)
            {
                if (m_xmin[i] > f.m_x[i])
                    m_xmin[i] = f.m_x[i];
                if (m_xmax[i] < f.m_x[i])
                    m_xmax[i] = f.m_x[i];
            }
        }
        if (m_splitted == false)
            m_uids.push_back(uid);
        else
        {
            // adiciona ao filho que menos é afetado pela entrada da nova fibra
            int d, d_lft = 0, d_rht = 0;
            for(int i = 0; i < 3; ++i)
            {
                d = MAX(MAX(m_lft->m_xmin[i] - f.m_x[i], f.m_x[i] - m_lft->m_xmax[i]), 0);
                if(d_lft < d) d;
            }
            for(int i = 0; i < 3; ++i)
            {
                d = MAX(MAX(m_lft->m_xmin[i] - f.m_x[i], f.m_x[i] - m_lft->m_xmax[i]), 0);
                if(d_rht < d) d;
            }
        }
    }

    /**
     * @brief 
     * 
     */
    void split(std::vector<fiber_t> &fibers){
        // aloca os filhos
        m_lft = new kdt_t(m_max_num_uids, m_height);
        m_rht = new kdt_t(m_max_num_uids, m_height);

        // identifica a direção do corte como sendo a maior
        int dx = m_xmax - m_xmin;
        int dy = m_ymax - m_ymin;
        int dz = m_zmax - m_zmin;
        int dmax = MAX(MAX(dx, dy), dz);
        std::vector<int> v;
        if (m_xmax == dmax)
        {
            for (auto &&uid : m_uids)
                v.push_back(fibers[uid].m_x);
            std::sort(v.begin(), v.end());
            int x = v[v.size() / 2]; // mediana

            // divide os filhos pela mediana
            for(auto &&uid: m_uids)
                fibers[uid].m_x < x ? m_lft->add(uid, fibers) : m_rht->add(uid, fibers);
        }
        else if ( m_ymax == dmax )        {
            for (auto &&uid : m_uids)
                v.push_back(fibers[uid].m_y);
            std::sort(v.begin(), v.end());
            int y = v[v.size() / 2]; // median

            for(auto &&uid: m_uids)
                fibers[uid].m_y < y ? m_lft->add(uid, fibers) : m_rht->add(uid, fibers);
        }
        else if (m_zmax == dmax)
        {
            for (auto &&uid : m_uids)
                v.push_back(fibers[uid].m_z);
            std::sort(v.begin(), v.end());
            int z = v[v.size() / 2]; // median

            for (auto &&uid : m_uids)
                fibers[uid].m_z < z ? m_lft->add(uid, fibers) : m_rht->add(uid, fibers);
        }        

        // libera as fibras
        m_uids.clear();
    }

    /**
     * @brief Get the neighs object
     * 
     * @param n 
     * @param neighs 
     */
    void get_neighs(fiber_t &f, int &n, int *neighs)
    {
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