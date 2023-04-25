import os 
import time
import numpy as np
import pandas as pd 
import random
#from line_profiler import LineProfiler


def filter_backbone(bb: dict, map_pids_rod: dict, map_pids_layer: dict, ascending: bool = True):
    if len(bb) == 0:
        return dict(), dict() # empty dictionary
    
    # min and max y coordinates
    layer_min = np.min([p['layer'] for p in bb.values()])
    layer_max = np.max([p['layer'] for p in bb.values()])
    
    # current layer
    layer = layer_min if ascending else layer_max

    # find all particles in the current layer
    pids_prev = map_pids_layer[layer]
    
    # set of active particles
    pids_active = list(pids_prev)
    for layer in sorted(map_pids_layer.keys(), reverse=not ascending):
        # update the current layer
        layer += 1 if ascending else -1
        # if the current layer is out of the range of y coordinates, skip
        if layer < layer_min or layer > layer_max:
            continue
        # find all particles in the current layer
        pids_layer = map_pids_layer[layer]
        # for all particle in the current layer, check if they are neighbors of the previous layer
        pids_add = [] # list of indices of particles to be added, because they are neighbors of the previous layer
        for pid_A in pids_layer:
            xz_A = bb[pid_A]['xz']
            for pid_B in pids_prev:
                xz_B = bb[pid_B]['xz']
                # if the particle is above (or below) another particle in the previous layer
                if np.sum(np.abs(xz_A-xz_B)) == 0:
                    pids_add.append(pid_A)
                    break

        # if no particle is found in the current layer, raise an exception
        if len(pids_add) == 0:
            return dict(), dict() # empty dictionary
        
        # IdxL is the list of particle indices in the level but not in ids_part_add
        pids_layer = list(set(pids_layer) - set(pids_add))
        for pid_A in pids_layer:
            xz_A = bb[pid_A]['xz']
            # searching for neighbors of each particle in the current layer
            for pid_B in pids_add:
                xz_B = bb[pid_B]['xz']
                if np.sum(np.abs(xz_A-xz_B)) == 1:
                    # there is a neighbor in the current layer
                    pids_add.append(pid_A)
                    break

        # add the particles in ids_part_add to the active particles
        pids_active += pids_add

        # update the list of particles in the current layer
        map_pids_layer[layer] = pids_add
        
        # update the list of particles in the previous layer
        pids_prev = pids_add
    
    # drop keys from the dictionary that are not in the list of active particles    
    bb = {pid: p for pid, p in bb.items() if pid in pids_active}

    rids = set([p['rid'] for p in bb.values()])
    
    map_pids_rod = {rid:pids for rid, pids in map_pids_rod.items() if rid in rids}

    return bb, map_pids_rod

def create_maps(bb: pd.DataFrame):
    # create maps
    # map_rod_particles[id_rod] = list of particles in the rod
    map_pids_rod = {}
    # map_layer_particles[layer] = list of particles in the layer
    map_pids_layer = {}
    for pid, p in bb.items():
        rid = p['rid'] # rod id
        layer = p['layer'] # layer
        if rid not in map_pids_rod:
            map_pids_rod[rid] = []
        if layer not in map_pids_layer:
            map_pids_layer[layer] = []
        map_pids_rod[rid].append(pid)
        map_pids_layer[layer].append(pid)
    return map_pids_rod, map_pids_layer


