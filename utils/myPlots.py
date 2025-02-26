# -*- coding: utf-8 -*-
"""
Created on Wed May 10 08:11:24 2023

@author: rebeccaa
"""

import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
import CoolProp

def myPhPlot(P, h, fluid):
    
    # # add computed P and h data points
    # plt.plot(h, P, color='green', marker = 'o')
    
    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'PH', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iT, num=25)
    myPlot.calc_isolines(CoolProp.iSmass, num=15)
    
    # add labels
    myPlot.xlabel("Specific enthaply, [J/kg]")
    myPlot.ylabel("Pressure, [Pa]")
    
    # show plot
    myPlot.show()
    
    return myPlot



def myTsPlot(T, s, fluid):
    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'TS', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iP, num=25)
    # plot.calc_isolines(CoolProp.iP, iso_range=[1,50], num=10, rounding=True)
    
    # add computed T and s data points
    plt.plot(s, T, color='green', marker = 'o')
    
    # add labels
    myPlot.xlabel("Specific entropy, [J/kg/K]")
    myPlot.ylabel("Temperature, [K]")
    
    # show plot
    myPlot.show()
    
    return myPlot