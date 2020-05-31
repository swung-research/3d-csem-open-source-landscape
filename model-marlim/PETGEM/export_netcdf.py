#!/usr/bin/env python3
# Author:  Octavio Castillo Reyes
# Contact: octavio.castillo@bsc.es
''' Export marlim model results using PETGEM to netcdf format
'''

# ---------------------------------------------------------------
#                         MARLIM MODEL
# ---------------------------------------------------------------
import xarray as xr
from datetime import datetime
import numpy as np
import h5py

# ---------------------------------------------------------------
# Import base dataset and specify PETGEM observation lines
# ---------------------------------------------------------------
ds = xr.load_dataset('../marlim_survey.nc', engine='h5netcdf')
line_il = 'data_il'
line_bs = 'data_bs'

# ---------------------------------------------------------------
# Open PETGEM results file
# ---------------------------------------------------------------
f = h5py.File('out/electric_fields.h5', 'r')

# ---------------------------------------------------------------
# Save inline data and broadside data for all frequencies
# ---------------------------------------------------------------
ds.data_il.data = f.get(line_il)[()]
ds.data_bs.data = f.get(line_bs)[()]

# ---------------------------------------------------------------
# Add info
# ---------------------------------------------------------------
ds.attrs['runtime'] = str(int(f.get('runtime')[()])) + ' s'
ds.attrs['n_procs'] = f.get('n_procs')[()]
ds.attrs['max_ram'] = '{:5.1f}'.format(f.get('max_mem')[()]) + ' GiB'
ds.attrs['n_cells'] = f.get('n_cells')[()]
ds.attrs['n_nodes'] = f.get('n_nodes')[()]
ds.attrs['n_dof'] = f.get('n_dof')[()]
ds.attrs['extent'] = ("x = -22800 - 22800; "
                      "y = -22800 - 22800; "
                      "z = -22800 - 22800")
ds.attrs['min_volume'] = f.get('min_volume')[()]
ds.attrs['max_volume'] = f.get('max_volume')[()]
ds.attrs['machine'] = ("Marenostrum4. Intel Xeon Platinum from Skylake generation; "
                       "2 sockets Intel Xeon Platinum 8160 CPU with 24 cores each @2.10GHz for a total of 48 cores per node; "
                       "386 Gb DDR4 RAM per node; SuSE Linux Enterprise")
ds.attrs['version'] = "PETGEM v" + str(f.get('version')[()])
ds.attrs['date'] = datetime.today().isoformat()

# These are my final results
ds.attrs['NOTE'] = 'Final results based on p2 basis order'

# ---------------------------------------------------------------
# Save it under <{model}_{code}_{p}.nc>
# ---------------------------------------------------------------
code = 'petgem'
ds.to_netcdf(f"../results/marlim_{code}.nc", engine='h5netcdf')
