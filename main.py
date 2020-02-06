# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# main.py
# Spring 2020
# Central hub for openDSS controls, utilizes the base script for the project.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import win32com.client
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from building import Building
import combine_yearly


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
    for solarDat in ['maximum.csv', 'minimum.csv', 'mean.csv', 'median.csv']:
        print('Looping through buildings and adding solar...')
        for building in building_list:
            print(building.name)
            load_max = []
            load_min = []
            load_mean = []
            # Limit of loop iterations and graph domain
            limit = building.maxKW + 1
            increment = 25
            ticks = [-25]
            v = []
            p = []
            q = []
            building.set_kw(0)
            for KW in range(0, limit, increment):
                print(str(KW) + '/' + str(building.maxKW) + 'kW, ' + str(building.KW/building.maxKW * 100) + '%')
                print('compiling base file...')
                dssText.Command = 'compile [' + fName + ']'
                # dssText.Command = 'set mode=yearly'
                print('Adding solar increments and monitors to the ' + building.name + ' building.')
                dssText.Command = 'New Loadshape.PV_Shape npts=35040 minterval=15 csvfile=' + path + 'BallState\\' + \
                                  solarDat
                dssText.Command = 'New ' + building.name + ' phases=3 bus1=' + building.bus + ' kv=.48 kVA=' + \
                                  str(building.KW) + ' irradiance=1 Pmpp=' + str(building.maxKW * .8) \
                                  + ' pf=1 %cutin=.1 %cutout=.1 Yearly=PV_Shape'
                dssText.Command = 'New monitor.SubVI element=Transformer.SubXF terminal=2 mode=0'
                dssText.Command = 'New monitor.SubPQ element=Transformer.SubXF terminal=1 mode=65 PPolar=No'
                print('Solving and exporting data.')
                dssText.Command = 'solve'
                # Don't plot, just export
                # dssText.Command = 'export monitor object=SubPQ channels=(1,2)'
                # dssText.Command = 'export monitor object=SubVI channels = (1,3,5)'
                dssText.Command = 'export monitor object=SubVI'
                dssText.Command = 'export monitor object=SubPQ'
                dssText.Command = 'closedi'
                print('Importing, grooming, and collecting data.')
                raw_values = open(path+'BallState\\Ball_State_Mon_subvi_1.csv', 'r').readlines()
                v1 = []
                for i in range(1, len(raw_values)):
                    value = raw_values[i].split(',')
                    v1.append(float(value[2]))
                v.append(v1)
                raw_values = open(path + 'BallState\\Ball_State_Mon_subpq_1.csv', 'r').readlines()
                p1 = []
                q1 = []
                for i in range(1, len(raw_values)):
                    value = raw_values[i].split(',')
                    p1.append(float(value[2]))
                    q1.append(float(value[3]))
                p.append(p1)
                q.append(q1)
                ticks.append(building.KW)
                load_max.append(np.max(v1[10:]))
                load_min.append(np.min(v1[10:]))
                load_mean.append(np.mean(v1[10:]))
                building.increment_solar(increment)

            # TODO: Pull P and Q values, do the same boxplots
            print('Plotting.')
            # pickle.dump(v, open(path + '\\v' + solarDat[0:len(solarDat)-4] + '.pickle', 'wb'))
            # Plot a scatter plot of max load volts vs PV penetration in kW
            fig = plt.figure()
            # plt.scatter(range(limit), load_max, color='blue')
            # plt.scatter(range(limit), load_min, color='green')
            # plt.scatter(range(limit), load_mean, color='orange')
            plt.title('Substations voltage p.u. vs kW solar penetration (steps of 25)')
            plt.xlabel('kW penetration')
            # plt.ylabel('max voltage at substation p.u.')
            # plt.grid()
            plt.boxplot(v)
            # plt.xticks(range(0, building.maxKW/increment), ticks)
            # Plot the ansi voltage limit line
            # plt.plot(range(limit), [1.05] * limit, color='red')
            # plt.plot(range(limit), [.95] * limit, color='red')
            # plt.legend(['ansi 105% voltage limit', 'ansi 95% voltage limit',  'Voltage maximums', 'Voltage minimums',
            #             'Voltage Means'])
            plt.savefig(path + '\\output' + building.name + solarDat[0:len(solarDat)-4] + '.png')
            fig = plt.figure()
            plt.title('Substation Power vs KW solar penetration (steps of 25)')
            plt.xlabel('kW penetration')
            plt.boxplot(p)
            plt.savefig(path + '\\outputp' + building.name + solarDat[0:len(solarDat)-4] + '.png')
            fig = plt.figure()
            plt.title('Substation Imaginary Power vs KW solar penetration (steps of 25)')
            plt.xlabel('kW penetration')
            plt.boxplot(q)
            plt.savefig(path + '\\outputq' + building.name + solarDat[0:len(solarDat) - 4] + '.png')
            # plt.show()
