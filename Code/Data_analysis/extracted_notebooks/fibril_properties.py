#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import gc
import re
import pandas as pd
import matplotlib.pyplot as plt
import glob
import re  # Importa o módulo de expressões regulares
from tqdm import tqdm

cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 12)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H', 'h']

#### config dream
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


# In[8]:


Color = cmap(np.linspace(0, 1, 12))

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import glob
import re  # Importa o módulo de expressões regulares

# Caminho para a pasta que contém os arquivos, ajuste para sua necessidade
caminho_pasta = '/home/robert/Datas/Collagen_fibril_zurik_ext/*.dat'

# Lista de chaves para o dicionário principal
chaves = [2, 8, 16, 32, 64, 128, 512, 1024, 4096, 8192, 10000]
Dicts = {chave: {} for chave in chaves}

# Listar todos os arquivos .dat na pasta especificada
arquivos = glob.glob(caminho_pasta)

# Expressão regular para encontrar o valor de 'ts'
regex_ts = re.compile(r'ts_(\d+)')

# Processar cada arquivo
for file_path in tqdm(arquivos):
    # Usar a expressão regular para encontrar o valor de 'ts'
    match_ts = regex_ts.search(file_path)
    if match_ts:
        ts = int(match_ts.group(1))  # Converte o valor capturado para inteiro

        # Verificar se o valor de 'ts' está em 'chaves'
        if ts in Dicts:
            dic_for_ts = Dicts[ts]
        else:
            continue  # Se 'ts' não estiver nas chaves, pule para o próximo arquivo

        # Ler o arquivo e processar o DataFrame
        df = pd.read_csv(file_path, sep=' ')
        df.columns = ['i', 'uid', 'x', 'y', 'z']

        # Contagem por camada
        contagem_por_camada = df.groupby('y').size()
        num_part = contagem_por_camada.values
        layer = contagem_por_camada.index.tolist()

        # Atualizar o dicionário 'Dicts'
        for i, count in zip(layer, num_part):
            if i in dic_for_ts:
                dic_for_ts[i].append(count)
            else:
                dic_for_ts[i] = [count]

# Neste ponto, 'Dicts' foi atualizado com os dados de todos os arquivos


# In[5]:


Dicts_mean = {}
for ts, camadas_ts in Dicts.items():  # Usando .items() para iterar sobre pares chave-valor
    # Calculando a média de partículas para cada camada e arredondando para o inteiro mais próximo
    layers = list(camadas_ts.keys())
    num_parts_mean = [round(sum(particulas) / len(particulas), 0) for particulas in camadas_ts.values()]

    Dicts_mean[ts] = [layers, num_parts_mean]


# In[6]:


import matplotlib.pyplot as plt

# Criando um gráfico de dispersão para cada ts
plt.figure(dpi = 600)  # Define o tamanho da figura
# Iterando sobre cada valor de ts no dicionário Dicts_mean
i = 0
for ts, data in Dicts_mean.items():

        layers, num_parts_mean = data  # Desempacotando os dados
            # Determinando o passo para selecionar uma centena de camadas
        step = max(1, len(layers) // 1000)  # Garante um passo mínimo de 1

        # Selecionando um subconjunto de camadas e suas médias correspondentes
        selected_layers = layers[::step]
        selected_means = num_parts_mean[::step]
        
        x = selected_layers - min(selected_layers)*np.ones(len(selected_layers))
        y = selected_means
        plt.scatter(x, selected_means, marker = markers[i], label=f'{ts}') 
        
        with open(f'mass_lenght_{ts}.dat', 'w') as file:
            for log_x_val, log_y_val in zip(x, y):
                file.write(f'{log_x_val}\t{log_y_val}\n')

        i+=1 # Cria um gráfico de dispersão

plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.xlabel("Distance from tips(u.m)" )
plt.ylabel("Num. of particles in section" )
plt.legend()
plt.show()

# In[17]:


file = 'mass_lenght_8.dat'
dados = np.loadtxt(file)

plt.figure(dpi = 600)
# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]
plt.scatter(x,f_x, marker = markers[1], edgecolor = Color[1], color = 'white', label = f'{8}')

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_8_left.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]

plt.plot(x1,y1,'-', color = Color[1])

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_8_right.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]

plt.plot(x1,y1,'-', color = Color[1])



file = 'mass_lenght_128.dat'
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]
plt.scatter(x,f_x, marker = markers[5], edgecolor = Color[5], color = 'white', label = f'{128}')

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_128_left.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]

plt.plot(x1,y1,'-', color = Color[5])

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_128_right.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]

plt.plot(x1,y1,'-', color = Color[5])

file = 'mass_lenght_10000.dat'
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = dados[:, 0]
f_x = dados[:, 1]
plt.scatter(x,f_x, marker = markers[10], edgecolor = Color[10], color = 'white', label = f' {10000}')

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_10000_left.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]

plt.plot(x1,y1,'-', color = Color[10])

dados = np.loadtxt('/home/robert/Datas/Fit_mass_lenght/fit_mass_10000_right.dat')
x1 = dados[:, 0]
y1 = dados[:, 1]


plt.plot(x1,y1,'-', color = Color[10])


