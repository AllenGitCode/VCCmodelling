# -*- coding: utf-8 -*-
"""
Created on Tue May  9 12:41:43 2023

@author: rebeccaa
"""

from utils.myVCCmodels import myVCCmodel
from utils.myPlots import myPhPlot, myTsPlot


if __name__ == "__main__":
    
    
    # example 1: show basic functionality
    fluid = 'R134a'
    P, H, T, S = myVCCmodel(280, 300, 5, 5, 1, fluid)
    myPhPlot(P, H, fluid)
    myTsPlot(T, S, fluid)