def random_remove(bb: dict, map_pids_rod: dict, map_pids_layer: dict, F: float = 1, sigma_cte: float = 1, m: int = 2):
    rods_id = np.unique([p['rid'] for p in bb.values()])
    # add_rods = rods to be added to the backbone
    # rem_rods = rods to be removed from the backbone
    add_rods = set()
    rem_rods = set()
    for rid in rods_id:
        pids_rod = map_pids_rod[rid]
        n = [] # n[i] is the number of particles in the layer i
        N = 0 # number of neighbor particles of the rod
        for pid_A in pids_rod:
            if pid_A not in bb:
                continue
            p_A = bb[pid_A]
            # get the coordinates x and z of the particle A
            xz_A = p_A['xz']
            # get the particles in the same layer of A (same coordinate y)
            pids_layer = map_pids_layer[p_A['layer']]
            n.append(len(pids_layer))
            for pid_B in pids_layer:
                # if the particle is the same as A or it is not in the backbone, skip
                if pid_B == pid_A or pid_B not in bb:
                    continue
                # get the coordinates x and z of the particle B
                xz_B = bb[pid_B]['xz']
                # check if B is a neighbor of A
                if np.sum(np.abs(xz_A-xz_B)) == 1:                    
                    N += 1
                    continue
        
        # calculate the probability of adding or removing the rod
        n = np.array(n)
        sigma = F/n 
        sigma_mean = np.mean(sigma)
        P = (sigma_mean/(N*sigma_cte))**m # probability of adding the rod
        r = np.random.random() # random number between 0 and 1
        if (r > P):
            add_rods.add(rid)
        else:
            rem_rods.add(rid)
    
    return add_rods, rem_rods


def read_backbone(fn: str):
    # Read backbone file
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
                        p = {'pid': pid, 'rid': int(row[1]), 'layer': int(row[3]),  'xz': np.array([int(row[2]), int(row[4])])}
                        bb[pid] = p
                        pid += 1
    return bb


def stress_strain(fn: str, m: int = 2):
    # read backbone
    tic = time.time()
    bb = read_backbone(fn) # bb1[rod_id, x, y, z]    
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")
    print('Number of particles:', len(bb))
    
    # create maps
    print('Creating maps')
    tic = time.time()
    map_pids_rod, map_pids_layer = create_maps(bb)
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")

    ## backbone filtering
    tic = time.time()
    print('Filtering backbone')
    bb, map_pids_rod = filter_backbone(bb, map_pids_rod, map_pids_layer, ascending=True)
    bb, map_pids_rod = filter_backbone(bb, map_pids_rod, map_pids_layer, ascending=False)
    toc = time.time()    
    print(f"   Elapsed time: {toc-tic:.2f} s")

    F = 0 # applied force
    forces = [F] # list of applied forces
    num_part_bb_active = [len(bb)] # list of number of particles in the backbone after each force    
    rem_rods_all = [[]] # list of rods removed from the backbone after each force

    #bb_len = len(bb)
    while True:        
        print('Number of particles:', len(bb))
        print('Random remove')
        tic = time.time()
        add_rods, rem_rods = random_remove(bb, map_pids_rod, map_pids_layer, F, 1, m)
        toc = time.time()
        print(f"   Elapsed time: {toc-tic:.2f} s")
      
        if len(rem_rods) == 0:
            F += 0.5 # increment the force
            print('Force:', F, '=================================')
        else:
            # clean bb by keeping only the particles with pid in add_rods
            print('Clean bb')
            tic = time.time()
            bb = {pid: p for pid, p in bb.items() if p['rid'] in add_rods}
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")

            # clean map_pids_layer
            print('Clean map_pids_layer')
            tic = time.time()
            map_pids_layer = {layer: [pid for pid in pids if pid in bb] for layer, pids in map_pids_layer.items()}
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")
                        
            print('Filtering backbone')
            tic = time.time()
            bb, map_pids_rod = filter_backbone(bb, map_pids_rod, map_pids_layer, ascending=True)            
            bb, map_pids_rod = filter_backbone(bb, map_pids_rod, map_pids_layer, ascending=False)
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")
            
            if not bool(bb): # if the backbone is empty, stop                
                break
            
        #brokenBonds =  numParticles - restParticles
        #num_part_removed.append(brokenBonds)
        #rem_rods.append(list_removed)

        

    print(F)
    #print(part_in_skeleton)

    #print(len(force))
    #print(len(part_in_skeleton))

    
    ##Save number of broken bonds
    num_part_bb_active = np.array(num_part_bb_active)/num_part_bb_active[0] * 100
    num_part_bb_active = num_part_bb_active.tolist()
    #return forces, num_part_removed, num_part_bb_active, rem_rods
 
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