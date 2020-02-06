# -*- coding: utf-8 -*-
"""
@author:  Rochlitz.R
"""

# ########################################################################### #
# # # # #                          example 3                          # # # # #
# ########################################################################### #
# # # # #                      computation script                     # # # # #
# ########################################################################### #


import segyio
#import discretize    # for the meshing
#import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator as rgi
from custEM.misc import write_h5
from custEM.misc import read_h5
from custEM.meshgen import meshgen_utils as mu

from custEM.core import MOD
from custEM.misc import mpi_print as mpp
import numpy as np
import dolfin as df

#res_h = segyio.tools.cube('./data/Horizontal_resistivity.sgy')[:, :, :]
#res_v = segyio.tools.cube('./data/Vertical_Resistivity.sgy')[:, :, :]

y = np.loadtxt('./data/resvec_x.txt') - 388993.
x = np.loadtxt('./data/resvec_y.txt') - 7518065.
z = np.loadtxt('./data/resvec_z.txt')

res_h = np.transpose(np.load('./data/res_h.npy')[::-1, :, ::-1], (1, 0, 2))
res_v = np.transpose(np.load('./data/res_v.npy')[::-1, :, ::-1], (1, 0, 2))

#mpp(len(x))
#mpp(len(y))
#mpp(len(z))

#nx, ny, nz = res_h.shape
#dx, dy, dz = 75, 25, 5
#
##x0 = 1e100
##y0 = 1e100
##with segyio.open('./data/Horizontal_resistivity.sgy') as f:
##    for i in range(nx*ny):
##        if f.header[i][segyio.TraceField.CDP_X] < x0:
##            x0 = f.header[i][segyio.TraceField.CDP_X]
##        if f.header[i][segyio.TraceField.CDP_Y] < y0:
##            y0 = f.header[i][segyio.TraceField.CDP_Y]
##x0, y0 = x0/10, y0/10
#
#x0, y0 = np.loadtxt('./data/x0.txt')
#
#mesh = discretize.TensorMesh([np.ones(nx)*dx, np.ones(ny)*dy, np.ones(nz)*dz], x0=[x0, y0, 'N'])
#
#mesh.vectorCCz
#np.savetxt('./data/resvec_x.txt', mesh.vectorCCx)
#np.savetxt('./data/resvec_y.txt', mesh.vectorCCy)
#np.savetxt('./data/resvec_z.txt', mesh.vectorCCz)

#mesh.plot_3d_slicer(np.log10(res_h))

interp_h = rgi((x,y,z), res_h, method='nearest')
interp_v = rgi((x,y,z), res_v, method='nearest')

#mpp(np.min(x), np.max(x))
#mpp(np.min(y), np.max(y))
#mpp(np.min(z), np.max(z))



def overwrite_markers(M, interp_func):

    # the anomaly was defined as block, which is larger than the target
    # anomaly. Thus, we need to keep the target anomaly markers ("3"), but
    # overwrite the remaining block markers with the layer marker "1"

    all_cells = [cell for cell in df.cells(M.FS.mesh)]
    midpoints = np.array([cell.midpoint().array() for cell in all_cells])

    tet_points = midpoints[midpoints[:, 2] < 0.]
    tet_ids = []

    counter = 0
    for idx, (x, y, z) in enumerate(midpoints):
        if z > 0.:
            pass
        else:
            tet_ids.append(idx)
        counter += 1
#    print(np.min(tet_points[:, 0]), np.max(tet_points[:, 0]))
#    print(np.min(tet_points[:, 1]), np.max(tet_points[:, 1]))
#    print(np.min(tet_points[:, 2]), np.max(tet_points[:, 2]))
#
#    raise SystemExit
    print('3d res interrpolation')
    tet_res_h = interp_h(tet_points)
    tet_res_v = interp_v(tet_points)
    return(tet_res_h, tet_res_v, tet_ids)


approaches = ['E_t']
omega = 1e0 * 2. * np.pi

# define anisotropic conductivity tensor for the brick anomaly:
# old syntax for anisotropy, deprecated!
aniso_cond = df.as_matrix(((0.1, 0., 0.), (0., 0.1, 0.), (0., 0., 1.)))

