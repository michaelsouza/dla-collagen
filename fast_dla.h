#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <math.h>
#include <stdexcept>
#include <vector>

#define MAX(a, b) (((a) > (b)) ? (a) : (b))

const double PI = 3.141592654;

// generate random number for the range (min, max)
double irand(int imin, int imax) {
  return (rand() / ((double)RAND_MAX)) * (imax - imin) + imin;
}

enum fiber_state_t { OVERLAP, FREE, BIND };

class fiber_t {
public:
  int m_uid;
  int m_x[3];
  int m_height;
  fiber_state_t m_state;

  fiber_t(int uid, int h, double radius) {
    m_uid = uid;
    m_height = h;
    random_reset(radius);
  }

  fiber_t(int uid, int h, int x, int y, int z) {
    m_uid = uid;
    m_height = h;
    m_x[0] = x;
    m_x[1] = y;
    m_x[2] = z;
    m_state = fiber_state_t::FREE;
  }

  void random_reset(double radius) {
    const double theta = irand(0, 2 * PI);
    const double phi = acos(irand(-1, 1));
    m_x[0] = radius * cos(theta) * sin(phi);
    m_x[1] = radius * sin(theta) * sin(phi);
    m_x[2] = radius * cos(phi);
    m_state = fiber_state_t::FREE;
  }

  void random_walk() {
    int &x = m_x[0];
    int &y = m_x[1];
    int &z = m_x[2];

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
    else if (imove == 4) {
      ++z;
      ++y;
    } else if (imove == 5) {
      --z;
      --y;
    }
    // (0, 1, -1)
    else if (imove == 6) {
      ++y;
      --z;
    } else if (imove == 7) {
      --y;
      ++z;
    }
  }
};

class kdt_t {
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

