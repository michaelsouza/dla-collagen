#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def cut_data(x, y, cut_x=2.5):
    # Find the indices where x crosses the cut value
    cut_indices = np.where(x < cut_x)[0]
    #print(cut_indices)
    
    # Check if any cut indices were found

    if len(cut_indices) > 0:
        # Get the last index where x crosses the cut value
        cut_index = cut_indices[-1] + 1
    else:
        # No cut indices were found, set cut_index to the length of x
        cut_index = len(x)
    
    # Keep only the data before the cut_index
    x = x[:cut_index]
    y = y[:cut_index]

    #print(x)
    #print(y)
    return x,y

def cut_data1(x, y, cut_x=0.8):
    # Find the indices where x crosses the cut value
    cut_indices = np.where(x > cut_x)[0]
    
    # Check if any cut indices were found
    if len(cut_indices) > 0:
        # Get the first index where x crosses the cut value
        cut_index = cut_indices[0]
    else:
        # No cut indices were found, set cut_index to the length of x
        cut_index = len(x)
    
    # Keep only the data after the cut_index
    x = x[cut_index:]
    y = y[cut_index:]

    return x, y

def analyse_data_ava(curve_data, curve_index, cut_x=2.75):
    ##read data
    file_number, x, y = curve_data[curve_index]
    #print(curve_data[curve_index])

    ## cut data
    x, y = cut_data(x, y, cut_x)
    x, y = cut_data1(x,y,1.08)

    ## linear regression
    # Reshape the data if needed
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    #print(x, y)
    # Create a linear regression model
    model = LinearRegression()

    # Fit the model to the data
    model.fit(x, y)

    # Get the coefficients (slope and intercept)
    slope = model.coef_[0][0]
    intercept = model.intercept_[0]

    # Calculate predicted y values
    y_pred = model.predict(x)

    # Calculate regression metrics
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # Return the regression results
    return slope, intercept, mse, r2, x, y, y_pred

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

# In[2]:


color=cmap(np.linspace(0, 1, 12))
color[0]

# In[20]:


x

# In[3]:


# Define the list of specific numbers
ts = [1024, 32,10000, 8192, 16, 4096, 2, 8, 128, 512, 64]
#plt.rc('axes', labelsize=35) ##tamanho do label
#plt.rc('xtick', labelsize=20) ##tamanho dos numeros nos eixos
#plt.rc('ytick', labelsize=20)
#plt.rc('legend', fontsize=14)
specific_numbers = sorted(ts)  # Sort the list in ascending order
gamma = np.loadtxt('/home/robert/Datas/gamma_ts.dat')

#### Data Cut
folder_path = '/home/robert/Datas/Ava_cut/'
# Get a list of all .dat files in the folder
dat_files = [file for file in os.listdir(folder_path) if file.endswith(".dat")]

# Create a dictionary to map specific numbers to file names
number_file_map = {}

# Iterate over each .dat file
for file_name in dat_files:
    # Extract the number from the file name using regular expressions
    number_match = re.search(r"\d+", file_name)
    if number_match:
        file_number = int(number_match.group())
    else:
        continue

    # Check if the file number is in the specific numbers list
    if file_number in specific_numbers:
        number_file_map[file_number] = file_name

i = 0


plt.figure(dpi = 600)
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[:]:
    print(file_number)
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Plot the curve
        plt.scatter(x, y, label = '%d' %gamma[i,0], marker=markers[i])
        i+=1


#### Data fit
folder_path = '/home/robert/Datas/Ava_reg/'
# Get a list of all .dat files in the folder
dat_files = [file for file in os.listdir(folder_path) if file.endswith(".dat")]

# Create a dictionary to map specific numbers to file names
number_file_map = {}

# Iterate over each .dat file
for file_name in dat_files:
    # Extract the number from the file name using regular expressions
    number_match = re.search(r"\d+", file_name)
    if number_match:
        file_number = int(number_match.group())
    else:
        continue

    # Check if the file number is in the specific numbers list
    if file_number in specific_numbers:
        number_file_map[file_number] = file_name

i = 0
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[:]:
    
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        if i ==0 or i == 10:
            # Plot the curve
            plt.plot(x, y, c = color[i])
        i+=1


#### Curva amarela
##reta vertical
# Definindo os pontos
ponto1 = (1.08, -2)
ponto2 = (1.08, -3.1)

plt.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], c = color[10], linewidth = 1.2)

##reta horizontal
# Definindo os pontos
ponto1 = (1.08, -3.1)
ponto2 = (1.49, -3.1)

plt.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], c = color[10], linewidth = 1.2)

pc = (1.08, -3.1)
plt.text(pc[0], pc[1]-0.2, r'$\gamma$ = 2.60', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))


