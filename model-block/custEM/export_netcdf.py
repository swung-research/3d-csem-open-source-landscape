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

from custEM.post import PlotFD
import custEM as ce
import xarray as xr
from datetime import datetime
import numpy as np

# import base dataset and specify custEM observation lines

ds = xr.load_dataset('../block_model_and_survey.nc', engine='h5netcdf')
lines = ['l1m_line_x', 'l2m_line_x', 'l3m_line_x']

# export everything to netcdf
for p in ['1', '2']:
    for model in ['layered', 'block']:

        # load interpolated modeling results on observation line
        mod = 'p' + str(p)
        if model == 'layered':
            mesh = 'layered_earth_p' + p
        else:
            mesh = 'block_model_p' + p

        P = PlotFD(mod=mod, mesh=mesh, approach='E_t', r_dir='./results')
        for i, line in enumerate(lines):            
            P.import_line_data(line, key='t' + str(i+1), EH='E')

        # save the three lines
        ds.line_1.data = np.vstack(
                [P.line_data['t1_E_t'][:, 0].real, 
                 P.line_data['t1_E_t'][:, 0].imag]).ravel('F') 
        ds.line_2.data = np.vstack(
                [P.line_data['t2_E_t'][:, 0].real, 
                 P.line_data['t2_E_t'][:, 0].imag]).ravel('F') 
        ds.line_3.data = np.vstack(
                [P.line_data['t3_E_t'][:, 0].real, 
                 P.line_data['t3_E_t'][:, 0].imag]).ravel('F') 
    
        mem_in_gib = 1e6 * P.max_mem / 1024**2
    
        # Add info
        ds.attrs['runtime'] = str(int(P.solution_time)) + ' s'
        ds.attrs['n_procs'] = P.mpi_procs * P.omp_threads
        ds.attrs['max_ram'] = f"{mem_in_gib :5.1f} GiB"
        ds.attrs['n_cells'] = P.cells
        ds.attrs['n_nodes'] = P.nodes
        ds.attrs['n_dof'] = P.dof
        ds.attrs['extent'] = ("x = -100000 - 100000; " 
                              "y = -100000 - 100000; "
                              "z = -100000 - 100000")
        ds.attrs['min_volume'] = P.min_volume
        ds.attrs['max_volume'] = P.max_volume
        ds.attrs['machine'] = ("PowerEdge R940 server; "
                               "144 Xeon Gold 6154 CPU @2.666 GHz; "
                               "~3 TB DDR4 RAM; Ubuntu 18.04")
        ds.attrs['version'] = "custEM v" + ce.__version__
        ds.attrs['date'] = datetime.today().isoformat()
 
        # These are quasi final results
        ds.attrs['NOTE'] = 'Quasi final'
    
        # Save it under <{model}_{code}_{p}.nc>
        code = 'custEM_p' + p
        ds.to_netcdf(f"../results/{model}_{code}.nc", engine='h5netcdf')