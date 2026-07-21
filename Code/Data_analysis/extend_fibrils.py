#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import os

def extract_ts_and_seed(filename):
    # Use expressões regulares para extrair 'ts' e 'seed' do nome do arquivo
    match = re.match(r"dla_mode_s_ts_(\d+)_.*seed_(\d+)_.*\.dat", filename)
    if match:
        ts = match.group(1)
        seed = match.group(2)
        return ts, seed
    return None, None

def get_new_filename(filename):
    ts, seed = extract_ts_and_seed(filename)
    if ts and seed:
        return f"ts_{ts}_seed_{seed}.dat"
    return None


# In[ ]:


# Substitua o caminho conforme necessário
#path = r'C:\Users\55859\Datas\Collagen_fibril_zurik'
path = './'

# Obtém a lista de arquivos .dat no diretório
dat_files = [file for file in os.listdir(path) if file.endswith(".dat")]

# Adiciona o caminho ao nome do arquivo
files = [os.path.join(path, file) for file in dat_files]

# Agora, 'caminho_completo' contém os caminhos completos dos arquivos .dat no diretório especificado
print(files)


# In[3]:


len(files)


# In[7]:


#new_folder = r'C:\Users\55859\Datas\Collagen_fibril_zurik_ext'
new_folder = '/home/robert/Datas/Collagen_fibril_zurik_ext/'

for caminho in files:
    ts, seed = extract_ts_and_seed(os.path.basename(caminho))
    if ts and seed:
        new_filename = f"ts_{ts}_seed_{seed}.dat"
        print(new_filename)
        fn = os.path.join(new_folder, new_filename)
        print(fn)
        with open(fn, "w") as fid, open(caminho, 'r') as fid2:
            fid.write('id uid x y z\n')
            for row in fid2:
                if 'uid:' in row:
                    row = row.split()
                    id = int(row[1])
                    x = int(row[2])
                    y = int(row[3])
                    z = int(row[4])
                    for i in range(0, 18):
                        fid.write('uid %d %d %d %d\n' % (id, x, y + i, z))


# In[3]:


caminho = '/home/robert/Documentos/GitHub/dla-collagen/codigo_finalizado/dla_mode_s_ts_32_nb_30000_seed_10000_.dat'
fn = "ts__seed_.dat"

with open(fn, "w") as fid, open(caminho, 'r') as fid2:
    fid.write('id uid x y z\n')
    for row in fid2:
        if 'uid:' in row:
            row = row.split()
            id = int(row[1])
            x = int(row[2])
            y = int(row[3])
            z = int(row[4])
            for i in range(0, 18):
                fid.write('uid %d %d %d %d\n' % (id, x, y + i, z))