####Curva Preta
##reta vertical
# Definindo os pontos
ponto1 = (1.5, -1.84)
ponto2 = (1.5, -2.66)

plt.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], c = color[0], linewidth = 1.2)

##reta horizontal
# Definindo os pontos
ponto1 = (1.09, -1.84)
ponto2 = (1.5, -1.84)

plt.plot([ponto1[0], ponto2[0]], [ponto1[1], ponto2[1]], c = color[0], linewidth = 1.2)

pc = (1.5, -1.84)
plt.text(pc[0], pc[1]+0.2, r'$\gamma$ = 1.94', ha='center', va='center', fontsize=10, bbox=dict(boxstyle='square,pad=0.3', fc="none", ec="none"))


# Adding labels and title
plt.xlabel('log s')
plt.ylabel('log P(s)')
#plt.grid(True)
# Criar uma legenda no canto inferior esquerdo
plt.legend()
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.show()

# In[23]:


y

# In[8]:


#### Data Cut
folder_path = '/home/robert/Datas/Lep/'
# Get a list of all .dat files in the folder
dat_files = [file for file in os.listdir(folder_path) if file.endswith(".dat")]

# Create a dictionary to map specific numbers to file names
number_file_map = {}

# Iterate over each .dat file
for file_name in dat_files:
    # Extract the number from the file name using regular expressions
    number_match = re.search(r"\d+", file_name)
    if number_match:
        file_number = int(number_match.group())
    else:
        continue

    # Check if the file number is in the specific numbers list
    if file_number in specific_numbers:
        number_file_map[file_number] = file_name

i = 0
plt.figure(dpi = 2000)
plt.rc('axes', labelsize=26) ##tamanho do label
plt.rc('xtick', labelsize=16) ##tamanho dos numeros nos eixos
plt.rc('ytick', labelsize=16)
plt.rc('legend', fontsize=13)
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[:]:
    print(file_number)
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Plot the curve
        plt.scatter(x, y, label=r'%d' %(file_number), marker=markers[i])
        i+=1

# Adding labels and title
plt.xlabel('log s')
plt.ylabel('log P(s)')

# Criar uma legenda no canto inferior esquerdo
plt.legend()
plt.tick_params(direction='in', top=True, right=True, labeltop=False, labelright=False)
plt.show()

# In[18]:


# Specify the folder path containing the .dat files
folder_path = '/home/robert/Datas/ava_sizes/'

# Define the list of specific numbers
ts = [1024, 8192, 16, 16384, 4096, 2, 8, 128, 512, 64]
specific_numbers = sorted(ts)  # Sort the list in ascending order

# Get a list of all .dat files in the folder
dat_files = [file for file in os.listdir(folder_path) if file.endswith(".dat")]
print(dat_files)

# Create a dictionary to map specific numbers to file names
number_file_map = {}

# Iterate over each .dat file
for file_name in dat_files:
    # Extract the number from the file name using regular expressions
    number_match = re.search(r"\d+", file_name)
    if number_match:
        file_number = int(number_match.group())
    else:
        continue

    # Check if the file number is in the specific numbers list
    if file_number in specific_numbers:
        number_file_map[file_number] = file_name

# Set up the plot
plt.figure(figsize=(9, 9))
plt.figure(dpi=300)
curve_index = np.linspace(0,9,10)
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
colors = plt.cm.inferno(np.linspace(0, 1, len(curve_index)))  # Esquema de cores Viridis
curve_data = []
i = 0
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[:6]:
    
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Save the data for the curve in a tuple and append to the list
        curve_data.append((file_number, x, y))

        # Plot the curve
        label = '%d' % file_number
        plt.scatter(x, y, label=label, marker=markers[i], color = colors[i])
        i+=1

# Adding labels and title
plt.xlabel('Ln(s)')
plt.ylabel(r'Ln$(P_{s})$')

# Criar uma legenda no canto inferior esquerdo
plt.legend()
plt.show()

plt.figure(figsize=(9,9))
plt.figure(dpi=300)
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[6:-1]:
    
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Save the data for the curve in a tuple and append to the list
        curve_data.append((file_number, x, y))

        # Plot the curve
        label = '%d' % file_number
        plt.scatter(x, y, label=label, marker=markers[i], color = colors[i])
        i+=1

# Adding labels and title
plt.xlabel('Ln(s)')
plt.ylabel(r'Ln$(P_{s})$')

# Criar uma legenda no canto inferior esquerdo
plt.legend()
plt.show()

# complete curve_data
curve_data = []
i = 0
# Iterate over specific numbers in ascending order
for file_number in specific_numbers[:]:
    
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Save the data for the curve in a tuple and append to the list
        curve_data.append((file_number, x, y))


# In[19]:


arquivo = '/home/robert/collagen_fibril/dla-collagen/codigo_finalizado/ava_2.txt'
dados = np.loadtxt(arquivo, delimiter=None)
s, p = np.unique(dados,return_counts=True)


