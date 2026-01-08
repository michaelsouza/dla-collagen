import os 
import time
import json
import argparse
import numpy as np
from collections import deque


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
                # Se a camada estiver vazia, todas as hastes restantes são consideradas deletadas
                # para o propósito de retorno, mas a limpeza real é feita em clear_rids.
                all_remaining_rids = set(self.rods.keys())
                deleted_rids = self.clear_rids(active_rids)
                return active_rids, deleted_rids

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
        all_current_rids = list(self.rods.keys())
        for rid in all_current_rids:
            if rid not in active_rids:
                if self.rods[rid].active: # Apenas inativa se já não estiver inativa
                    self.rods[rid].inactivate()                
                deleted_rids.add(rid)
        # update rods
        self.rods = {rid: self.rods[rid] for rid in self.rods if rid in active_rids}
        return deleted_rids
    
    def drop_rids(self, to_drop: set):
        # inactivate rods        
        for rid in to_drop:
            if rid in self.rods and self.rods[rid].active:
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
        if rid in self.ssd.rods:
            rod : Rod = self.ssd.rods[rid]
            rod.add_neigh_pid(self.pid)

    def del_neigh_rid(self, rid:int):
        if rid in self.neigh_rids:
            self.neigh_rids.remove(rid)

    def get_neigh_rids(self):
        return self.neigh_rids

    def innactive(self):
        if not self.active:
            return
        self.active = False
        if self.lid in self.ssd.layers:
            layer: Layer = self.ssd.layers[self.lid]
            layer.del_pid(self.pid)
        for rid in self.neigh_rids:
            if rid in self.ssd.rods:
                rod: Rod = self.ssd.rods[rid]
                rod.del_neigh_pid(self.pid)

    def to_str(self):
        s = f'"pid": {self.pid}, "rid": {self.rid}, "lid": {self.lid}, "xz": [{self.xz[0]}, {self.xz[1]}]'
        s += ', "neigh_rids": ['
        s += ",".join(map(str, sorted(list(self.neigh_rids))))
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
        self.m = 2
        self.sigma_cte = 1
        self.N = 0
        self.p = 0
        self.F = 1.0
        self.sigma_mean = 0.0

    def copy(self):
        rod = Rod(self.ssd, self.rid)
        rod.active = self.active
        rod.pids = self.pids.copy()
        rod.updated = self.updated
        rod.neigh_pids = self.neigh_pids.copy()
        rod.m = self.m
        rod.sigma_cte = self.sigma_cte
        rod.N = self.N
        rod.p = self.p
        rod.F = self.F
        rod.sigma_mean = self.sigma_mean
        return rod
        
    def add_pid(self, pid:int):
        self.pids.add(pid)
        self.updated = False

    def del_neigh_pid(self, pid:int):
        if pid in self.neigh_pids:
            self.neigh_pids.remove(pid)
        self.updated = False

    def add_neigh_pid(self, pid:int):
        self.neigh_pids.add(pid)
        self.updated = False

    def inactivate(self):
        if not self.active:
            return
        self.active = False
        for pid in self.pids:
            if pid in self.ssd.particles:
                particle:Particle = self.ssd.particles[pid]
                particle.innactive()
        for pid in self.neigh_pids:
            if pid in self.ssd.particles:
                particle:Particle = self.ssd.particles[pid]
                particle.del_neigh_rid(self.rid)

    def update_force(self, F:float):
        self.N = len(self.neigh_pids)
        if self.N == 0:
            self.p = 1.0
            return self.p            
        if self.F > 0:
            self.sigma_mean *= (F / self.F)
        self.p = (self.sigma_mean / (self.N * self.sigma_cte))**self.m
        self.F = F
        return self.p

    def update_sigma(self, F: float):
        n = np.zeros(len(self.pids))
        for i, pid_A in enumerate(self.pids):
            if pid_A in self.ssd.particles:
                particle: Particle = self.ssd.particles[pid_A]
                if particle.lid in self.ssd.layers:
                    n[i] = self.ssd.layers[particle.lid].len()
        
        valid_n = n[n > 0]
        if len(valid_n) > 0:
            self.sigma_mean = np.mean(self.F / valid_n)
        else:
            self.sigma_mean = 0
        self.updated = True
        return self.update_force(F)
            
    def prob_break(self, F:float):
        if self.updated:
            return self.update_force(F)
        else:
            return self.update_sigma(F)
    
    def to_str(self):
        s = f'"rid": {self.rid}, "pids": ['
        s += ",".join(map(str, sorted(list(self.pids))))
        s += '], "neigh_pids": ['
        s += ",".join(map(str, sorted(list(self.neigh_pids))))
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
        s += ",".join(map(str, sorted(list(self.pids))))
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


