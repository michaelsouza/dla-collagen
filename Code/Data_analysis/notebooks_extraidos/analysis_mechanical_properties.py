#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.font_manager as font_manager
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from collections import defaultdict
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def ava_sizes(ts_DF):
    for ts, df in sorted(ts_DF.items()):
        print('avalanches for ts : %d' % ts)
        with open('ava_%d.dat' % ts, 'w') as fid:
            # Assuming 'num_deleted_rods' is a column in your DataFrame
            lista = np.array(df['num_deleted_rods'])
            lista_sem_zeros = [x for x in lista if x != 0]
            
            nl = [lista_sem_zeros[0]]
            for i in range(1, len(lista_sem_zeros)):
                nl.append(lista_sem_zeros[i] - lista_sem_zeros[i-1])

            nl_sem_zeros = [x for x in nl if x != 0]
            for i in nl_sem_zeros:
                fid.write('%d\n' % i)

cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 12)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H', 'h']

plt.rcParams['text.usetex'] = True
#plt.rc('axes', titlesize=20)
plt.rc('axes', labelsize=20) ##tamanho do label
plt.rc('lines', markersize=6)
plt.rc('lines', linewidth=2)
plt.rc('legend', loc='best')
plt.rc('legend', fontsize=8)
plt.rc('xtick', labelsize=13) ##tamanho dos numeros nos eixos
plt.rc('ytick', labelsize=13)
plt.rc('font', family='serif')

ts = [2,8,16,32,64,128,512,1024,4096,8192,10000]
Color=cmap(np.linspace(0, 1, 12))

# In[2]:


##### Read files and create dict

# Crie um dicionário para armazenar listas de 'df' por 'ts'
ts_df = defaultdict(list)

#path = r'C:\Users\55859\Datas\Stress_carmona'
path = '/home/robert/Datas/Stress_carmona/'
for fn in tqdm(sorted(os.listdir(path))):
    if not fn.endswith('.txt'):
        continue    
    
    file_path = os.path.join(path, fn)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_frames = {}
    current_df = None

    # Extract the column names
    column_names = ['F','num_particles','num_deleted_particles','num_deleted_rods']

    # Define a regular expression pattern to match "ts_" followed by one or more digits
    pattern = r'ts_(\d+)'

    # Use re.findall() to find all matches in the file path
    numbers_after_ts = [match for match in re.findall(pattern, file_path)]

    ts = int(numbers_after_ts[0])

    # Iterate through the lines in the file (starting from the second line)
    for line in lines[1:]:
        line = line.strip()
        if line.startswith('-'):
            # This is a separator line; the following line contains the name of the DF
            current_df = line.lstrip('-').strip()
        elif line:
            # This line contains data for the current DF
            data = line.split(',')
            if current_df not in data_frames:
                data_frames[current_df] = {
                    'columns': column_names,
                    'data': []
                }
            data_frames[current_df]['data'].append(data)

    # Process each data frame ]
    for df_name, df_data in data_frames.items():
        df = pd.DataFrame(df_data['data'], columns=column_names)
        df['num_deleted_rods'] = pd.to_numeric(df['num_deleted_rods'], errors='coerce', downcast='integer')
        df['num_deleted_particles'] = pd.to_numeric(df['num_deleted_particles'], errors='coerce', downcast='integer')
        df['num_particles'] = pd.to_numeric(df['num_particles'], errors='coerce')
        df['F'] = pd.to_numeric(df['F'], errors='coerce')

        ts_df[ts].append(df)



# In[ ]:


##### Cut for mediumn force of broke

cut = []
for ts in sorted(ts_df.keys()):
    print(ts)
    ul = []
    for DF in (ts_df[ts]):
        ultima_linha = DF.tail(1)
        ul.append(ultima_linha)

    df_concatenado = pd.concat(ul, axis=0).reset_index(drop=True)
    cut.append(df_concatenado['F'].mean())

# In[4]:


##### Create a unique df for each ts

ts_DF = {}
for ts in ts_df.keys():
    dfs = []
    for i in range(len(ts_df[ts])):
        df = ts_df[ts][i]
        dfs.append(df)

    #print(dfs)
    df_conc = pd.concat(dfs, ignore_index=True)
    ts_DF[ts] = df_conc
    

# In[5]:


##### fix for ts 8 files

df = ts_DF[8]
# Drop rows with NaN values
df.dropna(inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)
ts_DF[8] = df


# In[6]:


##### Check for has nan values in dfs

df = ts_DF[8]
# Verificando a presença de NaN
nan_mask = df.isna()

# Contando NaN em cada coluna
nan_count = df.isna().sum()

# Verificando se há algum NaN no DataFrame
has_nan = df.isna().any().any()

# Visualizando linhas com NaN
rows_with_nan = df[df.isna().any(axis=1)]

# Imprimindo os resultados
print("Máscara de NaN:\n", nan_mask)
print("\nContagem de NaN por coluna:\n", nan_count)
print("\nHá NaN no DataFrame:", has_nan)
print("\nLinhas com NaN:\n", rows_with_nan)

# In[80]:


##### For check the number of avalanches in the process 

