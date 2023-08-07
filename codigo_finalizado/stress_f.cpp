#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <nlohmann/json.hpp>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <string>
#include <vector>
#include <chrono>
#include <boost/program_options.hpp>



class StressStrainData
{
public:
    StressStrainData()
    {
        lid_min = std::numeric_limits<int>::infinity();
        lid_max = -std::numeric_limits<int>::infinity();
    }

    StressStrainData *copy()
    {
        StressStrainData *ssd = new StressStrainData();
        for (auto &[rid, rod] : rods)
        {
            ssd->rods[rid] = rod->copy();
            ssd->rods[rid]->ssd = ssd;
        }
        for (auto &[pid, particle] : particles)
        {
            ssd->particles[pid] = particle->copy();
            ssd->particles[pid]->ssd = ssd;
        }
        for (auto &[lid, layer] : layers)
        {
            ssd->layers[lid] = layer->copy();
        }
        ssd->lid_min = lid_min;
        ssd->lid_max = lid_max;
        return ssd;
    }

    int num_active_particles()
    {
        int k = 0;
        for (auto &[_, particle] : particles)
        {
            if (particle->active)
            {
                k += 1;
            }
        }
        return k;
    }

    std::pair<std::set<int>, std::set<int>> filter_rids(bool reverse = true)
    {
        std::set<int> active_rids;
        std::vector<int> lids(lid_max - lid_min + 1);
        std::iota(lids.begin(), lids.end(), lid_min);
        if (reverse)
        {
            std::reverse(lids.begin(), lids.end());
        }
        for (int i = 0; i < lids.size(); i++)
        {
            int lid = lids[i];
            auto &lid_pids = layers[lid]->pids;

            if (i == 0)
            {
                for (auto pid_A : lid_pids)
                {
                    auto particle_A = particles[pid_A];
                    active_rids.insert(particle_A->rid);
                }
                continue;
            }
            if (lid_pids.empty())
            {
                active_rids.clear();
                return {active_rids, rods};
            }
            for (auto pid_A : lid_pids)
            {
                auto particle_A = particles[pid_A];
                for (auto rid_B : particle_A->get_neigh_rids())
                {
                    if (active_rids.find(rid_B) != active_rids.end())
                    {
                        active_rids.insert(particle_A->rid);
                        break;
                    }
                }
            }
            auto deleted_rids = clear_rids(active_rids);
            return {active_rids, deleted_rids};
        }
    }

    // ... rest of the methods

private:
    std::map<int, Rod *> rods;
    std::map<int, Layer *> layers;
    std::map<int, Particle *> particles;
    int lid_min;
    int lid_max;

    // Additional private methods if needed
};


class Particle
{
public:
    Particle(StressStrainData *ssd, int pid, int rid, int lid, std::vector<double> xz)
        : pid(pid), rid(rid), lid(lid), xz(xz), active(true), ssd(ssd) {}

    Particle *copy()
    {
        Particle *particle = new Particle(ssd, pid, rid, lid, xz);
        particle->active = active;
        particle->neigh_rids = neigh_rids;
        return particle;
    }

    void add_neigh_rid(int rid)
    {
        neigh_rids.insert(rid);
        Rod *rod = ssd->rods[rid];
        rod->add_neigh_pid(pid);
    }

    void del_neigh_rid(int rid)
    {
        neigh_rids.erase(rid);
    }

    std::set<int> get_neigh_rids()
    {
        return neigh_rids;
    }

    void inactivate()
    {
        active = false;
        Layer *layer = ssd->layers[lid];
        layer->del_pid(pid);
        for (int rid : neigh_rids)
        {
            Rod *rod = ssd->rods[rid];
            rod->del_neigh_pid(pid);
        }
    }

    std::string to_str()
    {
        std::string s = "\"pid\": " + std::to_string(pid) + ", \"rid\": " + std::to_string(rid) +
                        ", \"lid\": " + std::to_string(lid) + ", \"xz\": [" + std::to_string(xz[0]) + ", " + std::to_string(xz[1]) + "]";
        s += ", \"neigh_rids\": [";
        for (int rid : neigh_rids)
        {
            s += std::to_string(rid) + ",";
        }
        s += "]";
        s = "{" + s.replace(s.find(",]"), 2, "]") + "}";
        return s;
    }

