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
min_p_kw = min(P)
max_p_kw = max(P)
P = P / max_p_kw
min_p = min(P)

# Choose a load scaling s.t. our 1800 kw battery can't push out more than we need.
# Our problem stems from the fact that our battery can put out 1800 kW, but our minimum power is 17 and change.
# The simplest way to map this would be to use a battery exactly the deficit of power, but this is not realistic.
# The next simplest solution is to create an offset with a dead range the size of the difference between deficit and
# battery rating.
dead_zone_kw = kw_rated + min_p_kw
# Confirmed dead zone is our issue at ~7.4 kW.
dead_zone_pu = dead_zone_kw / max_p_kw
# The deficit is potentially a problem thanks to the scaling, We need to charge by at least the deficit when negative,
# so we have no issue when negative.  Technically the issue exists when less than 0, but it throws the numbers into the
# positive, therefore, not breaking any rules.
# The final, and probably best solution, is to go look at all positive values in the loadshape and change the scaling
# to never discharge at maximum.

load = []
for i in range(len(P)):
    if P[i] < 0:
        load.append(- P[i] / min_p)
    elif P[i] < -min_p:
        load.append(- P[i] / min_p)
    else:
        load.append(1)

# Perform the re-scaling mentioned above.
scale_factor = (- min_p_kw) / kw_rated
scale_factor -= .0019

for i in range(len(load)):
    if load[i] > 0:
        load[i] = load[i] * scale_factor

pd.DataFrame(load).to_csv('BallState/battery_load.csv', header=False, index=False)