ava_sizes(ts_DF)

# In[32]:


##### Check the frequence of forces for cut the data

cut = []
plt.figure(dpi = 600)
marker_index = 0
for ts in sorted(ts_DF):
    df = ts_DF[ts]
    Force, f = np.unique(df['F'], return_counts=True)
    f = f/f[0]

    plt.scatter(Force, f, marker=markers[marker_index], label=ts)
    marker_index = (marker_index + 1) % len(markers)  # Incrementar e ciclar pelo markers
    
    # Inicializar uma variável para armazenar temporariamente o último valor que satisfaz a condição
    last_value_meeting_condition = None

    # Verificar quais frequências são >= 0.25
    for i in range(len(f)):
        if f[i] <= 0.25:
            last_value_meeting_condition = Force[i]

    # Se um valor foi encontrado, adicione-o ao vetor cut
    if last_value_meeting_condition is not None:
        cut.append(last_value_meeting_condition)
    
# Imprimir o vetor cut para verificar
print(cut)
x = np.linspace(0,220,220)
y = np.ones(220)*0.25

plt.plot(x,y,'--',color='#006666')
plt.xlabel(r'$F$')
plt.ylabel(r'$\omega$')
plt.legend(loc = 'best')
plt.show


# In[33]:


##### Check the frequence of forces for cut the data

cut = []
plt.figure(dpi = 600)
marker_index = 0
for ts in sorted(ts_DF):
    df = ts_DF[ts]
    Rods, f = np.unique(df['num_deleted_rods'], return_counts=True)
    f = f/f[0]

    plt.scatter(Rods, f, marker=markers[marker_index], label=ts)
    marker_index = (marker_index + 1) % len(markers)  # Incrementar e ciclar pelo markers
    
    # Inicializar uma variável para armazenar temporariamente o último valor que satisfaz a condição
    last_value_meeting_condition = None

    # Verificar quais frequências são >= 0.25
    for i in range(len(f)):
        if f[i] >= 0.25:
            last_value_meeting_condition = Force[i]

    # Se um valor foi encontrado, adicione-o ao vetor cut
    if last_value_meeting_condition is not None:
        cut.append(last_value_meeting_condition)
    
# Imprimir o vetor cut para verificar
print(cut)
x = np.linspace(0,220,220)
y = np.ones(220)*0.25

#plt.plot(x,y,'--',color='#006666')
plt.xlabel(r'$Rods$')
plt.ylabel(r'$\omega$')
plt.legend(loc = 'best')
plt.show


# In[7]:


##### Dict with df mean for each ts 

ts_DFM = {}
for ts in sorted(ts_DF):
    
    ts_DFM[ts] = ts_DF[ts].groupby('F').mean().reset_index()
    ts_DFM[ts]['num_deleted_rods'] = ts_DFM[ts]['num_deleted_rods'].astype(int)
    ts_DFM[ts]['num_particles'] = ts_DFM[ts]['num_particles'].astype(int)

#ts_DFM

# In[8]:


##### Calc the mean of values and cut

for data,c in zip(ts_DFM,cut):
    ts_DFM[data] = ts_DFM[data][ts_DFM[data]["F"] <= c]

    ## Extend num_delete_rods
    ts_DFM[data]['num_deleted_rods'] =  ts_DFM[data]['num_deleted_rods'] 
    ts_DFM[data]['num_deleted_rods'] = ts_DFM[data]['num_deleted_rods'].astype(int)

    ## Normalize num particles
    ts_DFM[data]['num_particles_norm'] = ts_DFM[data]['num_particles']/ts_DFM[data]['num_particles'].max()

    ## Set zero in last line
    # Crie uma linha com valores escalares em um DataFrame
    line = pd.DataFrame({'F': [list(ts_DFM[data]['F'])[-1]],
                        'num_particles': [0],
                        'num_deleted_rods': [ts_DFM[data]['num_particles'][0]],
                        'num_particles_norm': [0]})

    # Use o método concat para adicionar a nova linha ao DataFrame
    #ts_DFM[data] = pd.concat([ts_DFM[data], line], ignore_index=True)

# In[9]:


### For convert to real force, you need to convert to strain and use a factor:

fcc = 0.3*(10**(-9))
dia_m = 1.5*(10**(-9))
A = np.loadtxt('/home/robert/dla-collagen/Rs.dat')
R = np.round(A[:,1],2)*dia_m

# In[10]:


plt.figure(dpi = 600)
plt.ylabel(r' % of Particles in Skeleton')
plt.xlabel(r"$F$")
i = 0
a = []
for ts, df in ts_DFM.items():
    
    y = df['num_particles_norm'].to_numpy()[:-1]
    x = df['F'].to_numpy()[:-1]
    #print(x[-1])
    a.append(x[-1])
    plt.scatter(x,y ,marker = markers[i], label = ts)
    

    i+= 1
a = np.array(a)
plt.legend()

# In[12]:


