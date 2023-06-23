import os 
import time
import json
import argparse
import numpy as np


class StressStrainData:
    def __init__(self) -> None:
        self.rods = {}
        self.layers = {}
        self.particles = {}
        self.lid_min = +np.inf
        self.lid_max = -np.inf

    def copy(self):
        ssd = StressStrainData()
        for rid, rod in self.rods.items():
            ssd.rods[rid] = rod.copy()
            ssd.rods[rid].ssd = ssd
        
        for pid, particle in self.particles.items():
            ssd.particles[pid] = particle.copy()
            ssd.particles[pid].ssd = ssd
        
        for lid, layer in self.layers.items():
            ssd.layers[lid] = layer.copy()

        ssd.lid_min = self.lid_min
        ssd.lid_max = self.lid_max
        return ssd

    def num_active_particles(self):
        k = 0
        for particle in self.particles.values():
            if particle.active:
                k +=1
        return k
    
    def filter_rids(self, reverse: bool = True):
        active_rids = set()
        for i, lid in enumerate(sorted(range(self.lid_min, self.lid_max + 1), reverse=reverse)):
            # pids in the current layer
            lid_pids = self.layers[lid].pids

            if i == 0:
                for pid_A in lid_pids:
                    particle_A: Particle = self.particles[pid_A]
                    active_rids.add(particle_A.rid)                    
                continue
            
            # layer is empty
            if len(lid_pids) == 0:
                active_rids.clear()
                return active_rids, self.rods.keys()

            for pid_A in lid_pids:
                particle_A: Particle = self.particles[pid_A]
                for rid_B in particle_A.get_neigh_rids():
                    if rid_B in active_rids:
                        active_rids.add(particle_A.rid)
                        break
        deleted_rids = self.clear_rids(active_rids)
        return active_rids, deleted_rids

    def clear_rids(self, active_rids:set):
        # inactive rods        
        deleted_rids = set()
        for rid in self.rods:
            if rid not in active_rids:
                self.rods[rid].inactivate()                
                deleted_rids.add(rid)
        # update rods
        self.rods = {rid: self.rods[rid] for rid in self.rods if rid not in deleted_rids}
        return deleted_rids
    
    def drop_rids(self, to_drop: set):
        # inactivate rods        
        for rid in self.rods:
            if rid in to_drop:
                self.rods[rid].inactivate()
        # update rods
        self.rods = {rid: self.rods[rid] for rid in self.rods if rid not in to_drop}
    
    def set_rods_exponent(self, m:int):
        for rod in self.rods.values():
            rod.m = m


class Particle:
    def __init__(self, ssd:StressStrainData, pid: int, rid: int, lid: int, xz):
        self.pid = pid
        self.rid = rid
        self.lid = lid
        self.xz = xz
        self.active = True
        self.neigh_rids = set()
        self.ssd = ssd

    def copy(self):
        particle = Particle(self.ssd, self.pid, self.rid, self.lid, self.xz.copy())
        particle.active = self.active
        particle.neigh_rids = self.neigh_rids.copy()
        return particle

    def add_neigh_rid(self, rid:int):
        self.neigh_rids.add(rid)
        rod : Rod = self.ssd.rods[rid]
        rod.add_neigh_pid(self.pid)

    def del_neigh_rid(self, rid:int):
        self.neigh_rids.remove(rid)

    def get_neigh_rids(self):
        return self.neigh_rids

    def innactive(self):
        self.active = False
        # remove the particle from the layer
        layer: Layer = self.ssd.layers[self.lid]
        layer.del_pid(self.pid)
        for rid in self.neigh_rids:
            # remove the particle from the neigh rods
            rod: Rod = self.ssd.rods[rid]
            rod.del_neigh_pid(self.pid)

    def to_str(self):
        s = f'"pid": {self.pid}, "rid": {self.rid}, "lid": {self.lid}, "xz": [{self.xz[0]}, {self.xz[1]}]'
        s += ', "neigh_rids": ['
        for rid in self.neigh_rids:
            s += f'{rid},'
        s += ']'
        s = '{' + s.replace(',]', ']') + '}'        
        return s

    @staticmethod
    def parse(ssd: StressStrainData, row: str):
        row = json.loads(row)
        pid = row['pid']
        rid = row['rid']
        lid = row['lid']
        xz = np.array(row['xz'], dtype=float)
        particle = Particle(ssd, pid, rid, lid, xz)
        particle.neigh_rids = set(row['neigh_rids'])
        particle.active = True
        return particle


