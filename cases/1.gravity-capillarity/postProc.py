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
        ax1.plot(plot_dict['x_to_plot'][i],plot_dict['y_to_plot'][i],plot_dict['symb'][i],label=plot_dict['label'][i])

    ax1.set_xlim(plot_dict['xlim'][0],plot_dict['xlim'][1])
    ax1.set_ylim(plot_dict['ylim'][0],plot_dict['ylim'][1])

    ax1.set_xlabel(plot_dict['xlabel'])
    ax1.set_ylabel(plot_dict['ylabel'])

    ax1.legend()

    plt.savefig(plot_dict['figname'], dpi=fig.dpi, bbox_inches = 'tight')
    plt.close()

# File with data from simulation (y Sw)
file = './postProcessing/sets/20000/acrossFlow_S.water.xy'

df = pd.read_table(file,names=['y','Sw'],sep='\s',engine='python')

# Plot of water saturation graph
dplot1 = {
    'x_to_plot':[df.y],
    'y_to_plot':[df.Sw],
    'xlabel':'Distance [m]',
    'ylabel':'Water Saturation',
    'xlim':[0,1],
    'ylim':[0,1],
    'label':['Sw'],
    'symb':['--'],
    'figname':'Sw.png'
}

plot(dplot1)

# Cutting values of saturation very close of 1
df = df[(df.Sw <= 0.999)].reset_index(drop=True)

# Analytical calculus of dS/dy
Spcirr = 0.0
Spcmax= 1.0
alpha = 0.5
pc0 = 1000

Spc = (df.Sw-Spcirr)/(Spcmax-Spcirr)
dpc = alpha*pc0*Spc**(-alpha-1)/(Spcmax-Spcirr)

rho_water = 1000
rho_gas = 1.0
g = 9.81

dSdy = ((rho_water-rho_gas)*g)/dpc

# Numerical calculus of dS/dy
dSdy_num = -np.gradient(df.Sw,df.y)

# Column in dataframe with absolute error
df['Error'] = abs(dSdy-dSdy_num)

# Plot of dS/dy graph
dplot2 = {
    'x_to_plot':[df.Sw,df.Sw],
    'y_to_plot':[dSdy_num,dSdy],
    'xlabel':'Water Saturation',
    'ylabel':'dS/dy [1/m]',
    'xlim':[0,1],
    'ylim':[0,20],
    'label':["Numerical","Analytical"],
    'symb':['.','-'],
    'figname':'dSdy.png'
}

plot(dplot2)

# Writing quantitative comparison in the terminal
print(f'\n\nMean absolute error in dS/dy = {df.Error.mean():.3f}')
print(f'Max absolute error in dS/dy = {df.Error.max():.3f}\n\n')