plt.figure(dpi=600)
plt.xlabel(r'$\epsilon (\%)$')
plt.ylabel('$\sigma(MPa)$', rotation = 90, labelpad=4)
i = 0
a = []
sig = []
for ts, df in ts_DFM.items():

    x = df['num_deleted_rods'].to_numpy()[1:-1]
    x = x/(int(df['num_particles'].max())/18)
    y = df['F'].to_numpy()[1:-1]*fcc/(np.pi*(R[i]**2))/1000000
    #print(x[-1])
    #a.append(x[-1])

    #### Importante pra caramba
    sig.append(y.max())
    plt.scatter(x,y ,marker = markers[i], label = ts)
    i+= 1
    with open(f'sigma_e_{ts}.dat', 'w') as file:
        for log_x_val, log_y_val in zip(x, y*1000000):
            file.write(f'{log_x_val}\t{log_y_val}\n')

#a = np.array(a)
    
# Configurar os tracinhos para dentro e desativar os labels superior e direito
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.ylim(-1,50)
plt.legend()

# In[88]:


### Calculo da taxa de variação para sigma em função de e
files= ['sigma_e_2.dat','sigma_e_8.dat','sigma_e_16.dat','sigma_e_32.dat','sigma_e_64.dat','sigma_e_128.dat','sigma_e_512.dat','sigma_e_1024.dat','sigma_e_4096.dat','sigma_e_8192.dat','sigma_e_10000.dat']
# Carregar dados

for file in files:
    print('lendo arquivo %s' %file)
    dados = np.loadtxt(file)

    # Separar 'x' e 'f(x)'
    x = np.round(dados[:, 0],2)
    f_x = np.round(dados[:, 1],2)

    # Remover pontos duplicados em 'x'
    _, idx_unicos = np.unique(x, return_index=True)
    #print(idx_unicos)
    x = x[idx_unicos]
    f_x = f_x[idx_unicos]

    # Primeira Derivada usando Diferenças Centrais
    #derivada1 = np.zeros_like(x)
    h = np.diff(x)
    # Calcula diferenças centrais para pontos internos
    derivada1 = (f_x[1:] - f_x[:-1]) / (x[1:] - x[:-1])

    # save data 
    fn = 'diff_'+file
    with open('%s' %fn, 'w') as file:
        for x, y in zip(np.round(x,2), np.round(derivada1,2)):
            file.write(f'{x}\t{y}\n')



# In[15]:


file = 'sigma_e_10000.dat'
plt.figure(dpi = 600)
plt.xlabel(r'$\epsilon $')
plt.ylabel(r'$\sigma$', rotation=0,labelpad=10)
# Carregar dados
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = (dados[:, 0])
f_x = (dados[:, 1])
print(len(x))
print(len(f_x))

# Remover pontos duplicados em 'x'
_, idx_unicos = np.unique(x, return_index=True)
#print(idx_unicos)
x = x[idx_unicos]
f_x = f_x[idx_unicos]

plt.scatter(x,f_x,marker=markers[0], label=ts)

# In[16]:


file = 'diff_sigma_e_10000.dat'

plt.figure(dpi = 600)
plt.xlabel(r'$\epsilon $')
plt.ylabel(r'$\frac{d \sigma}{d \epsilon}$', rotation=0,labelpad=10)
# Carregar dados
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = np.round(dados[:, 0],2)
f_x = np.round(dados[:, 1],2)
print(len(x))
print(len(f_x))

# Remover pontos duplicados em 'x'
_, idx_unicos = np.unique(x, return_index=True)
#print(idx_unicos)
x = x[idx_unicos]
f_x = f_x[idx_unicos]

plt.scatter(x,f_x,marker=markers[0], label=ts)


# In[17]:


file = 'sigma_e_10000.dat'
# Carregar dados
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = np.round(dados[:, 0],3)
f_x = np.round(dados[:, 1],3)

# Extraia esses índices de x e f_x
ind = np.where(x >= 0.01)[0]

x = x[ind]
y = f_x[ind]

ind2 = np.where(x<=0.28)
ind3 = np.where(x>=0.28)


x2 = x[ind2]
y2 = y[ind2]

x3 = x[ind3]
y3 = y[ind3]

fn = 'sig10000_non.dat'
with open('%s' %fn, 'w') as file:
    for i, j in zip(x2, y2):
        file.write(f'{i}\t{j}\n')

fn = 'sig10000_lin.dat'
with open('%s' %fn, 'w') as file:
    for i, j in zip(x3, y3):
        file.write(f'{i}\t{j}\n')


# In[12]:


file = 'sigma_e_8.dat'
dados = np.loadtxt(file)

plt.figure(dpi = 600)
# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]/1000000
plt.scatter(x,f_x, marker = markers[1], edgecolor = Color[1], color = 'white', label = f'{8}')

dados = np.loadtxt('fit8_lin.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000

plt.plot(x1,y1,'-', color = Color[1])

dados = np.loadtxt('fit8_non.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000

plt.plot(x1,y1,'-', color = Color[1])

pc = (0.38, 2)
plt.text(pc[0], pc[1]+0.2, r'$\alpha$ = $7.98\times10^{5}$', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))


file = 'sigma_e_128.dat'
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]/1000000
plt.scatter(x,f_x, marker = markers[5], edgecolor = Color[5], color = 'white', label = f'{128}')

