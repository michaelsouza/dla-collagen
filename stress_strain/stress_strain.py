import os 
import time
import numpy as np
import pandas as pd 
import random
import json
import sys

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

    def del_neigh_rid(self, rid:int):
        self.neigh_rids.remove(rid)

    def get_neigh_rids(self):
        return self.neigh_rids

    def innactive(self):
        self.active = False
        # remove the particle from the layer
        layer: Layer = LAYERS[self.lid]
        layer.del_pid(self.pid)
        for rid in self.neigh_rids:
            # remove the particle from the neigh rods
            rod: Rod = RODS[rid]
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
    def parse(row:str):
        row = json.loads(row)
        pid = row['pid']
        rid = row['rid']
        lid = row['lid']
        xz = np.array(row['xz'], dtype=float)
        particle = Particle(pid, rid, lid, xz)
        particle.neigh_rids = set(row['neigh_rids'])
        particle.active = True
        return particle

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

        for pid in self.neigh_pids:
            particle:Particle = PARTICLES[pid]
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
    def parse(row:str):
        row = json.loads(row)
        rid = row['rid']
        rod = Rod(rid)
        rod.pids = set(row['pids'])
        rod.neigh_pids = set(row['neigh_pids'])
        rod.active = True
        rod.updated = False
        return rod
                    

class Layer:
    def __init__(self, lid:int):
        self.lid = lid
        self.pids = set()

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


def create_neighs():    
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

    if os.path.exists(fn.replace('.dat', '.db')):
        print('Reading database %s' % fn)
        with open(fn.replace('.dat', '.db'), 'r') as fid:
            for row in fid:
                if row.startswith('{"pid":'):                    
                    particle = Particle.parse(row)
                    PARTICLES[particle.pid] = particle
                if row.startswith('{"rid":'):
                    rod = Rod.parse(row)
                    RODS[rod.rid] = rod
                if row.startswith('{"lid":'):
                    layer = Layer.parse(row)
                    LAYERS[layer.lid] = layer
        LID_MIN = min(LAYERS.keys())
        LID_MAX = max(LAYERS.keys())
        return

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
    LID = list(LAYERS.keys())
    LID_MAX = int(max(LID)) 
    LID_MIN = int(min(LID))
    

    create_neighs()

    # save the database
    with open(fn.replace('.dat','.db'), 'w') as fid:
        for pid in PARTICLES:
            fid.write(PARTICLES[pid].to_str() + '\n')
        for rid in RODS:
            fid.write(RODS[rid].to_str() + '\n')
        for lid in LAYERS:
            fid.write(LAYERS[lid].to_str() + '\n')


def filter_rids(active_rids:set, reverse: bool = True):
    for i, lid in enumerate(sorted(range(LID_MIN, LID_MAX + 1), reverse=reverse)):
        if i == 0:
            # all rods in the first layer are active
            for pid_A in LAYERS[lid].pids:
                particle_A: Particle = PARTICLES[pid_A]
                active_rids.add(particle_A.rid)
            continue
        
        # pids in the current layer
        lid_pids = LAYERS[lid].pids
        
        # layer is empty
        if len(lid_pids) == 0:
            active_rids.clear()
            return 

        for pid_A in lid_pids:
            particle_A: Particle = PARTICLES[pid_A]            
            for rid_B in particle_A.get_neigh_rids():
                if rid_B in active_rids:
                    active_rids.add(particle_A.rid)
                    break

def clear_rods(active_rids: set,  list = False):
    global RODS
    # inactivate rods
    removed_rods = []
    for rid in RODS:
        if rid not in active_rids:
            RODS[rid].inactivate()
            removed_rods.append(rid)
    RODS = {rid: RODS[rid] for rid in active_rids} # update rods
    if list:
        return removed_rods

def count():
    global PARTICLES
    cont = 0

    for particle in PARTICLES.values():
        if particle.active:
            cont +=1
     

    return cont

