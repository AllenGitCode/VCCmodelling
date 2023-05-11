# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:41:43 2023

@author: rebeccaa
"""


from utils.myVCCmodels import myVCCmodel, getMyPR
from utils.myPlots import myPhPlot, myTsPlot
from utils.myCompressorModels import myCompressor1



if __name__ == "__main__":
    
    
    # example 2: show how to include compressor data (n_comp(PR))
    fluid = 'R134a'
    Tevap = 280
    Tcond = 300
    myPR = getMyPR(Tevap, Tcond, fluid)
    n_vol, n_comp = myCompressor1(myPR)
    P, H, T, S = myVCCmodel(Tevap, Tcond, 5, 5, n_comp, fluid)
    myPhPlot(P, H, fluid)
    myTsPlot(T, S, fluid)
    
    # optionally could calculate compressor speed if displacement volume known
    # m_ref = rho1 * Vd_rate * n_vol