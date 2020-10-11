# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #                        layered earth                        # # # # #
# ########################################################################### #
# # # # #                    mesh generation script                   # # # # #
# ########################################################################### #

from custEM.meshgen import meshgen_utils as mu
from custEM.meshgen.meshgen_tools import BlankWorld
import numpy as np


# ######################### mesh for p2 computations ######################## #

# Define refinement-paths around receiver lcoations
points = np.concatenate((
    mu.line_x(-1e4, 1e4, n_segs=100, y=-3e3),
    mu.line_x(-1e4, 1e4, n_segs=100),
    mu.line_x(-1e4, 1e4, n_segs=100, y=3e3)))
rx = mu.refine_rx(points, 25., 30.)

# create world
M = BlankWorld(name='layered_earth_p2',
               m_dir='./meshes',
               x_dim=[-1.5e4, 1.5e4],
               y_dim=[-1.4e4, 1.4e4],
               z_dim=[-5e4, 5e4],
               preserve_edges=True)

# include water surface
M.build_surface()

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(4, [-600., -850., -3150.],
                           insert_struct=rx)

# add transmitter in water layer at -550 m depth
M.add_tx(mu.line_x(-100., 100., n_segs=3, z=-550.))

# append boudary mesh
M.there_is_always_a_bigger_world(10., 10., 10.)

# call TetGen
M.call_tetgen(tet_param='-pq1.6aA', export_vtk=True)


# ######################### mesh for p1 computations ######################## #

# Define refinement-paths around receiver lcoations
points = np.concatenate((
    mu.line_x(-1e4, 1e4, n_segs=100, y=-3e3),
    mu.line_x(-1e4, 1e4, n_segs=100),
    mu.line_x(-1e4, 1e4, n_segs=100, y=3e3)))
rx = mu.refine_rx(points, 1., 30.)

# create world
M = BlankWorld(name='layered_earth_p1',
               m_dir='./meshes',
               x_dim=[-3e4, 3e4],
               y_dim=[-3e4, 3e4],
               z_dim=[-5e4, 5e4],
               preserve_edges=True)

# include water surface
M.build_surface()

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(4, [-600., -850., -3150.],
                           insert_struct=rx)

# add transmitter in water layer at -550 m depth
M.add_tx(mu.line_x(-100., 100., n_segs=10, z=-550.))

M.there_is_always_a_bigger_world(10., 10., 10.)

# call TetGen
M.call_tetgen(tet_param='-pq1.2aA', export_vtk=True)