def stress_strain(fn: str, m: int = 2, verbose: bool = False):
    global RODS
    map_force_partsInSkeleton = {} # Num of parts in skeleton
    map_force_rodsRemoved = {} # Num of rids removed from skeleton by a force
    

    # read backbone
    tic = time.time()
    read_particles(fn)    
    toc = time.time()
    if verbose:
        print(f"   Elapsed time: {toc-tic:.2f} s")

    print("Backbone size init: %d" %len(RODS))
    
    # filter rods
    print('Filtering rods')

    active_rids = set() # active rods
    filter_rids(active_rids, reverse=False)
    clear_rods(active_rids)
    active_rids = set()
    filter_rids(active_rids, reverse=True)
    clear_rods(active_rids)
    #print(f"   Elapsed time: {toc-tic:.2f} s")

    print("Backbone filtred: %d" %len(RODS))

    # create maps
    init = count()
    map_force_partsInSkeleton[0] = [init]
    map_force_rodsRemoved[0] = []
 
    F = 0.5 # applied force
    print('Force:', F, '=================================')
    

    while True:
        removed = []
        list_removed_rids = []
        if verbose:  
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
        if verbose:
            print(f"   Elapsed time: {toc-tic:.2f} s")

        if verbose:
            print('Remove broken rods')
        tic = time.time()

        for rid in del_rids:
            if verbose:
                print("rid to be removed: %d" %rid)

            RODS[rid].inactivate()
        RODS = {rid: RODS[rid] for rid, rod in RODS.items() if rod.active} # update rods
        toc = time.time()
        #print(f"   Elapsed time: {toc-tic:.2f} s")
        list_removed_rids+=del_rids
    
        tic = time.time()

        if len(del_rids) == 0:
            F += 0.5 # increment the force
            print('Force:', F, '=================================')
            
            #print("sairam %d particulas" %R)

            cont = count()


            if F in map_force_rodsRemoved:
                # if key is in dictionary, append a value to its list
                map_force_rodsRemoved[F].append(list_removed_rids)
            else:
                # if key is not in dictionary, add the key and a value for it
                map_force_rodsRemoved[F] = list_removed_rids

            if F in map_force_partsInSkeleton:
                # if key is in dictionary, append a value to its list
                map_force_partsInSkeleton[F].append(cont)
            else:
                # if key is not in dictionary, add the key and a value for it
                map_force_partsInSkeleton[F] = [cont]

        else:

            if verbose:
                print('Filtering rods')
            active_rids = set() # active rods
            filter_rids(active_rids, reverse=False)
            removed = clear_rods(active_rids, list = True)
            list_removed_rids+=removed
            
            # if the backbone is empty, stop
            if len(active_rids) == 0:    

                
                if F in map_force_rodsRemoved:
                    # if key is in dictionary, append a value to its list
                    map_force_rodsRemoved[F].append(list_removed_rids)
                else:
                    # if key is not in dictionary, add the key and a value for it
                    map_force_rodsRemoved[F] = list_removed_rids

                if F in map_force_partsInSkeleton:
                    # if key is in dictionary, append a value to its list
                    map_force_partsInSkeleton[F].append(0)
                else:
                    # if key is not in dictionary, add the key and a value for it
                    map_force_partsInSkeleton[F] = [0]

                RODS.clear()
                PARTICLES.clear()
                LAYERS.clear()

                print('active_rids null!!')            
                break

            active_rids = set()
            filter_rids(active_rids, reverse=True)
            removed = clear_rods(active_rids, list = True)
            list_removed_rids+=removed

            # if the backbone is empty, stop
            if len(active_rids) == 0:    


                if F in map_force_rodsRemoved:
                    # if key is in dictionary, append a value to its list
                    map_force_rodsRemoved[F].append(list_removed_rids)
                else:
                    # if key is not in dictionary, add the key and a value for it
                    map_force_rodsRemoved[F] = list_removed_rids

                if F in map_force_partsInSkeleton:
                    # if key is in dictionary, append a value to its list
                    map_force_partsInSkeleton[F].append(0)
                else:
                    # if key is not in dictionary, add the key and a value for it
                    map_force_partsInSkeleton[F] = [0]

                RODS.clear()
                PARTICLES.clear()
                LAYERS.clear()

                print('active_rids null!!')            
                break
                   
            
            cont = count()


            if F in map_force_rodsRemoved:
                # if key is in dictionary, append a value to its list
                map_force_rodsRemoved[F].append(list_removed_rids)
            else:
                # if key is not in dictionary, add the key and a value for it
                map_force_rodsRemoved[F] = [list_removed_rids]

            if F in map_force_partsInSkeleton:
                # if key is in dictionary, append a value to its list
                map_force_partsInSkeleton[F].append(cont)
            else:
                # if key is not in dictionary, add the key and a value for it
                map_force_partsInSkeleton[F] = [cont]

    return map_force_partsInSkeleton, map_force_rodsRemoved

def listar_arquivos_em_pasta(caminho_da_pasta):
    files = []  # Lista para armazenar os caminhos completos dos arquivos

    # Verifica se o caminho especificado é uma pasta válida
    if os.path.isdir(caminho_da_pasta):
        # Percorre todos os arquivos e pastas dentro do caminho especificado
        for root, _, filenames in os.walk(caminho_da_pasta):
            for filename in filenames:
                caminho_completo = os.path.join(root, filename)
                files.append(caminho_completo)

    return files



def main(fn:str, m:int = 2):    
    ts = int(fn.split('ts_')[1].split('_')[0])

    # receive a seed from command line
    # Loop through the command line arguments
    for i in range(len(sys.argv)):
        # Check if the argument starts with "-seed"
        if sys.argv[i].startswith("-seed"):
            # Try to convert the next argument to an integer
            try:
                seed = int(sys.argv[i+1]) + p
                print(f"Seed value is {seed}")
            except (IndexError, ValueError):
                print("Invalid seed value")
                sys.exit(1)
            break
    else:
        # No "-seed" argument found
        print("No seed value provided")
        sys.exit(1)

    #random.seed(seed)
    np.random.seed(seed)

    tic = time.time()
    map_force_partsInSkeleton, map_force_rodsRemoved = stress_strain(fn, m, verbose=False)
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")
    #print(map_force_partsInSkeleton)
    ##Save porcent. of particles in skeleton 
    with open('/home/robert/data_fibril/stress/parts_removed%d_m%d_seed%d.txt' %(ts, m, seed), 'w') as fid:

        fid.write(f"force\tnumParts\tpartsRemoved\trodsRemoved\n")
        f = 0
        for j in map_force_partsInSkeleton.keys():
            k = (map_force_partsInSkeleton[j][-1]/map_force_partsInSkeleton[0][-1])*100
            l = map_force_rodsRemoved[j]
            f = map_force_partsInSkeleton[0][-1] - map_force_partsInSkeleton[j][-1]
            fid.write(f"{j}\t{k}\t{f}\t{l}\n")
    
    
if __name__ == '__main__':
    # set seed
    

    # Especifica o caminho da pasta que deseja listar os arquivos
    caminho_da_pasta = "/home/robert/Dropbox/data/files/particles"

    # Chama a função para listar os arquivos na pasta especificada
    files = listar_arquivos_em_pasta(caminho_da_pasta)

    # Imprime a lista de arquivos encontrados
    print(files)

    # power exponent
    m =2
    p = 0
    for fn in files:
        
        main(fn, m) 
        p+=1     
