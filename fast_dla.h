#include <math.h>
#include <cmath>
#include <cstdio>
#include <vector>
#include <cstdlib>
#include <stdexcept>
#include <algorithm>


#define MAX(a, b) (((a) > (b)) ? (a) : (b))

const double PI = 3.141592654;

class fiber_t
{
public:
    int m_uid;
    int m_x[3];
    int m_height;

    fiber_t(int uid, int x, int y, int z, int h)
    {
        m_uid = uid;
        m_x[0] = x;
        m_x[1] = y;
        m_x[2] = z;
        m_height = h;
    }
};

class kdt_t
{
public:
    int m_level;
    int m_xmin[3];
    int m_xmax[3];
    int m_dx[3];
    int m_height;
    int m_max_num_uids;
    kdt_t *m_lft;
    kdt_t *m_rht;
    bool m_splitted;
    std::vector<int> m_uids;

    kdt_t(int max_num_uids, int height)
    {
        m_level = 0;
        m_lft = nullptr;
        m_rht = nullptr;
        m_max_num_uids = max_num_uids;
        m_height = height;
        m_splitted = false;
        m_dx[0] = 1;
        m_dx[1] = height;
        m_dx[2] = 1;
    }

    ~kdt_t()
    {
        delete m_lft;
        delete m_rht;
    }

    /**
     * @brief
     *
     * @param uid
     * @param fibers
     */
    void add(int uid, std::vector<fiber_t> &fibers)
    {
        fiber_t &f = fibers[uid];
        // primeira fibra
        if (m_splitted == false && m_uids.size() == 0)
        {
            // inicializa o bounding box
            for (int i = 0; i < 3; ++i)
            {
                m_xmin[i] = f.m_x[i];
                m_xmax[i] = f.m_x[i] + m_dx[i];
            }
        }
        else
        {
            // atualiza o bounding box
            for (int i = 0; i < 3; ++i)
            {
                if (m_xmin[i] > f.m_x[i])
                    m_xmin[i] = f.m_x[i];
                if (m_xmax[i] < f.m_x[i] + m_dx[i])
                    m_xmax[i] = f.m_x[i] + m_dx[i];
            }
        }
        if (m_splitted == false)
        {
            m_uids.push_back(uid);
            if (m_uids.size() > m_max_num_uids)
                split(fibers);
        }
        else
        {
            // adiciona ao filho que menos é afetado pela entrada da nova fibra
            int d, d_lft = 0, d_rht = 0;
            for (int i = 0; i < 3; ++i)
            {
                d = MAX(m_lft->m_xmin[i] - f.m_x[i], f.m_x[i] + m_dx[i] - m_lft->m_xmax[i]);
                if (d_lft < d)
                    d_lft = d;
            }
            for (int i = 0; i < 3; ++i)
            {
                d = MAX(m_rht->m_xmin[i] - f.m_x[i], f.m_x[i] + m_dx[i] - m_rht->m_xmax[i]);
                if (d_rht < d)
                    d_rht = d;
            }

            if (d_lft < d_rht)
                m_lft->add(uid, fibers);
            else
                m_rht->add(uid, fibers);
        }
    }

    /**
     * @brief
     *
     * @param fibers
     */
    void split(std::vector<fiber_t> &fibers)
    {
        // aloca os filhos
        m_lft = new kdt_t(m_max_num_uids, m_height);
        m_rht = new kdt_t(m_max_num_uids, m_height);
        m_lft->m_level = m_level + 1;
        m_rht->m_level = m_level + 1;

        // identifica a direção do corte como sendo a mais longa
        int d[3] = {m_xmax[0] - m_xmin[0] - m_dx[0],
                    m_xmax[1] - m_xmin[1] - m_dx[1],
                    m_xmax[2] - m_xmin[2] - m_dx[2]};

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

        if (m_lft->m_uids.size() == 0 || m_rht->m_uids.size() == 0)
        {
            printf("split failed (empty child)\n");
            exit(EXIT_FAILURE);
        }

        // libera as fibras
        m_uids.clear();
    }

