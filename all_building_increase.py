# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# building_by_building.py
# Spring 2020
# Run a building by building scan that looks for voltage and overload issues for specific buildings at given levels.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import win32com.client
import pickle
import numpy as np
import matplotlib.pyplot as plt
from building import Building
import combine_yearly
import pandas

if __name__ == '__main__':

    # Open a link to the OpenDSS and start, print version to prove running.
    dssObj = win32com.client.Dispatch('OpenDSSEngine.DSS')
    dssObj.start(0)
    print(dssObj.Version)

    # Obtain link to the text command line
    dssText = dssObj.Text
    circuit = dssObj.ActiveCircuit

    # Modify below to match your pathing and filename
    path = 'C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\'
    fName = path + 'BallState\\Ball_State_Circuit.dss'

    # Load the buildings into building objects !! Needs to point to your file
    print('Loading the building solar information...')
    buildings = pickle.load(open(path + 'buildings.pickle', 'rb'))
    building_list = []
    max_kw = 0
    for building in buildings.keys():
        building_list.append(Building(int(buildings[building]['kVA_max']), buildings[building]['Name'],
                                      buildings[building]['bus1']))
        max_kw = max([max_kw, int(buildings[building]['kVA_max'])])

    # Loop by solar data csv
    for solarDat in ['maximum.csv', 'minimum.csv', 'mean.csv', 'median.csv']:
        # Loop by kW to add PV to every building
        limit = max_kw + 1
        increment = 25
        # Integer division trick to make round by increment
        max_kw = max_kw // increment * increment
        for kW in range(0, limit, increment):
            print(str(kW) + '/' + str(max_kw) + 'kW, ' + str(kW/max_kw * 100) + '%')
            print('compiling base file...')
            dssText.Command = 'compile [' + fName + ']'
            dssText.Command = 'New Loadshape.PV_Shape npts=35040 minterval=15 csvfile=' + path + 'BallState\\' + \
                              solarDat
            dssText.Command = 'New monitor.SubVI element=Transformer.SubXF terminal=2 mode=0'
            dssText.Command = 'New monitor.SubPQ element=Transformer.SubXF terminal=1 mode=65 PPolar=No'

            for building in building_list:
                print('Adding PV for: ' + building.name)
                dssText.Command = 'New ' + building.name + ' phases=3 bus1=' + building.bus + ' kv=.48 kVA=' + \
                                  str(building.KW) + ' irradiance=1 Pmpp=' + str(building.KW * .8) \
                                  + ' pf=1 %cutin=.1 %cutout=.1 Yearly=PV_Shape'
                building.increment_solar(increment)
            print('Solving and exporting data.')
            dssText.Command = 'solve'
            # Don't plot, just export
            dssText.Command = 'export monitor object=SubVI'
            dssText.Command = 'export monitor object=SubPQ'
            dssText.Command = 'closedi'
            # As of this point, we have export data at increments of <increment> kW, added to all buildings
