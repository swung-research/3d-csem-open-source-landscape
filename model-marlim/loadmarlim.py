"""
Load Marlim R3D Data
====================

You have to download the data yourself and put them into the directory
`model-marlim/DATA/`. This file just loads them and puts them on a discretize
mesh.

Links to download:

- Detailed resistivity model: https://doi.org/10.5281/zenodo.400233
- Computational resistivity model (upscaled and extended):
  https://doi.org/10.5281/zenodo.3748492
- CSEM data with noise: https://doi.org/10.5281/zenodo.1256787
- CSEM data without noise: https://doi.org/10.5281/zenodo.1807135
"""
import segyio
import discretize
import numpy as np
import xarray as xr
from os.path import abspath


def extract_model(model='orig'):
    """Extract original or computational model of Marlim R3D and store as npz.

    Extracts the original fine model or the computational model from the
    sgy-fiels and stores them as numpy-compressed npz files.

    Parameters
    ----------
    model : str; {<'orig'>; 'comp'}
        If model=='comp', the computational model is returned. Else the
        original model.
    """

    if model == 'comp':
        name_h = 'Mrl3d_Rh_20metersmesh.segy'
        name_v = 'Mrl3d_Rv_20metersmesh.segy'
        dx, dy, dz = 100, 100, 20  # Cell widths
    else:
        name_h = 'Horizontal_resistivity.sgy'
        name_v = 'Vertical_Resistivity.sgy'
        dx, dy, dz = 25, 75, 5  # Cell widths

    # Load horizontal and vertical cubes
    try:
        # Load and swap z for positive upwards
        res_h = segyio.tools.cube(abspath('./DATA/'+name_h))[:, :, ::-1]
        res_v = segyio.tools.cube(abspath('./DATA/'+name_v))[:, :, ::-1]
    except FileNotFoundError:
        s = "    "
        txt = f"\n{3*s}** DATA NOT FOUND! **\n\n"
        txt += f"{s}You have to download the data first and\n"
        txt += f"{s}place it in `model-marlim/DATA`.\n\n"
        txt += f"{s}For model='orig' you need\n"
        txt += f"{s}- Horizontal_resistivity.sgy\n"
        txt += f"{s}- Vertical_Resistivity.sgy\n"
        txt += f"{s}from https://doi.org/10.5281/zenodo.400233\n\n"
        txt += f"{s}For model='comp' you need\n"
        txt += f"{s}- novo_mrl3d_H_Z_meters.segy\n"
        txt += f"{s}- novo_mrl3d_Zmeters.segy\n"
        txt += f"{s}from https://doi.org/10.5281/zenodo.3748492\n"
        print(txt)
        return None, None

    # Reshape
    if model != 'comp':
        res_h = np.transpose(res_h[::-1, :, :], (1, 0, 2))
        res_v = np.transpose(res_v[::-1, :, :], (1, 0, 2))

    # Define number of cells and cell widths
    nx, ny, nz = res_h.shape

    # Extract origin
    x0 = 1e100
    y0 = 1e100
    with segyio.open('DATA/'+name_h) as f:
        for i in range(nx*ny):
            if f.header[i][segyio.TraceField.CDP_X] < x0:
                x0 = f.header[i][segyio.TraceField.CDP_X]
            if f.header[i][segyio.TraceField.CDP_Y] < y0:
                y0 = f.header[i][segyio.TraceField.CDP_Y]
    x0, y0 = x0/10, y0/10

    # Initialize mesh
    mesh = discretize.TensorMesh(
        [np.ones(nx)*dx, np.ones(ny)*dy, np.ones(nz)*dz],
        x0=[x0, y0, 'N'])

    # Save it
    np.savez_compressed(
            f"marlim_{model}.npz",
            hx=mesh.hx, hy=mesh.hy, hz=mesh.hz, x0=mesh.x0,
            res_h=res_h, res_v=res_v
    )