dados = np.loadtxt('fit128_lin.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000

plt.plot(x1,y1,'-', color = Color[5])

dados = np.loadtxt('fit128_non.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000

plt.plot(x1,y1,'-', color = Color[5])
pc = (0.38, 31)
plt.text(pc[0], pc[1]+0.2, r'$\alpha$ = $7.35\times10^{6}$', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))




file = 'sigma_e_10000.dat'
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]/1000000
plt.scatter(x,f_x, marker = markers[10], edgecolor = Color[10], color = 'white', label = f' {10000}')

dados = np.loadtxt('fit10000_lin.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000

plt.plot(x1,y1,'-', color = Color[10])

dados = np.loadtxt('fit10000_non.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]/1000000


plt.plot(x1,y1,'-', color = Color[10])

pc = (0.38, 41)
plt.text(pc[0], pc[1]+0.2, r'$\alpha$ = $1.099\times10^{7}$', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))



plt.axvspan(-0.01, 0.29, color='gray', alpha=0.1)  # 'alpha' control

# Nome das regiões
pc = (0.40, 48)
plt.text(pc[0], pc[1], 'Regime linear', ha='center', va='center', fontsize=15, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))

pc = (0.15, 48)
plt.text(pc[0], pc[1], 'Regime não linear', ha='center', va='center', fontsize=15, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))

plt.legend(loc = 'best')
plt.xlabel(r'$\epsilon (\%)$')
plt.ylabel('$\sigma(MPa)$', rotation = 90, labelpad=4)
plt.xlim(0.01,0.6)
plt.ylim(0,50)
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.savefig('teste.png')

# In[ ]:


# Carregar dados
dados = np.loadtxt('fit.dat')

# Separar 'x' e 'f(x)'
a = dados[:, 1]
print(a)
b = dados[:, 2]
x = np.linspace(0,0.28,100)
for i in range(len(a)):

    f_x = 10**(a[i]-b[i]*x)
    plt.plot(x,f_x,'-',linewidth = 1, c = color[i])



# Nome das regiões
pc = (0.45, 599900000)
plt.text(pc[0], pc[1], 'Regime linear\npara $\\sigma$ \n  $\\sigma = E\\epsilon$', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))

pc = (0.15, 599900000)
plt.text(pc[0], pc[1], 'Regime não linear\npara $\\sigma$ ', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))


# In[42]:



plt.figure(dpi=300)
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.ylabel(r'Log(Num. Removed Particles)')
plt.xlabel(r"Log(F)")
i = 0
a = []
for ts, df in ts_DFM.items():
    y = df['num_deleted_rods'].to_numpy()[:-1]
    x = df['F'].to_numpy()[:-1]
    #print(x[-1])
    #a.append(x[-1])
    plt.scatter(x,y ,marker = markers[i], label = ts)
    i+= 1

#a = np.array(a)
plt.xscale('symlog')
plt.yscale('symlog')
plt.legend()

# In[86]:


cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
plt.figure(figsize=(9,9))
plt.figure(dpi=300)
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.ylabel(r'Log(Num. Removed Particles)')
plt.xlabel(r"Log(F)")
i = 0
a = []
for ts, df in ts_DFM.items():

    #if i == 5:
        #break
    y = df['num_deleted_rods'].to_numpy()[2:-1]
    x = df['F'].to_numpy()[2:-1]
    plt.scatter(x,y ,marker = markers[i], label = ts)
    i+= 1
plt.xscale('log')
plt.yscale('log')
plt.legend()

# In[11]:


fc = []
Ts = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192, 10000]
for ts, df in ts_DFM.items():
    fc.append(df['F'][:-1].max()),
    Ts.append(ts)

fc

# In[16]:


## Sig_crit x Ts

Ts = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192, 10000]

y2 = np.mean(sig[-4:-1])*np.ones(len(Ts))
x1 = np.linspace(-300,10300,len(Ts))

plt.figure(dpi = 600)
plt.plot(Ts,sig,'s-', color='#006666' )
plt.plot(x1,y2,'--',c = 'black', label = f'{4.37}')
plt.xlabel(r"$T_{s}$")
plt.ylabel('$\sigma_{c}(Pa)$', rotation = 90, labelpad=0)
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.legend()
plt.xlim(-300,10300)
plt.ylim(0, 50000000)

# In[16]:


D = []
Ts = []
plt.figure(figsize=(9,9))
plt.figure(dpi=300)
plt.xlabel(r'$T_{s}$')
plt.ylabel(r'$\rho$',rotation = 0)
for ts, df in ts_DFM.items():
    D.append(df['num_particles'].max())
    Ts.append(ts)
D = np.array(D)
D = D/(201*17*17)
plt.plot(Ts,D, 's--', color = '#006666')
lt.ylim(0.15,0.7)

# In[23]:


### Sig_crit x dens

plt.figure(dpi=600)
plt.ylabel(r'$\sigma_{c}(MPa)$', rotation = 90, labelpad =4)
plt.xlabel(r'$\rho(\%)$',rotation = 0)
plt.plot(D,sig,'s', color = '#006666')

