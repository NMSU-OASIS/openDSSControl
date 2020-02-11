# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Randall Woodall
# building.py
# Spring 2020
# Represent a building, hold the maximum KW limits, the current KW, and basic information.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Building:
    # Initialize a building with a maximum KW and a name.
    def __init__(self, max_kw, name, bus):
        self.maxKW = max_kw
        self.name = name
        self.KW = 0
        self.bus = bus

    # Set KW to a specific value if known.
    def set_kw(self, kw):
        self.KW = kw

    # Increment KW by a given value.
    def increment_solar(self, increment):
        self.KW += increment
