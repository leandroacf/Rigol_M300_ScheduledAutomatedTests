#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:16:49 2026

@author: lfonseca

Perform scheduled measurements with the M300 Automation class.

"""

import schedule
import time
from M300_Automation import M300_MultAndSwitch
from datetime import datetime
from pathlib import Path

import numpy as np
# import matplotlib.pyplot as plt
# # %matplotlib inline



def my_task(label=0):
    print("Efetua Leitura e Salva Medidas em Subdiretorio...")

    timestamp = datetime.now().strftime("%Y_%m_%d")
    folder_path = Path(f"./{timestamp}")
    folder_path.mkdir(parents=True, exist_ok=True)

    # rm.list_resources()
    m300_control = M300_MultAndSwitch('USB0::0x1AB1::0x0C80::MM3A275100766::INSTR')

    ch_list_gen = np.arange(401,421)
    ch_list_tc = np.arange(421,423)

    x = m300_control.config_meas_Nchs_ACvolt(ch_list_arr=ch_list_gen)
    m300_control.write_meas_data_ACvolt(x,filename_csv=timestamp+'/meas_data_ACvolt_M'+str(label)+'.csv')
    # print(x)
    y = m300_control.config_meas_Nchs_thermocouplerT(ch_list_arr=ch_list_tc)
    m300_control.write_meas_data_thermocouplerT(y,filename_csv=timestamp+'/meas_data_TcT_M'+str(label)+'.csv')
    # print(y)

    m300_control.close()    

# Agenda de Medições
schedule.every().day.at("00:30").do(my_task,label=0)
schedule.every().day.at("03:30").do(my_task,label=1)
schedule.every().day.at("06:30").do(my_task,label=2)
schedule.every().day.at("09:30").do(my_task,label=3)
schedule.every().day.at("12:30").do(my_task,label=4)
schedule.every().day.at("15:30").do(my_task,label=5)
schedule.every().day.at("18:30").do(my_task,label=6)
schedule.every().day.at("21:30").do(my_task,label=7)

# schedule.every().day.at("15:34").do(my_task,label=0)
# schedule.every().day.at("15:36").do(my_task,label=1)
# schedule.every().day.at("15:38").do(my_task,label=2)
# schedule.every().day.at("10:35").do(my_task,label=3)
# schedule.every().day.at("12:35").do(my_task,label=4)
# schedule.every().day.at("14:35").do(my_task,label=5)
# schedule.every().day.at("16:35").do(my_task,label=6)
# schedule.every().day.at("18:35").do(my_task,label=7)
# schedule.every().day.at("20:35").do(my_task,label=8)
# schedule.every().day.at("22:35").do(my_task,label=9)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60) # Check every minute