class Rod:
    def __init__(self, ssd:StressStrainData, rid:int):
        self.ssd = ssd
        self.rid = rid
        self.active = True
        self.pids = set()
        self.updated = False
        self.neigh_pids = set()

        # force parameters
        self.m = 2
        self.sigma_cte = 1

        # force variables
        self.N = 0
        self.p = 0
        self.F = 1
        self.sigma_mean = 0

    def copy(self):
        rod = Rod(self.ssd, self.rid)
        rod.active = self.active
        rod.pids = self.pids.copy()
        rod.updated = self.updated
        rod.neigh_pids = self.neigh_pids.copy()

        # force parameters
        rod.m = self.m
        rod.sigma_cte = self.sigma_cte

        # force variables
        rod.N = self.N
        rod.p = self.p
        rod.F = self.F
        rod.sigma_mean = self.sigma_mean

        return rod
        
    def add_pid(self, pid:int):
        self.pids.add(pid)
        self.updated = False

    def del_neigh_pid(self, pid:int):
        self.neigh_pids.remove(pid)
        self.updated = False

    def add_neigh_pid(self, pid:int):
        self.neigh_pids.add(pid)
        self.updated = False

    def inactivate(self):
        self.active = False
        for pid in self.pids:
            particle:Particle = self.ssd.particles[pid]
            particle.innactive()

        for pid in self.neigh_pids:
            particle:Particle = self.ssd.particles[pid]
            particle.del_neigh_rid(self.rid)

    def update_force(self, F:float):
        self.N = len(self.neigh_pids)
        if self.N == 0:
            self.p = 1 # if rod not have neighs, the prob
            return self.p            
        self.sigma_mean *= (F / self.F)
        self.p = (self.sigma_mean / (self.N * self.sigma_cte))**self.m
        self.F = F # update the force
        return self.p

    def update_sigma(self, F: float):
        n = np.zeros(len(self.pids)) # number of neigh_pids per layer
        for i, pid_A in enumerate(self.pids):
            particle: Particle = self.ssd.particles[pid_A]
            n[i] = self.ssd.layers[particle.lid].len()
        self.sigma_mean = np.mean(self.F / n)
        self.updated = True
        return self.update_force(F)
            
    def prob_break(self, F:float):
        if self.updated:
            return self.update_force(F)
        else:
            return self.update_sigma(F)
    
    def to_str(self):
        s = f'"rid": {self.rid}, "pids": ['
        for pid in self.pids:
            s += f'{pid},'
        s += '], "neigh_pids": ['
        for pid in self.neigh_pids:
            s += f'{pid},'
        s += ']'
        s = '{' + s.replace(',]', ']') + '}'
        return s    

    @staticmethod
    def parse(ssd: StressStrainData, row: str):
        row = json.loads(row)
        rid = row['rid']
        rod = Rod(ssd, rid)
        rod.pids = set(row['pids'])
        rod.neigh_pids = set(row['neigh_pids'])
        rod.active = True
        rod.updated = False
        return rod
                    

class Layer:
    def __init__(self, lid:int):
        self.lid = lid
        self.pids = set()

    def copy(self):
        layer = Layer(self.lid)
        layer.pids = self.pids.copy()
        return layer

    def len(self):
        return len(self.pids)

    def add_pid(self, pid:int):
        self.pids.add(pid)

    def del_pid(self, pid:int):
        if pid in self.pids:
            self.pids.remove(pid)

    def to_str(self):
        s = f'"lid": {self.lid}, "pids": ['
        for pid in self.pids:
            s += f'{pid},'
        s += ']'
        s = '{' + s.replace(',]', ']') + '}'
        return s
    
    @staticmethod
    def parse(row:str):
        row = json.loads(row)
        lid = row['lid']
        layer = Layer(lid)
        layer.pids = set(row['pids'])
        return layer


def create_neighs(layers: dict, particles: dict):
    # create connections
    print('Creating connections')
    for pid_A in particles:
        particle_A: Particle = particles[pid_A]
        for pid_B in layers[particle_A.lid].pids:
            if pid_A == pid_B:
                continue
            particle_B: Particle = particles[pid_B]
            # check if the particles are neighbors
            if np.linalg.norm(particle_A.xz - particle_B.xz) <= 1:
                particle_A.add_neigh_rid(particle_B.rid)
                particle_B.add_neigh_rid(particle_A.rid)


