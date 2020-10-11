# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #                          block model                        # # # # #
# ########################################################################### #
# # # # #                    mesh generation script                   # # # # #
# ########################################################################### #

from custEM.meshgen import meshgen_utils as mu
from custEM.meshgen.meshgen_tools import BlankWorld
import numpy as np

# #########################      define blocks       ######################## #

# Note, for meshing purposes, the blocks are devided into sub_blocks with
# identical sub-surfaces to simplify writing the TetGen input file

# block 1
x1 = np.tile([[-500., 0.], [0., 500.]], (4, 1))
y1 = np.repeat([[-4e3, -3e3], [-3e3, 0.], [0., 3e3], [3e3, 4e3]], 2, axis=0)
z1 = -1600.

# block 2
x2 = [[0., 500.], [500., 5000.]]
y2 = [-3000., 0.]
z2 = [-1850., -1600.]

# block 3
x3 = [[-5000., -500.], [-500., 0.]]
y3 = [0., 3000.]
z3 = [[-2900., -1850], [-1850., -1600.]]


# ######################### mesh for p2 computations ######################## #

block_cell_size = 1e7

# Define refinement-paths around receiver lcoations
points = np.concatenate((
    mu.line_x(-1e4, 1e4, n_segs=100, y=-3e3),
    mu.line_x(-1e4, 1e4, n_segs=100),
    mu.line_x(-1e4, 1e4, n_segs=100, y=3e3)))
rx = mu.refine_rx(points, 25., 30.)

# create world
M = BlankWorld(name='block_model_p2',
               m_dir='./meshes',
               x_dim=[-1.5e4, 1.5e4],
               y_dim=[-1.4e4, 1.4e4],
               z_dim=[-5e4, 5e4],
               preserve_edges=True)

# include water surface
M.build_surface()

# add Block 1 that touches the 2nd to 3rd subsurface layer interface
for i in range(len(x1)):
    marker_pos = [np.mean(x1[i]), np.mean(y1[i]), -900.]
    poly = np.array([[x1[i, 0], y1[i, 0], 0.],
                     [x1[i, 0], y1[i, 1], 0.],
                     [x1[i, 1], y1[i, 1], 0.],
                     [x1[i, 1], y1[i, 0], 0.]])
    M.add_intersecting_anomaly(intersecting_layers=[1],
                               intersection_paths=[poly],
                               cell_size=block_cell_size,
                               bottom=z1,
                               marker=5,
                               marker_position=marker_pos)

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(4, [-600., -850., -3150.],
                           insert_struct=rx)

# add second block
for ix in range(len(x2)):
    M.add_brick(start=[x2[ix][0], y2[0], z2[0]],
                stop=[x2[ix][1], y2[1], z2[1]],
                cell_size=block_cell_size,
                marker=6)

# add third block
for ix in range(len(x3)):
    for iz in range(len(z3)):
        M.add_brick(start=[x3[ix][0], y3[0], z3[iz][0]],
                    stop=[x3[ix][1], y3[1], z3[iz][1]],
                    cell_size=block_cell_size,
                    marker=7)

# add transmitter in water layer at -550 m depth
M.add_tx(mu.line_x(-100., 100., n_segs=3, z=-550.))

# resolve face intersections
M.remove_duplicate_poly_faces()

# append boudary mesh
M.there_is_always_a_bigger_world(10., 10., 10.)

# call TetGen
M.call_tetgen(tet_param='-pq1.6aA', export_vtk=True)


# ######################### mesh for p1 computations ######################## #

block_cell_size = 1e6

# Define refinement-paths around receiver lcoations
points = np.concatenate((
    mu.line_x(-1e4, 1e4, n_segs=100, y=-3e3),
    mu.line_x(-1e4, 1e4, n_segs=100),
    mu.line_x(-1e4, 1e4, n_segs=100, y=3e3)))
rx = mu.refine_rx(points, 1., 30.)

# create world
M = BlankWorld(name='block_model_p1',
               m_dir='./meshes',
               x_dim=[-3e4, 3e4],
               y_dim=[-3e4, 3e4],
               z_dim=[-5e4, 5e4],
               preserve_edges=True)

# include water surface
M.build_surface()

# add Block 1 that touches the 2nd to 3rd subsurface layer interface
for i in range(len(x1)):
    marker_pos = [np.mean(x1[i]), np.mean(y1[i]), -900.]
    poly = np.array([[x1[i, 0], y1[i, 0], 0.],
                     [x1[i, 0], y1[i, 1], 0.],
                     [x1[i, 1], y1[i, 1], 0.],
                     [x1[i, 1], y1[i, 0], 0.]])
    M.add_intersecting_anomaly(intersecting_layers=[1],
                               intersection_paths=[poly],
                               cell_size=block_cell_size,
                               bottom=z1,
                               marker=5,
                               marker_position=marker_pos)

# build halfspace mesh and extend 2D surface mesh to 3D world
M.build_layered_earth_mesh(4, [-600., -850., -3150.],
                           insert_struct=rx)
# add second block
for ix in range(len(x2)):
    M.add_brick(start=[x2[ix][0], y2[0], z2[0]],
                stop=[x2[ix][1], y2[1], z2[1]],
                cell_size=block_cell_size,
                marker=6)

# add third block
for ix in range(len(x3)):
    for iz in range(len(z3)):
        M.add_brick(start=[x3[ix][0], y3[0], z3[iz][0]],
                    stop=[x3[ix][1], y3[1], z3[iz][1]],
                    cell_size=block_cell_size,
                    marker=7)

# add transmitter in water layer at -550 m depth
M.add_tx(mu.line_x(-100., 100., n_segs=10., z=-550.))

# resolve face intersections
M.remove_duplicate_poly_faces()

# append boudary mesh
M.there_is_always_a_bigger_world(10., 10., 10.)

# call TetGen
M.call_tetgen(tet_param='-pq1.2aA', export_vtk=True)
