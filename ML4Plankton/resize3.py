# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:27:52 2016
@author: eric
"""

import numpy as np
from PIL import Image
import sys


def aspect_resize(im, expect_dim):
    """
    image == input array
    ii == desired dimensions
    """
    print(im)
    ime = np.array(im)
    print(ime.shape)
    mm = [int(np.median(ime[0, :, :])), int(np.median(ime[1, :, :])), int(np.median(ime[2, :, 0]))]
    cen = np.floor(np.array((expect_dim, expect_dim)) / 2.0).astype('int')
    dim = ime.shape[0:2]
    if dim[0] > dim[1]:
        # get the largest dimension
        large_dim = max(dim)

        # ratio between the large dimension and required dimension
        rat = float(expect_dim) / large_dim

        # get the smaller dimension that maintains the aspect ratio
        small_dim = int(min(dim) * rat)

        # get the indices of the large and small dimensions
        large_ind = dim.index(max(dim))
        small_ind = dim.index(min(dim))
        dim = list(dim)

        # the dimension assignment may seem weird cause of how python indexes images
        dim[small_ind] = expect_dim
        dim[large_ind] = small_dim
        dim = tuple(dim)

        im = im.resize((expect_dim, small_dim))

        pad_up=(expect_dim-small_dim)/2

        if int(pad_up)==pad_up:
            pad_down=pad_up

        else:
            pad_up=pad_up+0.5
            pad_down=expect_dim-small_dim-pad_up

        ime=np.array(im)
        up=np.zeros((pad_up, expect_dim, 3), dtype='uint8')
        down=np.zeros((pad_down, expect_dim, 3), dtype='uint8')

        res=np.row_stack((up,ime))
        res_o=np.row_stack((res, down))

    elif dim[0] < dim[1]:
        # get the largest dimension
        large_dim = max(dim)

        # ratio between the large dimension and required dimension
        rat = float(expect_dim) / large_dim

        # get the smaller dimension that maintains the aspect ratio
        small_dim = int(min(dim) * rat)

        # get the indices of the large and small dimensions
        large_ind = dim.index(max(dim))
        small_ind = dim.index(min(dim))
        dim = list(dim)

        im=im.rotate(90)
        im=im.resize((expect_dim, small_dim))

        pad_up = (expect_dim - small_dim) / 2

        if int(pad_up) == pad_up:
            pad_down = pad_up

        else:
            pad_up = pad_up + 0.5
            pad_down = expect_dim - small_dim - pad_up

        ime = np.array(im)
        up = np.zeros((pad_up, expect_dim, 3), dtype='uint8')
        down = np.zeros((pad_down, expect_dim, 3), dtype='uint8')

        res = np.row_stack((up, ime))
        res_o = np.row_stack((res, down))


    else:
        res = im.resize((expect_dim, expect_dim))
        res_o = np.array(res)

    sz = res_o.shape
    print(sz)
    return res_o
