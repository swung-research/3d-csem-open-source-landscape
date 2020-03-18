# Block model


A simple marine model consisting of a layered, partially anisotropic background
in which three blocks are embedded. We compare the layered background results
to the semi-analytical 1D solutions of *empymod*.


## Loading the model and the survey

```python
import discretize
import xarray as xr

# Load model and survey
survey = xr.load_dataset('../block_model_and_survey.nc', engine='h5netcdf')

# Mesh
hx, hy, hz = survey.attrs['hx'], survey.attrs['hy'], survey.attrs['hz']
x0 = survey.attrs['x0']
mesh_model = discretize.TensorMesh([hx, hy, hz], x0=x0)

# Models
resh_bg, resh_bg = survey.attrs['resh_bg'], survey.attrs['resv_bg']
resh_tg, resv_bg = survey.attrs['resh_tg'], survey.attrs['resv_tg']

# Survey
src = survey.attrs['src']
strength = survey.attrs['strength']
freq = survey.attrs['freq']
rec_x = survey.x.data
rec_y = survey.attrs['rec_y']
rec_z = survey.attrs['rec_z']
```


## Saving the data

```python
# Save the three lines
survey.line_1_re.data = ... # y =-3000 RE (req. for layered and block model)
survey.line_1_im.data = ... # y =-3000 IM (req. for layered and block model)
survey.line_2_re.data = ... # y =    0 RE (req. for layered and block model)
survey.line_2_im.data = ... # y =    0 IM (req. for layered and block model)
survey.line_3_re.data = ... # y = 3000 RE (only req. for block model)
survey.line_3_im.data = ... # y = 3000 IM (only req. for block model)

# Add info
ds.attrs['runtime'] = ...   # Elapsed real time (wall time) [s]
ds.attrs['cputime'] = ...   # Total time [s] (for parallel comp. >> runtime)
ds.attrs['nthreads'] = ...  # Number of threads used
ds.attrs['maxram'] = ...    # Max RAM used
ds.attrs['ncell'] = ...     # Number of cells (for emg3d/SimPEG else 'N/A')
ds.attrs['nedges'] = ...    # Number of edges (for custEM/PETGEM else 'N/A')
ds.attrs['machine'] = ...   # Machine info, e.g.
#                           # "laptop with an i7-6600U CPU@2.6 GHz (x4)
#                           #  and 16 GB of memory, using Ubuntu 18.04"
ds.attrs['version'] = ...   # Version number of your code
ds.attrs['date'] = datetime.today().isoformat()

# Add other meta data: add whatever you think is important for your code
survey.attrs['...'] = ...

# Save it under <{model}_{code}.nc>
model = ...  # 'layered' or 'block'
code = ...   # 'custEM', 'emg3d', 'PETGEM', or 'SimPEG'
#            # custEM/PETGEM: you can add a '_{p}', where p = 'p1' or 'p2'
survey.to_netcdf(f"../results/{model}_{code}.nc", engine='h5netcdf')
```

=> **PETGEM**: Please save data as `data.conj()`. PETGEM has, as far as I could
see, the opposite Fourier definition than custEM/emg3d/SimPEG. It is best we
save it all with the same definition.


## Info

Every code should store its info directly in the data (`survey.attrs[]`) as
shown in the code snippet above.

**Please make sure to add all info-data as indicated!**