# In[ ]:


arquivo = '/home/robert/data_zurik/avalanche/avalanche_ts_2.txt'
dados = np.loadtxt(arquivo, delimiter=None)
s1, p1 = np.unique(dados,return_counts=True)

# In[ ]:


np.array_equal(p,p1)

# In[ ]:


plt.figure(figsize=(10,10))
plt.figure(dpi=300)
plt.scatter(np.log10(s),np.log10(p/np.sum(p)),color = 'red', label = 'new')
plt.scatter(np.log10(s1),np.log10(p1/np.sum(p1)), color = 'black', label = 'old')
plt.legend()


# In[ ]:


np.log(p)

# In[ ]:


plt.scatter(np.log(s),np.log(p))

# In[ ]:


import matplotlib.pyplot as plt
import matplotlib as mpl

# Example data (replace this with your actual data)
curve_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
cut = [2.30, 2.34, 2.5, 2.39, 2.46, 2.55, 2.47, 2.48, 2.64, 2.43]


colors = plt.cm.inferno(np.linspace(0, 1, len(curve_index)))  # Esquema de cores Viridis
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
# Define custom dark colors for each curve
dark_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# Set custom font for legends and tick labels
#mpl.rcParams['font.family'] = 'sans-serif'  # Use a font family that you prefer
#mpl.rcParams['font.sans-serif'] = ['Arial']  # Specify the font name

plt.figure(figsize = (9,9))
plt.figure(dpi=300)
exp_crit = []
for i in curve_index[:6]:
    slope, intercept, mse, r2, x, y, y_pred = analyse_data_ava(curve_data, i, cut[i])
    file_name = curve_data[i][0]
    exp_crit.append(slope)
    # Print the regression results for each curve
    print(f"Curve {file_name} - Angular Coefficient (Slope): {slope}, Intercept: {intercept}")
    print(f"Mean Squared Error (MSE): {mse}, R-squared (R2) Score: {r2}")
    print("------------------------------------")
    # Plot the data points for each curve with the custom dark color
    plt.scatter(x, y, label=f'Ts {file_name}', marker=markers[i], color=colors[i])

    # Plot the fitted regression line for each curve with the custom dark color
    plt.plot(x, y_pred, color=colors[i])

# Adding labels and title
plt.xlabel('Ln(s)')
plt.ylabel(r'Ln$(P_{s})$')
plt.xlim(1.08,2.7)
plt.legend()




plt.figure(figsize=(9, 9))
plt.figure(dpi=300)
for i in curve_index[6:-1]:
    print(i)
    slope, intercept, mse, r2, x, y, y_pred = analyse_data_ava(curve_data, i, cut[i])
    file_name = curve_data[i][0]
    # Print the regression results for each curve
    exp_crit.append(slope)
    print(f"Curve {file_name} - Angular Coefficient (Slope): {slope}, Intercept: {intercept}")
    print(f"Mean Squared Error (MSE): {mse}, R-squared (R2) Score: {r2}")
    print("------------------------------------")
    # Plot the data points for each curve with the custom dark color
    plt.scatter(x, y, label=f'Ts {file_name}', marker=markers[i], color=colors[i])

    # Plot the fitted regression line for each curve with the custom dark color
    plt.plot(x, y_pred, color=colors[i])


# Adding labels and title
plt.xlabel(r'Ln$(s)$')
plt.ylabel(r'Ln$(P_{s})$')
plt.xlim(1.08,2.6)
plt.legend()

plt.show()


# In[ ]:


x = []
for i in range(0,10):
    #print(x)
    x.append(curve_data[i][0])

x = np.array(x[:6])

y = np.array(exp_crit[:6])
plt.figure(figsize=(9,9))
plt.figure(dpi=300)
cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.xlabel(r'$T_{s}$')
plt.ylabel(r"$\gamma$", rotation=0)


plt.plot(x,y,'o-')

# In[ ]:


x

# In[ ]:


y

# In[ ]:


x1 = np.log(x) ##ln
y1 = y

 ## linear regression
# Reshape the data if needed
x1 = x1.reshape(-1, 1)
y1 = y1.reshape(-1, 1)
#print(x, y)
# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x1, y1)

# Get the coefficients (slope and intercept)
slope = model.coef_[0][0]
intercept = model.intercept_[0]

# Calculate predicted y values
y_pred = model.predict(x1)

# Calculate regression metrics
mse = mean_squared_error(y1, y_pred)
r2 = r2_score(y1, y_pred)

# In[ ]:


plt.figure(figsize=(9,9))
plt.figure(dpi = 300)
plt.viridis()
plt.scatter(x1,y1, marker = 'o')
plt.plot(x1,y_pred)
# Adding labels and title
plt.xlabel(r'Ln$ (T_{s})$')
plt.ylabel(r'$\gamma$', rotation = 0)
#plt.xlim(-100,100)

