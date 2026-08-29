#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import json
from collections import defaultdict
from collections import Counter
#import style
import matplotlib.pyplot as plt 
import os 
import time
import numpy as np
from collections import defaultdict, Counter
from scipy import stats

plt.rc('axes', titlesize=25)
plt.rc('axes', labelsize=15)
plt.rc('lines', markersize=6)
plt.rc('lines', linewidth=2)
plt.rc('legend', loc='best')
plt.rc('legend', fontsize=8)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.rc('font', family='serif')

cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 12)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H', 'h']
plt.rcParams['text.usetex'] = True

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

    def count_total_neighbors_for_rods(self):
        rod_total_neighbors = {}

        for rod in self.rods.values():
            total_neighbors = 0
            for pid in rod.pids:
                particle = self.particles[pid]
                total_neighbors += len(particle.neigh_rids)
            
            rod_total_neighbors[rod.rid] = total_neighbors

        return rod_total_neighbors

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
    #print('Creating connections')
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
        #print(f'   tElapsed {fn_db} in {toc:.2f} s')
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
            lid = y
            xz = np.array([x, z])
            p = Particle(ssd, pid, rid, lid, xz)
            # add particle to the backbone
            ssd.particles[pid] = p
            # add particle to the rod
            if rid not in ssd.rods:
                ssd.rods[rid] = Rod(ssd,rid)
            ssd.rods[rid].add_pid(pid)
            # add particle to the layer
            if lid not in ssd.layers:
                ssd.layers[lid] = Layer(lid)
            ssd.layers[lid].add_pid(pid)
            pid += 1
    lid = list(ssd.layers.keys())
    ssd.lid_max = int(max(lid))                                         
    ssd.lid_min = int(min(lid))
    
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
# A função create_neighs e o resto da classe permanecem os mesmos.




# In[4]:


# Estruturas para armazenar informações
pid_neighbors_count = Counter()
rid_to_pid = defaultdict(set)

#path = r'C:\Users\55859\Datas\Collagen_fibril_zurik_ext'
path = '/home/robert/Datas/Cores_fibrils/ts_8192_seed_6160.db' 

