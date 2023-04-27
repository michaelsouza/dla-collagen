import os 
import time
import numpy as np
import pandas as pd 
import random

# global variables
RODS = {}
LAYERS = {}
PARTICLES = {}
LID_MIN = None
LID_MAX = None

class Particle:
    def __init__(self, pid:int, rid:int, lid:int, xz):
        self.pid = pid
        self.rid = rid
        self.lid = lid
        self.xz = xz
        self.active = True
        self.neigh_rids = set()

    def add_neigh_rid(self, rid:int):
        self.neigh_rids.add(rid)
        rod : Rod = RODS[rid]
        rod.add_neigh_pid(self.pid)

    def del_neigh(self, rid:int):
        self.neigh_rids.remove(rid)

    def get_neighs(self):
        return self.neigh_rids

    def innactive(self):
        self.active = False
        for rid in self.neigh_rids:
            rod: Rod = RODS[rid]
            rod.del_neigh_pid(self.pid)
            layer: Layer = LAYERS[self.lid]
            layer.del_pid(self.pid)

class Rod:
    def __init__(self, rid:int):
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
            particle:Particle = PARTICLES[pid]
            particle.innactive()

    def update_force(self, F:float):
        self.N = len(self.neigh_pids)
        if self.N == 0:
            self.p = 1 # if rod not have neighs, the prob
            return self.p
            #raise Exception(f'N == 0 (rid={self.rid})')
        self.sigma_mean *= (F / self.F)
        self.p = (self.sigma_mean / (self.N * self.sigma_cte))**self.m
        self.F = F # update the force
        return self.p

    def update_sigma(self, F:float):
        n = np.zeros(len(self.pids)) # number of neigh_pids per layer
        for i, pid_A in enumerate(self.pids):
            particle: Particle = PARTICLES[pid_A]
            n[i] = LAYERS[particle.lid].len()
        self.sigma_mean = np.mean(self.F / n)
        self.updated = True
        return self.update_force(F)
            
    def prob_break(self, F:float):
        if self.updated:
            return self.update_force(F)
        else:
            return self.update_sigma(F)
                    

class Layer:
    def __init__(self, lid:int):
        self.lid = lid
        self.pids = set()

    def len(self):
        return len(self.pids)

    def add_pid(self, pid:int):
        self.pids.add(pid)

    def del_pid(self, pid:int):
        self.pids.remove(pid)
                   
def create_connections():
    # create connections
    print('Creating connections')
    for pid_A in PARTICLES:
        particle_A: Particle = PARTICLES[pid_A]
        for pid_B in LAYERS[particle_A.lid].pids:
            if pid_A == pid_B:
                continue
            particle_B: Particle = PARTICLES[pid_B]
            # check if the particles are neighbors
            if np.linalg.norm(particle_A.xz - particle_B.xz) <= 1:
                particle_A.add_neigh_rid(particle_B.rid)
                particle_B.add_neigh_rid(particle_A.rid)


def read_particles(fn: str):
    global LID_MAX
    global LID_MIN

    # Read particles file
    print('Reading', fn)
    bb = {}  # backbone
    pid = 0
    with open(fn, 'r') as fid:
        # each line is a particle and a rod is a set of particles
        for row in fid:
            row = row.split()
            # extract the fiber center (rectangular trapezoid)
            v = np.zeros(5)
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
            lid = y
            xz = np.array([x, z])
            p = Particle(pid, rid, lid, xz)
            # add particle to the backbone
            PARTICLES[pid] = p
            # add particle to the rod
            if rid not in RODS:
                RODS[rid] = Rod(rid)
            RODS[rid].add_pid(pid)
            # add particle to the layer
            if lid not in LAYERS:
                LAYERS[lid] = Layer(lid)
            LAYERS[lid].add_pid(pid)
            pid += 1
    LID_MAX = np.max(LAYERS.keys())
    LID_MIN = np.min(LAYERS.keys())


def filter_rids(active_rids:set, ascending: bool = True):
    if len(PARTICLES) == 0:
        return dict(), dict() # empty dictionary
    
    for i, lid in enumerate(sorted(LAYERS, reverse=not ascending)):
        if i == 0:
            # all rods in the first layer are active
            for pid_A in LAYERS[lid].pids:
                particle_A: Particle = PARTICLES[pid_A]
                active_rids.add(particle_A.rid)
            continue
        
        # pids in the current layer
        lid_pids = LAYERS[lid].pids
        for pid_A in lid_pids:
            particle_A: Particle = PARTICLES[pid_A]            
            for rid_B in particle_A.get_neighs():
                if rid_B in active_rids:
                    active_rids.add(particle_A.rid)
                    break