x = np.loadtxt('fit_stress.dat')
x1 = np.linspace(min(x.T[0]), max(x.T[0]), 100)
plt.plot(x1,6.95*(10**5)*np.exp(6.23*x1)/1000000,'-', linewidth = '2',  label = r'$6.95 \times 10^{5}e^{6.08\rho}$')
plt.legend(loc = 'upper left')
#plt.ylim(40,220)
# Configurar os tracinhos para dentro e desativar os labels superior e direito
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
#plt.ylim(-1000000,50000000)

# In[19]:


# Abrir um arquivo .dat em modo de escrita
with open('stress.dat', 'w') as arquivo:
    # Iterar sobre os elementos das listas
    for item1, item2 in zip(D, sig):
        # Escrever cada par de itens em uma linha, separados por espaço
        arquivo.write(f'{item1} {item2}\n')

# In[ ]:




# In[53]:


plt.figure(dpi=600)
plt.ylabel(r'$F_{c}$')
plt.xlabel(r'$\rho$',rotation = 0)
plt.plot(D,sig,'s', color = 'darksalmon')


yreg = alpha*D+ beta

plt.plot(D,yreg,'-', linewidth = '2',  label = fr'${alpha}*\rho {beta}$')
plt.legend(loc = 'best')
#plt.ylim(40,220)


# In[18]:


np.mean(D[6:])

# In[25]:


D

# In[24]:


plt.figure(dpi=600)
plt.ylabel(r'$\sigma_{c}(Pa)$', rotation = 90, labelpad =0)
plt.xlabel(r'$\rho(\%)$',rotation = 0)
plt.plot(D,sig,'s-', color = '#006666')

x = np.loadtxt('fit_stress.dat')
plt.plot(x.T[0],x.T[1],'-', linewidth = '2',  label = r'$7.9 \times \exp(6.08 \rho)$')
plt.legend(loc = 'upper left')
#plt.ylim(40,220)
# Configurar os tracinhos para dentro e desativar os labels superior e direito
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.ylim(-1000000,50000000)

# In[92]:


fc

# In[91]:


dif = np.diff(fc)
ind = np.arange(1,len(fc))

plt.figure(figsize=(9,9))
plt.figure(dpi=300)
plt.plot(ind, dif, 'o-')
plt.xlabel('Diff')
plt.ylabel(r'$\delta F_{crit}$')
plt.ylim(-2,70)

# In[19]:


Fm = []
plt.figure(figsize=(9,9))
plt.figure(dpi=300)
plt.xlabel(r'$T_{s}$')
plt.ylabel(r'F$_{crit}$')
for ts, df in ts_DFM.items():
    Fm.append(df['F'].max())

plt.plot(fc, 'o-', color = 'k')
plt.ylim(40,225)

# In[ ]:


D = []
plt.figure(figsize=(9,9))
plt.figure(dpi=300)
plt.xlabel(r'$T_{s}$')
plt.ylabel(r'$\rho$',rotation = 0)
for ts, df in ts_DFM.items():
    D.append(df['num_particles'].max())
D = np.array(D)
D = D/(201*17*17)
plt.plot(D, 'o-', color = 'k')
plt.ylim(0.1,0.7)

# In[ ]:



plt.figure(figsize=(9,9))
plt.figure(dpi=300)
plt.ylabel(r'F$_{crit}$')
plt.xlabel(r'$\rho$')
alpha, beta, r2 = regressao_linear(D,Fm)
yreg = alpha*D+ beta
print(f"Alpha: {alpha}")
print(f"Beta: {beta}")
print(f"R^2: {r2}")
plt.plot(D,yreg)
plt.scatter(D,Fm, marker = 'o')


# In[ ]:


wdir = '/home/robert/Documentos/Stress/'
for fn in sorted(os.listdir(wdir)):
    if not fn.endswith('.db'):
        continue

    print(fn)

# In[ ]:




# In[ ]:


import plotly.graph_objects as go
fig = go.Figure()
#plt.figure(figsize=(10,10))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
#plt.ylabel(r'Num. of Removed Particles')
#plt.xlabel(r"$F$")

i = 0
for ts, df in ts_DFM.items():
    x = df['F'].to_numpy()[3:-1]
    
    y = df['num_deleted_rods'].to_numpy()[3:-1]
    x = x[y>1000]
    y = y[y>1000]
    #alpha,beta,r2 = regressao_linear(np.log(x),np.log(y))
    #print(alpha,beta,r2)
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=ts))
    #plt.scatter(, , marker = markers[i], label = ts)
    i+= 1
fig.update_layout(
    template = 'seaborn',
    width = 600,
    height = 600,
    xaxis=dict(title='Eixo X',type = 'log'),
    yaxis=dict(title='Eixo Y', type='log'),  # Escala logarítmica no eixo Y
)
fig.show()
#plt.legend()

# In[ ]:


