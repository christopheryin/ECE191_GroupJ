# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:27:52 2016

@author: eric
"""

import numpy as np
from PIL import Image
import sys


def aspect_resize(im, ii):
    """
    image == input array
    ii == desired dimensions
    """
    print(im)
    ime = np.array(im)
    print(ime.shape)
    mm = [int(np.median(ime[0, :, :])), int(np.median(ime[1, :, :])), int(np.median(ime[2, :, 0]))]
    cen = np.floor(np.array((ii, ii))/2.0).astype('int')
    dim = ime.shape[0:2]
    if dim[0] != dim[1]:
        # get the largest dimension
        large_dim = max(dim)
        
        # ratio between the large dimension and required dimension
        rat = float(ii)/large_dim
        
        # get the smaller dimension that maintains the aspect ratio
        small_dim = int(min(dim)*rat)
        
        # get the indices of the large and small dimensions
        large_ind = dim.index(max(dim))
        small_ind = dim.index(min(dim))
        dim = list(dim)
        
        # the dimension assignment may seem weird cause of how python indexes images
        dim[small_ind] = ii
        dim[large_ind] = small_dim
        dim = tuple(dim)

        im = im.resize((ii, small_dim))
        ime = np.array(im)
        half = np.floor((ime.shape[0]/2, ime.shape[1]/2)).astype(int)
        #half = np.floor(np.array((im.shape[0,2])/2.0)).astype('int')
        
        # make an empty array, and place the new image in the middle
        res = np.zeros((ii, ii, 3), dtype='uint8')
        res[:, :, 0] = mm[0]
        res[:, :, 1] = mm[1]
        res[:, :, 2] = mm[2]

        
        if large_ind == 1:
            test = res[cen[0]-half[0]:cen[0]+half[0], cen[1]-half[1]:cen[1]+half[1]+1]
            if test.shape != ime.shape:
                res[cen[0]-half[0]:cen[0]+half[0]+1, cen[1]-half[1]:cen[1]+half[1]+1] = im
            else:
                res[cen[0]-half[0]:cen[0]+half[0], cen[1]-half[1]:cen[1]+half[1]+1] = im
        else:
            test = res[cen[0]-half[0]:cen[0]+half[0]+1, cen[1]-half[1]:cen[1]+half[1]]
            if test.shape != ime.shape:
                res[cen[0]-half[0]:cen[0]+half[0]+1, cen[1]-half[1]:cen[1]+half[1]+1] = im
            else:
                res[cen[0]-half[0]:cen[0]+half[0]+1, cen[1]-half[1]:cen[1]+half[1]] = im
    else:
        res = im.resize((ii, ii))
        res = np.array(res)
        #half = np.floor((ime.shape[0] / 2, ime.shape[1] / 2)).astype(int)


    sz = res.shape
    print(sz)
    return res