    static Particle *parse(StressStrainData *ssd, const std::string &row)
    {
        auto j = nlohmann::json::parse(row);
        int pid = j["pid"];
        int rid = j["rid"];
        int lid = j["lid"];
        std::vector<double> xz = j["xz"].get<std::vector<double>>();
        Particle *particle = new Particle(ssd, pid, rid, lid, xz);
        particle->neigh_rids = std::set<int>(j["neigh_rids"].begin(), j["neigh_rids"].end());
        particle->active = true;
        return particle;
    }

private:
    int pid;
    int rid;
    int lid;
    std::vector<double> xz;
    bool active;
    std::set<int> neigh_rids;
    StressStrainData *ssd;
};


class Rod
{
public:
    Rod(StressStrainData *ssd, int rid)
        : ssd(ssd), rid(rid), active(true), updated(false), m(2), sigma_cte(1), N(0), p(0), F(1), sigma_mean(0) {}

    Rod *copy()
    {
        Rod *rod = new Rod(ssd, rid);
        rod->active = active;
        rod->pids = pids;
        rod->updated = updated;
        rod->neigh_pids = neigh_pids;

        // force parameters
        rod->m = m;
        rod->sigma_cte = sigma_cte;

        // force variables
        rod->N = N;
        rod->p = p;
        rod->F = F;
        rod->sigma_mean = sigma_mean;

        return rod;
    }

    void add_pid(int pid)
    {
        pids.insert(pid);
        updated = false;
    }

    void del_neigh_pid(int pid)
    {
        neigh_pids.erase(pid);
        updated = false;
    }

    void add_neigh_pid(int pid)
    {
        neigh_pids.insert(pid);
        updated = false;
    }

    void inactivate()
    {
        active = false;
        for (int pid : pids)
        {
            Particle *particle = ssd->particles[pid];
            particle->inactivate();
        }
        for (int pid : neigh_pids)
        {
            Particle *particle = ssd->particles[pid];
            particle->del_neigh_rid(rid);
        }
    }

    double update_force(double F)
    {
        N = neigh_pids.size();
        if (N == 0)
        {
            p = 1; // if rod not have neighs, the prob
            return p;
        }
        sigma_mean *= (F / this->F);
        p = std::pow(sigma_mean / (N * sigma_cte), m);
        this->F = F; // update the force
        return p;
    }

    double update_sigma(double F)
    {
        std::vector<double> n(pids.size(), 0); // number of neigh_pids per layer
        int i = 0;
        for (int pid_A : pids)
        {
            Particle *particle = ssd->particles[pid_A];
            n[i++] = ssd->layers[particle->lid]->len();
        }
        sigma_mean = std::accumulate(n.begin(), n.end(), 0.0) / n.size();
        sigma_mean = F / sigma_mean;
        updated = true;
        return update_force(F);
    }

    double prob_break(double F)
    {
        return updated ? update_force(F) : update_sigma(F);
    }

    std::string to_str()
    {
        std::string s = "\"rid\": " + std::to_string(rid) + ", \"pids\": [";
        for (int pid : pids)
        {
            s += std::to_string(pid) + ",";
        }
        s += "], \"neigh_pids\": [";
        for (int pid : neigh_pids)
        {
            s += std::to_string(pid) + ",";
        }
        s += "]";
        s = "{" + s.replace(s.find(",]"), 2, "]") + "}";
        return s;
    }

    static Rod *parse(StressStrainData *ssd, const std::string &row)
    {
        auto j = nlohmann::json::parse(row);
        int rid = j["rid"];
        Rod *rod = new Rod(ssd, rid);
        rod->pids = std::set<int>(j["pids"].begin(), j["pids"].end());
        rod->neigh_pids = std::set<int>(j["neigh_pids"].begin(), j["neigh_pids"].end());
        rod->active = true;
        rod->updated = false;
        return rod;
    }

private:
    StressStrainData *ssd;
    int rid;
    bool active;
    std::set<int> pids;
    bool updated;
    std::set<int> neigh_pids;

