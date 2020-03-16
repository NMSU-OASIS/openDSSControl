# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 16, 2020
# load_scaler.py
# Create a battery loadshape that will perfectly compensate when the solar loadshape is added in.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~0

import pandas as pd

kw_rated = 1800
kwh = 4000

data = pd.read_csv('BallState/Ball_State_Mon_subpq_1.csv')

P = data[' P1 (kW)']
P = P / max(P)
min_p = min(P)

load = []
for i in range(len(P)):
    # if P[i] < 0:
    #     load.append(P[i] / min_p)
    if P[i] < -min_p:
        load.append(- P[i] / min_p)
    else:
        load.append(1)

pd.DataFrame(load).to_csv('battery_load.csv', header=False, index=False)