def extract_section():
    """Extract original or computational model of Marlim R3D and store as npz.

    Extracts the original fine model or the computational model from the
    sgy-fiels and stores them as numpy-compressed npz files.

    Parameters
    ----------
    model : str; {<'orig'>; 'comp'}
        If model=='comp', the computational model is returned. Else the
        original model.
    """

    # Get original mesh and resistivities.
    try:
        data = np.load('marlim_orig.npz')
    except:
        extract_model(model='orig')
        data = np.load('marlim_orig.npz')

    full_res_h = data['res_h']
    full_res_v = data['res_v']
    mesh = discretize.TensorMesh(
            [data['hx'], data['hy'], data['hz']], x0=data['x0'])
    del data

    # Get chosen data and extract the y-coordinate; find corresponding index.
    try:
        data = xr.load_dataset('marlim_data.nc', engine='h5netcdf')
    except:
        create_survey(store_data=True, noise=False)
        data = xr.load_dataset('marlim_data.nc', engine='h5netcdf')

    ycoord = data.attrs['rec_y']
    ny = np.argmin(abs(mesh.vectorCCy - ycoord))
    del data

    # Store relevant sections.
    res_h = full_res_h[:, ny, :]
    res_v = full_res_v[:, ny, :]
    del full_res_h, full_res_v

    # Save it.
    np.savez_compressed(
            f"marlim_sections.npz",
            hx=mesh.hx, hy=np.array([10]), hz=mesh.hz,
            x0=np.array([mesh.x0[0], ycoord-5, mesh.x0[2]]),
            res_h=res_h, res_v=res_v
    )


def load_data(noise=False):
    """Load CSEM data for our selected source and receiver positions.

    Parameters
    ----------
    noise : bool
        If True, noisy data is loaded, else the clean data. Default is clean.


    Returns
    -------
    data_il, data_bs : DataArray
        The data in an xarray-DataArray

    """
    if noise:
        name = 'EW_Survey/AddedNoise/'
        suffix = 'addednoise'
    else:
        name = 'EW_nonoise/Synthetic/'
        suffix = 'windowed'

    try:
        path = 'DATA/'+name
        inline = 'mr3d_04Tx013a_04Rx251a_'+suffix+'.nc'
        broadside = 'mr3d_04Tx014a_04Rx251a_'+suffix+'.nc'
        data_il = xr.load_dataset(abspath(path+inline))
        data_bs = xr.load_dataset(abspath(path+broadside))

    except FileNotFoundError:
        s = "    "
        txt = f"\n{3*s}** DATA NOT FOUND! **\n\n"
        txt += f"{s}Download the file `EW_nonoise.zip` (`noise=False`)\n"
        txt += f"{s}or the file `EW_Survey.zip` (`noise=True`), place\n"
        txt += f"{s}it in `model-marlim/DATA/`, und unzip it there.\n"
        txt += f"{s}Links:\n"
        txt += f"{s}- With noise: https://doi.org/10.5281/zenodo.1256787\n"
        txt += f"{s}- Without noise: https://doi.org/10.5281/zenodo.1807135\n"
        print(txt)
        return None, None

    return data_il, data_bs


