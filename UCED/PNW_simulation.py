# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 11:45:39 2018

@author: jkern
"""

############################################################################
#                           UC/ED Simulation

# This file simulates power system/market operations for the CAISO and MID-C
# markets, stores the data in appropriate places and calculates wholesale
# electricity prices.
############################################################################

############################################################################
# Simulates power system operations for as many simulation days as
# specified (max is 358)
days = 358

# PACIFIC NORTHWEST
import PNW_wrapper
PNW_wrapper.sim(days)

############################################################################
#                    WHOLESALE ELECTRICITY PRICES

#import PNW_price_calculation
import PNW_emission_calculation