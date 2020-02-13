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
        increment = 200
        # Integer division trick to make round by increment
        max_kw = max_kw // increment * increment
        overvoltage = []
        undervoltage = []
        overload = []
        steps = 0
        for kW in range(0, limit, increment):
            print(str(kW) + '/' + str(max_kw) + 'kW, ' + str(kW/max_kw * 100) + '%')
            print('compiling base file...')
            dssText.Command = 'compile [' + fName + ']'
            dssText.Command = 'New Loadshape.PV_Shape npts=35040 minterval=15 csvfile=' + path + 'BallState\\' + \
                              solarDat
            # dssText.Command = 'New monitor.SubVI element=Transformer.SubXF terminal=2 mode=0'
            # dssText.Command = 'New monitor.SubPQ element=Transformer.SubXF terminal=1 mode=65 PPolar=No'

            for building in building_list:
                print('Adding PV for: ' + building.name)
                dssText.Command = 'New ' + building.name + ' phases=3 bus1=' + building.bus + ' kv=.48 kVA=' + \
                                  str(building.KW) + ' irradiance=1 Pmpp=' + str(building.KW * .8) \
                                  + ' pf=1 %cutin=.1 %cutout=.1 Yearly=PV_Shape'
                if building.maxKW > building.KW + increment:
                    building.increment_solar(increment)
            print('Solving and exporting data.')
            dssText.Command = 'solve'
            # Don't plot, just export
            # dssText.Command = 'export monitor object=SubVI'
            # dssText.Command = 'export monitor object=SubPQ'
            dssText.Command = 'closedi'
            steps += 1
            # As of this point, we have export data at increments of <increment> kW, added to all buildings
            # Want to see: Overloads, Overvolts, Undervolts, Amount of power exported in a year, voltage min max and
            # mean
            volt_except = pandas.read_csv(path + 'BallState\\Ball_State\\DI_yr_1\\DI_VoltExceptions_1.CSV')
            overvoltage.append(volt_except[' "Overvoltage"'].sum())
            undervoltage.append(volt_except[' "Undervoltages"'].sum())
            overloads = pandas.read_csv(path + 'BallState\\Ball_State\\DI_yr_1\\DI_Overloads_1.CSV')
            ol_count = overloads[' "Element"'].loc[overloads[' "Element"'] != ' "Line.L9"'].count()
            overload.append(ol_count)
            if ol_count > 0:
                break
        plt.figure()
        plt.scatter(range(0, steps * increment, increment), overvoltage)
        plt.grid()
        plt.title('Count of overvolts at each 25 kW step of solar (all buildings).')
        plt.ylabel('Overvolt count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Over_volts_all' +
                    solarDat[0:len(solarDat) - 4] + '.png')
        plt.figure()
        plt.scatter(range(0, steps * increment, increment), undervoltage)
        plt.grid()
        plt.title('Count of undervolts at each 25 kW step of solar (all buildings).')
        plt.ylabel('Undervolt count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Under_volts_all' +
                    solarDat[0:len(solarDat) - 4] + '.png')
        plt.figure()
        plt.scatter(range(0, steps * increment, increment), overload)
        plt.grid()
        plt.title('Count of overloads at each 25 kW step of solar (all buildings).\nExcludes Line.L9')
        plt.ylabel('Overload count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Overloads_' +
                    solarDat[0:len(solarDat) - 4] + '.png')