def read_or_create_ssd(fn_dat: str):
    fn_db = fn_dat.replace('.dat','.db')
    ssd = StressStrainData()

    if os.path.exists(fn_db):
        print('Reading ', fn_db)
        tic = time.time()
        with open(fn_db, 'r') as fid:
            for row in fid:
                if row.startswith('{"pid":'):
                    particle = Particle.parse(ssd, row)
                    ssd.particles[particle.pid] = particle
                if row.startswith('{"rid":'):
                    rod = Rod.parse(ssd, row)
                    ssd.rods[rod.rid] = rod
                if row.startswith('{"lid":'):
                    layer = Layer.parse(row)
                    ssd.layers[layer.lid] = layer
        ssd.lid_min = min(ssd.layers.keys())
        ssd.lid_max = max(ssd.layers.keys())
        toc = time.time() - tic
        print(f'   tElapsed {fn_db} in {toc:.2f} s')
        return ssd

    print('Creating ', fn_db)
    pid = 0
    with open(fn_dat, 'r') as fid:
        # each line is a particle and a rod is a set of particles
        for row in fid:
            row = row.split()
            # extract the fiber center (rectangular trapezoid)
            x = int(row[2])
            y = int(row[3])
            z = int(row[4])
            if np.abs(x) > 8:
                continue
            if np.abs(y) > 100:
                continue
            if np.abs(z) > 8:
                continue
            # add particle to the backbone
            rid = int(row[1])
            if rid not in ssd.rods:
                ssd.rods[rid] = Rod(ssd, rid)
            lid = y
            xz = np.array([x, z])
            # extend the rod
            for _ in range(18):
                p = Particle(ssd, pid, rid, lid, xz)
                # add particle to the backbone
                ssd.particles[pid] = p
                # add particle to the rod
                ssd.rods[rid].add_pid(pid)
                # add particle to the layer
                if lid not in ssd.layers:
                    ssd.layers[lid] = Layer(lid)
                ssd.layers[lid].add_pid(pid)
                pid += 1
                lid += 1
    lid = list(ssd.layers.keys())
    ssd.lid_max = int(max(lid))
    ssd.lid_min = int(min(lid))

    # check if there is any empty layer
    for lid in range(-100, 101):
        if lid not in ssd.layers or ssd.layers[lid].len() == 0:
            raise Exception(f'Layer {lid} is empty')
    
    create_neighs(ssd.layers, ssd.particles)

    # save the database
    with open(fn_db, 'w') as fid:
        for pid in ssd.particles:
            fid.write(ssd.particles[pid].to_str() + '\n')
        for rid in ssd.rods:
            fid.write(ssd.rods[rid].to_str() + '\n')
        for lid in ssd.layers:
            fid.write(ssd.layers[lid].to_str() + '\n')

    return ssd


def random_deleted_rids(ssd: StressStrainData, F):
    # sort k random float numbers in the range [0,1]
    r = np.random.random(len(ssd.rods))
    del_rids = []  # rods to be deleted
    for i, rid in enumerate(ssd.rods):
        rod: Rod = ssd.rods[rid]
        #TODO Question: can we delete the rods from the first or last layers?
        if r[i] < rod.prob_break(F):
            del_rids.append(rid)
    return del_rids


class Logger:
    def __init__(self):
        self.F = []
        self.num_active_particles = []
        self.num_deleted_rods = []

    def log(self, F, num_active_particles, num_deleted_rods):
        self.F.append(F)
        self.num_active_particles.append(num_active_particles)
        self.num_deleted_rods.append(num_deleted_rods)

    def save(self, fn):
        with open(fn, 'w') as fid:
            fid.write('F, num_active_particles, num_deleted_rods\n')
            for i in range(len(self.F)):
                fid.write(f'{self.F[i]}, {self.num_active_particles[i]}, {self.num_deleted_rods[i]}\n')


def stress_strain(ssd: StressStrainData, verbose: bool = False) -> Logger:
    # sweep the layers from up to down
    active_rids, deleted_rids = ssd.filter_rids(reverse=False)    
    
    # sweep the layers from down to up
    active_rids, deleted_rids = ssd.filter_rids(reverse=True)    

    # init logger
    logger = Logger()    
    logger.log(0, ssd.num_active_particles(), 0) 

    all_deleted_rids = []
    F = 0.5 # applied force
    while True:
        if verbose:  
            print('Number of rods:', len(ssd.rods))
            print('Force:', F, '=================================')
            print('Applying force')

        # random rods inactivation
        deleted_rids = random_deleted_rids(ssd, F)
        if len(deleted_rids) == 0:
            logger.log(F, ssd.num_active_particles(), len(all_deleted_rids))
            F += 0.5 # increment the force
            continue

        ssd.drop_rids(deleted_rids)
        all_deleted_rids += deleted_rids        
    
        if verbose:
            print('Filtering rods')
        
        # sweep the layers from up to down        
        active_rids, deleted_rids = ssd.filter_rids(reverse=False)
        all_deleted_rids += deleted_rids
        
        # if the backbone is empty, stop
        if len(active_rids) == 0:    
            break
        
        # sweep the layers from down to up        
        active_rids, deleted_rids = ssd.filter_rids(reverse=True)        
        all_deleted_rids += deleted_rids

        # if the backbone is empty, stop
        if len(active_rids) == 0:
            break
    logger.log(F, ssd.num_active_particles(), len(all_deleted_rids))
    return logger


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description='Process command line arguments.')

    # Add the desired command-line arguments    
    parser.add_argument('-file', type=str, help='File argument description', default='/home/michael/gitrepos/dla-collagen/mode_s_ts_2_nb_30000_seed_130_.dat')
    parser.add_argument('-m', type=int, help='Exponent of the rods', default=2)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments    
    fn = args.file
    m = args.m

    np.random.seed(4321)

    # Read particles
    tic = time.time()
    ssd = read_or_create_ssd(fn)
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")

    ssd.set_rods_exponent(m)
    
    for k in range(0, 1000):
        ssd_copy = ssd.copy()
        print("rodada: %d" % k)
        tic = time.time()
        logger = stress_strain(ssd_copy, verbose=False)
        toc = time.time()
        print(f"   Elapsed time: {toc-tic:.2f} s")
        
        # Save porcent. of particles in skeleton
        fn_log = fn.replace('.dat', f'_m_{m}_k_{k}.csv')
        logger.save(fn_log)


if __name__ == '__main__':
    main()