pf_EH = 'H'
linE1 = 'x0_-5000.0_x1_5000.0_y_0.0_z_0.0_n_200_line_x'
linE2 = 'x0_-5000.0_x1_5000.0_y_0.0_z_50.0_n_200_line_x'

# new syntax for (in this case VTI) anisotropy in development:
# aniso_cond = [0.1, 0.1, 1.]

# ########################## run p1 computations ############################ #

p = 2
mod = 'p2'
mesh = 'marlim'

cond = 1./np.array([0.3, 1., 5., 1., 10., 100., 1000.])

for approach in approaches:       # all approaches

    # Initialize MODel
    M = MOD(mod, mesh, approach, p=p, overwrite=True,
            m_dir='./meshes', r_dir='./results')

    M.FS.DOM.domain_func.set_values(np.arange(M.FS.DOM.domain_func.size()))
    dg11 = df.FunctionSpace(M.FS.mesh, "DG", 0)
    dg22 = df.FunctionSpace(M.FS.mesh, "DG", 0)
    dg1 = df.Function(dg11)
    dg2 = df.Function(dg22)
    dg1.vector()[:] = 1e8
    dg2.vector()[:] = 1e8

    mpp('...  interpolating resitivites  ...')
    a, b, ids = overwrite_markers(M, interp_h)
    r_h = np.ones((M.FS.DOM.domain_func.size())) * 1e8
    r_v = np.ones((M.FS.DOM.domain_func.size())) * 1e8
    dg_space = df.TensorFunctionSpace(M.FS.mesh, "DG", 0)
    dg1.vector()[ids] = a
    dg2.vector()[ids] = b

    df.File('sig_h.pvd') << dg1
    df.File('sig_v.pvd') << dg2

    write_h5(M.MP.mpi_cw, dg1, 'res_h.h5')
    write_h5(M.MP.mpi_cw, dg2, 'res_v.h5')
    read_h5(M.MP.mpi_cw, dg1, 'res_h.h5')
    read_h5(M.MP.mpi_cw, dg2, 'res_v.h5')

    sig = np.concatenate((1./dg1.vector()[:].reshape(-1, 1),
                          1./dg1.vector()[:].reshape(-1, 1),
                          1./dg2.vector()[:].reshape(-1, 1)), axis=1)

    # define frequency and conductivities
    M.MP.update_model_parameters(omega=1. * 2. * np.pi,
                                 sigma_anom=[],
                                 sigma_ground=cond.tolist(),
                                 procs_per_proc=1)

    M.MP.sigma = sig
    M.MP.tensor_flag = True
    M.MP.topo = None

    M.FS.DOM.n_domains = len(dg1.vector().get_local())

    M.FE.build_var_form(check_sigma_conformity=False,
                        pf_type='halfspace',
                        s_type='path',
                        closed_path=True,
                        path = mu.line_x(-5., 5., z=-500., n_segs=2),
                        n_segs=11,
                        pf_EH_flag=pf_EH,
                        sigma_from_func=True)

#    df.File('sig.pvd') << M.FE.sigma_func
#    raise SystemExit

    M.solve_main_problem()
#
#    # load existing model only for interpolation purposes
#    M = MOD(mod, mesh, approach, p=p, overwrite=False, load_existing=True,
#            m_dir='./meshes', r_dir='./results')
#
#    # create regular 5 km inteprolation line in x-dir at surface
#    M.I.create_line_meshes('x',  x0=-1e4, x1=1e4, z=-601., n_segs=100, line_name='l1')
#    M.I.create_line_meshes('x',  x0=-1e4, x1=1e4, y=3e-3, z=-601., n_segs=100, line_name='l2')
#    M.I.create_line_meshes('x',  x0=-1e4, x1=1e4, y=3e3, z=-601., n_segs=100, line_name='l3')
#
#    # interpolate fields on the observation line
#    if '_s' in approach:   # if secondary field formulation used
#        quantities = ['H_t', 'E_t', 'H_s', 'E_s']
#    else:                  # if total field formulation used
#        quantities = ['H_t', 'E_t']
#    for q in quantities:
#        M.I.interpolate(q, linE1)
#        M.I.interpolate(q, linE2)
#    M.I.synchronize()