# Adding a background color
#plt.gca().set_facecolor('#f0f0f0')


print('R2: %f ' %r2)
print('slope: %f' %slope)

# In[ ]:


x = []
for i in range(0,10):
    #print(x)
    x.append(curve_data[i][0])

x = np.array(x[:6])

y = np.array(exp_crit[:6])

# In[ ]:


x

# In[ ]:


y

# In[ ]:




# In[ ]:


plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times New Roman"
plt.figure(figsize=(9,9))
plt.plot(x,y, '-o')



# In[ ]:


x = np.log(x)
x

# In[ ]:


 ## linear regression
# Reshape the data if needed
x = x.reshape(-1, 1)
y = y.reshape(-1, 1)
#print(x, y)
# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x, y)

# Get the coefficients (slope and intercept)
slope = model.coef_[0][0]
intercept = model.intercept_[0]

# Calculate predicted y values
y_pred = model.predict(x)

# Calculate regression metrics
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

# In[ ]:


plt.figure(figsize=(10,10))
plt.viridis()
plt.scatter(x,y, marker = 's', s = 80, color = colors[1])
plt.plot(x,y_pred, color = colors[1], linewidth = 4)
# Adding labels and title
plt.xlabel(r'$log (T_{s})$', fontsize=25)
plt.ylabel(r'$\gamma$', fontsize=25)

# Adding a background color
#plt.gca().set_facecolor('#f0f0f0')

# Customize tick labels
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
print('R2: %f ' %r2)
print('slope: %f' %slope)

# In[ ]:


import matplotlib.pyplot as plt
plt.style.use('style.mplstyle')

# In[ ]:


plt.figure(figsize = (8,8))
cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.xlabel(r'$log(s)$')
plt.ylabel(r"$log (P_{s})$")


for i in curve_index[:6]:
    slope, intercept, mse, r2, x, y, y_pred = analyse_data_ava(curve_data, i, cut[i])
    file_name = curve_data[i][0]
    exp_crit.append(slope)
    # Plot the data points for each curve with the custom dark color
    plt.scatter(x, y, label=f'Ts {file_name}', marker= markers[i])

    # Plot the fitted regression line for each curve with the custom dark color
    plt.plot(x, y_pred)


plt.legend()
plt.savefig('avalanche_ts_6_fit.png')

# In[ ]:


cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.ylabel(r'$P_{s}$')
plt.xlabel(r"$s$")
# Iterate over speci                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       fic numbers in ascending order
i = 0
for file_number in specific_numbers[:6]:
    
    if file_number in number_file_map:
        file_name = number_file_map[file_number]
        file_path = os.path.join(folder_path, file_name)
        data = np.loadtxt(file_path)

        # Separate the columns
        x = data[:, 0]
        y = data[:, 1]

        # Save the data for the curve in a tuple and append to the list
        curve_data.append((file_number, x, y))

        # Plot the curve
        label = '%d' % file_number
        plt.scatter(x, y, label=label, marker=markers[i])
        i+=1
plt.legend()
plt.savefig('avalanche_ts_6.png')

# In[ ]:


x = []
for i in range(0,10):
    #print(x)
    x.append(curve_data[i][0])

x = np.array(x[:6])

y = np.array(exp_crit[:6])

cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.xlabel(r'$T_{s}$')
plt.ylabel(r"$\gamma$")

plt.plot(x,y, marker = markers[1], color = colors[2])
plt.savefig('gamma_ts.png')

# In[ ]:


x

# In[ ]:


x1 = np.log(x)

# In[ ]:


x1

# In[ ]:


cmap = plt.get_cmap('inferno')
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=cmap(np.linspace(0, 1, 10)))
markers = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '+', 'H']
plt.xlabel(r'$ln(T_{s})$')
plt.ylabel(r"$\gamma$")

## linear regression
# Reshape the data if needed
x1 = x1.reshape(-1, 1)
y = y.reshape(-1, 1)
#print(x, y)
# Create a linear regression model
model = LinearRegression()

# Fit the model to the data
model.fit(x1, y)

# Get the coefficients (slope and intercept)
slope = model.coef_[0][0]
intercept = model.intercept_[0]

# Calculate predicted y values
y_pred = model.predict(x1)

# Calculate regression metrics
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

plt.scatter(x1,y, marker = markers[1], color = colors[2])
plt.plot(x1,y_pred, color = colors[2])
print('R2: %f ' %r2)
print('slope: %f' %slope)

plt.savefig('reg_gamma_ts.png')

# In[ ]:


%pip install mpmath



# In[ ]:


import powerlaw
import numpy as np 
data = np.linspace(0,100,100)
results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')
