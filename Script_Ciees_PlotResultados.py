#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:38:27 2026

@author: lfonseca

Plot measurement results obtained with Script_Ciees_MedeLampadas.py

Configure measurement parameters prior to use

"""

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from os import listdir
import pandas as pd
plt.close('all')


#%% parametros para os plots
working_dir_data = '10LampMeasure_ValidateAutomation'
ls_plot_days = ['2026_05_28','2026_05_29','2026_05_30','2026_05_31',\
                  '2026_06_01','2026_06_02']

# map_timing = {0: "00:30",1: "03:30",2: "06:30",3: "09:30",4: "12:30",\
#               5: "15:30",6: "18:30",7: "21:30"}
map_timing = {0: "02:35",1: "04:35",2: "08:35",3: "10:35",4: "12:35",\
              5: "14:35",6: "16:35",7: "18:35",8: "20:35",9: "22:35"}
Ch_ThermoCoup = np.array([421,422])
Ch_CurrentSensor = np.array([401, 402, 403, 404, 405, 406, 407, 408,\
                                409, 410])
# Ch_CurrentSensor = np.array([401, 402, 403, 404, 405, 406, 407, 408,\
#                                 409, 410, 411, 412, 413, 414, 415, 416,\
#                                 417, 418, 419, 420])    

CurrentSensor_CalFactor = np.array([0.335,0.335, 0.335, 0.331, 0.335, 0.334,\
                                   0.329, 0.331, 0.334, 0.330])
# CurrentSensor_CalFactor = np.array([0.335,0.335, 0.335, 0.331, 0.335, 0.334,\
#                                    0.329, 0.331, 0.334, 0.330, 0.332, 0.331,\
#                                    0.329 ,0.330 ,0.329 ,0.334, 0.331, 0.333,\
#                                    0.334, 0.331])

#%% definicoes funcoes
def plot_m300measdata_TcT_Nchannels(\
    listdir_days = ls_plot_days,\
    Nchannels = Ch_ThermoCoup,\
    number_map = map_timing,\
    working_dir = working_dir_data,\
    outputfig_name = 'Plot_TermoPar.png'):
    
    # ls_plot_days = [working_dir_data+'//' + item for item in ls_plot_days_base]
    
    res = []
    for i in listdir_days:
        # Iterate directory
        print(working_dir+'//'+i)
        for file in listdir(working_dir+'//'+i):
            # check only text files
            if np.logical_and(file.endswith('.csv'),'meas_data_TcT' in file):
                res.append(i+'/'+file)
    res.sort()

    xlabel_ls = []
    ydata_ls = []
    for i in res:
        xlabel_ls.append(i[0:10].replace('_','/')+'\n'+number_map[int(i[-5])])
        dataread = np.genfromtxt(working_dir+'//'+i, delimiter=',',skip_header=1)
        ydata_arr=dataread[::,1]
        ydata_ls.append(ydata_arr)
    d2plot = np.array(ydata_ls)
    
    fig, ax = plt.subplots(figsize=(7,4))
    xticks_ax = np.arange(0,len(xlabel_ls))
    Ch_ls=[]
    for i in np.arange(len(Nchannels)):

        ax.plot(xticks_ax, d2plot[::,i], marker='o',\
                label='Ch '+str(Nchannels[i]), linewidth=2)
        Ch_ls.append('Ch. '+str(Nchannels[i])+' (deg C)')

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

    date_hour_ls = []
    for i in np.arange(len(xlabel_ls)):
        date_hour_ls.append(xlabel_ls[i].replace('\n',' '))
    
    data_temp=pd.DataFrame(d2plot,columns=Ch_ls,index=date_hour_ls)
        
    return data_temp

def plot_m300measdata_ACvolt_Nchannels(\
    listdir_days = ls_plot_days,\
    Nchannels = Ch_CurrentSensor,\
    number_map = map_timing,\
    working_dir = working_dir_data,\
    #,np.array([0.333,0.333]),\
    calibration_sensor_arr=CurrentSensor_CalFactor,\
    outputfig_name = 'Plot_ACvoltage.png'):

    res = []
    for i in listdir_days:
        # Iterate directory
        for file in listdir(working_dir+'//'+i):
            # check only text files
            if np.logical_and(file.endswith('.csv'),'meas_data_ACvolt' in file):
                res.append(i+'/'+file)
    res.sort()

    xlabel_ls = []
    ydata_ls = []
    for i in res:
        xlabel_ls.append(i[0:10].replace('_','/')+'\n'+number_map[int(i[-5])])
        dataread = np.genfromtxt(working_dir+'//'+i, delimiter=',',skip_header=1)
        idxs_inpch = np.where(np.isin(dataread[::,0], Nchannels))[0]
        ydata_arr=dataread[idxs_inpch,1]
        ydata_ls.append(ydata_arr)
    d2plot = np.array(ydata_ls)
    
    # print(ydata_arr)
    fig, ax = plt.subplots(1,2,figsize=(10,5))
    xticks_ax = np.arange(0,len(xlabel_ls))
    idx_ax = 0    
    
    Ch_ls = []
    Ch_ls_curr = []
    # Ch_ls.append('Label')
    for i in np.arange(len(Nchannels)):

        ax[idx_ax].plot(xticks_ax, d2plot[::,i]/1e-3, marker='o',\
                label='Ch. '+str(Nchannels[i]), linewidth=2)
        Ch_ls.append('Ch. '+str(Nchannels[i])+' (V)')
        Ch_ls_curr.append('Ch. '+str(Nchannels[i])+' (mA)')
        
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

    d2plot_curr = np.zeros(np.shape(d2plot))
    for i in np.arange(len(Nchannels)):

        ax[idx_ax].plot(xticks_ax, (d2plot[::,i]/calibration_sensor_arr[i])/1e-3, marker='o',\
                label='Ch. '+str(Nchannels[i]), linewidth=2)
        d2plot_curr[::,i]=(d2plot[::,i]/calibration_sensor_arr[i])/1e-3
        
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
        
    date_hour_ls = []
    for i in np.arange(len(xlabel_ls)):
        date_hour_ls.append(xlabel_ls[i].replace('\n',' '))
    
    data_V=pd.DataFrame(d2plot,columns=Ch_ls,index=date_hour_ls)
    # data_full_AC.to_csv("MeasData_Voltage.csv")
    data_mA=pd.DataFrame(d2plot_curr,columns=Ch_ls_curr,index=date_hour_ls)
    # dd2.to_csv("MeasData_Current_Estimated.csv")


    return data_V,data_mA

def export_meas2csv(data_V,df_mA,data_temp):

    data_concat_v=pd.concat([data_V,data_temp], axis=1)
    data_concat_v.to_csv("MeasData_Voltage_Temperature.csv")
    data_concat_ma=pd.concat([data_mA,data_temp], axis=1)
    data_concat_ma.to_csv("MeasData_EstimatedCurr_Temperature.csv")
    
    
#%% Get data and plot/export

data_temp=plot_m300measdata_TcT_Nchannels()
data_V,data_mA=plot_m300measdata_ACvolt_Nchannels()
export_meas2csv(data_V,data_mA,data_temp)
