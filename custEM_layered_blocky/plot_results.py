# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #               layered earth and blocky model                # # # # #
# ########################################################################### #
# # # # #                    visualization script                     # # # # #
# ########################################################################### #

# Note, plots will be saved in the *plots* directory

import matplotlib.pyplot as plt
from custEM.post import PlotFD as Plot
import numpy as np

# define parameters
plt.ioff()

lines = ['l1_line_x', 'l2_line_x', 'l3_line_x']
lines = ['l1_line_x', 'l2_line_x']

lines = ['l1m_line_x', 'l2m_line_x', 'l3m_line_x']

p = 2

mesh_l = 'layered_earth_p' + str(p)
mesh_b = 'blocky_model_p' + str(p)

mod = 'p' + str(p)

epm_1 = np.zeros((101, 3), dtype=complex)
epm_2 = np.zeros((101, 3), dtype=complex)

epm_1[:, :1] = np.load('../data/epm1_1d.npy')[:, :1]
epm_2[:, :1] = np.load('../data/epm1_1d.npy')[:, 1:]

# inititalize Plot instance
P = Plot(mod=mod, mesh=mesh_l, approach='E_t',
         r_dir='./results', s_dir='./plots')



# plot everything
for j, line in enumerate(lines):
    mod = 'p' + str(p)
#    mod2 = 'p2'
    P.import_line_data(line, mesh=mesh_l, key='t1')
#    P.import_line_data(line, mesh=mesh_l2, mod=mod2, key='t2')

    if j == 0:
        epm = epm_1
    else:
        epm = epm_2

    P.line_data['ref' + str(j) + '_E_t'] = epm
    P.line_coords['ref' + str(j)] = P.line_coords[line]

    out_name = '../data/custEM_results/'
    if j == 0:
        out_name += 'y_-3000_'
    elif j == 1:
        out_name += 'y_0_'
    else:
        out_name += 'y_3000_'

    np.save(out_name + 'coords.npy', P.line_coords[line].real)
    np.save(out_name + 'E_le_p'+ str(p) + '.npy', P.line_data['t1_E_t'][:, :3])
#    np.save(out_name + 'E_bm.npy', P.line_data['t2_E_t'][:, :3])
    np.save(out_name + 'H_le_p' + str(p) + '.npy', P.line_data['t1_H_t'][:, :3])
#    np.save(out_name + 'H_bm.npy', P.line_data['t2_H_t'][:, :3])

    fields = 'E'  # choose either 'E', 'H' or 'EH'
#    P.plot_line_data(key='t1', EH=fields, label='p1', xlim=[-10., 10.])
#    P.plot_line_data(key='t2', EH=fields, label='p2', title=line, new=False)
#    P.plot_line_data(key='ref' + str(j), EH=fields, label='empymod', new=False)
#    plt.savefig('new_results.pdf', bbox_inches='tight', pad_inches=0)

    P.plot_line_errors(key='ref' + str(j), EH=fields, key2='t1',
                       label='p1 misfit', xlim=[-10., 10.])
#    P.plot_line_errors(key='ref' + str(j), EH=fields, key2='t2',
#                       new=False, label='p2 misfit')
#    plt.savefig('new_misfits.pdf', bbox_inches='tight', pad_inches=0)

# plt.savefig('results.pdf', bbox_inches='tight', pad_inches=0)
plt.ion()   # uncomment to enable showing the plot
plt.show()  # uncomment to enable showing the plot