plt.figure(figsize=(10, 6))
i = 0
for ts, df in ts_DFM.items():
    x = df['F'].to_numpy()[3:-1]
    
    y = df['num_deleted_rods'].to_numpy()[3:-1]
    x = x[y>1000]
    y = y[y>1000]
    #alpha,beta,r2 = regressao_linear(np.log(x),np.log(y))
    #print(alpha,beta,r2)
    plt.plot(x,y,'o',ms=7,markerfacecolor='none',label=f'Ts - {ts}')
    #plt.scatter(, , marker = markers[i], label = ts)
    i+= 1

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Força')
plt.ylabel('Deformação')
plt.legend()
plt.show()

# In[ ]:




# In[ ]:


ts_DFM.items()

# In[ ]:


plt.figure(figsize=(10, 6))
i = 0
for ts, df in ts_DFM.items():
    x = df['F'].to_numpy()[3:-1]
    
    y = df['num_deleted_rods'].to_numpy()[3:-1]
    #x = x[y>1000]
    #y = y[y>1000]
    #alpha,beta,r2 = regressao_linear(np.log(x),np.log(y))
    #print(alpha,beta,r2)
    plt.plot(x,y,'o',ms=7,markerfacecolor='none',label=f'Ts - {ts}')
    #plt.scatter(, , marker = markers[i], label = ts)
    i+= 1
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('Força')
plt.ylabel('Deformação')
plt.legend()
plt.show()

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np

# Cria um intervalo de valores para x (evitando x = 0)
x = np.linspace(0.1, 5, 500)

# Calcula os valores correspondentes de 1/x
y = 1 / x

# Plota o gráfico da função
plt.plot(x, y, label='1/x')

# Adiciona rótulos aos eixos
plt.xlabel('x')
plt.ylabel('1/x')

# Adiciona uma legenda
plt.legend()

# Exibe o gráfico
plt.show()


# In[ ]:


pip install -U plotly

# In[ ]:


import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def regressao_linear(x, y):
    # Verifique se as entradas têm o mesmo tamanho
    if len(x) != len(y):
        raise ValueError("As listas de entrada devem ter o mesmo tamanho.")

    # Converta as listas em arrays do numpy
    x = np.array(x).reshape(-1, 1)
    y = np.array(y)

    # Crie um modelo de regressão linear
    modelo = LinearRegression()

    # Treine o modelo
    modelo.fit(x, y)

    # Faça previsões com base no modelo treinado
    y_pred = modelo.predict(x)

    # Calcule o coeficiente de determinação (R²)
    r2 = r2_score(y, y_pred)

    # Retorne os coeficientes da regressão e o R²
    return modelo.coef_[0], modelo.intercept_,r2
    

# In[ ]:


best_r2 = 0
best_i = 0
for i in range(30,len(x)):
    alpha, beta, r2 = regressao_linear(x[-i:],y[-i:])
    if(best_r2 > r2):
        r2 = best_r2
        best_i = i

# In[ ]:


x = np.linspace(0,100,100)
y = np.linspace(0,100,100) * 52
best_r2 = 0

best_i = 0
for i in range(30,len(x)):
    alpha, beta, r2 = regressao_linear(x[-i:],y[-i:])
    if(best_r2 > r2):
        r2 = best_r2
        best_i = i


# In[ ]:


best_i

# In[ ]:


alpha

# In[ ]:


for ts, df in ts_DFM.items():
    best_r2 = 0
    best_i = 0
    x = df['F'].to_numpy()
    print(x)
    print(x[-30:])

# In[ ]:


reg_stress = []
for ts, df in ts_DFM.items():
    best_r2 = 0
    best_i = 0
    x = df['F'].to_numpy()
    y = df['num_deleted_rods'].to_numpy()
    for i in range(30,len(x)):
        alpha, beta, r2 = regressao_linear(x[-i:],y[-i:])
        
        if(best_r2 < r2):
            best_r2 = r2

            best_i = i
            print(r2)
            print(best_i)

    reg_stress.append([r2, x[-best_i:],alpha*x[-best_i:]])

# In[ ]:


reg_stress[1][1]

# In[ ]:


from sklearn.metrics import mean_squared_error, r2_score

plt.figure(figsize=(8,8))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.ylabel(r' % of Particles in Skeleton')
plt.xlabel(r"$F$")

df = ts_DFM[8]

best_r2 = 0
best_i = 0
x = df['F'].to_numpy()
y = df['num_deleted_rods'].to_numpy()
for i in range(100,len(x)):
    alpha, beta, r2 = regressao_linear(x[-i:],y[-i:])
    if(best_r2 < r2):
        
        best_r2 = r2
        best_i = i
        #print(r2)
plt.scatter(np.log(df['F'].to_numpy()[:-1]), np.log(df['num_deleted_rods'].to_numpy()[:-1]), marker = markers[0], label = ts)
x = np.array(df['F'].to_numpy()[:-1])
y = np.array(df['num_deleted_rods'].to_numpy()[:-1])
x = x[1:]
y = y[1:]
alpha, beta, r2 = regressao_linear(np.log(x),np.log(y))
plt.plot(np.log(x), alpha*np.log(x)+beta,c = 'red')
print(alpha,beta,r2)
plt.show()

# In[ ]:


ts_DFM.items()

# In[ ]:


import matplotlib.pyplot as plt

