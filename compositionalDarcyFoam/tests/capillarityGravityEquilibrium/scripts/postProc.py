# -*- coding: utf-8 -*-
'''
    PorousMedia: A Wikki Brasil project
    File name: postProc.py
    Author: Gabriel M. Magalhães (Wikki Brasil)
    Date created: 16/03/2022

    Script to post-process results of gravity-capillarity tutorial
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot(plot_dict):
    '''
        Assemble and create a graph following a standard style

        Parameters:
            plot_dict (dictionary): parameters to construct the graph
            keys:
                x_to_plot (list of lists of floats): values to plot in X-axis
                y_to_plot (list of lists of floats): values to plot in Y-axis
                symb (list of strings): symbol to use in each curve
                label (list of strings): legend to use in each curve
                xlim (list with two floats): X-axis limits [Xmin,Xmax]
                ylim (list with two floats): Y-axis limits [Ymin,Ymax]
                xlabel (str): X-axis title
                ylabel (str): Y-axis title
                figname (str): name of the generated graph


        Return:
            Save the graph with the name defined in the key 'figname'
        '''

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(1,1,1)
    ax1.clear()

    for i in range(len(plot_dict['x_to_plot'])):
        ax1.plot(plot_dict['x_to_plot'][i],plot_dict['y_to_plot'][i],plot_dict['symb'][i],color=plot_dict['color'][i],markevery=4,label=plot_dict['label'][i])

    ax1.set_xlim(plot_dict['xlim'][0],plot_dict['xlim'][1])
    ax1.set_ylim(plot_dict['ylim'][0],plot_dict['ylim'][1])

    ax1.set_xlabel(plot_dict['xlabel'])
    ax1.set_ylabel(plot_dict['ylabel'])

    ax1.legend()

    plt.savefig(plot_dict['figname'], dpi=fig.dpi, bbox_inches = 'tight')

time = '1e+07'
# File with data from simulation (y Sw)
file = f'postProcessing/sets/{time}/acrossFlow_S.water.xy'

df = pd.read_table(file,names=['y','Sw'],sep='\s',engine='python')

# File with data from impesFoam simulation (y Sw)
file = './scripts/impes.csv'

dfImpes = pd.read_table(file,names=['y','Sw'],sep=',',engine='python')

# Plot of water saturation graph
dplot1 = {
    'x_to_plot':[df.y, dfImpes.y],
    'y_to_plot':[df.Sw, dfImpes.Sw],
    'xlabel':'Distance [m]',
    'ylabel':'Water Saturation',
    'xlim':[0,1],
    'ylim':[0,1],
    'color':['r','b'],
    'label':['porousMedia', 'impesFoam'],
    'symb':['--','.'],
    'figname':'Sw.png'
}

plot(dplot1)
Sw=df.Sw.to_numpy()
# Cutting values of saturation very close of 1
df = df[(df.Sw <= 0.99)].reset_index(drop=True)
dfImpes = dfImpes[(dfImpes.Sw <= 0.99)].reset_index(drop=True)

# Analytical calculus of dS/dy
Spcirr = 0.0
Spcmax= 1.0
alpha = 0.5
pc0 = 1000

Spc = (Sw-Spcirr)/(Spcmax-Spcirr)
dpc = alpha*pc0*Spc**(-alpha-1)/(Spcmax-Spcirr)

Spce = (df.Sw-Spcirr)/(Spcmax-Spcirr)
dpce = alpha*pc0*Spce**(-alpha-1)/(Spcmax-Spcirr)

Spcei = (dfImpes.Sw-Spcirr)/(Spcmax-Spcirr)
dpcei = alpha*pc0*Spcei**(-alpha-1)/(Spcmax-Spcirr)

rho_water = 1000
rho_gas = 1.0
g = 9.81

dSdy = ((rho_water-rho_gas)*g)/dpc
dSdye = ((rho_water-rho_gas)*g)/dpce
dSdyei = ((rho_water-rho_gas)*g)/dpcei

# Numerical calculus of dS/dy
dSdy_num = -np.gradient(df.Sw,df.y)

# Numerical calculus of dS/dy
dSdy_num_impes = -np.gradient(dfImpes.Sw,dfImpes.y)

# Column in dataframe with absolute error
df['Error Coupled'] = abs(dSdye-dSdy_num)

# Column in dataframe with absolute error
df['Error Impes'] = abs(dSdyei-dSdy_num_impes)

# Plot of dS/dy graph
dplot2 = {
    'x_to_plot':[Sw, df.Sw, dfImpes.Sw],
    'y_to_plot':[dSdy, dSdy_num, dSdy_num_impes],
    'xlabel':'Water Saturation',
    'ylabel':'dS/dy [1/m]',
    'xlim':[0,1],
    'ylim':[0,20],
    'label':["Analytical", "porousMedia", "impesFoam"],
    'color':['k','r','b'],
    'symb': ['-','--','.'],
    'figname':'dSdy.png'
}

plot(dplot2)

# Writing quantitative comparison in the terminal
print(f'\n\nMean absolute error in dS/dy = {df["Error Coupled"].mean():.3f}')
print(f'Max absolute error in dS/dy = {df["Error Coupled"].max():.3f}\n\n')

# Writing quantitative comparison in the terminal
print(f'\n\nMean absolute error in dS/dy = {df["Error Impes"].mean():.3f}')
print(f'Max absolute error in dS/dy = {df["Error Impes"].max():.3f}\n\n')