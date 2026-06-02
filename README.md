# Intro and Objectives
This is a simple automation code for the DAQ Rigol M300 (M300 Series data acquisition and switch system).
The objective is to perform automated electrical measurements with the Rigol M300 equipment under a python code (pyvisa based). A scheduled measurement setup is implemented through scripts. Export data and plots are implemented in another script.

# How to Setup and Performa a Measurement
* Configure a script with channels settings and scheduled measurements (example is Script_Measure_Lamps_M300.py)
* Perform measurements and when data is available use a script to plot and/or export the measured data (example is Script_PlotExport_Measured_Lamps_M300.py)
