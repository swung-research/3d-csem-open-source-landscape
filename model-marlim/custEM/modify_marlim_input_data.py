# -*- coding: utf-8 -*-
"""
This script can be used to modify the input data provided by
Correa and Menezes (2018):
    "Marlim R3D: A realistic model for controlled-source electromagnetic
    simulations — Phase 2: The controlled-source electromagnetic data set"

The required input data can be downloaded from:

    https://zenodo.org/record/400233
    
For the custEM simulations, you need the following files placed in the 
directory 'model-marlim/DATA'  # (or ../DATA):

    Sea_Bottom-mr3d.xyz
    Miocene-mr3d.xyz
    Oligocene-mr3d.xyz
    Blue_mark-mr3d.xyz
    Top_of_Salt-mr3d.xyz
    Base_of_salt-mr3d.xyz
    
    Horizontal_resistivity.sgy
    Vertical_Resistivity.sgy
    EW_nonoise.zip  # extract zip file!

For any questions or issues, contact

    raphael.rochlitz@leibniz-liag.de

"""

# install missing packages via pip or conda !

import segyio
import discretize
import numpy as np
import xarray as xr

import os

if os.path.isfile('../marlim_survey.nc'):
    pass
else:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import loadmarlim
    os.chdir('../')
    loadmarlim.create_survey()
    os.chdir('./custEM')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # #              First part - Rx & Tx coordinates               # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# %% load original survey information

data = xr.load_dataset('../marlim_survey.nc', engine='h5netcdf')

# defined shifting from real coordinates to local coordinates
easting_shift = -390275.0
northing_shift = -7518065.

rx = np.array([data.rec_x, data.rec_y, data.rec_z])
rx[0] += easting_shift
rx[1] += northing_shift

tx_il = np.zeros((len(data.src_x[::2]), 3))
tx_bs = np.zeros((len(data.src_x[::2]), 3))

tx_il[:, 0] = data.src_x[::2] + easting_shift
tx_il[:, 1] = np.ones(data.src_x[::2].size) * data.data_il.attrs['src_y'] +\
              northing_shift
tx_il[:, 2] = data.data_il.attrs['src_z']

tx_bs[:, 0] = data.src_x[::2] + easting_shift
tx_bs[:, 1] = np.ones(data.src_x[::2].size) * data.data_bs.attrs['src_y'] +\
              northing_shift    
tx_bs[:, 2] = data.data_bs.attrs['src_z']
    
if not os.path.exists('data'):
    os.makedirs('data')

np.savetxt('data/tx_inline_shifted.xyz', tx_il)
np.savetxt('data/tx_broadside_shifted.xyz', tx_bs)
np.savetxt('data/rx_shifted.xyz', rx)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # #             Second part - restivitiy information            # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# %% import  original Marlim 3RD data, which can be downlaoded from

#             https://zenodo.org/record/400233

# load sgy data, which are located in the subdirectory *data* (can be changed)
try:
    res_h = segyio.tools.cube('../DATA/Horizontal_resistivity.sgy')
    res_v = segyio.tools.cube('../DATA/Vertical_Resistivity.sgy')
except FileNotFoundError:
    print("Resistivity data not found!")
    print("You have to download the data first and")
    print("place it in `model-marlim/DATA`.")
    print("You need:")
    print("    Horizontal_resistivity.sgy")
    print("    Vertical_Resistivity.sgy")
    print("    from https://doi.org/10.5281/zenodo.400233")

# %% modify original data and obtain translated coordinates of the grid

# transform to right-handed coordinate system
res_h = np.transpose(res_h[::-1, :, ::-1], (1, 0, 2))
res_v = np.transpose(res_v[::-1, :, ::-1], (1, 0, 2))

nx, ny, nz = res_h.shape   # grid dimensions
dx, dy, dz = 25, 75, 5     # grid spacing of sgy files
x0, y0 = 1e100, 1e100      # dummy values

