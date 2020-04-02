# -*- coding: utf-8 -*-
"""
This script can be used to reproduce the results presented in Figure 4 by
Correa and Menezes (2018):
    "Marlim R3D: A realistic model for controlled-source electromagnetic
    simulations — Phase 2: The controlled-source electromagnetic data set"

Note that custEM was not optimized for adopting externall provided resistivity
information on different grids for now. Anyway, this example shows the
principal applicability by manually incoporating the resistivity interpolation
and intercepting some parts of the usual modeling workflow.

For any questions or issues, contact

    raphael.rochlitz@leibniz-liag.de

"""

# ########################################################################### #
# # # # #                         Marlim R3D                          # # # # #
# ########################################################################### #
# # # # #                      computation script                     # # # # #
# ########################################################################### #

# If tools are missing, install them into the current conda environment
from scipy.interpolate import RegularGridInterpolator as rgi
from custEM.core import MOD
from custEM.misc import mpi_print as mpp
import numpy as np
import dolfin as df


def overwrite_markers(M, interp_func, marker_copy):

    """
    Manually overwrite markers for conductivity interpolation. A new marker is
    assigned to each cell within the subsurface layers (originally markers >1).
    Conductivities are interpolated on the midpoints of all these cells.

    Outside of the central part covered by the resistivities provided on the
    Marlim R3D repositiory, the outermost values at the Marlim model boundaries
    are used to expand the covered area in horizontal direction.

    For the water layer, the water depth slightly increases towards the custEM
    mesh boundaries to enable a more consistent extension of the hihgly
    conductive water layer, even though the boundary-mesh is halfspace-like.
    The dependency is formulated in the **bathy_extent** function.
    """

    all_cells = [cell for cell in df.cells(M.FS.mesh)]
    midpoints = np.array([cell.midpoint().array() for cell in all_cells])

    inner_dim = 1.14e4

    def bathy_extent(x, y):

        """
        Extent bathymetry outside of central area.
        """

        z_val = np.abs(x)
        if np.abs(x) < np.abs(y):
            z_val = np.abs(y)
        return(-z_val / 20. - 200.)

    for j in range(len(midpoints)):
        if (midpoints[j, 0] < -inner_dim or midpoints[j, 0] > inner_dim or
            midpoints[j, 1] < -inner_dim or midpoints[j, 1] > inner_dim) and \
           midpoints[j, 2] < bathy_extent(midpoints[j, 0], midpoints[j, 1]):
            marker_copy[j] = 99
        elif midpoints[j, 2] < -inner_dim:
            marker_copy[j] = 99               # 99 is just a dummy value

    tet_ids = []
    water_ids = []

    counter = 0
    for idx, (x, y, z) in enumerate(midpoints):
        if marker_copy[idx] == 0:             # cell is in air domain
            pass
        elif marker_copy[idx] == 1:           # cell is in water domain
            water_ids.append(idx)
        else:                                 # cell is in subsurface
            tet_ids.append(idx)
        counter += 1

    tet_points = midpoints[tet_ids]
    tet_res_h = interp_h(tet_points)          # interpolation in relevant cells
    tet_res_v = interp_v(tet_points)          # interpolation in relevant cells

    return(tet_res_h, tet_res_v, tet_ids, water_ids)


# %% Preliminaries

# import modified Marlim R3D resitivity data, optimized as custEM input
grid_vectors = np.load('data/res_grid_extended.npy')
res_h = np.load('data/res_h_extended.npy')
res_v = np.load('data/res_v_extended.npy')

# set up interpolation objects with log-transformed resistivities
interp_h = rgi((grid_vectors[0], grid_vectors[1], grid_vectors[2]),
               np.log10(res_h), method='linear')
interp_v = rgi((grid_vectors[0], grid_vectors[1], grid_vectors[2]),
               np.log10(res_v), method='linear')

# delete original resistivity data to save some RAM
del res_h
del res_v

# import shifted Rx positions (with respect to custEM mesh)
inline = np.loadtxt('data/tx_inline_shifted.xyz')
broadside = np.loadtxt('data/tx_broadside_shifted.xyz')

# define mesh, frequencies and polynomial order
mesh = 'marlim_fig4_reciprocal'
frequencies = [0.125, 0.25, 0.5, 0.75, 1., 1.25]
p = 2


# %% run p2 computations for all frequencies
for fi, freq in enumerate(frequencies):       # all approaches

    # Initialize MODel
    mod = 'f_' + str(freq)
    M = MOD(mod, mesh, 'E_t', p=p, overwrite=True,
            m_dir='./meshes', r_dir='./results')

    # define frequency and conductivities
    M.MP.update_model_parameters(f=freq,     # dummy values for sigma, to be
                                 sigma_ground=np.ones(7))      # overwritten

    # copy original marker function
    marker_copy = np.zeros(M.FS.DOM.domain_func.size(), dtype=int)
    marker_copy[:] = M.FS.DOM.domain_func.array()

    # initialize new domain function with cell-wise marker numbering
    M.FS.DOM.domain_func.set_values(np.arange(M.FS.DOM.domain_func.size()))

    # set up resistivity function, initialize with default value for airspace
    DG = df.FunctionSpace(M.FS.mesh, "DG", 0)
    res_h = df.Function(DG)
    res_v = df.Function(DG)
    res_h.vector()[:] = 1e8
    res_v.vector()[:] = 1e8

    # overwrite markers and interpolate values on subsurface cells
    mpp('...  interpolating resitivites  ...')
    res_interp_h, res_interp_v, sub_ids, water_ids = \
        overwrite_markers(M, interp_h, marker_copy)

    # set water resistivity and subsurface values (reverse log transform)
    res_h.vector()[water_ids] = 0.32
    res_v.vector()[water_ids] = 0.32
    res_h.vector()[sub_ids] = 10**res_interp_h
    res_v.vector()[sub_ids] = 10**res_interp_v

    # convert resistivities to custEM conformal format,
    # a list of 3 VTI conductivity values for each cell
    sig = np.concatenate((1./res_h.vector()[:].reshape(-1, 1),
                          1./res_h.vector()[:].reshape(-1, 1),
                          1./res_v.vector()[:].reshape(-1, 1)), axis=1)

    # export interpolated conductivities for visualization if desired
    # df.File(M.out_dir + '/res_h.pvd') << res_h
    # df.File(M.out_dir + '/res_v.pvd') << res_v

    # overwrite domain markers and conductivities manually
    M.MP.sigma = sig
    # overwrite anisotropy flag
    M.MP.tensor_flag = True
    # overwrite topo flag (implementation issue, will be resolved in future)
    M.MP.topo = 'None'
    # overwrite value for different domain markers
    M.FS.DOM.n_domains = len(res_h.vector().get_local())

    # conduct the real FE stuff
    M.FE.build_var_form(check_sigma_conformity=False)
    M.solve_main_problem(convert_to_H=False)

    # import existing FE results, if exported before
    # M = MOD(mod, mesh, 'E_t', p=p, overwrite=False,
    #         load_existing=True, m_dir='./meshes', r_dir='./results')

    # conduct interpolation of receiver
    M.IB.on_topo = False
    if fi == 0:
        M.IB.create_path_mesh(inline, 'inline', suffix='line_x')
        M.IB.create_path_mesh(broadside, 'broadside', suffix='line_x')
    M.IB.interpolate('E_t', 'inline_path_line_x')
    M.IB.interpolate('E_t', 'broadside_path_line_x')
    M.IB.synchronize()
    del M