def create_survey(store_data=False, noise=False):
    """Create survey from by extracting info from original data."""

    # Load the data
    data_il, data_bs = load_data(noise)

    # The data was stored in NetCDF, which can't handle complex data.
    # So it is stored in `complex_demod`: [real, imag, real, imag, ...]
    em_il = data_il.emf[::2, :] + 1j*data_il.emf[1::2, :]
    em_bs = data_bs.emf[::2, :] + 1j*data_bs.emf[1::2, :]

    # Get source positions
    src_x_il = np.unique(data_il['srcpos'].data[:, 0])
    src_x_bs = np.unique(data_bs['srcpos'].data[:, 0])

    # Exclude source positions close to receiver
    off_il = abs(src_x_il - data_il.x_r) > 750
    off_bs = abs(src_x_bs - data_bs.x_r) > 750

    # Broadside has two receivers less, remove them
    xco, int_il, int_bs = np.intersect1d(
        src_x_il[off_il], src_x_bs[off_bs], return_indices=True)
    noff = xco.size

    src_x_il = src_x_il[off_il][int_il]
    src_x_bs = src_x_bs[off_bs][int_bs]

    # y-coordinate (Northing) is a single value
    src_y_il = np.unique(data_il['srcpos'].data[:, 1])
    src_y_bs = np.unique(data_bs['srcpos'].data[:, 1])

    # z-coordinate
    src_z_il = -np.unique(data_il['srcpos'].data[:, 2])[off_il][int_il]
    src_z_bs = -np.unique(data_bs['srcpos'].data[:, 2])[off_bs][int_bs]

    # Collect them
    src_il = [src_x_il, src_y_il, src_z_il]
    src_bs = [src_x_bs, src_y_bs, src_z_bs]

    s = "    "
    print(f"\n{s}                   Inline     Broadside")
    print(f"{s}recid       :: {data_il.attrs['recid']:>10}   "
          f"{data_bs.attrs['recid']:>10}")
    print(f"{s}lineid      :: {data_il.attrs['lineid']:>10}   "
          f"{data_bs.attrs['lineid']:>10}")
    print(f"{s}src-y (N)   :: {src_y_il[0]:>10.1f}   {src_y_bs[0]:>10.1f}")
    print(f"{s}rec-x (E)   :: {data_il.x_r:>10.1f}   {data_bs.x_r:>10.1f}")
    print(f"{s}rec-y (N)   :: {data_il.y_r:>10.1f}   {data_bs.y_r:>10.1f}")
    print(f"{s}rec-z (Z)   :: {data_il.z_r:>10.1f}   {data_bs.z_r:>10.1f}")
    print()
    print(f"{s}nr. offsets :: {src_x_il.size:10}   {src_x_bs.size:10}")
    print()
    print(f"{s}frequencies :: {data_il.freqs} Hz")
    print(f"{s}components  :: {data_il.emf.emf_fieldtype.split()}")

    # Initiate data with zeros
    dataset = {}
    for i, data in enumerate([data_il, data_bs]):
        lineid = ['data_il', 'data_bs'][i]
        dataset[lineid] = xr.DataArray(
            data=np.zeros((noff*2, data.freqs.size, 6), dtype=float),
            dims=['src_x', 'freqs', 'components'],
            coords={
                'src_x': np.vstack([xco, xco]).ravel('F'),
                'freqs': data.freqs,
                'components': data_il.emf.emf_fieldtype.split()},
        )
        dataset[lineid].attrs['src_y'] = [src_il, src_bs][i][1]
        dataset[lineid].attrs['src_z'] = [src_il, src_bs][i][2]
        dataset[lineid].attrs['lineid'] = data.attrs['lineid']

    # Create a Dataset from the DataArray
    ds = xr.Dataset(dataset)

    # Add general survey information
    ds.attrs['strength'] = 1.0       # Normalized
    ds.attrs['src_theta'] = 0.0
    ds.attrs['src_dip'] = 0.0
    ds.attrs['rec_x'] = data_il.x_r
    ds.attrs['rec_y'] = data_il.y_r
    ds.attrs['rec_z'] = -data_il.z_r
    ds.attrs['rec_theta'] = 0.0
    ds.attrs['rec_dip'] = 0.0

    # Add meta data (see README for more info)
    # We don't fill it out here as this is only dummy data
    ds.attrs['runtime'] = 'N/A'
    ds.attrs['n_procs'] = 'N/A'
    ds.attrs['max_ram'] = 'N/A'
    ds.attrs['n_cells'] = 'N/A'
    ds.attrs['n_nodes'] = 'N/A'
    ds.attrs['n_dof'] = 'N/A'
    ds.attrs['extent'] = 'N/A'
    ds.attrs['min_vol'] = 'N/A'
    ds.attrs['max_vol'] = 'N/A'
    ds.attrs['machine'] = 'N/A'
    ds.attrs['version'] = 'N/A'
    ds.attrs['date'] = 'N/A'

    # Store to disk
    ds.to_netcdf(f'marlim_survey.nc', engine='h5netcdf')

    # Store data too
    if store_data:

        # Re-arrange data
        nil = int(em_il[:, 0].size/6)
        tmp_il = em_il.data.reshape(nil, -1, 6, order='F')
        tmp_il = tmp_il[off_il, :, :][int_il, :, :]

        nbs = int(em_bs[:, 0].size/6)
        tmp_bs = em_bs.data.reshape(nbs, -1, 6, order='F')
        tmp_bs = tmp_bs[off_bs, :, :][int_bs, :, :]

        # Store data
        ds.data_il.data[::2, :, :] = tmp_il.real
        ds.data_il.data[1::2, :, :] = tmp_il.imag

        ds.data_bs.data[::2, :, :] = tmp_bs.real
        ds.data_bs.data[1::2, :, :] = tmp_bs.imag

        # Delete our meta-data
        del ds.attrs['runtime']
        del ds.attrs['n_procs']
        del ds.attrs['max_ram']
        del ds.attrs['n_cells']
        del ds.attrs['n_nodes']
        del ds.attrs['n_dof']
        del ds.attrs['extent']
        del ds.attrs['min_vol']
        del ds.attrs['max_vol']
        del ds.attrs['machine']
        del ds.attrs['version']
        del ds.attrs['date']

        # Store to disk
        if noise:
            add = '_noise'
        else:
            add = ''

        ds.to_netcdf(f'marlim_data{add}.nc', engine='h5netcdf')
