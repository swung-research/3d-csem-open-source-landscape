# -*- coding: utf-8 -*-
"""
This script can be used to build a mesh for reproducing the results presented
in Figure 4 by Correa and Menezes (2018):

    "Marlim R3D: A realistic model for controlled-source electromagnetic
    simulations — Phase 2: The controlled-source electromagnetic data set"

For any questions or issues, contact

    raphael.rochlitz@leibniz-liag.de

"""

# ########################################################################### #
# # # # #                         marlim R3D                          # # # # #
# ########################################################################### #
# # # # #                    mesh generation script                   # # # # #
# ########################################################################### #

from custEM.meshgen import meshgen_utils as mu
from custEM.meshgen.meshgen_tools import BlankWorld
from custEM.misc.synthetic_definitions import flat_topo
import numpy as np


# %% specify parameters

# revert z-values of topography data from the interface xyz-files
# in this case, these files are located in the *data* directory

for topo_file in ['Sea_Bottom-mr3d', 'Miocene-mr3d',
                  'Oligocene-mr3d', 'Blue_mark-mr3d',
                  'Top_of_Salt-mr3d', 'Base_of_salt-mr3d']:

    topo_data = np.loadtxt('../DATA/' + topo_file + '.xyz')
    topo_data[:, 2] *= -1.
    np.savetxt('data/' + topo_file + '_reverted.xyz', topo_data)

# defined shifting from real coordinates to local coordinates
easting_shift = -390275.0
northing_shift = -7518065.

# load shifted Rx and Tx coordinates (with flipped z-axis)
inline = np.loadtxt('data/tx_inline_shifted.xyz')
broadside = np.loadtxt('data/tx_broadside_shifted.xyz')
rx = np.loadtxt('data/rx_shifted.xyz')

# define inner domain dimension (extent of surface-topography files)
# define reciprocal Tx and refined reciprocal Rx positions
dim = 1.14e4
tx_rcp = np.array([[rx[0] - 5., rx[1], 0.],
                   [rx[0] + 5., rx[1], 0.]])

# shift Tx to the correct topography, as interpolated in the mesh
tx_rcp = mu.assign_topography(tx_rcp, 'data',
                              'Sea_Bottom-mr3d_reverted.xyz', z=7.,
                              centering=False,
                              easting_shift=easting_shift,
                              northing_shift=northing_shift)

# refine inline (il) and broadside (bs) reciprocal Rx locations
il_rcp = mu.refine_rx(inline, 5.)
bs_rcp = mu.refine_rx(broadside, 5.)


# %% create poly file
# create world
M = BlankWorld(name='marlim_fig4_reciprocal', m_dir='./meshes',
               topo=flat_topo,
               x_dim=[-dim, dim],
               y_dim=[-dim, dim],
               z_dim=[-dim, dim],
               boundary_mesh_cell_size=0.,
               outer_area_cell_size=1e7,
               layer_cell_sizes=[1e9, 1e9, 1e9, 1e8, 1e9, 1e9, 1e9],
               interface_cell_sizes=[1e7, 1e7, 1e6, 1e6, 1e7, 1e7],
               centering=False,
               t_dir='data',
               easting_shift=easting_shift,
               northing_shift=northing_shift,
               preserve_edges=True)

# build surface mesh
M.build_surface()

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(7,   # layer depths are dummy values if topo is used
                           layer_depths=[-1., -2., -3., -4., -5., -6.],
                           subsurface_topos=['Sea_Bottom-mr3d_reverted.xyz',
                                             'Miocene-mr3d_reverted.xyz',
                                             'Oligocene-mr3d_reverted.xyz',
                                             'Blue_mark-mr3d_reverted.xyz',
                                             'Top_of_Salt-mr3d_reverted.xyz',
                                             'Base_of_salt-mr3d_reverted.xyz'],
                           insert_struct=[tx_rcp])
# here, the small tx is also included via "insert_struct" in the sea bottom
# interface for a proper mesh generation at this interface

# add reciprocal receiver refinement edges
M.add_paths(il_rcp)
M.add_paths(bs_rcp)

# add reciprocal tx 5 m above sea_bottom ("assign_topography" before)
M.add_tx(tx_rcp)

# extend the computational domain with halfspace-like boundary mesh
M.there_is_always_a_bigger_world(1.1, 1.1, 1.1, cell_sizes=[0., 1e9])
M.there_is_always_a_bigger_world(2., 2., 2., initial=False)

# call TetGen
M.call_tetgen(tet_param='-pq2.0aA', export_vtk=True)
