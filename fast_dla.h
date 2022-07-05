#include <vector>
#include <algorithm>

#define MAX(a, b) (((a) > (b)) ? (a) : (b))

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

    int m_level;
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
        m_level = 0;
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
                d = MAX(m_lft->m_xmin[i] - f.m_x[i], f.m_x[i] - m_lft->m_xmax[i]);
                if(d_lft < d) d_lft = d;
            }
            for(int i = 0; i < 3; ++i)
            {
                d = MAX(m_rht->m_xmin[i] - f.m_x[i], f.m_x[i] - m_rht->m_xmax[i]);
                if(d_rht < d) d_rht = d;
            }

            if(d_lft < d_rht)
                m_lft->add(uid, fibers);
            else
                m_rht->add(uid, fibers);
        }
    }

    /**
     * @brief 
     * 
     */
    void split(std::vector<fiber_t> &fibers)
    {
        // aloca os filhos
        m_lft = new kdt_t(m_max_num_uids, m_height);
        m_rht = new kdt_t(m_max_num_uids, m_height);
        m_lft->m_level = m_level + 1;
        m_rht->m_level = m_level + 1;

        // identifica a direção do corte como sendo a mais longa
        int d[3] = {m_xmax[0] - m_xmin[0],
                    m_xmax[1] - m_xmin[1],
                    m_xmax[2] - m_xmin[2]};
        
        int imax = 0;
        for (int i = 0; i < 3; ++i)
            if (d[i] > d[imax])
                imax = i;

        std::vector<int> v;
        for (auto &&uid : m_uids)
            v.push_back(fibers[uid].m_x[imax]);
        std::sort(v.begin(), v.end());
        int x = v[v.size() / 2]; // mediana

        // divide os filhos pela mediana
        for (auto &&uid : m_uids)
            fibers[uid].m_x[imax] < x ? m_lft->add(uid, fibers) : m_rht->add(uid, fibers);

        // libera as fibras
        m_uids.clear();
    }

    /**
     * @brief Get the neighs object
     * 
     * @param n 
     * @param neighs 
     */
    void get_neighs(fiber_t &f, int &n, std::vector<int>& neighs)
    {
        if (m_level == 0)
            n = 0;
        // se a fibra estiver em contato com uma face do bounding box,
        // então ao menos uma componente de dxmin ou dxmax deve ser nula.
        int fid = -1; // indice da face tocada

        bool touch = true;
        for (int i = 0; i < 3 && touch; ++i)
            if (m_xmin[i] > f.m_x[i] || m_xmax[i] < f.m_x[i])
                touch == false;
        
        if (touch == false)
            return;

        if (m_splitted)
        {
            m_lft->get_neighs(f, n, neighs);
            m_rht->get_neighs(f, n, neighs);            
        }

        for(int i = 0; i < m_uids.size(); ++i)
            neighs[n + i] = m_uids[i];
    }
};

inline bool share_face(int *umin, int *umax, int *p)
{
    // não compartilha qualquer face
    if (umin[1] <= p[1] && p[1] < umax[1])
        return false;

    // compartilha a face da frente
    if (umin[0] == (p[0] + 1) && umin[2] == p[2])
        return true;

    // compartilha a face de cima
    if (umin[0] == p[0] && umax[2] == p[2])
        return true;

    // compartilha a face de trás
    if (umax[0] == p[0] && umin[2] == p[2])
        return true;

    // compartilha a face de baixo
    if (umin[0] == p[0] && umin[2] == (p[2] + 1))
        return true;

    return false;
}

/**
 * @brief 
 * 
 * @param f 
 * @param n    Na entrada, n indica o número de elementos em uids. Na saída, se f estiver 
 *             em overlap com alguma fibra, então n == -1, caso contrário, n retorna o 
 *             número de elementos de uids que compartilham uma face com f.
 * @param uids Na entrada, os n primeiros elementos de uids são as índices das fibras que
 *             podem estar em contato com a fibra f. Na saída, n é atualizado e todos os 
 *             n primeiros índices estão efetivamente em contato com f.
 * @param fibers vetor de todas as fibras do cluster.
 */
void bind_filter(fiber_t& f, int n, std::vector<int> uids, std::vector<fiber_t> fibers)
{
    // base e topo da fibra f (note que ftop é diferente de fmax)
    int fmin[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
    int ftop[3] = {f.m_x[0], f.m_x[1] + f.m_h, f.m_x[2]};
    
    int k = 0; // número de fibras do cluster em contato com a fibra f
    for(int i = 0; i < n; ++i )
    {
        int uid = uids[i];
        fiber_t& u = fibers[uid];
        // umin e umax definem o bounding box da fibra u
        int umin[3] = {u.m_x[0], u.m_x[1], u.m_x[2]};
        int umax[3] = {u.m_x[0] + 1, f.m_x[1] + u.m_h, u.m_x[2]};

        // check overlap
        // se as fibras estiverem em overlap, o topo (ftop) ou 
        // a base (fmin) da fibra f estará contida no bounding 
        // box da fibra u.
        bool overlap = true;        
        for (int j = 0; j < 3; j++)
        {
            if (ftop[j] < umin[j] || ftop[j] > umax[j])
            {
                overlap = false;
                break;
            }
            if (fmin[j] < umin[j] || fmin[j] > umax[j])
            {
                overlap = false;
                break;
            }
        }
        if (overlap)
        {
            n = -1;
            return;
        }

        // verificação/identificação da face em contato com a fxmin ou ftop
        //    (1,0,1) +-------------------------+ (1,h,1)
        //          / |z                       /| 
        // (0,0,1) +--------------------------+ |
        //         |  |-----------------------|-+ (1,h,0)
        //         | /x                       |/ 
        // (0,0,0) +--------------------------+ (0,h,0)
        //                       y
        // umin = (0,0,0)
        // umax = (1,h,1)        

        if(share_face(umin, umax, fmin))
            uids[k++] = uid;
        
        if(share_face(umin, umax, ftop))
            uids[k++] = uid;
    }
    n = k;
}

bool test_kdt()
{
    const int height = 18;
    int max_num_uids = 10;
    int num_bind = 10;
    std::vector<fiber_t> fibers;

    int uid = 0;
    int x = 0;
    int y = -height / 2;
    int z = 0;
    fibers.push_back(fiber_t(uid, x, y, z, height));

    int dx = 1;
    int dy = height;
    int dz = 1;

    fiber_t &f = fibers[uid];
    kdt_t kdt(max_num_uids, height);

    bool new_fiber = true;
    while(uid < num_bind)
    {        
        int x = 0; // rand
        int y = -height / 2; // rand
        int z = 0; // rand
        if(new_fiber)
            fibers.push_back(fiber_t(++uid, x, y, z, height));
        else
        {
            fibers[uid].m_x[0] = x;
            fibers[uid].m_x[1] = y;
            fibers[uid].m_x[2] = z;
        }

        kdt.add(uid, fibers);
    }
}