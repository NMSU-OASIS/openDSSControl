# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 2020
# solar_loadshapes.py
# Build loadshapes from the hourly values from Aurora
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pandas as pd
import numpy as np

f_list = ['BallState/synthesized_loads/Bracken Hourly.csv',
          'BallState/synthesized_loads/Emens Auditorium Hourly.csv',
          'BallState/synthesized_loads/Emens Parking Hourly.csv',
          'BallState/synthesized_loads/Ground Mount Hourly.csv',
          'BallState/synthesized_loads/Noyer Hourly.csv',
          'BallState/synthesized_loads/Robert Bell Hourly.csv',
          'BallState/synthesized_loads/Telecommunications Hourly.csv',
          'BallState/synthesized_loads/Whittinger Hourly.csv']

for f in f_list:
    data = pd.read_csv(f)
    # kw = kwh in this case (avg over the hour)
    kw = data['Energy Production [kWh]']
    # Make a loadshape
    kw = kw / max(kw)
    # save back to a file
    kw.to_csv(f[0:f.find('.')] + '_mod.csv', header=False, index=False)