plt.rc('axes', titlesize=25)
plt.rc('axes', labelsize=25)
plt.rc('lines', markersize=12)
plt.rc('lines', linewidth=4)
plt.rc('legend', loc='best')
plt.rc('legend', fontsize=21)
plt.rc('xtick', labelsize=21)
plt.rc('ytick', labelsize=21)


# In[ ]:


plt.figure(figsize=(10,10))


markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.ylabel(r'Num. of Removed Particles')
plt.xlabel(r"$F$")

i = 0
for ts, df in ts_DFM.items():
    plt.scatter(np.log10(df['F'].to_numpy()[1:-1]), np.log10(df['num_deleted_rods'].to_numpy()[1:-1]), marker = markers[i], label = ts)
    #plt.plot(reg_stress[i][1], reg_stress[i][2])
    i+= 1

    if i == 9:
        break

plt.legend()

# In[ ]:


reg_stress

# In[ ]:


for ts in tqdm(sorted(ts_DF)):
    ts_DF[ts] = ts_DF[ts].groupby('F').mean().reset_index()

ts_DF

# In[ ]:


ts_df[1024]


# In[ ]:


dfA = {'name':[], 'F':[], 'num_particles':[]}
for i in tqdm(range(len(DF['ts']))):
    ts = DF['ts'][i]
    if ts != 2:
        continue
    k = DF['k'][i]
    seed = DF['seed'][i]
    df = DF['df'][i]
    name = f'{k}_{seed}'
    n = len(df)
    dfA['name'].extend(n * [name])
    dfA['F'].extend(df['F'].to_list())
    dfA['num_particles'].extend(df['num_particles'].to_list())
    
# convert to dataframe
dfA = pd.DataFrame(dfA)


# In[ ]:


dfA


# In[ ]:


def groupby_ts(DF, agg='mean'):
    DF_agg = {}
    for i in range(len(DF['ts'])):
        ts = DF['ts'][i]
        df = DF['df'][i]
        print(df.columns)
        
        if ts not in DF_agg:
            
            DF_agg[ts] = []
        DF_agg[ts].append(df)
    # aggregate
    for ts in DF_agg:
        DF_agg[ts] = pd.concat(DF_agg[ts])
        if agg == 'mean':
            DF_agg[ts] = DF_agg[ts].groupby('F').mean().reset_index()
        elif agg == 'count':
            DF_agg[ts] = DF_agg[ts].groupby('F').count().reset_index()
        else:
            raise ValueError(f'agg={agg} not supported')
    return DF_agg

# In[ ]:


DF_agg = groupby_ts(DF, agg='count')
DF_agg

# In[ ]:


DF_agg = groupby_ts(DF, agg='count')

dfA = {'ts':[], 'F':[], 'num_particles':[]}
for ts in DF_agg:
    df = DF_agg[ts]
    print(df)

    # normalize
    df['num_particles'] = df['num_particles'] / df['num_particles'].max()
    dfA['ts'].extend(len(df) * [ts])
    dfA['F'].extend(df['F'].values) # type: ignore
    dfA['num_particles'].extend(df['num_particles'].values) # type: ignore

dfA = pd.DataFrame(dfA)
dfA.sort_values(by=['ts', 'F'], inplace=True)
dfA


# In[ ]:


# Encontre os índices das linhas onde 'num_part' < 0.25
indices_linhas = dfA["F"][dfA['num_particles'] < 0.25]

indices_linhas

# In[ ]:


dfts = df.values()
dfts


# In[ ]:


dfts

# In[ ]:


def plot_F_vs_num_particles(DF):
    DF_agg = groupby_ts(DF, agg='mean')
    # mean number of particles for each force
    dfA = {'ts':[], 'F':[], 'num_particles':[]}
    for ts in DF_agg:
        df = DF_agg[ts]
        # normalize
        df['num_particles'] = df['num_particles'] / df['num_particles'].max()
        dfA['ts'].extend(len(df) * [ts])
        dfA['F'].extend(df['F'].values) # type: ignore
        dfA['num_particles'].extend(df['num_particles'].values) # type: ignore

    dfA = pd.DataFrame(dfA)
    dfA.sort_values(by=['ts', 'F'], inplace=True)
    fig = px.line(dfA, x='F', y='num_particles', color='ts', title='F vs num_particles')
    # resize figure
    fig.update_layout(
        autosize=False,
        width=800,
        height=600,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        # paper_bgcolor="LightSteelBlue",
    )
    fig.show()


# In[ ]:


plot_F_vs_num_particles(DF)

# In[ ]:


# count number of particles for each force
DF_agg = groupby_ts(DF, agg='count')

# mean number of particles for each force
dfA = {'ts':[], 'F':[], 'sample_size':[]}
for ts in DF_agg:
    df = DF_agg[ts]
    # normalize
    df['num_particles'] = df['num_particles'] / df['num_particles'].max()
    dfA['ts'].extend(len(df) * [ts])
    dfA['F'].extend(df['F'].values) # type: ignore
    dfA['sample_size'].extend(df['num_particles'].values) # type: ignore

dfA = pd.DataFrame(dfA)
dfA.sort_values(by=['ts', 'F'], inplace=True)