try:
    with open(path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            if 'pid' in data and 'rid' in data:
                pid = data['pid']
                rid = data['rid']
                rid_to_pid[rid].add(pid)

                neigh_rids = data.get('neigh_rids', [])
                pid_neighbors_count[pid] = len(neigh_rids)

except Exception as e:
    print(f"Erro ao processar o arquivo: {e}")

# Agora somamos o número de vizinhos de todos os 'pids' para cada 'rid'
links_count = {rid: sum(pid_neighbors_count[pid] for pid in pids) for rid, pids in rid_to_pid.items()}

# Opcional: Salvar o resultado em um arquivo
output_file_path = 'saida_vizinhos_por_rid.json'
try:
    with open(output_file_path, 'w') as outfile:
        json.dump(links_count, outfile, indent=4)
    print(f"Dados salvos com sucesso em {output_file_path}")
except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")


# Em seguida, calculamos a distribuição desses números de vizinhos
distribution = Counter(links_count.values())
distribution

x = sorted(list(distribution.keys()))
y = np.array([distribution[i] for i in x])
y = y/sum(y)

# In[3]:


# Caminho para a pasta 'Core_fibrils'
#path = r'C:\Users\55859\Datas\Cores_fibrils'
path = '/home/robert/Datas/Cores_fibrils'

# Dicionário para armazenar os resultados finais
final_results = defaultdict(lambda: defaultdict(int))
X = defaultdict(lambda: defaultdict(int))

# Listando todos os arquivos no diretório
for filename in os.listdir(path):
    if filename.startswith("ts_") and filename.endswith(".db"):
        ts_value = int(filename.split('_')[1].split('.')[0])  # Extraindo o valor de 'ts'

        file_path = os.path.join(path, filename)
        
        # Inicializando as estruturas de dados para este arquivo
        pid_neighbors_count = Counter()
        rid_to_pid = defaultdict(set)

        ###
        # Processando o arquivo
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    data = json.loads(line.strip())
                    if 'pid' in data and 'rid' in data:
                        pid = data['pid']
                        rid = data['rid']
                        rid_to_pid[rid].add(pid)

                        neigh_rids = data.get('neigh_rids', [])
                        pid_neighbors_count[pid] = len(neigh_rids)

            # Somando o número de vizinhos de todos os 'pids' para cada 'rid'
            links_count = {rid: sum(pid_neighbors_count[pid] for pid in pids) for rid, pids in rid_to_pid.items()}
        ###
            # Calculando a distribuição
            distribution = Counter(links_count.values())

            # Preparando os dados x e y
            x = sorted(distribution.keys())
            y = np.array([distribution[i] for i in x])
            

            # Agregando os resultados
            for x_val, y_val in zip(x, y):
                final_results[ts_value][x_val] += y_val
                X[ts_value][x_val]+=1

        except Exception as e:
            print(f"Erro ao processar o arquivo {filename}: {e}")

# Convertendo os resultados finais para uma forma mais fácil de usar
final_results = {ts: dict(values) for ts, values in final_results.items()}
fr = {ts: final_results[ts] for ts in sorted(final_results)}
# Exibindo os resultados
for ts, values in fr.items():
    print(f"ts: {ts}, distribuição: {values}")


# In[11]:


plt.figure(dpi=600)
i = 0

# Supondo que fr é um dicionário fornecido contendo os dados a serem plotados
for ts, values in fr.items():
    # Convertendo chaves e valores para arrays numpy para facilitar a manipulação
    x = np.array(list(values.keys()))
    y = np.array(list(values.values()))
    m = np.array(list(X[ts].values()))
    
    x_nonzero = x[x!=0]
    y_nonzero = y[x!=0]
    m_nonzero = m[x!=0]


    # Aplicando a lógica de remoção de valores baseada em x (análogo à primeira_lista)
    indices_para_remover = []
    indice_zero = None
    for idx, valor in enumerate(x_nonzero):
        if valor == 0:
            indice_zero = idx
            
        elif valor % 2 != 0:
            indices_para_remover.append(idx)  # Adicionar índice de valor ímpar


    # Passo 3: Remover os valores correspondentes na segunda lista
    valores_removidos = [y_nonzero[i] for i in indices_para_remover if i != indice_zero]

    # Passo 4: Calcular a soma dos valores removidos
    soma = sum(valores_removidos)
    print(soma/sum(y_nonzero/10))
    # Ajustando y baseado nos índices para remover, excluindo o valor associado ao índice do valor zero
    y_ajustado = np.delete(y_nonzero, indices_para_remover)
    x_ajustado = np.delete(x_nonzero, indices_para_remover)
    m_ajustado = np.delete(m_nonzero, indices_para_remover)
    print(x_ajustado)
    # Plotando os valores ajustados
    plt.scatter(x_ajustado, y_ajustado/m_ajustado, marker=markers[i], label=f'{ts}')
    i += 1

# Adicionando rótulos e título ao gráfico
plt.xlabel(r'$C_{l}$')
plt.ylabel(r'$N$', rotation=0, labelpad=10)

plt.legend()
plt.show()


# In[33]:


X

# In[10]:



# Uso do código
ssd = read_or_create_ssd('/home/robert/Datas/Cores_fibrils/ts_8192_seed_6160.db')
total_neighbors_count = ssd.count_total_neighbors_for_rods()

# Exibindo os resultados
for rid, count in total_neighbors_count.items():
    print(f"Rod {rid} tem um total de {count} ligações.")


# In[28]:


# Caminho para a pasta 'Core_fibrils'
directory_path = '/home/robert/Datas/Cores_fibrils'

# Dicionário para armazenar os resultados finais
final_results = defaultdict(lambda: defaultdict(int))
X = defaultdict(lambda: defaultdict(int))
# Listando todos os arquivos no diretório
for filename in os.listdir(directory_path):
    if filename.startswith("ts_") and filename.endswith(".db"):
        ts_value = int(filename.split('_')[1].split('.')[0])  # Extraindo o valor de 'ts'

        file_path = os.path.join(directory_path, filename)
        
        # Inicializando as estruturas de dados para este arquivo
        pid_neighbors_count = Counter()
        rid_to_pid = defaultdict(set)

        ###
        # Processando o arquivo
        try:
            # Uso do código
            ssd = read_or_create_ssd(file_path)
            total_neighbors_count = ssd.count_total_neighbors_for_rods()

        ###
            # Calculando a distribuição
            distribution = Counter(total_neighbors_count.values())

            # Preparando os dados x e y
            x = sorted(distribution.keys())
            y = np.array([distribution[i] for i in x])
            X 

            # Agregando os resultados
            for x_val, y_val in zip(x, y):
                final_results[ts_value][x_val] += y_val
                X[ts_value][x_val]+=1
        except Exception as e:
            print(f"Erro ao processar o arquivo {filename}: {e}")

# Convertendo os resultados finais para uma forma mais fácil de usar
final_results = {ts: dict(values) for ts, values in final_results.items()}

# Exibindo os resultados
for ts, values in final_results.items():
    print(f"ts: {ts}, distribuição: {values}")


# In[31]:


int(X[128][1])

# In[25]:


a,b = np.unique(c,return_counts=True)

# In[27]:


a

# In[26]:


b

# In[5]:


total_neighbors_count

# In[6]:


distribution = Counter(total_neighbors_count.values())

# In[16]:


distribution[]

# In[4]:


final_results[128]

# In[7]:


final_results[2]

# In[6]:


dist_ts = final_results[2]
print(dist_ts)
x = sorted(dist_ts.keys())
y = np.array([dist_ts[i] for i in x])
y_normalized = y / sum(y)

# In[23]:


for ts in fr.keys():
    dist_ts = fr[ts]
    #print(dist_ts)
    x = sorted(dist_ts.keys())
    # Cálculos
    dados = x
    media = np.mean(dados)
    mediana = np.median(dados)
    moda = stats.mode(dados)[0][0]  # Retorna o valor mais frequente
    desvio_padrao = np.std(dados, ddof=1)  # Use ddof=1 para amostra
    variancia = np.var(dados, ddof=1)  # Use ddof=1 para amostra
    amplitude = np.max(dados) - np.min(dados)
    assimetria = stats.skew(dados)
    curtose = stats.kurtosis(dados, fisher=True)  # Fisher=True retorna a curtose excessiva

    # Exibindo os resultados
    print(f"Média: {media}")
    print(f"Mediana: {mediana}")
    print(f"Moda: {moda}")
    print(f"Desvio Padrão: {desvio_padrao}")
    print(f"Variância: {variancia}")
    print(f"Amplitude: {amplitude}")
    print(f"Assimetria: {assimetria}")
    print(f"Curtose: {curtose}")
    y = np.array([dist_ts[i] for i in x])
    y_normalized = y / sum(y)
    x = np.array(x)
    plt.figure(dpi = 600)
    plt.scatter(x[x%2 == 0], np.array(y_normalized)[x%2 == 0], color='#006666', label = '%d'%ts)
    plt.xlabel("Number of links")
    plt.ylabel("% of links")
    plt.legend()
    plt.show()

# In[24]:


import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

for ts in fr.keys():
    dist_ts = fr[ts]
    x = sorted(dist_ts.keys())
    dados = x
    y = np.array([dist_ts[i] for i in x])
    y_normalized = y / sum(y)

    # Cálculo dos percentis para 95% dos dados
    lower_percentile = np.percentile(dados, 2.5)
    upper_percentile = np.percentile(dados, 97.5)

    # Plot
    plt.figure(dpi=600)
    plt.scatter(x, y_normalized, color='#006666', label='%d' % ts)
    plt.xlabel("Number of links")
    plt.ylabel("% of links")

    # Desenhando linhas verticais para os percentis
    plt.axvline(x=lower_percentile, color='red', linestyle='--')
    plt.axvline(x=upper_percentile, color='red', linestyle='--')

    plt.legend()
    plt.show()

# In[9]:


for ts, values in fr.items():
    x = np.array(list(values.keys()))
    y = np.array(list(values.values()))
    print(x)

# In[8]:


plt.figure(dpi=600)
i = 0

# Plotando as curvas para cada valor de ts em um mesmo gráfico
for ts, values in fr.items():
    x = np.array(list(values.keys()))
    y = np.array(list(values.values()))
    
    # Ignorando os valores de x igual a zero
    non_zero_indices = x != 0
    plt.plot(x[non_zero_indices][x[non_zero_indices] % 2 == 0], y[non_zero_indices][x[non_zero_indices] % 2 == 0]/50,marker = markers[i], label=f'ts: {ts}')
    i+=1
# Adicionando rótulos e título ao gráfico
plt.xlabel(r'$C_{l}$')
plt.ylabel(r'$N$', rotation=0, labelpad=10)

plt.legend()
plt.show()


# In[13]:


plt.figure(dpi=600)
i = 0

# Plotando as curvas para cada valor de ts em um mesmo gráfico
for ts, values in fr.items():
    x = np.array(list(values.keys()))
    y = np.array(list(values.values()))
    
    # Ignorando os valores de x igual a zero

    plt.scatter(x,y,marker = markers[i], label=f'{ts}')
    i+=1
# Adicionando rótulos e título ao gráfico
plt.xlabel(r'$C_{l}$')
plt.ylabel(r'$N$', rotation=0, labelpad=10)

plt.legend()
plt.show()

# In[34]:


X[128]

# In[37]:


m = np.array(list(X[128].values()))
m

# In[39]:


import matplotlib.pyplot as plt
import numpy as np

plt.figure(dpi=600)
i = 0

# Supondo que fr é um dicionário fornecido contendo os dados a serem plotados
for ts, values in fr.items():
    # Convertendo chaves e valores para arrays numpy para facilitar a manipulação
    x = np.array(list(values.keys()))
    y = np.array(list(values.values()))
    m = np.array(list(X[ts].values()))
    
    x_nonzero = x[x!=0]
    y_nonzero = y[x!=0]


    # Aplicando a lógica de remoção de valores baseada em x (análogo à primeira_lista)
    indices_para_remover = []
    indice_zero = None
    for idx, valor in enumerate(x_nonzero):
        if valor == 0:
            indice_zero = idx
            
        elif valor % 2 != 0:
            indices_para_remover.append(idx)  # Adicionar índice de valor ímpar


    # Passo 3: Remover os valores correspondentes na segunda lista
    valores_removidos = [y_nonzero[i] for i in indices_para_remover if i != indice_zero]

    # Passo 4: Calcular a soma dos valores removidos
    soma = sum(valores_removidos)
    print(soma/sum(y_nonzero/50))
    # Ajustando y baseado nos índices para remover, excluindo o valor associado ao índice do valor zero
    y_ajustado = np.delete(y, indices_para_remover)
    x_ajustado = np.delete(x, indices_para_remover)
    m_ajustado = np.delete(m, indices_para_remover)
    
    # Plotando os valores ajustados
    plt.scatter(x_ajustado, y_ajustado/m_ajustado, marker=markers[i], label=f'{ts}')
    i += 1

# Adicionando rótulos e título ao gráfico
plt.xlabel(r'$C_{l}$')
plt.ylabel(r'$N$', rotation=0, labelpad=10)

plt.legend()
plt.show()


# In[40]:


x_ajustado

# In[ ]:




# In[ ]:


import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Substitua isso pelo seu dicionário de distribuição
# Exemplo: distribuicao = {0: 0.1, 1: 0.2, 2: 0.4, 3: 0.2, 4: 0.1}
distribuicao = fr[2]

# Convertendo o dicionário em um array para análise
valores, densidades = zip(*distribuicao.items())
valores = np.array(valores)
densidades = np.array(densidades)

# Normalizando as densidades para obter frequências (se necessário)
densidades /= densidades.sum()

# Gerando dados para análise com base nas densidades
dados = np.random.choice(valores, size=10000, p=densidades)

# Estatísticas Descritivas
media = np.mean(dados)
mediana = np.median(dados)
desvio_padrao = np.std(dados)
print("Média:", media)
print("Mediana:", mediana)
print("Desvio Padrão:", desvio_padrao)

# Histograma
plt.hist(dados, bins=len(valores), density=True, alpha=0.6, color='g')
plt.title("Histograma dos Dados")
plt.xticks(valores)
plt.show()

# Teste de Shapiro-Wilk para Normalidade
shapiro_test = stats.shapiro(dados)
print("Teste de Shapiro-Wilk: Estatística =", shapiro_test[0], ", p-valor =", shapiro_test[1])

# QQ-Plot
stats.probplot(dados, dist="norm", plot=plt)
plt.title("QQ-Plot")
plt.show()