    // force parameters
    int m;
    double sigma_cte;

    // force variables
    int N;
    double p;
    double F;
    double sigma_mean;
};



class Layer
{
public:
    Layer(int lid) : lid(lid) {}

    Layer *copy()
    {
        Layer *layer = new Layer(lid);
        layer->pids = pids;
        return layer;
    }

    size_t len()
    {
        return pids.size();
    }

    void add_pid(int pid)
    {
        pids.insert(pid);
    }

    void del_pid(int pid)
    {
        pids.erase(pid);
    }

    std::string to_str()
    {
        std::string s = "\"lid\": " + std::to_string(lid) + ", \"pids\": [";
        for (int pid : pids)
        {
            s += std::to_string(pid) + ",";
        }
        s += "]";
        s = "{" + s.replace(s.find(",]"), 2, "]") + "}";
        return s;
    }

    static Layer *parse(const std::string &row)
    {
        auto j = nlohmann::json::parse(row);
        int lid = j["lid"];
        Layer *layer = new Layer(lid);
        layer->pids = std::set<int>(j["pids"].begin(), j["pids"].end());
        return layer;
    }

private:
    int lid;
    std::set<int> pids;
};

#include <cmath> // For std::sqrt

void create_neighs(std::map<int, Layer *> &layers, std::map<int, Particle *> &particles)
{
    // Creating connections
    for (auto &[pid_A, particle_A] : particles)
    {
        for (int pid_B : layers[particle_A->lid]->pids)
        {
            if (pid_A == pid_B)
            {
                continue;
            }
            Particle *particle_B = particles[pid_B];
            // Check if the particles are neighbors
            double distance = std::sqrt(std::pow(particle_A->xz[0] - particle_B->xz[0], 2) +
                                        std::pow(particle_A->xz[1] - particle_B->xz[1], 2));
            if (distance <= 1)
            {
                particle_A->add_neigh_rid(particle_B->rid);
                particle_B->add_neigh_rid(particle_A->rid);
            }
        }
    }
}



StressStrainData *read_or_create_ssd(const std::string &fn_dat)
{
    std::string fn_db = fn_dat;
    fn_db.replace(fn_db.find(".dat"), 4, ".db");
    StressStrainData *ssd = new StressStrainData();

    if (std::filesystem::exists(fn_db))
    {
        std::cout << "Reading " << fn_db << '\n';
        auto tic = std::clock();
        std::ifstream fid(fn_db);
        std::string row;
        while (std::getline(fid, row))
        {
            if (row.find("{\"pid\":") == 0)
            {
                Particle *particle = Particle::parse(ssd, row);
                ssd->particles[particle->pid] = particle;
            }
            if (row.find("{\"rid\":") == 0)
            {
                Rod *rod = Rod::parse(ssd, row);
                ssd->rods[rod->rid] = rod;
            }
            if (row.find("{\"lid\":") == 0)
            {
                Layer *layer = Layer::parse(row);
                ssd->layers[layer->lid] = layer;
            }
        }
        ssd->lid_min = std::min_element(ssd->layers.begin(), ssd->layers.end())->first;
        ssd->lid_max = std::max_element(ssd->layers.begin(), ssd->layers.end())->first;
        auto toc = (std::clock() - tic) / (double)CLOCKS_PER_SEC;
        // std::cout << "   tElapsed " << fn_db << " in " << toc << " s\n";
        return ssd;
    }

    std::cout << "Creating " << fn_db << '\n';
    int pid = 0;
    std::ifstream fid(fn_dat);
    std::string row;
    while (getline(fid, row_str))
    {
        vector<string> row;
        string word = "";
        for (auto c : row_str)
        {
            if (c == ' ')
            {
                row.push_back(word);
                word = "";
            }
            else
            {
                word += c;
            }
        }
        row.push_back(word);
        // extract the fiber center (rectangular trapezoid)
        int x = stoi(row[2]);
        int y = stoi(row[3]);
        int z = stoi(row[4]);
        if (abs(x) > 8)
        {
            continue;
        }
        if (abs(y) > 100)
        {
            continue;
        }
        if (abs(z) > 8)
        {
            continue;
        }
        // add particle to the backbone
        int rid = stoi(row[1]);
        int lid = y;
        vector<int> xz = {x, z};
        Particle p(ssd, pid, rid, lid, xz);
        // add particle to the backbone
        ssd.particles[pid] = p;
        // add particle to the rod
        if (ssd.rods.find(rid) == ssd.rods.end())
        {
            ssd.rods[rid] = Rod(ssd, rid);
        }
        ssd.rods[rid].add_pid(pid);
        // add particle to the layer
        if (ssd.layers.find(lid) == ssd.layers.end())
        {
            ssd.layers[lid] = Layer(lid);
        }
        ssd.layers[lid].add_pid(pid);
        pid += 1;
    }

    ssd->lid_max = std::max_element(ssd->layers.begin(), ssd->layers.end())->first;
    ssd->lid_min = std::min_element(ssd->layers.begin(), ssd->layers.end())->first;

    create_neighs(ssd->layers, ssd->particles);

    // Save the database
    std::ofstream ofid(fn_db);
    for (const auto &[pid, particle] : ssd->particles)
    {
        ofid << particle->to_str() << '\n';
    }
    for (const auto &[rid, rod] : ssd->rods)
    {
        ofid << rod->to_str() << '\n';
    }
    for (const auto &[lid, layer] : ssd->layers)
    {
        ofid << layer->to_str() << '\n';
    }

    return ssd;
}