  kdt_t(int max_num_uids, int height) {
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

  ~kdt_t() {
    delete m_lft;
    delete m_rht;
  }

  /**
   * @brief
   *
   * @param uid
   * @param fibers
   */
  void add(int uid, std::vector<fiber_t> &fibers) {
    fiber_t &f = fibers[uid];
    // primeira fibra
    if (m_splitted == false && m_uids.size() == 0) {
      // inicializa o bounding box
      printf("ok \n");
      for (int i = 0; i < 3; ++i) {
        m_xmin[i] = f.m_x[i];
        m_xmax[i] = f.m_x[i] + m_dx[i];
        printf("xmin: %d , xmax: %d \n", m_xmin[i], m_xmax[i]);
      }
    } else {
      // atualiza o bounding box
      printf("Att bound\n");
      for (int i = 0; i < 3; ++i) {
        if (m_xmin[i] > f.m_x[i])
          m_xmin[i] = f.m_x[i];
        if (m_xmax[i] < f.m_x[i] + m_dx[i])
          m_xmax[i] = f.m_x[i] + m_dx[i];
        printf("xmin: %d , xmax: %d \n", m_xmin[i], m_xmax[i]);
      }
    }

    if (m_splitted == false) {
      m_uids.push_back(uid);
      if (m_uids.size() > m_max_num_uids)
        split(fibers);
    } else {
      // adiciona ao filho que menos é afetado pela entrada da nova fibra
      int d, d_lft = 0, d_rht = 0;
      for (int i = 0; i < 3; ++i) {
        d = MAX(m_lft->m_xmin[i] - f.m_x[i],
                f.m_x[i] + m_dx[i] - m_lft->m_xmax[i]);
        if (d_lft < d)
          d_lft = d;
      }
      for (int i = 0; i < 3; ++i) {
        d = MAX(m_rht->m_xmin[i] - f.m_x[i],
                f.m_x[i] + m_dx[i] - m_rht->m_xmax[i]);
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
  void split(std::vector<fiber_t> &fibers) {
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
      fibers[uid].m_x[imax] < x ? m_lft->add(uid, fibers)
                                : m_rht->add(uid, fibers);

    if (m_lft->m_uids.size() == 0 || m_rht->m_uids.size() == 0) {
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
  void get_neighs(const fiber_t &f, std::vector<int> &neighs) {
    // inicializacao do n
    if (m_level == 0)
      neighs.clear();

    bool touch = true;
    for (int i = 0; i < 3 && touch; ++i)
      if (f.m_x[i] < (m_xmin[i] - m_dx[i]) ||
          m_xmax[i] < (f.m_x[i] + m_dx[i])) {
        touch == false;
        return;
      }

    if (m_splitted) {
      m_lft->get_neighs(f, neighs);
      m_rht->get_neighs(f, neighs);
    }

    // resize neighs
    for (int i = 0; i < m_uids.size(); ++i) {
      neighs.push_back(m_uids[i]);
    }
  }

  // calc diametro entre xmin e xmax
  int diameter() {
    int diam = 0;
    for (int i = 0; i < 3; ++i) {
      auto d = m_xmax[i] - m_xmin[i];
      diam += d * d;
    }
    return int(std::sqrt(diam)) + 1;
  }
};

/**
 * @brief Retorna true se houver ao menos uma face compartilhada e false em caso
 *        contrário.
 *
 * @param umin
 * @param umax
 * @param p
 * @return true
 * @return false
 */
inline int num_shared_faces(const int umin[3], const int umax[3],
                            const int p[3]) {
  // verificação/identificação da face em contato com a fxmin ou ftop
  //           (1,0,1) +-------------------------+ (1,h,1) = umax
  //                 / |z                       /|
  //        (0,0,1) +--------------------------+ |
  //                |  +-----------------------|-+ (1,h,0)
  //                | /x                       |/
  // umin = (0,0,0) +--------------------------+ (0,h,0)
  //                             y

  const int umin_x = umin[0];
  const int umin_y = umin[1];
  const int umin_z = umin[2];

  const int umax_x = umax[0];
  const int umax_y = umax[1];
  const int umax_z = umax[2];

  const int p_x = p[0];
  const int p_y = p[1];
  const int p_z = p[2];

  // não compartilha qualquer face
  if (!(umin_y <= p_y && p_y < umax_y))
    return 0;

  int num_faces = umax_y - p_y;

  // compartilha a face da frente
  if ((umin_x - 1) == p_x && umin_z == p_z)
    return num_faces;

  // compartilha a face de cima
  if (umin_x == p_x && umax_z == p_z)
    return num_faces;

  // compartilha a face de trás
  if (umax_x == p_x && umin_z == p_z)
    return num_faces;

  // compartilha a face de baixo
  if (umin_x == p_x && (umin_z - 1) == p_z)
    return num_faces;

  return 0;
}

/**
 * @brief      Se f estiver em overlap com alguma fibra, seu estado é alterado
 * para OVERLAP, caso contrário, uids é atualizado para os índices das fibras em
 * contato com f.
 *
 * @param f    Fibra a ser avaliada.
 * @param uids Na entrata, é o vetor de índices das fibras que podem estar em
 * contato com a fibra f. Na saída, é atualizado para os índices que estão
 * efetivamente em contato com f.
 * @param fibers vetor de todas as fibras do cluster.
 */
void filter_shared_faces(fiber_t &f, std::vector<int> uids, std::vector<fiber_t> &fibers) {
  // verificação/identificação da face em contato com a fxmin ou ftop
  //           (1,0,1) +-------------------------+ (1,h,1) = umax
  //                 / |z                       /|
  //        (0,0,1) +--------------------------+ |
  //                |  |-----------------------|-+ (1,h,0)
  //                | /x                       |/
  // umin = (0,0,0) +--------------------------+ (0,h,0)
  //                             y

  printf("neighs= ");
  // base e topo da fibra f (note que ftop é diferente de fmax)
  int fmin[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int ftop[3] = {f.m_x[0], f.m_x[1] + f.m_height - 1, f.m_x[2]};
  int fmax[3] = {f.m_x[0], f.m_x[1] + f.m_height - 1, f.m_x[2]};

  int k = 0; // número de fibras do cluster em contato com a fibra f
  for (int i = 0; i < uids.size(); ++i) {
    int uid = uids[i];
    fiber_t &u = fibers[uid];
    // umin e umax definem o bounding box da fibra u
    int umin[3] = {u.m_x[0], u.m_x[1], u.m_x[2]};
    int umax[3] = {u.m_x[0] + 1, f.m_x[1] + u.m_height, u.m_x[2] + 1};

    // check overlap
    // se as fibras estiverem em overlap, o topo (ftop) ou
    // a base (fmin) da fibra f estará contida no bounding
    // box da fibra u.
    bool overlap = true;
    for (int j = 0; j < 3; j++) {
      if (ftop[j] < umin[j] || ftop[j] > umax[j]) {
        overlap = false;
        break;
      }
      if (fmin[j] < umin[j] || fmin[j] > umax[j]) {
        overlap = false;
        break;
      }
    }
    if (overlap) {
      f.m_state = fiber_state_t::OVERLAP;
      return;
    }

    // verificação/identificação da face em contato com a fxmin ou ftop
    //           (1,0,1) +-------------------------+ (1,h,1) = umax
    //                 / |z                       /|
    //        (0,0,1) +--------------------------+ |
    //                |  |-----------------------|-+ (1,h,0)
    //                | /x                       |/
    // umin = (0,0,0) +--------------------------+ (0,h,0)
    //                             y

    if (num_shared_faces(umin, umax, fmin))
      uids[k++] = uid;

    if (num_shared_faces(umin, umax, ftop))
      uids[k++] = uid;
  }
  uids.resize(k);
}

/**
 * @brief
 *
 * @param f
 * @param max_dist
 * @param radius
 * @return true
 * @return false
 */
inline bool check_out_sim(fiber_t &f, int max_dist, int radius) {

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
inline bool check_bind(fiber_t &f, std::vector<int> &uids,
                       std::vector<fiber_t> &fibers, char mode) {
  filter_shared_faces(f, uids, fibers);
  if (f.m_state == OVERLAP || uids.size() == 0)
    return false;

  if (mode == 's') {
    for (auto &&uid : uids) {
      fiber_t &u = fibers[uid];
      // checa se a base de u está em bind com f
      for (int i = 0; i <= 4; ++i)
        if (u.m_x[1] == (f.m_x[1] + 4 * i))
          return true;

      // checa se a base de f está em bind com u
      for (int i = 0; i <= 4; ++i)
        if (f.m_x[1] == (u.m_x[1] + 4 * i))
          return true;
    }
  } else if (mode == 'n') {
    for (auto &&uid : uids) {
      fiber_t &u = fibers[uid];

      // checa se a base de u está em bind com f
      if (f.m_x[1] <= u.m_x[1] && u.m_x[1] < (f.m_x[1] + f.m_height))
        return true;

      // checa se a base de f está em bind com u
      if (u.m_x[1] <= f.m_x[1] && f.m_x[1] < (u.m_x[1] + f.m_height))
        return true;
    }
  }
  return false;
}

/**
 * @brief Retorna o número de faces expostas.
 *
 * @param f
 * @param kdt
 * @param fibers
 * @return int
 * @remark O número máximo de faces expostas é 4 * f.m_height.
 */
int energy_surface(fiber_t &f, kdt_t &kdt, std::vector<fiber_t> &fibers) {
  //     .+------+
  //   .' | N  .'|
  //  +------+'  |
  //  | W |  | E |
  //  |  ,+--|---+
  //  |.'  S | .'
  //  +------+'

  std::vector<int> neighs;
  kdt.get_neighs(f, neighs);

  const int xmax[] = {f.m_x[0] + 1, f.m_x[1] + f.m_height, f.m_x[2] + 1};
  int energy = 4 * f.m_height;

  for (auto &&uid : neighs) {
    fiber_t &u = fibers[uid];
    energy -= num_shared_faces(f.m_x, xmax, u.m_x);
  }
  return energy;
}

void rolling_surface(fiber_t &f, kdt_t &kdt, std::vector<fiber_t> &fibers,
                     char mode, int tmax) {
  int xold[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int xopt[3] = {f.m_x[0], f.m_x[1], f.m_x[2]};
  int Emin = energy_surface(f, kdt, fibers);
  for (int ts = 0; ts < tmax; ++ts) {
    f.random_walk();
  }
}