def find_deleted_rod_clusters(ssd: StressStrainData, deleted_rids: set) -> list[int]:
    if not deleted_rids:
        return []

    visited_rids = set()
    cluster_sizes = []

    for rid in deleted_rids:
        if rid in visited_rids:
            continue
        
        current_cluster_size = 0
        queue = deque([rid])
        visited_rids.add(rid)

        while queue:
            current_rid = queue.popleft()
            current_cluster_size += 1
            
            if current_rid in ssd.rods:
                rod = ssd.rods[current_rid]
                for pid in rod.pids:
                    if pid in ssd.particles:
                        particle = ssd.particles[pid]
                        for neigh_rid in particle.get_neigh_rids():
                            if neigh_rid in deleted_rids and neigh_rid not in visited_rids:
                                visited_rids.add(neigh_rid)
                                queue.append(neigh_rid)
        
        cluster_sizes.append(current_cluster_size)

    return sorted(cluster_sizes, reverse=True)


def create_neighs(layers: dict, particles: dict):
    for pid_A in particles:
        particle_A: Particle = particles[pid_A]
        for pid_B in layers[particle_A.lid].pids:
            if pid_A == pid_B:
                continue
            particle_B: Particle = particles[pid_B]
            if np.linalg.norm(particle_A.xz - particle_B.xz) <= 1:
                particle_A.add_neigh_rid(particle_B.rid)
                particle_B.add_neigh_rid(particle_A.rid)


def read_or_create_ssd(fn_dat: str):
    fn_db = fn_dat.replace('.dat','.db')
    ssd = StressStrainData()

    if os.path.exists(fn_db):
        print('Reading ', fn_db)
        tic = time.time()
        try:
            with open(fn_db, 'r') as fid:
                for row in fid:
                    if row.startswith('{"pid":'):
                        particle = Particle.parse(ssd, row)
                        ssd.particles[particle.pid] = particle
                    elif row.startswith('{"rid":'):
                        rod = Rod.parse(ssd, row)
                        ssd.rods[rod.rid] = rod
                    elif row.startswith('{"lid":'):
                        layer = Layer.parse(row)
                        ssd.layers[layer.lid] = layer
            
            if not ssd.layers:
                raise ValueError("No layers found in .db file.")
            
            ssd.lid_min = min(ssd.layers.keys())
            ssd.lid_max = max(ssd.layers.keys())
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not read {fn_db} properly ({e}). Recreating from .dat file.")
            # Se a leitura falhar, força a recriação a partir do .dat se ele existir
            return read_or_create_ssd(fn_db.replace('.db', '.dat'))
        toc = time.time() - tic
        print(f'   tElapsed {fn_db} in {toc:.2f} s')
        return ssd

    print('Creating ', fn_db)
    pid = 0
    with open(fn_dat, 'r') as fid:
        for row in fid:
            row = row.split()
            if len(row) < 5: continue
            
            x = int(row[2]); y = int(row[3]); z = int(row[4])
            if np.abs(x) > 8 or np.abs(y) > 100 or np.abs(z) > 8:
                continue
                
            rid = int(row[1]); lid = y
            xz = np.array([x, z])
            p = Particle(ssd, pid, rid, lid, xz)
            ssd.particles[pid] = p

            if rid not in ssd.rods:
                ssd.rods[rid] = Rod(ssd,rid)
            ssd.rods[rid].add_pid(pid)
            
            if lid not in ssd.layers:
                ssd.layers[lid] = Layer(lid)
            ssd.layers[lid].add_pid(pid)
            pid += 1

    if not ssd.layers:
        raise ValueError("Could not create any layers from .dat file. Check file format.")

    ssd.lid_max = max(ssd.layers.keys())                                         
    ssd.lid_min = min(ssd.layers.keys())
    
    create_neighs(ssd.layers, ssd.particles)

    with open(fn_db, 'w') as fid:
        for pid in ssd.particles:
            fid.write(ssd.particles[pid].to_str() + '\n')
        for rid in ssd.rods:
            fid.write(ssd.rods[rid].to_str() + '\n')
        for lid in ssd.layers:
            fid.write(ssd.layers[lid].to_str() + '\n')

    return ssd


