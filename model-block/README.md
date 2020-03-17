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
survey.line_1.data = ... # Data y=-3000 (required for layered and block model)
survey.line_2.data = ... # Data y=0 (required for layered and block model)
survey.line_3.data = ... # Data y=3000 (only required for the block model)

# Add info
survey.attrs['...'] = ...  # SEE BELOW FOR KEYS

# Add other meta data: add whatever you think is important for your code
survey.attrs['...'] = ...

# Save it under <{model}_{code}.nc>
model = ...  # 'layered' or 'block'
code = ...   # 'custEM', 'emg3d', 'PETGEM', or 'SimPEG'
#            # custEM/PETGEM: you can add a '_{p}', where p = 'p1' or 'p2'
survey.to_netcdf(f"../results/{model}_{code}.nc",
                 invalid_netcdf=True, engine='h5netcdf')
```


## Info

Every code should store its info directly in the data (`survey.attrs[]`) under
the following keywords:
- 'runtime': Elapsed real time (wall time), in s
- 'cputime'; Total runtime, in s (for parallel comp. much higher than runtime)
- 'nthreads': Number of threads used
- 'maxram': Max RAM used
- 'ncell': Number of cells (for emg3d/SimPEG)
- 'nedges': Number of edges (for custEM/PETGEM)
- 'machine': Machine info, e.g. "laptop with an i7-6600U CPU@2.6 GHz (x4) and
  16 GB of memory, using Ubuntu 18.04"
- 'version': Version number of your code
- 'date': Date, use `datetime.today().isoformat()`

**Please make sure to add all info-data as indicated!**
