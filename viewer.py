# https://educapes.capes.gov.br/bitstream/capes/565584/3/Minicurso%20-%20Simulacoes%20com%20VPython%20-%20tutorial.pdf

import time
import numpy as np
from vpython import *

def read_dat(fdat):
    df = {}
    with open(fdat, 'r') as fid:
        for row in fid.readlines():
            row = row.split()
            if row[0] == 'add':
                uid = int(row[1])
                x = int(row[2])
                y = int(row[3])
                z = int(row[4])
                df[uid] = {'p':[(x,y,z)], 'bind':False}
            elif row[0] == 'bind':
                df[uid]['bind'] = True
            elif row[0] == 'move':
                uid = int(row[1])
                x = int(row[2])
                y = int(row[3])
                z = int(row[4])
                df[uid]['p'].append((x,y,z))         
    return df   

def random_walk(b, p, df, speed=10):
    b.visible = True
    time.sleep(1.0/speed)
    for u in df['p']:
        b.pos = p
        p.x = u[0]
        p.y = u[1]
        p.z = u[2]
        time.sleep(1.0/speed)
    if df['bind']:
        b.color = color.red
    else:
        b.visible = False

# create invisible boxes
print('read dat')
df = read_dat('dla.dat')
print('creating boxes')
B = {}
for uid in df:
    x, y, z = df[uid]['p'][0]
    p = vector(x, y, z)
    b = box(pos=p, length=1, width=1, height=18, color=color.green, visible=False)
    B[uid] = (b, p)

# simulate random walk
#for uid in sorted(df):
#    b, p = B[uid]
#    p = vector(x, y, z)
#    random_walk(b, p, df[uid], 1000)

for uid in sorted(df):
    if not df[uid]['bind']:
        continue
    b, p = B[uid]
    b.visible = True
    x, y, z = df[uid]['p'][-1]
    print('uid=', uid)
    print('(x,y,z)=',x,y,z)
    b.pos = vector(x, y, z)
    time.sleep(0.1)
#time.sleep(300)