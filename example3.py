# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:41:43 2023

@author: rebeccaa
"""


from utils.myVCCmodels import myVCCmodel, getMyPR, getMyRho1, getMyLMTD, getMyCOP
from utils.myPlots import myPhPlot, myTsPlot
from utils.myCompressorModels import myCompressor1

import numpy
import matplotlib.pyplot as plt
from CoolProp.Plots import PropertyPlot
import CoolProp


if __name__ == "__main__":
    
    
    # example 3: apply to practical problem of interest
    #  - find cycle that produces desired Qcond, and report COP & compressor speed

    
    # define Heat Pump system parameters / sizes:
    Ucond = 1000
    Acond = 2
    Uevap = 1000
    Aevap = 2
    Tocond = 40 + 273
    Ticond = 30 + 273
    Toevap = 0 + 273
    Tievap = 8 + 273
    SH = 5
    SC = 5
    fluid = 'R134a'
    Tcond_min = Tocond + 0.05 # as close as possible to the water-temp-profile, while ensuring we avoid a neg LMTD calculation
    Tcond_max = Tcond_min + 20 # or could code so we get one in which LMTDcond is 15 or 20
    Tevap_max = Toevap - 0.05 # as close as possible to the brine-temp-profile, while ensuring we avoid a neg LMTD calculation
    Tevap_min = Tevap_max - 20 # or could code so we get one in which LMTDevap is 15 or 20
    tol_cond = 0.01
    tol_evap = 0.01
    temp_step = 0.15
    
    # set a desired Qcond value:
    # (Note a check will be done to ensure it is a value that is actually
    # possible to achieve given your pre-defined Ucond, Acond, Tcond_min and
    # Tcond_max parameters.
    LMTDcond_min = getMyLMTD('counter',Tcond_min,Tcond_min,Ticond,Tocond)
    LMTDcond_max = getMyLMTD('counter',Tcond_max,Tcond_max,Ticond,Tocond)
    Qcond_min = Ucond * Acond * LMTDcond_min
    Qcond_max = Ucond * Acond * LMTDcond_max
    
    Qcond_wanted = 30 * 1000 # Watts
    
    assert Qcond_wanted < Qcond_max, "Your wanted Qcond is too large for your condenser conditions"
    assert Qcond_wanted > Qcond_min, "Your wanted Qcond is too small for your condenser conditions"    
    
    
    # initialize Tevap to its min value
    Tevap = Tevap_min
    
    # initialize Tcond to its min value
    Tcond = Tcond_min
    
    diff_ = numpy.array([])
    Qcond1_ = numpy.array([])
    Qcond_wanted_ = numpy.array([])
    convergedCOP_ = numpy.array([])
    COP_ = numpy.array([])
    count = 0
    while True:
        
        count = count + 1
        print(count)
        
        # for a current Tevap, Tcond combo, determine PR which is used to determine n_comp
        myPR = getMyPR(Tevap, Tcond, fluid)
        #myRho1 = getMyRho1(Tevap, SH, fluid)
        n_vol, n_comp = myCompressor1(myPR)
        
        # then, Tevap, Tcond, and n_comp are used to determine the cycle
        P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
        
        # but the above cycle might not fit with system size and operating conditions
        # so check:
        LMTDcond = getMyLMTD('counter',Tcond,Tcond,Ticond,Tocond)
        LMTDevap = getMyLMTD('counter',Tievap,Toevap,Tevap,Tevap)
        Qcond1 = Ucond*Acond*LMTDcond
        m_ref = Qcond1 / (H[1] - H[5]) # from m_ref we can calc Vd_rate and then comp. speed knowing Vd
        Qevap1 = Uevap*Aevap*LMTDevap
        Qevap2 = m_ref * (H[0] - H[6])
        
        COP = getMyCOP(H)
        
        # collect for later visualization
        diff = abs(Qevap1 - Qevap2)
        diff_ = numpy.append(diff_, diff)
        Qcond1_ = numpy.append(Qcond1_, Qcond1)
        Qcond_wanted_ = numpy.append(Qcond_wanted_, Qcond_wanted)
        COP_ = numpy.append(COP_, COP)
        
        if abs(Qcond1 - Qcond_wanted)/Qcond_wanted < tol_cond and abs(Qevap1 - Qevap2)/Qevap2 < tol_evap:
            # cycle found!
            # can calc COP, compressor speed
            # and exit iterative-while loop
            break
            
            # or instead of breaking, we will save results and 
            # let the search continue until max Tcond and max Tevap reached
            convergedCOP_ = numpy.append(convergedCOP_, COP)
            myPhPlot(P, H, fluid)
            myTsPlot(T, S, fluid)
            if Tcond < Tcond_max - temp_step:
                Tcond = Tcond + temp_step
            else:
                Tcond = Tcond_min
                if Tevap < Tevap_max - temp_step:
                    Tevap = Tevap + temp_step
                else:
                    # Tcond and Tevap both reached their maxs before cycle found
                    AssertionError(True), "Tcond and Tevap both reached their maxs before cycle found"
            
        else:
            # cycle does not match model nor required Qcond
            # need to update (increase) Tcond slightly and try again (which is like increasing PR)
            # but we only will increase Tcond until its pre-set limit
            # otherwise we set Tcond back down to initial and increase Tevap (but break if we hit its pre-set limit)
            if Tcond < Tcond_max - temp_step:
                Tcond = Tcond + temp_step
            else:
                Tcond = Tcond_min
                if Tevap < Tevap_max - temp_step:
                    Tevap = Tevap + temp_step
                else:
                    # Tcond and Tevap both reached their maxs before cycle found
                    AssertionError(True), "Tcond and Tevap both reached their maxs before cycle found"
                
    # once we reach this point, cycle has been found
    # calc COP, compressor speed
    myRho1 = getMyRho1(Tevap, SH, fluid)
    Vd_rate = m_ref / (myRho1 * n_vol)
    Vd = 0.5
    comp_speed = Vd / Vd_rate 
    
    # visualize convergence process
    # on x-axis:
    #   count
    # on y-axis:
    #   Qcond_wanted_
    #   Qcond1_
    #   diff_ which is abs(Qevap1 - Qevap2)    
    fig, ax = plt.subplots()
    ax.plot(Qcond_wanted_, '--', color='red', label="Capacity")
    ax.plot(Qcond1_, 'x', color='black', label="Qcond1")
    ax.plot(diff_, 'o', color='blue', label="Qevap1-Qevap2")
    plt.xlabel('iteration')
    plt.ylabel('Q, kW')
    #ax.legend(['Capacity','Qcond1','Qevap1 - Qevap2'])
    plt.legend()
    ax.plot(Qcond_wanted_, '--', color='red', label="Capacity")
    plt.show()
    
    fig, ax = plt.subplots()
    ax.plot(COP_, 'x', color='blue')
    plt.show()
    
    
    # Ph plot
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'PH', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iT, num=25)
    myPlot.calc_isolines(CoolProp.iSmass, num=15)
    
    # add computed P and h data points
    plt.plot(H, P, color='green', marker = 'o')
    
    plt.xlim([225000, 525000])
    plt.ylim([50000, 10000000])
    plt.legend(['3-1','3-2','3-3'])
    
    myPlot.show()
    
    
    # Ts plot
    # make background thermophysical property lines using library
    Fluid = 'HEOS::' + fluid
    myPlot = PropertyPlot(Fluid, 'TS', unit_system='SI', tp_limits = 'ACHP')
    myPlot.calc_isolines(CoolProp.iQ, num=11)
    myPlot.calc_isolines(CoolProp.iP, num=25)
    # plot.calc_isolines(CoolProp.iP, iso_range=[1,50], num=10, rounding=True)
    
    # add computed T and s data points
    plt.plot(S, T, color='green', marker = 'o')
    
    plt.xlim([1050, 2000])
    plt.ylim([240, 400])
    plt.legend(['3-1','3-2','3-3'])
    
    # show plot
    myPlot.show()
    
    print('case 3')
    print('P2=',P[1])
    print('P1=',P[0])
    print('PR=',myPR)
    print('ncomp=',n_comp)
    