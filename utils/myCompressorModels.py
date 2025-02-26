# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:05:36 2023

@author: rebeccaa
"""


def myCompressor1(PR):
    
    # compressor specs given in:
    # Ouadha et al., 2008
    # (https://doi.org/10.1504/IJEX.2008.019115)
    
    # input checking
    if PR < 1.5:
        print('Problem: this compressor model is not')
        print('defined for your specificed PR.')
        return

    n_vol = 1.95125 - 0.80946*PR + 0.17054*PR**2 - 0.01221*PR**3;
    n_comp = 0.66768 + 0.0025*PR - 0.00303*PR**2
    
    return n_vol, n_comp