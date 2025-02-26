# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:41:43 2023

@author: rebeccaa
"""


from utils.myVCCmodels import myVCCmodel, getMyPR
from utils.myPlots import myPhPlot, myTsPlot
from utils.myCompressorModels import myCompressor1
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
import CoolProp


if __name__ == "__main__":
    
    
    # example 2: show how to include compressor data
    fluid = 'R134a'
    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'PH', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iT, num=25)
    myPlot.calc_isolines(CoolProp.iSmass, num=15)
    
    
    Tevap = 270
    Tcond = 300
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 0, 0, n_comp, fluid)
    plt.plot(H, P, color='green', marker = 'o')
    print('2-1')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    Tevap = 270
    Tcond = 300
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
    plt.plot(H, P, color='red', marker = 'o')
    print('2-2')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    Tevap = 265
    Tcond = 325
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
    plt.plot(H, P, color='blue', marker = 'o')
    print('2-3')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    plt.xlim([200000, 500000])
    plt.ylim([100000, 10000000])
    plt.legend(['2-1','2-2','2-3'])
    
    myPlot.show()
    
    
    #myPhPlot(P, H, fluid)
    #myTsPlot(T, S, fluid)
    
    
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'TS', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iP, num=25)
    # plot.calc_isolines(CoolProp.iP, iso_range=[1,50], num=10, rounding=True)
    
    
    Tevap = 270
    Tcond = 300
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 0, 0, n_comp, fluid)
    plt.plot(S, T, color='green', marker = 'o')
    print('2-1')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    Tevap = 270
    Tcond = 300
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
    plt.plot(S, T, color='red', marker = 'o')
    print('2-2')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    Tevap = 265
    Tcond = 325
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
    plt.plot(S, T, color='blue', marker = 'o')
    print('2-3')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    
    plt.xlim([1050, 1850])
    plt.ylim([240, 375])
    plt.legend(['2-1','2-2','2-3'])
    
    # show plot
    myPlot.show()
