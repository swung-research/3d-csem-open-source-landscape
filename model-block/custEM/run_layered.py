# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R
"""

# ########################################################################### #
# # # # #                        layered earth                        # # # # #
# ########################################################################### #
# # # # #                     computation script                      # # # # #
# ########################################################################### #

from custEM.core import MOD
import numpy as np

# ###################      define physical parameters       ################# #

res_ground = [0.3, 1., 2., 1000.]
sigma_ground = np.repeat(1./np.array(res_ground), 3).reshape(-1, 3)
sigma_ground[2, 2] *= (1./2.)  # Apply VTI anisotropy for third layer
frequency = 1.
source_current = 800.

# ####################### run p1 and p2 computations ######################## #

for p in [1]:

    mod = 'p' + str(p)
    mesh = 'layered_earth_p' + str(p)

    # Initialize model instance
    M = MOD(mod, mesh, 'E_t', p=p, overwrite=True,
            m_dir='./meshes', r_dir='./results')

    # update physical parameters
    M.MP.update_model_parameters(f=frequency,
                                 sigma_ground=sigma_ground.tolist(),
                                 J=source_current)

    # update fem parameters and define transmitter
    M.FE.build_var_form()
    # old non-automatized syntax
    #    M.FE.build_var_form(s_type='line',
    #                        start=[-100., 0., -550.],
    #                        stop=[100., 0., -550.])

    # Call solver, autoamtically convert to H-fields, and export results
    M.solve_main_problem()

    # load existing model only for interpolation purposes
    M = MOD(mod, mesh, 'E_t', p=p, overwrite=False, load_existing=True,
            m_dir='./meshes', r_dir='./results')

    # create regular inteprolation lines in x-direction at sea floor
    M.IB.create_line_meshes('x',  x0=-1e4, x1=1e4, y=-3e3, z=-600.1,
                            n_segs=100, line_name='l1m')
    M.IB.create_line_meshes('x',  x0=-1e4, x1=1e4, y=0., z=-600.1,
                            n_segs=100, line_name='l2m')
    M.IB.create_line_meshes('x',  x0=-1e4, x1=1e4, y=3e3, z=-600.1,
                            n_segs=100, line_name='l3m')

    for line in ['l1m_line_x', 'l2m_line_x', 'l3m_line_x']:
        M.IB.interpolate('E_t', line)
        M.IB.interpolate('H_t', line)
    M.IB.synchronize()  # synchronize all processes after interpolation