    /**
     * @brief Get the neighs object
     *
     * @param n número de vizinhas na lista neighs
     * @param neighs lista dos uids do vizinhos
     */
    void get_neighs(fiber_t &f, int &n, std::vector<int> &neighs)
    {
        // inicializacao do n
        if (m_level == 0)
            n = 0;

        bool touch = true;
        for (int i = 0; i < 3 && touch; ++i)
            if (f.m_x[i] < (m_xmin[i] - m_dx[i]) || m_xmax[i] < (f.m_x[i] + m_dx[i]))
            {
                touch == false;
                return;
            }

        if (m_splitted)
        {
            m_lft->get_neighs(f, n, neighs);
            m_rht->get_neighs(f, n, neighs);
        }

        // resize neighs
        if ((m_uids.size() + n) > neighs.size())
        {
            neighs.resize(2 * (m_uids.size() + n));
        }

        for (int i = 0; i < m_uids.size(); ++i)
            neighs[n + i] = m_uids[i];
    }

    // calc diametro entre xmin e xmax
    int diameter()
    {
        int diam = 0;
        for (int i = 0; i < 3; ++i)
        {
            auto d = (m_xmax[i] - m_xmin[i]);
                diam += d * d;
        }
        return int(std::sqrt(diam));
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
 * @param f    Fibra a ser avaliada.
 * @param n    Na entrada, n indica o número de elementos em uids. Na saída, se f estiver
 *             em overlap com alguma fibra, então n == -1, caso contrário, n retorna o
 *             número de elementos de uids que compartilham uma face com f.
 * @param uids Na entrada, os n primeiros elementos de uids são as índices das fibras que
 *             podem estar em contato com a fibra f. Na saída, n é atualizado e todos os
 *             n primeiros índices estão efetivamente em contato com f.
 * @param fibers vetor de todas as fibras do cluster.
 */
void bind_filter(fiber_t &f, int n, std::vector<int> uids, std::vector<fiber_t> fibers)
{
    printf("neighs= ");
    // base e topo da fibra f (note que ftop é diferente de fmax)
    int fmin[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
    int ftop[3] = {f.m_x[0], f.m_x[1] + f.m_height - 1, f.m_x[2]};
    int fmax[3] = {f.m_x[0], f.m_x[1] + f.m_height - 1, f.m_x[2]};

    int k = 0; // número de fibras do cluster em contato com a fibra f
    for (int i = 0; i < n; ++i)
    {
        int uid = uids[i];
        fiber_t &u = fibers[uid];
        // umin e umax definem o bounding box da fibra u
        int umin[3] = {u.m_x[0], u.m_x[1], u.m_x[2]};
        int umax[3] = {u.m_x[0] + 1, f.m_x[1] + u.m_height, u.m_x[2]};

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
            printf("%d (overlap)\n", uid);
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

        if (share_face(umin, umax, fmin))
        {
            printf("%d ", uid);
                uids[k++] = uid;
        }

        if (share_face(umin, umax, ftop))
        {
            printf("%d ", uid);
                uids[k++] = uid;
        }
    }
    n = k;
    printf("\n");
}

void random_step(fiber_t &f)
{
    int &x = f.m_x[0];
    int &y = f.m_x[1];
    int &z = f.m_x[2];

    const int imove = rand() % 8;
    // (1, 0, 0)
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
}

inline bool check_out_sim(fiber_t &f, int max_dist, int radius)
{
    for (int i = 0; i < 3; ++i)
        if (std::abs(f.m_x[i]) > max_dist * radius)
            return true;
    return false;
}

/**
 * @brief
 *
 * @param f
 * @param n
 * @param uids
 * @param fibers
 * @param mode
 * @return true
 * @return false
 */
inline bool bind(fiber_t &f, int n, std::vector<int> &uids, std::vector<fiber_t> &fibers, char mode)
{
    if ('s')
    {
        if (n > 0)
        {
            for (int i = 0; i < n; ++i)
            {
                fiber_t &u = fibers[uids[i]];
                // check header
                for (int i = 0; i <= 4; ++i)
                    if (u.m_x[1] == (f.m_x[1] + 4 * i))
                        return true;

                // check tail
                for (int i = 0; i <= 4; ++i)
                    if (u.m_x[1] == (f.m_x[1] + f.m_height + 4 * i))
                        return true;
            }
        }
        return false;
    }
    else
        if (n > 0)
        {
            for (int i = 0; i < n; ++i)
            {
                fiber_t &u = fibers[uids[i]];
                // check header
                for (int i = 0; i <= 18; ++i)
                    if (u.m_x[1] == (f.m_x[1] + i))
                        return true;

                // check tail
                for (int i = 0; i <= 18; ++i)
                    if (u.m_x[1] == (f.m_x[1] + f.m_height + i))
                        return true;
            }
        }
        return false;
}
/**
int energy_surface(fiber_t &f, int n, std::vector<int> &uids, std::vector<fiber_t> &fibers)
{
    //     .+------+
    //   .' | N  .'|
    //  +------+'  |
    //  | W |  | E |
    //  |  ,+--|---+
    //  |.'  S | .'
    //  +------+'

    //TODO A LISTA DE VIZINHOS DEVE SER ATUALIZADA A CADA NOVA POSIÇÃO, ENTÃO É PRECISO PASSAR A KDT COMO ARGUMENTO DE ENTRADA.
    const int K = 4 * f.m_height + 2;
    bool E[K];
    for(int i = 0; i < K; ++i) 
        E[false];

    for (int i = 0; i < uids; i++)
    {
        fiber_t &u = fibers[uids[i]];        
    }
    return E;
}
**/

/**
void rolling_surface(fiber_t &f, int n, std::vector<int> &uids, std::vector<fiber_t> &fibers, char mode, int tmax)
{
    int xold[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
    int xopt[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
    int Emin = energy_surface(f, n, uids, fibers);
    for(int ts = 0; ts < tmax; ++ts)
    {
        random_step(f);
    }
}
**/
/**
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
**/
// generate random number for the range (min, max)
double irand(int imin, int imax)
{
    return (rand() / ((double)RAND_MAX)) * (imax - imin) + imin;

}

bool dla_collagen(int num_bind, char s)
{
    const int height = 18;
    int max_num_uids = 10;
    //int num_bind = 10;
    int max_dist = 10;
    std::vector<fiber_t> fibers;

    // first fiber
    int uid = 0;
    int x = 0;
    int y = -height / 2;
    int z = 0;
    fibers.push_back(fiber_t(uid, x, y, z, height));

    fiber_t &f = fibers[uid];
    kdt_t kdt(max_num_uids, height);

    int num_neighs = 0;
    std::vector<int> neighs_uid;
    bool new_fiber = true;
    int xold[3];
    while (uid < num_bind)
    {
        const int radius = kdt.diameter();
        printf("uid: %d\n", uid);

        while (true)
        {
            //launch new fiber
            if (new_fiber)
            {
                const double theta = irand(0, 2 * PI);
                const double phi = acos(irand(-1, 1));
                xold[0] = radius * cos(theta) * sin(phi);
                xold[1] = radius * sin(theta) * sin(phi);
                xold[2] = radius * cos(phi);
                fibers.push_back(fiber_t(++uid, xold[0], xold[1], xold[2], height));
                new_fiber = false;
            }
            // save current position
            for (int i = 0; i < 3; ++i)
                xold[i] = fibers[uid].m_x[i];

            // random walk
            random_step(fibers[uid]);

            // check out of simulation?
            if (check_out_sim(fibers[uid], max_dist, radius))
                break;

            // get possible neighs
            kdt.get_neighs(fibers[uid], num_neighs, neighs_uid);

            // check overlap or bind?
            if (num_neighs > 0)
            {
                bind_filter(fibers[uid], num_neighs, neighs_uid, fibers);
                printf("touch boundbox");

                // check overlap
                if (num_neighs == -1)
                {
                    printf("overlap\n");
                    // restore x
                    for (int i = 0; i < 3; ++i)
                        fibers[uid].m_x[i] = xold[i];
                    continue;
                }

                // check bind
                if (num_neighs > 0)
                {
                    new_fiber = bind(fibers[uid], num_neighs, neighs_uid, fibers, s);

                    if(new_fiber)
                    {
                        printf("fiber add");
                        break;
                    }

                    /**
                    if(new_fiber)
                    {
                        rolling_surface(fibers[uid], num_neighs, neighs_uids, fibers, 'n');
                        break;
                    }
                    **/
                }
            }
        }
    }
}
