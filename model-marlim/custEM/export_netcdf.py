# -*- coding: utf-8 -*-
"""
@author: Rochlitz.R
"""

# ########################################################################### #
# # # # #                         marlim model                        # # # # #
# ########################################################################### #
# # # # #                    visualization script                     # # # # #
# ########################################################################### #

# Note, plots will be saved in the *plots* directory

from custEM.post import PlotFD
import custEM as ce
import xarray as xr
from datetime import datetime

# import base dataset and specify custEM observation lines
ds = xr.load_dataset('../marlim_survey.nc', engine='h5netcdf')
line_il = 'inline_path_line_x'
line_bs = 'broadside_path_line_x'

p = '2'
mesh = 'marlim_fig4_reciprocal'
frequencies = [0.125, 0.25, 0.5, 0.75, 1., 1.25]
mod = 'f_' + str(frequencies[0])

solution_time = 0

# plot everything
for i, freq in enumerate(frequencies):
    mod = 'f_' + str(freq)
    
    # inititalize Plot instance and import data
    P = PlotFD(mod=mod, mesh=mesh, approach='E_t', r_dir='./results')
    solution_time += P.solution_time 
    
    P.import_line_data(line_il, key='il' + str(i))
    P.import_line_data(line_bs, key='bs' + str(i))

    # Save inline and broadside data for each frequency
    # Divide all data by factor 10 for normalizing the transmitter moment,
    # because the Tx was included with length 10 m in the mesh
    ds.data_il.data[::2, i, :3] = P.line_data[
            'il' + str(i) + '_E_t'].real / 10. # Inline RE
    ds.data_il.data[1::2, i, :3] = P.line_data[
            'il' + str(i) + '_E_t'].imag / 10. # Inline IM

    ds.data_bs.data[::2, i, :3] = P.line_data[
            'bs' + str(i) + '_E_t'].real / 10. # Inline RE
    ds.data_bs.data[1::2, i, :3] = P.line_data[
            'bs' + str(i) + '_E_t'].imag / 10. # Inline IM

    ds.data_il.data[::2, i, 3:] = P.line_data[
            'il' + str(i) + '_H_t'].real / 10. # Inline RE
    ds.data_il.data[1::2, i, 3:] = P.line_data[
            'il' + str(i) + '_H_t'].imag / 10. # Inline IM

    ds.data_bs.data[::2, i, 3:] = P.line_data[
            'bs' + str(i) + '_H_t'].real / 10. # Inline RE
    ds.data_bs.data[1::2, i, 3:] = P.line_data[
            'bs' + str(i) + '_H_t'].imag / 10. # Inline IM

mem_in_gib = 1e6 * P.max_mem / 1024**2

# Add info
ds.attrs['runtime'] = str(int(solution_time)) + ' s'
ds.attrs['n_procs'] = P.mpi_procs * P.omp_threads
ds.attrs['max_ram'] = f"{mem_in_gib :5.1f} GiB"
ds.attrs['n_cells'] = P.cells
ds.attrs['n_nodes'] = P.nodes
ds.attrs['n_dof'] = P.dof
ds.attrs['extent'] = ("x = -22800 - 22800; " 
                      "y = -22800 - 22800; "
                      "z = -22800 - 22800")
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
ds.to_netcdf(f"../results/marlim_{code}.nc", engine='h5netcdf')