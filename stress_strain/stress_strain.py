import os 
import time
import numpy as np
import pandas as pd 
import random

RODS = {}
LAYERS = {}
PARTICLES = {}

class Particle:
    def __init__(self, pid, rid, layer, xz):
        self.pid = pid
        self.rid = rid
        self.layer = layer
        self.xz = xz
        self.active = True
        self.neighs = set()

    def add_neigh(self, rid):
        self.neighs.add(rid)
        rod : Rod = RODS[rid]
        rod.add_neigh(self.pid)

    def del_neigh(self, rid):
        self.neighs.remove(rid)

    def get_neighs(self):
        return self.neighs

    def innactive(self):
        self.active = False
        for rid in self.neighs:
            rod: Rod = RODS[rid]
            rod.del_neigh(self.rid)
            layer: Layer = LAYERS[self.layer]
            layer.del_pid(self.r)

class Rod:
    def __init__(self, rid):
        self.rid = rid
        self.active = True
        self.pids = set()
        self.N = 0
        self.p = 0
        self.F = 0
        self.m = 2
        self.sigma_cte = 1
        self.sigma_mean = 0
        self.updated = False
        self.neigh_pids = set()

    def add_pid(self, pid):
        self.pids.add(pid)
        self.updated = False

    def del_neigh(self, pid):
        self.neigh_pids.remove(pid)
        self.updated = False

    def add_neigh(self, pid):
        self.neigh_pids.add(pid)
        self.updated = False

    def inactivate(self, bb):
        self.active = False
        for pid in self.pids:
            particle:Particle = PARTICLES[pid]
            particle.innactive()

    def update_force(self, F):
        self.N = len(self.neigh_pids)
        self.sigma_mean *= (F / self.F)
        self.p = (self.sigma_mean / self.N * self.sigma_cte)**self.m
        self.F = F
        return self.p

    def update_sigma(self, F):
        n = []
        for pid_A in self.pids:
            particle: Particle = PARTICLES[pid]
            n.append(particle.layer.size())
        self.sigma_mean = np.mean(self.F / np.array(n))
        self.updated = True
        return self.update_force(F)
            
    def del_prob(self, F):
        if self.updated:
            return self.update_force(F)
        else:
            return self.update_sigma(F)
                    
    
class Layer:
    def __init__(self, layer:int):
        self.layer = layer
        self.pids = set()

    def size(self):
        return len(self.pids)

    def add_pid(self, pid):
        self.pids.add(pid)

    def del_pid(self, pid):
        self.pids.remove(pid)

def create_connections():
    # create connections
    print('Creating connections')
    for pid_A in PARTICLES:
        particle_A: Particle = PARTICLES[pid_A]
        for pid_B in LAYERS[particle_A.layer].pids:
            if pid_A == pid_B:
                continue
            particle_B: Particle = PARTICLES[pid_B]
            # check if the particles are neighbors
            if np.linalg.norm(particle_A.xz - particle_B.xz) <= 1:
                particle_A.add_neigh(particle_B.rid)
                particle_B.add_neigh(particle_A.rid)


def read_particles(fn: str):
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
            if -8 <= int(row[2]) <= 8:
                if -8 <= int(row[4]) <= 8:
                    if -100 <= int(row[3]) <= 100:
                        # add particle to the backbone
                        rid = int(row[1])
                        layer = int(row[3])
                        xz = np.array([int(row[2]), int(row[4])])
                        p = Particle(pid, rid, layer, xz)
                        # add particle to the backbone
                        PARTICLES[pid] = p
                        # add particle to the rod
                        if rid not in RODS:
                            RODS[rid] = Rod(rid)
                        RODS[rid].add_particle(pid)
                        # add particle to the layer
                        if layer not in LAYERS:
                            LAYERS[layer] = Layer(layer, set())
                        LAYERS[layer].add_particle(pid)
                        pid += 1


def filter_rids(active_rids:set, ascending: bool = True):
    if len(PARTICLES) == 0:
        return dict(), dict() # empty dictionary
    
    # min and max y coordinates
    layer_min = np.min(LAYERS)
    layer_max = np.max(LAYERS)
    
    # current layer
    layer = layer_min if ascending else layer_max

    # active first layer 
    for pid_A in LAYERS[layer].pids:
        particle_A: Particle = PARTICLES[pid_A]
        active_rids.add(particle_A.rid)
    
    for layer in sorted(LAYERS, reverse=not ascending):
        # update the current layer
        layer += 1 if ascending else -1
        # if the current layer is out of the range of y coordinates, skip
        if layer < layer_min or layer > layer_max:
            continue
        # pids in the current layer
        layer_pids = LAYERS[layer].pids
        for pid_A in layer_pids:
            particle_A: Particle = PARTICLES[pid_A]            
            for rid_B in particle_A.get_neighs():
                if rid_B in active_rids:
                    active_rids.add(particle_A.rid)
                    break


def stress_strain(fn: str, m: int = 2):
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
    print(f"   Elapsed time: {toc-tic:.2f} s")

    # inactivate rods
    print('Inactivating rods')
    tic = time.time()
    for rid in RODS:
        if rid not in active_rids:
            RODS[rid].inactivate() 
    RODS = {rid: RODS[rid] for rid in active_rids} # update rods
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")

    # create maps
    F = 1 # applied force
    print('Force:', F_new, '=================================')
    while True:        
        print('Number of rods:', len(RODS))
        print('Random remove')
        tic = time.time()
        # sort k random float numbers in the range [0,1]
        r = np.random.random(len(active_rids))
        del_rods = False # rods to be deleted
        for i, rid in enumerate(RODS):
            rod: Rod = RODS[rid]
            if r[i] < rod.del_prob(F):
                del_rods = True
                rod.inactivate()
        # clean bb by keeping only the particles with pid on active_rids
        RODS = {rid: RODS[rid] for rid, rod in RODS.elements() if rod.active} # update rods
        toc = time.time()
        print(f"   Elapsed time: {toc-tic:.2f} s")
      
        if del_rods == 0:
            F += 0.5 # increment the force
            print('Force:', F, '=================================')
        else:
            print('Filtering rods')
            tic = time.time()
            active_rids = set() # active rods
            filter_rids(active_rids, ascending=True)
            filter_rids(active_rids, ascending=False)
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")

             # if the backbone is empty, stop
            if len(active_rods) == 0:                
                break

            # inactivate rods
            print('Inactivating rods')
            tic = time.time()
            for rid in RODS:
                if rid not in active_rids:
                    RODS[rid].inactivate() 
            RODS = {rid: RODS[rid] for rid in active_rids} # update rods
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")

            # check if there is any empty layer
            for layer in LAYERS:
                if len(LAYERS[layer].pids) == 0:
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
        'stress_strain/mode_s_ts_1_nb_20000_seed_101_.dat',
        # 'mode_s_ts_10_nb_20000_seed_102_.dat',
        # 'mode_s_ts_100_nb_20000_seed_103_.dat',
        # 'mode_s_ts_1000_nb_20000_seed_104_.dat',
        'stress_strain/mode_s_ts_10000_nb_20000_seed_105_.dat',
    ]

    # power exponent
    m = 2    
    for fn in files:
        main(fn, m)        