def stress_strain(fn: str, m: int = 2):
    global RODS

    # read backbone
    tic = time.time()
    read_particles(fn)    
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")
    
    # create connections
    tic = time.time()
    create_connections()
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")
    
    # filter rods
    print('Filtering rods')
    tic = time.time()
    active_rids = set() # active rods
    filter_rids(active_rids, ascending=True)
    filter_rids(active_rids, ascending=False)
    toc = time.time()
    #print(f"   Elapsed time: {toc-tic:.2f} s")

    # inactivate rods
    print('Inactivating rods')
    tic = time.time()
    for rid in RODS:
        if rid not in active_rids:
            RODS[rid].inactivate()
    RODS = {rid: RODS[rid] for rid in active_rids} # update rods
    toc = time.time()
    #print(f"   Elapsed time: {toc-tic:.2f} s")

    # create maps
    F = 1 # applied force
    print('Force:', F, '=================================')
    list_removed_rids = []
    while True:        
        print('Number of rods:', len(RODS))
        print('Force:', F, '=================================')
        print('Applying force')
        tic = time.time()
        # sort k random float numbers in the range [0,1]
        r = np.random.random(len(RODS))
        del_rids = [] # rods to be deleted
        for i, rid in enumerate(RODS):
            rod: Rod = RODS[rid]
            #TODO Question: can we delete the rods from the first or last layers?
            if r[i] < rod.prob_break(F):
                del_rids.append(rid)
        toc = time.time()
        print(f"   Elapsed time: {toc-tic:.2f} s")

        print('Remove broken rods')
        tic = time.time()
        #print(del_rids)
        for rid in del_rids:
            print("rid to be removed: %d" %rid)
            RODS[rid].inactivate()
        
        RODS = {rid: RODS[rid] for rid, rod in RODS.items() if rod.active} # update rods
        toc = time.time()
        #print(f"   Elapsed time: {toc-tic:.2f} s")
        list_removed_rids+=del_rids
        if len(del_rids) == 0:
            F += 0.5 # increment the force
            print('Force:', F, '=================================')
        else:
            print('Filtering rods')
            tic = time.time()
            active_rids = set() # active rods
            filter_rids(active_rids, ascending=True)
            filter_rids(active_rids, ascending=False)
            toc = time.time()
            #print(f"   Elapsed time: {toc-tic:.2f} s")

             # if the backbone is empty, stop
            if len(active_rids) == 0:                
                break

            # inactivate rods
            #print('Inactivating rods')
            tic = time.time()
            #print(active_rids)

            for rid in RODS:
                if rid not in active_rids:
                    #TODO: Por alguma razão, acontece de um rod, chamar sua lista de vizinhos
                    #      e esa lista conter alguem que ja foi removido, da erro e o codigo quebra.
                    #      Algo semelhante acontece na hora de pegar vizinho na camada em alguns casos
                    print('rid to be removed: ', rid)
                    RODS[rid].inactivate() 
            RODS = {rid: RODS[rid] for rid, rod in RODS.items() if rod.active}


            #RODS = {rid: RODS[rid] for rid in active_rids} # update rods
            toc = time.time()
            #print(f"   Elapsed time: {toc-tic:.2f} s")

            # check if there is any empty layer
            #print('Check if fibril was broken')
            tic = time.time()
            for layer in LAYERS:
                if len(LAYERS[layer].pids) == 0:
                    tic = time.time()
                    print("fibril broken!!!")
                    #print(f"   Elapsed time: {toc-tic:.2f} s")
                    break
            

def main(fn:str, m:int = 2):    
    ts = int(fn.split('ts_')[1].split('_')[0])
    # lp = LineProfiler()
    # lp_wrapper = lp(stress_strain)
    # force, Broken, part_in_skeleton, Removed = lp_wrapper(fn, m)
    # lp.print_stats()

    #random.seed(1234)
    stress_strain(fn, m)

    # Save number of broken bonds
    # with open('broken_bonds_%d_m%d.txt' %(ts, m), 'w') as fid:
    #         fid.write(f"force\tbroken\n")
    #         for x,y in zip(force,Broken):
    #             fid.write(f"{x}\t{y}\n")

    # # Save porcent. of particles in skeleton 
    # with open('porcet_parts_%d_m%d.txt' %(ts, m), 'w') as fid:
    #     # Write each pair of values to a new    line in the file
    #     for x, y in zip(force, part_in_skeleton):
    #         fid.write(f"{x}\t{y}\n")

    # # Save removed rods
    # with open('removed_parts_%d_m%d.txt' %(ts, m), 'w') as fid:
    #     # Write each pair of values to a new    line in the file
    #     for x, y in zip(force, Removed):
    #         fid.write(f"{x}\t{y}\n")

if __name__ == '__main__':
    # set seed
    

    files = [
        '/home/robert/Dropbox/data/files/particles/mode_s_ts_1_nb_20000_seed_101_.dat',

        # 'mode_s_ts_10_nb_20000_seed_102_.dat',
        # 'mode_s_ts_100_nb_20000_seed_103_.dat',
        # 'mode_s_ts_1000_nb_20000_seed_104_.dat',
        #'stress_strain/mode_s_ts_10000_nb_20000_seed_105_.dat',
    ]

    # power exponent
    m = 2    
    for fn in files:
        main(fn, m)        