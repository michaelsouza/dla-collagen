import os 
import time
import numpy as np
import pandas as pd 
import random
#from line_profiler import LineProfiler


def filter_backbone(bb: dict, dict, m_neig_pid:dict, m_pids_layer: dict, active_rids:set, ascending: bool = True):
    if len(bb) == 0:
        return dict(), dict() # empty dictionary
    
    # min and max y coordinates
    layer_min = np.min([p['layer'] for p in bb.values()])
    layer_max = np.max([p['layer'] for p in bb.values()])
    
    # current layer
    layer = layer_min if ascending else layer_max

    # activate first layer    
    for pid_A in m_pids_layer[layer]:
        active_rids.add(bb[pid_A]['rid'])
    
    for layer in sorted(m_pids_layer.keys(), reverse=not ascending):
        # update the current layer
        layer += 1 if ascending else -1
        # if the current layer is out of the range of y coordinates, skip
        if layer < layer_min or layer > layer_max:
            continue
        # pids in the current layer
        pids_layer = m_pids_layer[layer]
        for pid_A in pids_layer:            
            for rid_B in m_neig_pid[pid_A]:
                if rid_B in active_rids:                
                    rid_A = bb[pid_A]['rid']
                    active_rids.add(rid_A)
                    break        
    
    return active_rids

def create_maps(bb: pd.DataFrame, F:float, sigma_cte: float, m: float):
    # create maps
    # m_rod_particles[rid] = list of particles in the rod
    m_pids_rod = {}
    # m_layer_particles[layer] = list of particles in the layer
    m_pids_layer = {}
    for pid, p in bb.items():
        rid = p['rid'] # rod id
        layer = p['layer'] # layer
        if rid not in m_pids_rod:
            m_pids_rod[rid] = []
        if layer not in m_pids_layer:
            m_pids_layer[layer] = [] # TODO: use set instead of list?
        m_pids_rod[rid].append(pid)
        m_pids_layer[layer].append(pid)

    # m_rods_particles[pid] = list of rods neighboring the particle
    m_neig_pid = {}
    # m_rod_values[rid] = (N, sigma_mean)
    prob_rod = {}
    rods_id = np.unique([p['rid'] for p in bb.values()])
    for rid in rods_id:
        pids_rod = m_pids_rod[rid] 
        N = 0 # number of neighbor particles of the rod
        n = [] # number of particles in each layer of the rod
        for pid_A in pids_rod:
            p_A = bb[pid_A]
            # get the coordinates x and z of the particle A
            xz_A = p_A['xz']
            # get the particles in the same layer of A (same coordinate y)
            pids_layer = m_pids_layer[p_A['layer']]
            n.append(len(pids_layer))
            for pid_B in pids_layer:
                # get the coordinates x and z of the particle B
                xz_B = bb[pid_B]['xz']
                # check if B is a neighbor of A
                if np.sum(np.abs(xz_A-xz_B)) == 1:                    
                    if pid_B not in m_neig_pid:
                        m_neig_pid[pid_B] = set()
                    m_neig_pid[pid_B].append(rid)
                    N += 1
        sigma_mean = F / np.mean(n)
        prob_rod[rid] = {'N': N, 'sigma_mean': sigma_mean, 'p': (sigma_mean / (N * sigma_cte))**m}
    return m_pids_rod, m_pids_layer, m_neig_pid, prob_rod


def update_force(bb, m_pids_layer, m_pids_rod, prob_rod, F_new, F_old, add_rod, sigma_cte, m):
    # update the values of the rods that were not removed
    for rid_A in add_rod:
        A_vals = prob_rod[rid_A]
        N, sigma_mean = A_vals['N'], A_vals['sigma_mean']        
        n = [] # number of particles in each layer of the rod
        for pid_A in m_pids_rod[rid_A]:
            n.append(len(m_pids_layer[bb[pid_A]['layer']]))
        sigma_mean *= (F_new / F_old)
        A_vals['sigma_mean'] = sigma_mean
        A_vals['p'] = (sigma_mean / (N * sigma_cte))**m


def update_maps(bb, active_rids, m_pids_layer, m_pids_rod, m_neig_pid, prob_rod):
    del_rids = set(m_pids_rod.keys()) - active_rids
    prob_rod = {rid: prob_rod[rid] for rid in active_rids}
    # some rods were removed
    for rid_A in del_rids:
        for pid_A in m_pids_rod[rid_A]:
            # reduce number of neighbors of the particles in the rod            
            for rid_B in m_neig_pid[pid_A]:
                if rid_B not in prob_rod:
                    continue
                prob_rod[rid_B]['N'] -= 1
            # remove pid_A from the m_pids_layer
            m_pids_layer[bb[pid_A]['layer']].remove(pid_A)
            


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
    active_rids = np.unique([p['rid'] for _, p in bb.items()])
    print('Number of rods:', len(active_rids))
    
    # create maps
    F_new = 1 # applied force
    sigma_cte = 1 # constant to calculate the stress
    m = 2 # exponent of the stress
    print('Creating maps')
    tic = time.time()
    m_pids_rod, m_pids_layer, m_neig_pid, prob_rod = create_maps(bb, F_new, sigma_cte, m)
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")

    ## backbone filtering
    tic = time.time()
    print('Filtering backbone')
    active_rids = set()
    filter_backbone(bb, m_neig_pid, m_pids_rod, m_pids_layer, active_rids, ascending=True)
    filter_backbone(bb, m_neig_pid, m_pids_rod, m_pids_layer, active_rids, ascending=False)
    toc = time.time()
    print(f"   Elapsed time: {toc-tic:.2f} s")

    update_maps(bb, active_rids, m_pids_layer, m_pids_rod, m_neig_pid, prob_rod)
    update_force(bb, m_pids_layer, m_pids_rod, prob_rod, F_new, F_new, sigma_cte, m)
    
    print('Force:', F_new, '=================================')
    while True:        
        print('Number of particles:', len(bb))

        print('Random remove')
        tic = time.time()
        # sort k random float numbers in the range [0,1]
        r = np.random.random(len(active_rids))
        rem_rods = []
        for i, rid in enumerate(active_rids):
            if r[i] < prob_rod[rid]['p']:
                rem_rods.append(rid)                
        # clean bb by keeping only the particles with pid on active_rids
        bb = {pid: p for pid, p in bb.items() if p['rid'] in active_rids}
        toc = time.time()
        print(f"   Elapsed time: {toc-tic:.2f} s")
      
        if len(rem_rods) == 0:
            F_old = F_new
            F_new += 0.5 # increment the force
            print('Force:', F, '=================================')
            update_force(bb, m_pids_layer, m_pids_rod, prob_rod, F, F-0.5, add_rods, sigma_cte, m)
            continue
        else:
            # clean bb by keeping only the particles with pid in add_rods
            print('Clean bb')
            tic = time.time()
            bb = {pid: p for pid, p in bb.items() if p['rid'] in add_rods}
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")

            # clean m_pids_layer
            print('Clean m_pids_layer')
            tic = time.time()
            m_pids_layer = {layer: [pid for pid in pids if pid in bb] for layer, pids in m_pids_layer.items()}
            toc = time.time()
            print(f"   Elapsed time: {toc-tic:.2f} s")
                        
            print('Filtering backbone')
            tic = time.time()
            bb, m_pids_rod = filter_backbone(bb, m_pids_rod, m_pids_layer, ascending=True)            
            bb, m_pids_rod = filter_backbone(bb, m_pids_rod, m_pids_layer, ascending=False)
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