std::vector<int> random_deleted_rids(StressStrainData *ssd, double F)
{
    // Sort k random float numbers in the range [0,1]
    std::vector<double> r(ssd->rods.size());
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0, 1);
    for (double &value : r)
    {
        value = dis(gen);
    }

    std::vector<int> del_rids; // Rods to be deleted
    int i = 0;
    for (const auto &[rid, rod] : ssd->rods)
    {
        // TODO Question: can we delete the rods from the first or last layers?
        if (r[i++] < rod->prob_break(F))
        {
            del_rids.push_back(rid);
        }
    }
    return del_rids;
}

std::vector<int> random_deleted_rids(StressStrainData *ssd, double F)
{
    // Sort k random float numbers in the range [0,1]
    std::vector<double> r(ssd->rods.size());
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0, 1);
    for (double &value : r)
    {
        value = dis(gen);
    }

    std::vector<int> del_rids; // Rods to be deleted
    int i = 0;
    for (const auto &[rid, rod] : ssd->rods)
    {
        // TODO Question: can we delete the rods from the first or last layers?
        if (r[i++] < rod->prob_break(F))
        {
            del_rids.push_back(rid);
        }
    }
    return del_rids;
}



class Logger
{
public:
    Logger() {}

    void log(double F, int num_active_particles, int num_deleted_rods)
    {
        this->F.push_back(F);
        this->num_active_particles.push_back(num_active_particles);
        this->num_deleted_rods.push_back(num_deleted_rods);
    }

    void save(const std::string &fn, int k)
    {
        std::string new_folder = "/home/robert/Documentos/Data_zurik/Stress/";
        std::string fn_ = fn;
        fn_.replace(fn_.find("/home/robert/Documentos/Data_zurik/"), 40, new_folder);

        std::ofstream fid(fn_, std::ios::app);

        if (k == 0)
        {
            fid << "f,num_active_particles,num_deleted_particles,num_deleted_rods\n";
        }

        int initial_active_particles = num_active_particles[0];
        for (size_t i = 0; i < F.size(); ++i)
        {
            int a = initial_active_particles - num_active_particles[i];
            fid << F[i] << "," << num_active_particles[i] << "," << a << "," << num_deleted_rods[i] << "\n";
        }

        fid << "----------------------------------------------" << k << "\n";
    }

private:
    std::vector<double> F;
    std::vector<int> num_active_particles;
    std::vector<int> num_deleted_rods;
};