def random_deleted_rids(ssd: StressStrainData, F):
    r = np.random.random(len(ssd.rods))
    del_rids = []
    # Usar uma lista de chaves para evitar problemas de modificação durante a iteração
    rod_keys = list(ssd.rods.keys())
    for i, rid in enumerate(rod_keys):
        if i < len(r):
            rod: Rod = ssd.rods[rid]
            if r[i] < rod.prob_break(F):
                del_rids.append(rid)
    return del_rids


class Logger:
    def __init__(self):
        self.F = []
        self.num_active_particles = []
        self.deleted_rod_clusters = []

    def log(self, F, num_active_particles, deleted_rod_clusters):
        self.F.append(F)
        self.num_active_particles.append(num_active_particles)
        self.deleted_rod_clusters.append(deleted_rod_clusters)

    def save(self, output_filepath, k):
        output_directory = os.path.dirname(output_filepath)
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
        
        mode = 'w' if k == 0 else 'a'
        with open(output_filepath, mode) as fid:
            if k > 0:
                 fid.write('----------------------------------------------%d\n' % k)

            if k == 0:
                fid.write('f,num_active_particles,num_deleted_particles,total_deleted_rods,avalanche_sizes\n')
            
            initial_particles = self.num_active_particles[0] if self.num_active_particles else 0
            for i in range(len(self.F)):
                a = initial_particles - self.num_active_particles[i]
                clusters = self.deleted_rod_clusters[i]
                total_deleted_this_step = sum(clusters)
                clusters_str = "-".join(map(str, clusters)) if clusters else "0"
                fid.write(f'{self.F[i]},{self.num_active_particles[i]},{a},{total_deleted_this_step},"{clusters_str}"\n')


def stress_strain(ssd: StressStrainData, verbose: bool = False) -> Logger:
    ssd.filter_rids(reverse=False)    
    ssd.filter_rids(reverse=True)    

    logger = Logger()    
    logger.log(0, ssd.num_active_particles(), []) 

    F = 0.5
    while True:
        if verbose:  
            print(f'Force: {F:.2f}, Rods: {len(ssd.rods)} =================================')

        ssd_snapshot = ssd.copy()
        prob_deleted_rids = random_deleted_rids(ssd, F)

        if not prob_deleted_rids:
            logger.log(F, ssd.num_active_particles(), [])
            F += 0.5
            continue

        ssd.drop_rids(set(prob_deleted_rids))
        active_rids_after_down_sweep, structural_deleted_rids1 = ssd.filter_rids(reverse=False)
        
        if not active_rids_after_down_sweep:
            if verbose: print("Ruptura detectada (varredura para baixo)!")
            total_avalanche_rids = set(prob_deleted_rids) | structural_deleted_rids1
            avalanche_clusters = find_deleted_rod_clusters(ssd_snapshot, total_avalanche_rids)
            logger.log(F, 0, avalanche_clusters)
            break

        active_rids_after_up_sweep, structural_deleted_rids2 = ssd.filter_rids(reverse=True)
        total_avalanche_rids = set(prob_deleted_rids) | structural_deleted_rids1 | structural_deleted_rids2
        avalanche_clusters = find_deleted_rod_clusters(ssd_snapshot, total_avalanche_rids)

        if not active_rids_after_up_sweep:
            if verbose: print("Ruptura detectada (varredura para cima)!")
            logger.log(F, 0, avalanche_clusters)
            break
        
        logger.log(F, ssd.num_active_particles(), avalanche_clusters)
            
    return logger


def main():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-file', type=str, help='File argument description', default='data.dat')
    parser.add_argument('-m', type=int, help='Exponent of the rods', default=2)
    parser.add_argument('-n', type=int, help='number of repetitions for statistic', default=1)
    args = parser.parse_args()

    fn = args.file
    m = args.m
    n = args.n

    tic = time.time()
    ssd = read_or_create_ssd(fn)
    toc = time.time()
    print(f"Reading/Creating data structure took: {toc-tic:.2f} s")

    ssd.set_rods_exponent(m)
    
    base_name = os.path.splitext(fn)[0]
    fn_log = f"{base_name}_m_{m}.txt"

    for k in range(0, n):
        ssd_copy = ssd.copy()
        print(f"\n--- Starting simulation run {k+1}/{n} ---")
        tic = time.time()
        logger = stress_strain(ssd_copy, verbose=False)
        toc = time.time()
        print(f"   Run {k+1} finished in: {toc-tic:.2f} s")
        
        logger.save(fn_log, k)
        print(f"   Results for run {k+1} saved to {fn_log}")


if __name__ == '__main__':
    main()