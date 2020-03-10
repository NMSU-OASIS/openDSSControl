# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# March 6, 2020
# panel_angles.py
# Plot a side view of the aerocompact panels.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import matplotlib.pyplot as plt
import math
import numpy as np

x_start = -math.cos(math.radians(15))
x_end = math.cos(math.radians(15))
y_peak = math.sin(math.radians(15))

plt.plot([x_start, 0], [0, y_peak])
plt.plot([0, x_end], [y_peak, 0])
plt.axis([-1, 1, -1, 1])

plt.show()
