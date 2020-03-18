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
    for building in buildings.keys():
        building_list.append(Building(int(buildings[building]['kVA_max']), buildings[building]['Name'],
                                      buildings[building]['bus1']))

    # Loop through loading the buildings and printing the outputs
    for building in building_list:
        print(building.name)
        load_max = []
        load_min = []
        load_mean = []
        # Limit of loop iterations and graph domain
        limit = building.maxKW + 1
        start = 0
        increment = 5
        building.set_kw(0)
        overvoltage = []
        undervoltage = []
        overload = []
        steps = 0
        if start != 0:
            building.set_kw(start)
        for KW in range(start, limit, increment):
            print(str(KW) + '/' + str(building.maxKW) + 'kW, ' + str(building.KW/building.maxKW * 100) + '%')
            print('compiling base file...')
            dssText.Command = 'compile [' + fName + ']'
            print('Adding solar increments and monitors to the ' + building.name + ' building.')
            # This will now be in the opendss model as it is static.
            # dssText.Command = 'New Loadshape.PV_Shape npts=35040 minterval=15 csvfile=' + path + 'BallState\\' + \
            #                   solarDat
            dssText.Command = 'New ' + building.name + ' phases=3 bus1=' + building.bus + ' kv=.48 kVA=' + \
                              str(building.KW) + ' irradiance=1 Pmpp=' + str(building.KW * .8) \
                              + ' pf=1 %cutin=.1 %cutout=.1 Yearly=PV_Shape'
            # dssText.Command = 'New monitor.SubVI element=Transformer.SubXF terminal=2 mode=0'
            # dssText.Command = 'New monitor.SubPQ element=Transformer.SubXF terminal=1 mode=65 PPolar=No'
            print('Solving and exporting data.')
            dssText.Command = 'solve'
            # Don't plot, just export
            # dssText.Command = 'export monitor object=SubVI'
            # dssText.Command = 'export monitor object=SubPQ'
            dssText.Command = 'closedi'
            steps += 1
            print('Importing, grooming, and collecting data.')
            # For individual buildings, we're only interested in overloads and over-volts
            volt_except = pandas.read_csv(path + 'BallState\\Ball_State\\DI_yr_1\\DI_VoltExceptions_1.CSV')
            overvoltage.append(volt_except[' "Overvoltage"'].sum())
            undervoltage.append(volt_except[' "Undervoltages"'].sum())
            building.increment_solar(increment)
            overloads = pandas.read_csv(path + 'BallState\\Ball_State\\DI_yr_1\\DI_Overloads_1.CSV')
            ol_count = overloads[' "Element"'].loc[overloads[' "Element"'] != ' "Line.L9"'].count()
            overload.append(ol_count)
            if ol_count > 0:
                break
        plt.figure()
        plt.scatter(range(start, start + steps * increment, increment), overvoltage)
        plt.grid()
        plt.title('Count of overvolts at each 25 kW step of solar (' + building.name + ').')
        plt.ylabel('Overvolt count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Over_volts_' + building.name +
                    solarDat[0:len(solarDat) - 4] + '.png')
        plt.close()
        plt.figure()
        plt.scatter(range(start, start + steps * increment, increment), undervoltage)
        plt.grid()
        plt.title('Count of undervolts at each 25 kW step of solar (' + building.name + ').')
        plt.ylabel('Undervolt count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Under_volts_' + building.name +
                    solarDat[0:len(solarDat) - 4] + '.png')
        plt.close()
        plt.figure()
        plt.scatter(range(start, start + steps * increment, increment), overload)
        plt.grid()
        plt.title('Count of overloads at each 25 kW step of solar (' + building.name + ').\nExcludes Line.L9')
        plt.ylabel('Overload count')
        plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\Overloads_' + building.name +
                    solarDat[0:len(solarDat) - 4] + '.png')
        plt.close()
