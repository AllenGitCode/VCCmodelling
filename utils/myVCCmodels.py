# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:28:20 2023

@author: rebeccaa
"""

from CoolProp.CoolProp import PropsSI
import numpy as np


def getMyCOP(H):
    
    # H is an array of 7-8 values
    COP = (H[4] - H[1]) / (H[1] - H[0])
    
    return COP


def getMyPR(Tevap, Tcond, fluid):
    
    P1 = PropsSI("P", "T", Tevap, "Q", 1, fluid)
    P2 = PropsSI("P", "T", Tcond, "Q", 1, fluid)
    myPR = P2 / P1
    
    return myPR

def getMyRho1(Tevap, SH, fluid):
    
    T1 = Tevap + SH
    P1 = PropsSI("P", "T", Tevap, "Q", 1, fluid)
    rho1 = PropsSI("D", "T", T1, "P", P1, fluid)
    
    return rho1


def getMyLMTD(direction,T_hot_in,T_hot_out,T_cold_in,T_cold_out):
    
    # assuming double-pipe heat exchanger
    
    if direction == 'counter':
        dT1 = T_hot_in - T_cold_out
        dT2 = T_hot_out - T_cold_in
        
    elif direction == 'parallel':
        dT1 = T_hot_in - T_cold_in;
        dT2 = T_hot_out - T_cold_out;
        
    myLMTD = ( dT1 - dT2 ) / np.log( dT1 / dT2 );
    
    return myLMTD


def myVCCmodel(Tevap, Tcond, SH, SC, n, fluid):
    
    # input checking
    if n <= 0 or n > 1:
        print('Problem:')
        print('n should be specified 0 < n =< 1.')
        print('Check calculations.')
        return 

    if SC < 0:
        print('Problem: can not specify negative value.')
        print('Check calculations.')
        return
    
    # Point *1*: inlet to compressor
    T1 = Tevap + SH
    P1 = PropsSI("P", "T", Tevap, "Q", 1, fluid)
    H1 = PropsSI("H", "P|gas", P1, "T", T1, fluid)
    S1 = PropsSI("S", "H", H1, "P", P1, fluid)

    # Point *3*: inlet to strupeventil
    T3 = Tcond - SC
    P3 = PropsSI("P", "T", Tcond, "Q", 0, fluid)
    
    # Point *2*: inlet to cond
    P2 = P3
    H2_is = PropsSI("H", "P", P2, "S", S1, fluid)
    H2 = (H2_is - H1) / n + H1
    T2 = PropsSI("T", "H", H2, "P", P2, fluid)
    S2 = PropsSI("S", "P", P2, "H", H2, fluid)
    
    # Point *3* again
    H3 = PropsSI("H", "T|liquid", T3, "P", P3, fluid)
    S3 = PropsSI("S", "H", H3, "P", P3, fluid)
    
    # Point *4*: inlet to evap
    H4 = H3
    T4 = Tevap 
    P4 = P1 
    S4 = PropsSI("S", "H", H4, "P", P4, fluid)
    
    # Fill out some other points:
    # sat. vap point between points *2* and *3*
    T23_v = Tcond
    H23_v = PropsSI("H", "P", P2, "Q", 1, fluid)
    S23_v = PropsSI("S", "P", H2, "Q", 1, fluid)
    P23_v = P2
    # sat. liquid point between points *2* and *3*
    T23_l = Tcond
    H23_l = PropsSI("H", "P", P2, "Q", 0, fluid)
    S23_l = PropsSI("S", "P", P2, "Q", 0, fluid)
    P23_l = P2
    # sat. vap point between points *4* and *1*
    T41_v = Tevap
    H41_v = PropsSI("H", "P", P1, "Q", 1, fluid)
    S41_v = PropsSI("S", "P", P1, "Q", 1, fluid)
    P41_v = P1

    # Samler variablene og returnerer:
    T = [T1, T2, T23_v, T23_l, T3, T4, T41_v, T1]
    S = [S1, S2, S23_v, S23_l, S3, S4, S41_v, S1]
    P = [P1, P2, P23_v, P23_l, P3, P4, P41_v, P1]
    H = [H1, H2, H23_v, H23_l, H3, H4, H41_v, H1]
    
    return P, H, T, S