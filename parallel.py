import os
import sys
import multiprocessing as mp
import tqdm

ARGV = []
##read cmds from .txt
with open('cmd_dla.txt', 'r') as fid:
    for row in fid.readlines():
        ARGV.append(row)

pool = mp.Pool(mp.cpu_count()-1)

print('cpu n°:%d' %mp.cpu_count())
for _ in tqdm.tqdm(pool.imap_unordered(os.system, ARGV), total=len(ARGV)):
    pass
pool.close()