with segyio.open('../DATA/Horizontal_resistivity.sgy') as f:
    for i in range(nx*ny):
        if f.header[i][segyio.TraceField.CDP_X] < x0:
            x0 = f.header[i][segyio.TraceField.CDP_X]
        if f.header[i][segyio.TraceField.CDP_Y] < y0:
            y0 = f.header[i][segyio.TraceField.CDP_Y]
x0, y0 = x0/10, y0/10

mesh = discretize.TensorMesh([np.ones(nx)*dx, np.ones(ny)*dy,
                              np.ones(nz)*dz], x0=[x0, y0, 'N'])

# add offsets in x- and y- direction (translation of computational domain)
easting_shift = -390275.0
northing_shift = -7518065.

x = mesh.vectorCCx + easting_shift
y = mesh.vectorCCy + northing_shift
z = mesh.vectorCCz


# %% downward z extension to -30 km

nx, ny, nz = res_h.shape
z_extension = np.array([-30000.])
# 38 and 76 are the approximately constant corresponding resistivitiy values
# at the bottom of the provided Marlim R3D data in the sgy files
dummy1a = np.ones((nx, ny, len(z_extension))) * 38.
dummy1b = np.ones((nx, ny, len(z_extension))) * 76.

res_h = np.dstack((dummy1a, res_h))
res_v = np.dstack((dummy1b, res_v))
z = np.append(z_extension, z)


# %% x extension on both sides to an extent of -30 to 30 km

nx, ny, nz = res_h.shape
x_extension1 = np.array([-30000.])
dummy1a = np.ones((len(x_extension1), ny, nz))
dummy1b = np.ones((len(x_extension1), ny, nz))
# use resistivity values from the outermost vertical slice on this side of the
# cube for a constant extension towards the new limits
for j in range(len(x_extension1)):
    dummy1a[j, :, :] = res_h[0, :, :]
    dummy1b[j, :, :] = res_v[0, :, :]

x_extension2 = np.array([30000.])
dummy2a = np.ones((len(x_extension2), ny, nz))
dummy2b = np.ones((len(x_extension2), ny, nz))
# use resistivity values from the outermost vertical slice on this side of the
# cube for a constant extension towards the new limits
for j in range(len(x_extension2)):
    dummy2a[j, :, :] = res_h[-1, :, :]
    dummy2b[j, :, :] = res_v[-1, :, :]

res_h = np.concatenate((dummy1a, res_h, dummy2a), axis=0)
res_v = np.concatenate((dummy1b, res_v, dummy2b), axis=0)
x = np.append(x_extension1, x)
x = np.append(x, x_extension2)


# %% y extension on both sides to an extent of -30 to 30 km

nx, ny, nz = res_h.shape
y_extension1 = np.array([-30000.])
dummy1a = np.ones((nx, len(y_extension1), nz))
dummy1b = np.ones((nx, len(y_extension1), nz))
# use resistivity values from the outermost vertical slice on this side of the
# cube for a constant extension towards the new limits
for j in range(len(y_extension1)):
    dummy1a[:, j, :] = res_h[:, 0, :]
    dummy1b[:, j, :] = res_v[:, 0, :]

y_extension2 = np.array([30000.])
dummy2a = np.ones((nx, len(y_extension2), nz))
dummy2b = np.ones((nx, len(y_extension2), nz))
# use resistivity values from the outermost vertical slice on this side of the
# cube for a constant extension towards the new limits
for j in range(len(y_extension2)):
    dummy2a[:, j, :] = res_h[:, -1, :]
    dummy2b[:, j, :] = res_v[:, -1, :]

res_h = np.concatenate((dummy1a, res_h, dummy2a), axis=1)
res_v = np.concatenate((dummy1b, res_v, dummy2b), axis=1)
y = np.append(y_extension1, y)
y = np.append(y, y_extension2)


# %% store data for further usage

np.save('data/res_h_extended.npy', res_h)
np.save('data/res_v_extended.npy', res_v)
np.save('data/res_grid_extended.npy', [x, y, z])
