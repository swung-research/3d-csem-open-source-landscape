#!/usr/bin/env python3
# Author:  Octavio Castillo Reyes
# Contact: octavio.castillo@bsc.es
''' Export layered earth and blocky model results using PETGEM to netcdf format
'''

# ---------------------------------------------------------------
#                 LAYERED EARTH AND BLOCKY MODEL
# ---------------------------------------------------------------
import xarray as xr
from datetime import datetime
import numpy as np
import h5py

# ---------------------------------------------------------------
# Import base dataset and specify petgem observation lines
# ---------------------------------------------------------------
ds = xr.load_dataset('../block_model_and_survey.nc', engine='h5netcdf')
lines = ['l1m_line_x', 'l2m_line_x', 'l3m_line_x']

# ---------------------------------------------------------------
# Open PETGEM results file
# ---------------------------------------------------------------
sol_block = h5py.File('out/block.h5', 'r')

# ---------------------------------------------------------------
# Export to netcdf: block model
# ---------------------------------------------------------------
model = 'block'
# Save line 1
real_line1 = sol_block.get('line1')[()].conjugate().real
imag_line1 = sol_block.get('line1')[()].conjugate().imag
ds.line_1.data = np.vstack((real_line1, imag_line1)).ravel('F')

# Save line 2
real_line2 = sol_block.get('line2')[()].conjugate().real
imag_line2 = sol_block.get('line2')[()].conjugate().imag
ds.line_2.data = np.vstack((real_line2, imag_line2)).ravel('F')

# Save line 3
real_line3 = sol_block.get('line3')[()].conjugate().real
imag_line3 = sol_block.get('line3')[()].conjugate().imag
ds.line_3.data = np.vstack((real_line3, imag_line3)).ravel('F')

# Add info
ds.attrs['runtime'] = str(int(sol_block.get('runtime')[()])) + ' s'
ds.attrs['n_procs'] = sol_block.get('n_procs')[()]
ds.attrs['max_ram'] = '{:5.1f}'.format(sol_block.get('max_mem')[()]) + ' GiB'
ds.attrs['n_cells'] = sol_block.get('n_cells')[()]
ds.attrs['n_nodes'] = sol_block.get('n_nodes')[()]
ds.attrs['n_dof'] = sol_block.get('n_dof')[()]
ds.attrs['extent'] = ("x = -100000 - 100000; "
                      "y = -100000 - 100000; "
                      "z = -100000 - 100000")
ds.attrs['min_volume'] = sol_block.get('min_volume')[()]
ds.attrs['max_volume'] = sol_block.get('max_volume')[()]
ds.attrs['machine'] = ("Marenostrum4. Intel Xeon Platinum from Skylake generation; "
                       "2 sockets Intel Xeon Platinum 8160 CPU with 24 cores each @2.10GHz for a total of 48 cores per node; "
                       "386 Gb DDR4 RAM per node; SuSE Linux Enterprise")
ds.attrs['version'] = "PETGEM v" + str(sol_block.get('version')[()])
ds.attrs['date'] = datetime.today().isoformat()

# These are my final results
ds.attrs['NOTE'] = 'Final results based on p2 basis order'

# Save it under <{model}_{code}_{p}.nc>
code = 'petgem'
ds.to_netcdf(f"../results/{model}_{code}.nc", engine='h5netcdf')

# ---------------------------------------------------------------
# Export to netcdf: layered model
# ---------------------------------------------------------------
sol_layered = h5py.File('out/layered.h5', 'r')

# ---------------------------------------------------------------
# Export to netcdf: block model
# ---------------------------------------------------------------
model = 'layered'
# Save line 1
real_line1 = sol_layered.get('line1')[()].conjugate().real
imag_line1 = sol_layered.get('line1')[()].conjugate().imag
ds.line_1.data = np.vstack((real_line1, imag_line1)).ravel('F')

# Save line 2
real_line2 = sol_layered.get('line2')[()].conjugate().real
imag_line2 = sol_layered.get('line2')[()].conjugate().imag
ds.line_2.data = np.vstack((real_line2, imag_line2)).ravel('F')

# Save line 3
real_line3 = sol_layered.get('line3')[()].conjugate().real
imag_line3 = sol_layered.get('line3')[()].conjugate().imag
ds.line_3.data = np.vstack((real_line3, imag_line3)).ravel('F')

# Add info
ds.attrs['runtime'] = str(int(sol_layered.get('runtime')[()])) + ' s'
ds.attrs['n_procs'] = sol_layered.get('n_procs')[()]
ds.attrs['max_ram'] = '{:5.1f}'.format(sol_layered.get('max_mem')[()]) + ' GiB'
ds.attrs['n_cells'] = sol_layered.get('n_cells')[()]
ds.attrs['n_nodes'] = sol_layered.get('n_nodes')[()]
ds.attrs['n_dof'] = sol_layered.get('n_dof')[()]
ds.attrs['extent'] = ("x = -100000 - 100000; "
                      "y = -100000 - 100000; "
                      "z = -100000 - 100000")
ds.attrs['min_volume'] = sol_layered.get('min_volume')[()]
ds.attrs['max_volume'] = sol_layered.get('max_volume')[()]
ds.attrs['machine'] = ("Marenostrum4. Intel Xeon Platinum from Skylake generation; "
                       "2 sockets Intel Xeon Platinum 8160 CPU with 24 cores each @2.10GHz for a total of 48 cores per node; "
                       "386 Gb DDR4 RAM per node; SuSE Linux Enterprise")
ds.attrs['version'] = "PETGEM v" + str(sol_layered.get('version')[()])
ds.attrs['date'] = datetime.today().isoformat()

# These are my final results
ds.attrs['NOTE'] = 'Final results based on p2 basis order'

# Save it under <{model}_{code}_{p}.nc>
code = 'petgem'
ds.to_netcdf(f"../results/{model}_{code}.nc", engine='h5netcdf')
