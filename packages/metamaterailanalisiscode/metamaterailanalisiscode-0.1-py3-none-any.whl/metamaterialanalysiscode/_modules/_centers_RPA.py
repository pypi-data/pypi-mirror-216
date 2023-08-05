"""
This is a hidden module that creates the Right Prism Auxetic cell centers.
"""

import numpy as np


def _centers_RPA(a, h, stx, dimensions) -> np.ndarray[np.ndarray[np.float16, np.float16]]:
    """
    Function that creates the cloud of the center points of the Auxetic cells that shape the Right Prism model.
    """
    ncx = int(dimensions[0]//(1.5*stx))
    ncy = int(dimensions[1]//(2*a))
    ncz = int(dimensions[2]//h)

    n = ncx*ncy*ncz
    centers = np.zeros((n, 3))

    centers[0] = np.array([stx, a, round(h/2, 4)])

    for i in range(ncx):
        for j in range(ncy):
            for k in range(ncz):
                if i == 0 and j == 0 and k == 0:
                    continue
                elif i % 2 == 0:
                    centers[i*ncy*ncz + j*ncz + k] = np.array([stx + i*1.5*stx, a + j*2*a, k*h + round(h/2, 4)])
                else:
                    centers[i*ncy*ncz + j*ncz + k] = np.array([stx + i*1.5*stx, 2*a + j*2*a, k*h + round(h/2, 4)])

    return centers
