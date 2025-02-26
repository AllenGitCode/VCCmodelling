# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:41:43 2023

@author: rebeccaa
"""

from utils.myVCCmodels import myVCCmodel
from utils.myPlots import myPhPlot, myTsPlot
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
import CoolProp


if __name__ == "__main__":
    
    
    # example 1: show basic functionality
    fluid = 'R134a'
    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'PH', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iT, num=25)
    myPlot.calc_isolines(CoolProp.iSmass, num=15)
    
    P, H, T, S = myVCCmodel(270, 300, 0, 0, 1, fluid)
    plt.plot(H, P, color='green', marker = 'o')
    
    P, H, T, S = myVCCmodel(270, 300, 5, 5, 0.6, fluid)
    plt.plot(H, P, color='red', marker = 'o')
    
    P, H, T, S = myVCCmodel(265, 325, 5, 5, 0.6, fluid)
    plt.plot(H, P, color='blue', marker = 'o')
    
    plt.xlim([200000, 500000])
    plt.ylim([100000, 10000000])
    plt.legend(['1-1','1-2','1-3'])
    
    myPlot.show()
    

    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'TS', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iP, num=25)
    # plot.calc_isolines(CoolProp.iP, iso_range=[1,50], num=10, rounding=True)

    P, H, T, S = myVCCmodel(270, 300, 0, 0, 1, fluid)
    plt.plot(S, T, color='green', marker = 'o')
    
    P, H, T, S = myVCCmodel(270, 300, 5, 5, 0.6, fluid)
    plt.plot(S, T, color='red', marker = 'o')
    
    P, H, T, S = myVCCmodel(265, 325, 5, 5, 0.6, fluid)
    plt.plot(S, T, color='blue', marker = 'o')

    plt.xlim([1050, 1850])
    plt.ylim([240, 375])
    plt.legend(['1-1','1-2','1-3'])
    
    # show plot
    myPlot.show()
    
    
    
    #myTsPlot(T, S, fluid)