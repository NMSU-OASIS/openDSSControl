# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# penetration_graph.py
# Spring 2020
# Graph the output of all_building_increase for bus mins/maxes.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 22})

# Import all data (1.0 multiplier only for now).
primax = pandas.read_csv('E:\\Github\\openDSSControl\\BallState\\primary_maxes_1.csv')
primin = pandas.read_csv('E:\\Github\\openDSSControl\\BallState\\primary_mins_1.csv')
secmax = pandas.read_csv('E:\\Github\\openDSSControl\\BallState\\secondary_maxes_1.csv')
secmin = pandas.read_csv('E:\\Github\\openDSSControl\\BallState\\secondary_mins_1.csv')

# Plot primaries as red dots, secondaries as blue dots?
for column in primax.columns:
    if column != 'step' and column != 'total':
        plt.scatter(primax['step'], primax[column], color='red', marker='x')
        plt.scatter(primin['step'], primin[column], color='red', marker='x')
for column in secmax.columns:
    if column != 'step' and column != 'total':
        plt.scatter(secmax['step'], secmax[column], color='blue', marker='x')
        plt.scatter(secmin['step'], secmin[column], color='blue', marker='x')

plt.figure()
legend = ['Ansi upper limit', 'Ansi lower limit']
for column in primax.columns:
    if column != 'step' and column != 'total':
        plt.scatter(primax['total'], primax[column], color='red', marker='x')
        plt.scatter(primin['total'], primin[column], color='red', marker='o')
for column in secmax.columns:
    if column != 'step' and column != 'total':
        plt.scatter(secmax['total'], secmax[column], color='blue', marker='x')
        plt.scatter(secmin['total'], secmin[column], color='blue', marker='o')
plt.xlabel('Solar Penetration (kVA)')
plt.ylabel('Volts (p.u.)')
plt.title('Voltage vs. Solar Penetration (red=primary, blue=secondary)')
plt.plot(secmax['total'], [1.05] * len(secmax['total']), color='green')
plt.plot(secmax['total'], [.95] * len(secmax['total']), color='orange')
plt.legend(legend)
plt.show()