fig = px.line(dfA, x='F', y='sample_size', color='ts', title='F vs sample_size')
# resize figure
fig.update_layout(
    autosize=False,
    width=800,
    height=600,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    # paper_bgcolor="LightSteelBlue",
)
fig.show()


# In[ ]:


import matplotlib.pyplot as plt
# count number of particles for each force
DF_agg = groupby_ts(DF, agg='count')

# mean number of particles for each force
dfA = {'ts':[], 'F':[], 'sample_size':[]}
for ts in DF_agg:
    df = DF_agg[ts]
    # normalize
    df['num_particles'] = df['num_particles'] / df['num_particles'].max()
    dfA['ts'].extend(len(df) * [ts])
    dfA['F'].extend(df['F'].values) # type: ignore
    dfA['sample_size'].extend(df['num_particles'].values) # type: ignore



dfA = pd.DataFrame(dfA)
dfA.sort_values(by=['ts', 'F'], inplace=True)
display(dfA)

x = dfA['F'].tolist()

y = dfA['simple_size'].tolist()

plt.Figure(figsize=(14,14))

plt.plot(x, y, label=f'ts={ts}', linewidth = 4,linestyle='dashed')


plt.xlabel('Force',fontdict=fontlabel)
plt.ylabel('Particles in skeleton',fontdict=fontlabel)
plt.legend( loc = 'upper right',prop=fontlegend)
plt.xticks(size = 20, family = 'serif', weight = 'normal')
plt.yticks(size = 20, family = 'serif', weight = 'normal')
plt.tick_params(direction = 'in',bottom = True, top= True, left= True, right= True )
#plt.grid(True)
plt.tight_layout()
plt.show()


# In[ ]:


## new def

import matplotlib.pyplot as plt

def plot_F_vs_num_particles(DF):
    DF_agg = groupby_ts(DF, agg='mean')
    # mean number of particles for each force
    dfA = {'ts': [], 'F': [], 'num_particles': []}
    for ts in DF_agg:
        df = DF_agg[ts]
        #display(df)

        # normalize
        
        #df['num_particles'] = df['num_particles'] / df['num_particles'].max()
        dfA['ts'].extend(len(df) * [ts])
        dfA['F'].extend(df['F'].values) # type: ignore
        dfA['num_particles'].extend(df['num_particles'].values) # type: ignore
        


    dfA = pd.DataFrame(dfA)
    dfA.sort_values(by=['ts', 'F'], inplace=True)
    
    plt.figure(figsize=(14,14))
    # Create a separate line plot for each ts value
    unique_ts = dfA['ts'].unique()
    for ts in unique_ts[:9]:
        subset = dfA[dfA['ts'] == ts]
        #print(type(subset['F']))
        x = subset['F'].tolist()
        x.append(x[-1])
        y = subset['num_particles'].tolist()

        y.append(0)
        norm = [x / y[0] for x in y]
        plt.plot(x, norm, label=f'ts={ts}', linewidth = 4,linestyle='dashed')


    plt.xlabel('Force',fontdict=fontlabel)
    plt.ylabel('% particles in skeleton',fontdict=fontlabel)
    plt.legend( loc = 'upper right',prop=fontlegend)
    plt.xticks(size = 20, family = 'serif', weight = 'normal')
    plt.yticks(size = 20, family = 'serif', weight = 'normal')
    plt.tick_params(direction = 'in',bottom = True, top= True, left= True, right= True )
    #plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(14,14))
    for ts in unique_ts[:9]:
        subset = dfA[dfA['ts'] == ts]
        #print(type(subset['F']))
        x = subset['F'].tolist()
        #x.append(x[-1])
        y = subset['num_particles'].tolist()
        #y.append(0)
        removed = [y[0] - x for x in y[:]]

        plt.plot(x, removed, label=f'ts={ts}', linewidth = 4,linestyle='dashed')


    plt.xlabel('Force',fontdict=fontlabel)
    plt.ylabel('Num. of broken bonds',fontdict=fontlabel)
    plt.legend( loc = 'best',prop=fontlegend)
    plt.xticks(size = 20, family = 'serif', weight = 'normal')
    plt.yticks(size = 20, family = 'serif', weight = 'normal')
    plt.tick_params(direction = 'in',bottom = True, top= True, left= True, right= True )
    #plt.grid(True)
    plt.tight_layout()
    plt.show()

# In[ ]:




# In[ ]:


DF_agg = groupby_ts(DF, agg='count')
F_MAX = {}
for ts in DF_agg:    
    df = DF_agg[ts]
    min_count = 0.25 * df['num_particles'].max()
    F_MAX[ts] = df[df['num_particles'] >= min_count]['F'].max()

print('F_MAX:', F_MAX)

DF_threshold = {col:[] for col in DF}
for i in range(len(DF['ts'])):
    df = DF['df'][i]
    ts = DF['ts'][i]
    f_max = F_MAX[ts]
    for col in DF: # type: ignore
        if col == 'df':
            continue
        DF_threshold[col].append(DF[col][i])
    DF_threshold['df'].append(df[df['F'] <= f_max])

plot_F_vs_num_particles(DF_threshold)
