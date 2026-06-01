#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:38:27 2026

@author: lfonseca

Plot measurement results obtained with Script_Ciees_MedeLampadas.py

Configure measurement parameters in portuguese for operator usage

"""

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from os import listdir
plt.close('all')


#%% parametros para os plots
list_dias_plot = ['2026_05_28','2026_05_29','2026_05_30','2026_05_31',\
                  '2026_06_01']
mapeamento_horarios = {0: "02:35",1: "04:35",2: "08:35",3: "10:35",4: "12:35",\
              5: "14:35",6: "16:35",7: "18:35",8: "20:35",9: "22:35"}
Canais_TermoPares = np.array([421,422])
Canais_LoopCorrente = np.array([401, 402, 403, 404, 405, 406, 407, 408,\
                                409, 410])
# Canais_LoopCorrente = np.array([401, 402, 403, 404, 405, 406, 407, 408,\
#                                 409, 410, 411, 412, 413, 414, 415, 416,\
#                                 417, 418, 419, 420])    

Fator_Calibracap_Loops = np.array([0.333, 0.333, 0.333, 0.333, 0.333, 0.333,\
                                   0.333, 0.333, 0.333, 0.333])
# Fator_Calibracap_Loops = np.array([0.333, 0.333, 0.333, 0.333, 0.333, 0.333,\
#                                    0.333, 0.333, 0.333, 0.333, 0.333, 0.333,\
#                                    0.333, 0.333, 0.333, 0.333, 0.333, 0.333,\
#                                    0.333, 0.333])

#%% definicoes funcoes
def plot_m300measdata_TcT_Nchannels(\
    listdir_days = list_dias_plot,\
    Nchannels = Canais_TermoPares,\
    number_map = mapeamento_horarios,\
    outputfig_name = 'Plot_TermoPar.png'):

    res = []
    for i in listdir_days:
        # Iterate directory
        for file in listdir(i):
            # check only text files
            if np.logical_and(file.endswith('.csv'),'meas_data_TcT' in file):
                res.append(i+'/'+file)
    res.sort()

    xlabel_ls = []
    ydata_ls = []
    for i in res:
        xlabel_ls.append(i[0:10].replace('_','/')+'\n'+number_map[int(i[-5])])
        dataread = np.genfromtxt(i, delimiter=',',skip_header=1)
        ydata_arr=dataread[::,1]
        ydata_ls.append(ydata_arr)
    d2plot = np.array(ydata_ls)
    
    fig, ax = plt.subplots(figsize=(7,4))
    xticks_ax = np.arange(0,len(xlabel_ls))
    for i in np.arange(len(Nchannels)):

        ax.plot(xticks_ax, d2plot[::,i], marker='o',\
                label='Ch '+str(Nchannels[i]), linewidth=2)

    typ_fontsize=9
    ax.set_xticks(xticks_ax[0:-1:3])
    ax.set_xticklabels(xlabel_ls[0:-1:3],rotation=45)
    ax.set_xlabel('Meas. Date and Time (a.u.)',fontsize=typ_fontsize)
    ax.set_ylabel('Temperature (deg C)',fontsize=typ_fontsize)
    ax.legend(prop={'size': typ_fontsize})
    ax.grid()
    ax.tick_params(axis='both', labelsize=7)
    ax.set_title('Temperature (Thermocoupler)',fontsize=typ_fontsize)
    fig.tight_layout()
    
    # 5. Display the plot
    plt.show()
    
    fig.savefig(outputfig_name, dpi=300, bbox_inches='tight')
        

def plot_m300measdata_ACvolt_Nchannels(\
    listdir_days = list_dias_plot,\
    Nchannels = Canais_LoopCorrente,\
    number_map = mapeamento_horarios,\
    #,np.array([0.333,0.333]),\
    calibration_sensor_arr=Fator_Calibracap_Loops,\
    outputfig_name = 'Plot_ACvoltage.png'):

    res = []
    for i in listdir_days:
        # Iterate directory
        for file in listdir(i):
            # check only text files
            if np.logical_and(file.endswith('.csv'),'meas_data_ACvolt' in file):
                res.append(i+'/'+file)
    res.sort()

    xlabel_ls = []
    ydata_ls = []
    for i in res:
        xlabel_ls.append(i[0:10].replace('_','/')+'\n'+number_map[int(i[-5])])
        dataread = np.genfromtxt(i, delimiter=',',skip_header=1)
        idxs_inpch = np.where(np.isin(dataread[::,0], Nchannels))[0]
        ydata_arr=dataread[idxs_inpch,1]
        ydata_ls.append(ydata_arr)
    d2plot = np.array(ydata_ls)
    # print(ydata_arr)
    fig, ax = plt.subplots(1,2,figsize=(10,5))
    xticks_ax = np.arange(0,len(xlabel_ls))
    idx_ax = 0    

    for i in np.arange(len(Nchannels)):

        ax[idx_ax].plot(xticks_ax, d2plot[::,i]/1e-3, marker='o',\
                label='Canal '+str(Nchannels[i]), linewidth=2)
    # print(d2plot[::,i])
    typ_fontsize=9
    ax[idx_ax].set_xticks(xticks_ax[0:-1:3])
    ax[idx_ax].set_xticklabels(xlabel_ls[0:-1:3],rotation=45)
    ax[idx_ax].set_xlabel('Meas. Date and Time (a.u.)',fontsize=typ_fontsize)
    ax[idx_ax].set_ylabel('Voltage AC RMS (mV)',fontsize=typ_fontsize)
    ax[idx_ax].legend(prop={'size': typ_fontsize})
    ax[idx_ax].grid()
    ax[idx_ax].tick_params(axis='both', labelsize=7)
    ax[idx_ax].set_title('Voltage Meas.',fontsize=typ_fontsize)

    idx_ax = 1

    for i in np.arange(len(Nchannels)):

        ax[idx_ax].plot(xticks_ax, (d2plot[::,i]/calibration_sensor_arr[i])/1e-3, marker='o',\
                label='Canal '+str(Nchannels[i]), linewidth=2)
        # print(np.shape(d2plot[::,i]/1e-3))
    # print(d2plot[::,i])
    typ_fontsize=9
    ax[idx_ax].set_xticks(xticks_ax[0:-1:3])
    ax[idx_ax].set_xticklabels(xlabel_ls[0:-1:3],rotation=45)
    ax[idx_ax].set_xlabel('Meas. Date and Time (a.u.)',fontsize=typ_fontsize)
    ax[idx_ax].set_ylabel('Current AC RMS (mA)',fontsize=typ_fontsize)
    ax[idx_ax].legend(prop={'size': typ_fontsize})
    ax[idx_ax].grid()
    ax[idx_ax].tick_params(axis='both', labelsize=7)
    ax[idx_ax].set_title('Estimated Current ',fontsize=typ_fontsize)


    fig.tight_layout()
    
    # 5. Display the plot
    plt.show()
    
    fig.savefig(outputfig_name, dpi=300, bbox_inches='tight')
        

    
    
#%% o que sera realmente executado

plot_m300measdata_TcT_Nchannels()
plot_m300measdata_ACvolt_Nchannels()

