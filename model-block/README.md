# Block model


A simple marine model consisting of a layered, partially anisotropic background
in which three blocks are embedded. We compare the layered background results
to the semi-analytical 1D solutions of *empymod*.


## Loading the model and the survey

```python
import discretize
import xarray as xr

# Load model and survey
ds = xr.load_dataset('../block_model_and_survey.nc', engine='h5netcdf')

# Mesh
hx, hy, hz = ds.attrs['hx'], ds.attrs['hy'], ds.attrs['hz']
x0 = ds.attrs['x0']
mesh_model = discretize.TensorMesh([hx, hy, hz], x0=x0)

# Models
resh_bg, resh_bg = ds.attrs['resh_bg'], ds.attrs['resv_bg']
resh_tg, resv_bg = ds.attrs['resh_tg'], ds.attrs['resv_tg']

# Survey
src = ds.attrs['src']
strength = ds.attrs['strength']
freq = ds.attrs['freq']
rec_x = ds.x.data
rec_y = ds.attrs['rec_y']
rec_z = ds.attrs['rec_z']
```


## Saving the data

```python
# Save the three lines; data is saved like
# np.array([[Re[0], Im[0], Re[1], Im[1], ..., Re[-1], Im[-1]])
ds.line_1.data = ... # y =-3000 (req. for layered and block model)
ds.line_2.data = ... # y =    0 (req. for layered and block model)
ds.line_3.data = ... # y = 3000 (only req. for block model)

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
model = ...  # 'layered' or 'block'
code = ...   # 'custEM', 'emg3d', 'PETGEM', or 'SimPEG'
#            # custEM/PETGEM: you can add a '_{p}', where p = 'p1' or 'p2'
ds.to_netcdf(f"../results/{model}_{code}.nc", engine='h5netcdf')
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

If you want to get an idea of the content and format of the info-data to
provide have a look at the `BlockModel-Comparison.ipynb`, there you see the
info provided from `emg3d`.
