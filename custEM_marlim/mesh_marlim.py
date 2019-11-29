# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #                          example 1                          # # # # #
# ########################################################################### #
# # # # #                    mesh generation script                   # # # # #
# ########################################################################### #

from custEM.meshgen import meshgen_utils as mu
from custEM.meshgen.meshgen_tools import BlankWorld
from custEM.misc.synthetic_definitions import flat_topo
import numpy as np

rx_p1 = mu.refine_rx(mu.line_x(start=-5e3, stop=5e3, n_segs=200), 1., 30.)
rx_p2 = mu.refine_rx(mu.line_x(start=-5e3, stop=5e3, n_segs=200), 20., 30.)

# ######################### mesh for p1 computations ######################## #


# for ff in ['Sea_Bottom-mr3d.xyz', 'Miocene-mr3d.xyz', 'Oligocene-mr3d.xyz',
#           'Blue_mark-mr3d.xyz', 'Top_of_Salt-mr3d.xyz',
#           'Base_of_salt-mr3d.xyz']:
#    bla = np.loadtxt('meshes/para/topo/' + ff)
#    bla[:, 2] *= -1.

points = np.concatenate((
    mu.line_x(-1e4, 1e4, n_segs=100, y=-3e3),
    mu.line_x(-1e4, 1e4, n_segs=100),
    mu.line_x(-1e4, 1e4, n_segs=100, y=3e3)))

dim = 1.1e4
rx = mu.refine_rx(points, 20., 30.)

# create world
M = BlankWorld(name='marlim', m_dir='./meshes',
               topo=flat_topo,
               x_dim=[-dim, dim],
               y_dim=[-dim, dim],
               z_dim=[-6e3, 6e3],
               airspace_cell_size=1e8,
               subsurface_cell_size=1e7,
               outer_area_cell_size=1e5,
               layer_cell_sizes=[1e8, 1e8, 1e8, 5e6, 1e7, 5e6, 1e8],
               centering=False,
               easting_shift=-388993.,
               northing_shift=-7518065.,
               preserve_edges=True)

# add transmitter: 1 km y-directed dipole and 10 km x-directed observation line
M.build_surface()

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(7,
                           layer_depths=[-10., -20., -30., -40., -50., -60.],
                           subsurface_topos=['Sea_Bottom-mr3d_reverted.xyz',
                                             'Miocene-mr3d_reverted.xyz',
                                             'Oligocene-mr3d_reverted.xyz',
                                             'Blue_mark-mr3d_reverted.xyz',
                                             'Top_of_Salt-mr3d_reverted.xyz',
                                             'Base_of_salt-mr3d_reverted.xyz'])


# add the dipping plate anomaly
#M.add_plate(1000., 1000., 100., [500., 100., -700.], 45., 117., cell_size=1e3)

# add the brick anomaly for which an anisotropic conductivity is set later on
#M.add_brick(start=[-1000., -300., -700.],
#            stop=[-500.0, 700.0, -200.],
#            cell_size=1e3)

M.add_paths([mu.line_x(-5., 5., z=-500., n_segs=11)])

# extend the computational domain (reduce boundary artifacts for low freqs.)
#M.there_is_always_a_bigger_world(x_fact=1e1, y_fact=1e1, z_fact=1e1)

# call TetGen
M.call_tetgen(tet_param='-pq1.6aA', export_vtk=True)