plt.legend(loc = 'best')
plt.xlabel("Distance from tips(u.m)" )
plt.ylabel("Num. of particles in section" )
plt.ylim(0,350)
plt.xlim(0,4500)
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.savefig('teste.png')

# In[21]:


from tkinter import Y

file = 'mass_lenght_2.dat'
plt.figure(dpi = 600)
plt.xlabel("Distance from tips(u.m)" )
plt.ylabel("Num. of particles in section" )
# Carregar dados
dados = np.loadtxt(file)

# Separar 'x' e 'f(x)'
x = (dados[:, 0])
y = (dados[:, 1])

ind = np.where(y == max(y))[0]
print(int(ind))
plt.scatter(x,y,marker=markers[0], label=ts)

# In[27]:


ts

# In[29]:


ts = [2,8,16,32,64,128,512,1024,4096,8192,10000]   
for i in ts:
    
    file = f"mass_lenght_{i}.dat"
    plt.figure(dpi=600)
    plt.xlabel("Distance from tips (u.m)")
    plt.ylabel("Num. of particles in section")

    # Carregar dados
    dados = np.loadtxt(file)

    # Separar 'x' e 'f(x)'
    x = dados[:, 0]
    y = dados[:, 1]

    plt.scatter(x, y, marker='o')  # Usei 'o' como marcador padrão

    # Encontrar o índice do máximo valor de 'y'
    ind = np.argmax(y)

    # Separar os dados em duas partes com base no índice do máximo valor de 'y'
    x1 = x[:ind + 1]
    y1 = y[:ind + 1]

    x2 = x[ind:]
    y2 = y[ind:]

    # Salvar os dados em dois arquivos diferentes
    fn_left = file[:-4] + "_left.dat"
    with open(fn_left, 'w') as f_left:
        for log_x_val, log_y_val in zip(x1, y1):
            f_left.write(f'{log_x_val}\t{log_y_val}\n')

    fn_right = file[:-4] + "_right.dat"
    with open(fn_right, 'w') as f_right:
        for log_x_val, log_y_val in zip(x2, y2):
            f_right.write(f'{log_x_val}\t{log_y_val}\n')

    plt.show()


# In[14]:


print(file[:-4])

# In[3]:


# Caminho para a pasta que contém os arquivos, ajuste para sua necessidade
caminho_pasta = '/home/robert/Datas/Collagen_fibril_zurik_ext/*.dat'

# Listar todos os arquivos .dat na pasta especificada
arquivos = glob.glob(caminho_pasta)

# Expressão regular para encontrar o valor de 'ts'
regex_ts = re.compile(r'ts_(\d+)')

DF = {}

# Processar cada arquivo
for file_path in tqdm(arquivos):
    # Usar a expressão regular para encontrar o valor de 'ts'
    match_ts = regex_ts.search(file_path)
    if match_ts:
        ts = int(match_ts.group(1))  # Converte o valor capturado para inteiroão estiver nas chaves, pule para o próximo arquivo

        # Ler o arquivo e processar o DataFrame
        df = pd.read_csv(file_path, sep=' ')
        df.columns = ['i', 'uid', 'x', 'y', 'z']

        if ts in DF.keys():
            DF[ts].append(df)
        else:
            DF[ts] = [df]

length = {}
for ts in sorted(DF.keys()):
    for df in DF[ts]:
        l = df['y'].max() - df['y'].min()
        
        if ts in length.keys():
            length[ts].append(l)
        else:
            length[ts] = [l]

# In[ ]:


length

# In[17]:


type(length[2])

# In[4]:


i = 0
plt.figure(dpi = 600)
ts = []
ml = []
for key, l in length.items():
    media=sum(l) / len(l) if len(l) > 0 else 0
    ts.append(key)
    ml.append(media)
    plt.plot(key,media,'s--')
    i+=1

plt.xlabel(r'$T_{s}$')

# In[ ]:


ml


# In[ ]:


L = [3668, 3695, 3764, 3808, 3891, 3928, 3913, 3912, 3892, 3892, 3917]

# In[5]:


x = np.array(ts)
y = np.array(ml)

# In[7]:


np.mean(ml[6:11])

# In[6]:


x1 = np.linspace(-150, 10150,len(x))
y1 = np.ones(len(x1))*np.mean(ml[6:11])


# In[18]:


plt.figure(dpi = 600)
plt.plot(x,y,'s-', color = 'darkred')
plt.plot(x1,y1,'--k')
plt.ylabel(r'T_{s}')

# In[14]:


y1[0]

# In[15]:


(14.07+14.14+14.06+14.16+13.95)/5

# In[10]:


plt.figure(dpi = 600)
plt.plot(x,y,'s-', color = '#006666')
plt.plot(x1,y1,'--k', label = f'{int(y1[0])}')
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.xlabel(r'$T_{s}$')
plt.ylabel(r"Length(u.m)")
plt.legend()
plt.xlim(-250,10150)
plt.ylim(3650,3950)

# In[13]:


y

# In[6]:


x = np.array(ts)
y = np.array(ml)

# In[9]:


plt.figure(dpi = 600)
plt.plot(np.log(x),(y), 's-', color = '#006666')
plt.xlabel(r'Ln $T_{s}$')
plt.ylabel(r'$L$', rotation = 0,labelpad=18)

# In[ ]:



