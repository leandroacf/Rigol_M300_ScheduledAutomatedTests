#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perform automated electrical measurements with the Rigol M300 equipment 
(pyvisa based). 
This version covers AC voltage and thermocoupler measurements

Author: Leandro Andrade Couto Fonseca (lfonseca@cti.gov.br)
Date: 2026/03/02
Version: 0.1
comments: some parameters are hardcoded for simplicity
"""

#%% imports
import numpy as np
# %matplotlib inline
import pyvisa as pvisa

#%% class defs
class M300_MultAndSwitch:
    def __init__(self, resource_name):
        """Connect and start instrument."""
        self.rm = pvisa.ResourceManager()
        self.inst = self.rm.open_resource(resource_name)
        self.inst.timeout = 165000 
        print(f"Conected to: {self.inst.query('*IDN?')}")

    def reset(self):
        self.inst.write("*RST")

    def config_meas_Nchs_ACvolt(self,ch_list_arr=np.array(401),vrange_str='MIN',acbw_str='20'):

        lst_str = [str(num) for num in ch_list_arr]
        ch_list_str = ",".join(lst_str)
        self.inst.write(':CONF:VOLT:AC '+vrange_str+',DEF,(@'+ch_list_str+')')
        # print(':CONF:VOLT:AC '+vrange_str+',DEF,(@'+ch_list_str+')')
        self.inst.write(':ROUT:CHAN:DEL 0,(@'+ch_list_str+')')
        self.inst.write('VOLT:AC:BAND '+acbw_str+',(@'+ch_list_str+')')
        
        aux=np.zeros(len(ch_list_arr))
        for i in np.arange(5):
            self.inst.write(':ROUT:SCAN (@'+ch_list_str+')')
            result_str = self.inst.query(':READ?')
            # np.array(result_str.split(','))
            result = [float(num) for num in result_str.split(',')]
            aux=aux+result
        result = aux/5
        return np.array([ch_list_arr,result])

    def write_meas_data_ACvolt(self,result_arr,filename_csv='meas_data_ACvolt.csv'):
        np.savetxt(filename_csv, result_arr.transpose(), delimiter=',',header='Meas. Channel, AC Voltage (V)')
        
    def config_meas_Nchs_thermocouplerT(self,ch_list_arr=np.array([421,422])):
        lst_str = [str(num) for num in ch_list_arr]
        ch_list_str = ",".join(lst_str)
        self.inst.write('CONF:TEMP TC,T,1,DEF,(@'+ch_list_str+')')
        self.inst.write(':ROUT:SCAN (@'+ch_list_str+')')
        result_str = self.inst.query(':READ?')
        # np.array(result_str.split(','))
        result = [float(num) for num in result_str.split(',')]
        return np.array([ch_list_arr,result])        

    def write_meas_data_thermocouplerT(self,result_arr,filename_csv='meas_data_TcT.csv'):
        np.savetxt(filename_csv, result_arr.transpose(), delimiter=',',header='Meas. Channel, Temperature (degC)')
        
    def close(self):
        """Fecha a sessão de comunicação."""
        self.inst.close()
        self.rm.close()

# #%% run test 
# m300_control = M300_MultAndSwitch('USB0::0x1AB1::0x0C80::MM3A275100766::INSTR')

# #%% channel list for AC reading
# ch_list_gen = np.arange(401,421)
# ch_list_tc = np.arange(421,423)
# # ch_list_str

# #%% measure and check results

# x = m300_control.config_meas_Nchs_ACvolt(ch_list_arr=ch_list_gen)
# m300_control.write_meas_data_ACvolt(x,)
# print(x)
# y = m300_control.config_meas_Nchs_thermocouplerT(ch_list_arr=ch_list_tc)
# m300_control.write_meas_data_thermocouplerT(y)
# print(y)

# #%% close instrument
# m300_control.close()
