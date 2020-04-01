# Marlim R3D

Marlim R3D is a realistic resistivity model with corresponding
controlled-source electromagnetic data. The model was created by Carvalho and
Menezes (2017), and the resulting CSEM data, computed with *SBLwiz* from
*EMGS*, was presented by Correa and Menezes (2019). Both model and CSEM data
were released under the CC-BY 4.0 license and are available to download on
Zenodo.


### References

- **B. R. Carvalho and P. T. L. Menezes, 2017**, Marlim R3D: a realistic model
  for CSEM simulations - phase I: model building: Brazilian Journal of Geology,
  47, 633-644; DOI:
  [10.1590/2317-4889201720170088](https://doi.org/10.1590/2317-4889201720170088).
- **Correa, J. L. and P. T. L. Menezes, 2019**, Marlim R3D: A realistic model
  for controlled-source electromagnetic simulations - Phase 2: The
  controlled-source electromagnetic data set: Geophysics, 84(5), E293-E299;
  DOI: [10.1190/geo2018-0452.1](https://doi.org/10.1190/geo2018-0452.1).
- Fine Model;
  DOI: [10.5281/zenodo.400233](https://doi.org/10.5281/zenodo.400233)
- Computation Model (personal communication; TODO: ask for uploading it)
- With noise;
  DOI: [10.5281/zenodo.1256787](https://doi.org/10.5281/zenodo.1256787)
- Without noise;
  DOI: [10.5281/zenodo.1807135](https://doi.org/10.5281/zenodo.1807135)

### Required files

For the data comparison, from
[10.5281/zenodo.1807135](https://doi.org/10.5281/zenodo.1807135):

- EW_nonoise.zip
- NS_nonoise.zip

To create the FD-models, from
[10.5281/zenodo.400233](https://doi.org/10.5281/zenodo.400233):

- Horizontal_resistivity.sgy
- Vertical_Resistivity.sgy

To create the FE-models additionally, from
[10.5281/zenodo.400233](https://doi.org/10.5281/zenodo.400233):

- Sea_Bottom-mr3d.xyz
- Miocene-mr3d.xyz
- Oligocene-mr3d.xyz
- Blue_mark-mr3d.xyz
- Top_of_Salt-mr3d.xyz
- Base_of_salt-mr3d.xyz


## Loading the model

We do not want to store the resistivity model and the CSEM data in our repo -
the reader has to download them and put them in a folder `model-marlim/DATA`.
The file `loadmarlim.py` contains functions to load the resistivity model and
the CSEM data and stores them in an easier accessible format. If the functions
cannot find the data it prints a help-text with the link where the data can be
downloaded and instructions where to put them.

To create the model-files you have to run in `model-marlim/` the following
code in Python:
```python
import loadmarlim
loadmarlim.extract_model('comp')  # => creates `model-marlim/marlim_comp.npz`
loadmarlim.extract_model('orig')  # => creates `model-marlim/marlim_orig.npz`
```

Now to load the models in `model-marlim/{CODE}/.` run
```python
import discretize
import numpy as np
data = np.load('../marlim_comp.npz')  #  or 'marlim_orig.npz'
res_h = data['res_h']
res_v = data['res_v']

mesh = discretize.TensorMesh(
    [data['hx'], data['hy'], data['hz']], x0=data['x0'])
```

**Note:** The computational models are not yet publicly available, I sent them
once to you, I received them directly from the authors. I wrote them asking to
put in on Zenodo too, so we can properly link to them and cite it.


## Loading the survey and the comparison data

To load the survey (in `model-marlim/{CODE}/`):
```python
import xarray as xr
data = xr.load_dataset('../marlim_survey.nc', engine='h5netcdf')
```

If you want to compare your CSEM results to the published ones you first have
to create the data file. Run the following command (in the directory
`model-marlim/`):
```python
import loadmarlim
loadmarlim.create_survey(store_data=True)
```
This creates the file `model-marlim/marlim_data.nc`.

From now on you can load the data in your `model-marlim/{CODE}/`-directory like
this:
```python
import xarray as xr
data = xr.load_dataset('../marlim_data.nc', engine='h5netcdf')
```


## Saving the data

Assuming you are in the directory `model-marlim/{CODE}/`.
```python
import xarray as xr

# Load survey as template
ds = xr.load_dataset('../marlim_survey.nc', engine='h5netcdf')

# Save the two lines; the data has shape (408, 6, 6) => (noff*2, nfreq, ncomp)
ds.data_il.data = ... # Inline
ds.data_bs.data = ... # Broadside
# If you only store ex, ey, and ez, which is sufficient for the paper, do
# ds.data_{il;bs}.data[:, :, :3] = ...

# Add info
ds.attrs['runtime'] = ...  # Elapsed real time (wall time) [s]
ds.attrs['n_procs'] = ...  # Number of processes (cores, procs, threads)
ds.attrs['max_ram'] = ...  # Max RAM used
ds.attrs['n_cells'] = ...  # Number of cells (FD codes, else 'N/A')
ds.attrs['n_nodes'] = ...  # Number of nodes (FE codes, else 'N/A')
ds.attrs['n_dof'] = ...    # Number of dof (FE codes, else 'N/A')
ds.attrs['extent'] = ...   # (xmin, xmax, ymin, ymax, zmin, zmax) mesh ext.
ds.attrs['min_vol'] = ...  # Volume of smallest voxel
ds.attrs['max_vol'] = ...  # Volume of largest voxel
ds.attrs['machine'] = ...  # Machine info, e.g.
#                          # "laptop with an i7-6600U CPU@2.6 GHz (x4)
#                          #  and 16 GB of memory, using Ubuntu 18.04"
ds.attrs['version'] = ...  # Version number of your code
ds.attrs['date'] = datetime.today().isoformat()

# Add other meta data: add whatever you think is important for your code
ds.attrs['...'] = ...

# Save it under <{model}_{code}.nc>
code = ...   # 'custEM', 'emg3d', 'PETGEM', or 'SimPEG'
#            # custEM/PETGEM: you can add a '_{p}', where p = 'p1' or 'p2'
ds.to_netcdf(f"../results/marlim_{code}.nc", engine='h5netcdf')
```

A note regarding `runtime` and `max_ram`: Only profile the solution of the
actual system `Ax=b`. Mesh creation, model and field interpolation, and all
other pre- and post-processing steps do not fall under this measure.

=> **PETGEM**: Please save data as `data.conj()`. PETGEM has, as far as I could
see, the opposite Fourier definition than custEM/emg3d/SimPEG. It is best we
save it all with the same definition.


## Info

Every code should store its info directly in the data (`ds.attrs[]`) as shown
in the code snippet above.

**Please make sure to add all info-data as indicated!**
