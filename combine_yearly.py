#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# November 2019
# combine_yearly.py
# Get median values for irradiance and stretch to 15 minute values
# Using GHI to simplify our lives
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import statistics
import matplotlib.pyplot as plt
import numpy as np

dataF = ['climateData/00.csv', 'climateData/01.csv', 'climateData/02.csv', 'climateData/03.csv', 'climateData/04.csv',
         'climateData/05.csv', 'climateData/06.csv', 'climateData/07.csv', 'climateData/08.csv', 'climateData/09.csv',
         'climateData/10.csv', 'climateData/11.csv', 'climateData/12.csv', 'climateData/13.csv', 'climateData/14.csv',
         'climateData/15.csv', 'climateData/16.csv', 'climateData/17.csv', 'climateData/18.csv', 'climateData/98.csv',
         'climateData/99.csv']

# Collect GHI from the file
ghi = []
for i in range(365 * 24 * 2):
    ghi.append([])
for i in range(len(dataF)):
    year = open(dataF[i]).readlines()
    for j in range(3, len(year)):
        ghi[j-3].append(float(year[j].split(',')[7]))

# Collect medians and means
medGhi = []
meanGhi = []
maxGhi = []
minGhi = []
for value in ghi:
    medGhi.append(statistics.median(value))
    meanGhi.append(statistics.mean(value))
    maxGhi.append(np.max(value))
    minGhi.append(np.min(value))

plt.subplot(2, 5, 1)
plt.ylim([0, 1100])
plt.plot(ghi[16992:17040])
plt.title('Winter Solstice All GHI')
plt.subplot(2, 5, 2)
plt.ylim([0, 1100])
plt.plot(medGhi[16992:17040])
plt.title('Winter Solstice Median GHI')
plt.subplot(2, 5, 3)
plt.ylim([0, 1100])
plt.plot(meanGhi[16992:17040])
plt.title('Winter Solstice Mean GHI')
plt.subplot(2, 5, 4)
plt.ylim([0, 1100])
plt.plot(maxGhi[16992:17040])
plt.title('Winter Solstice Max GHI')
plt.subplot(2, 5, 5)
plt.ylim([0, 1100])
plt.plot(minGhi[16992:17040])
plt.title('Winter Solstice Min GHI')
plt.subplot(2, 5, 6)
plt.ylim([0, 1100])
plt.plot(ghi[8208:8256])
plt.title('Summer Solstice All GHI')
plt.subplot(2, 5, 7)
plt.ylim([0, 1100])
plt.plot(medGhi[8208:8256])
plt.title('Summer Solstice Median GHI')
plt.subplot(2, 5, 8)
plt.ylim([0, 1100])
plt.plot(meanGhi[8208:8256])
plt.title('Summer Solstice Mean GHI')
plt.subplot(2, 5, 9)
plt.ylim([0, 1100])
plt.plot(maxGhi[8208:8256])
plt.title('Summer Solstice Max GHI')
plt.subplot(2, 5, 10)
plt.ylim([0, 1100])
plt.plot(minGhi[8208:8256])
plt.title('Summer Solstice Min GHI')
plt.savefig('C:\\Users\\rwoodall\\PycharmProjects\\openDSSControl\\GHI.png')

# Store outputs
maximumMed = max(medGhi)
maximumMean = max(meanGhi)
maximumMax = max(maxGhi)
maximumMin = max(minGhi)

out = open('BallState\\maximum.csv', 'w')
out1 = open('BallState\\minimum.csv', 'w')
out2 = open('BallState\\median.csv', 'w')
out3 = open('BallState\\mean.csv', 'w')
for value in minGhi:
    out1.write(str(value/maximumMin) + '\n' + str(value/maximumMin) + '\n')

for value in maxGhi:
    out.write(str(value/maximumMax) + '\n' + str(value/maximumMax) + '\n')

for value in medGhi:
    out2.write(str(value/maximumMed) + '\n' + str(value/maximumMed) + '\n')

for value in meanGhi:
    out3.write(str(value/maximumMean) + '\n' + str(value/maximumMean) + '\n')

out.close()
out1.close()
out2.close()
out3.close()