Logger stress_strain(StressStrainData *ssd, bool verbose = false)
{
    // Sweep the layers from up to down
    auto [active_rids1, deleted_rids1] = ssd->filter_rids(false);

    // Sweep the layers from down to up
    auto [active_rids2, deleted_rids2] = ssd->filter_rids(true);

    // Init logger
    Logger logger;
    logger.log(0, ssd->num_active_particles(), 0);

    std::vector<int> all_deleted_rids;
    double F = 0.5; // Applied force
    while (true)
    {
        if (verbose)
        {
            std::cout << "Number of rods: " << ssd->rods.size() << '\n';
            std::cout << "Force: " << F << " =================================\n";
            std::cout << "Applying force\n";
        }

        // Random rods inactivation
        auto deleted_rids = random_deleted_rids(ssd, F);
        if (deleted_rids.empty())
        {
            logger.log(F, ssd->num_active_particles(), all_deleted_rids.size());
            F += 0.5; // Increment the force
            continue;
        }

        ssd->drop_rids(deleted_rids);
        all_deleted_rids.insert(all_deleted_rids.end(), deleted_rids.begin(), deleted_rids.end());

        if (verbose)
        {
            std::cout << "Filtering rods\n";
        }

        // Sweep the layers from up to down
        auto [active_rids3, deleted_rids3] = ssd->filter_rids(false);
        all_deleted_rids.insert(all_deleted_rids.end(), deleted_rids3.begin(), deleted_rids3.end());

        // If the backbone is empty, stop
        if (active_rids3.empty())
        {
            logger.log(F, 0, all_deleted_rids.size());
            break;
        }

        // Sweep the layers from down to up
        auto [active_rids4, deleted_rids4] = ssd->filter_rids(true);
        all_deleted_rids.insert(all_deleted_rids.end(), deleted_rids4.begin(), deleted_rids4.end());

        // If the backbone is empty, stop
        if (active_rids4.empty())
        {
            logger.log(F, 0, all_deleted_rids.size());
            break;
        }
    }

    logger.log(F, ssd->num_active_particles(), all_deleted_rids.size());
    return logger;
}


int main(int argc, char *argv[])
{
    namespace po = boost::program_options;

    // Create an argument parser
    po::options_description desc("Process command line arguments.");

    // Add the desired command-line arguments
    desc.add_options()("file", po::value<std::string>()->default_value("/home/michael/gitrepos/dla-collagen/mode_s_ts_2_nb_30000_seed_130_.dat"), "File argument description")("m", po::value<int>()->default_value(2), "Exponent of the rods")("n", po::value<int>()->default_value(1000), "Number of repetitions for statistic");

    // Parse the command-line arguments
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    // Access the values of the arguments
    std::string fn = vm["file"].as<std::string>();
    int m = vm["m"].as<int>();
    int n = vm["n"].as<int>();

    // Seed random number generator
    std::srand(4321);

    // Read particles
    auto tic = std::chrono::high_resolution_clock::now();
    auto ssd = read_or_create_ssd(fn);
    auto toc = std::chrono::high_resolution_clock::now();
    // std::chrono::duration<double> elapsed = toc - tic;
    // std::cout << "   Elapsed time: " << elapsed.count() << " s\n";

    ssd->set_rods_exponent(m);
    std::string fn_log = fn;
    fn_log.replace(fn_log.find(".dat"), 4, "_m_" + std::to_string(m) + ".txt");

    for (int k = 0; k < n; ++k)
    {
        auto ssd_copy = ssd->copy();
        // std::cout << "Round: " << k << "\n";
        tic = std::chrono::high_resolution_clock::now();
        auto logger = stress_strain(ssd_copy, false);
        toc = std::chrono::high_resolution_clock::now();
        // elapsed = toc - tic;
        // std::cout << "   Elapsed time: " << elapsed.count() << " s\n";

        // Save percentage of particles in skeleton
        logger.save(fn_log, k);
    }

    return 0;
}
