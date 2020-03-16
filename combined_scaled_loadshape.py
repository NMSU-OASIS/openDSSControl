# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2020
# combined_scaled_loadshape.py
# Take the loadshapes, scale by size, make a total loadshape.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas as pd
import matplotlib.pyplot as plt

f_list = {'BallState/Building_1.csv': 1028,
          'BallState/Building_2.csv': 1145,
          'BallState/Building_3.csv': 1246.2,
          'BallState/Building_4.csv': 1164,
          'BallState/Building_5.csv': 1095,
          'BallState/Building_7.csv': 661,
          'BallState/Building_8.csv': 1024,
          'BallState/Building_10.csv': 1012,
          'BallState/Building_12.csv': 847,
          'BallState/Building_13.csv': 320,
          'BallState/Building_14.csv': 381,
          'BallState/Building_15.csv': 1144.7,
          'BallState/Building_16.csv': 683,
          'BallState/Building_17.csv': 259,
          'BallState/Building_18.csv': 197,
          'BallState/Building_21.csv': 336,
          'BallState/Building_23.csv': 98,
          'BallState/Building_24.csv': 54,
          'BallState/Building_25.csv': 47,
          'BallState/Building_26.csv': 0,
          'BallState/Building_27.csv': 342,
          'BallState/Building_28.csv': 176,
          'BallState/Building_30.csv': 157,
          'BallState/Lighting_1.csv': 25.7,
          'BallState/Lighting_2.csv': 18.95,
          'BallState/Lighting_3.csv': 14.57,
          'BallState/Lighting_4.csv': 14.57,
          'BallState/Lighting_5.csv': 17.6,
          'BallState/Lighting_6.csv': 29.5,
          'BallState/Lighting_7.csv': 23.32}

total = None
for key in f_list.keys():
    data = pd.read_csv(key, header=None)
    data = data * f_list[key]
    if total is None:
        total = data
    else:
        total = total + data
# print(total)

# plt.plot(total)
# plt.show()
total = total / max(total.values)
total.to_csv('combined_scaled_loadshape.csv', header=False, index=False)
