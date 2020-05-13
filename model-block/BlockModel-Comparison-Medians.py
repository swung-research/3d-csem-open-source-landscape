#!/usr/bin/env python
# coding: utf-8

# # Block Model with a 1D background - Comparison
# 
# ### For the model, see the notebook BlockModel.ipynb

# In[1]:


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# ## Load data

# In[3]:


def extract_lines(name):
    inp = xr.load_dataset(name, engine='h5netcdf')
    print_attributes(inp)
    out = np.stack([
        inp.line_1[::2]+1j*inp.line_1[1::2],
        inp.line_2[::2]+1j*inp.line_2[1::2],
        inp.line_3[::2]+1j*inp.line_3[1::2],
    ]).T
    return out


def print_attributes(inp):
    for key in ['runtime', 'n_procs', 'max_ram',
                'n_cells', 'n_nodes', 'n_dof', 'extent',
                'min_vol', 'max_vol', 'machine',
                'version', 'date']:
        print(f"{key:10} : {inp.attrs[key]}")


# In[4]:


ds = xr.load_dataset('block_model_and_survey.nc', engine='h5netcdf')
rec_x = ds.x[::2].data
rec_y = ds.attrs['rec_y']


# ### Semi-analytical background result from `empymod`

# In[5]:


epm_1d = extract_lines('results/layered_empymod.nc')


# ### `emg3d`

# In[6]:


# BACKGROUND
egd_bg = extract_lines('results/layered_emg3d.nc')
print(f"\n= - = - =  :  {14*'= - '}=\n")
# 3D
egd_tg = extract_lines('results/block_emg3d.nc')


# ### `PETGEM`

# In[7]:


# BACKGROUND
ptg_bg = extract_lines('results/layered_petgem.nc')
print(f"\n= - = - =  :  {14*'= - '}=\n")
# 3D
ptg_tg = extract_lines('results/block_petgem.nc')


# ### `custEM`

# In[8]:


# BACKGROUND
#cst_bg = extract_lines('results/layered_custEM_p1.nc')
cst_bg = extract_lines('results/layered_custEM_p2.nc')
print(f"\n= - = - =  :  {14*'= - '}=\n")
# 3D
#cst_tg = extract_lines('results/block_custEM_p1.nc')
cst_tg = extract_lines('results/block_custEM_p2.nc')


# ### `SimPEG`

# In[9]:


## BACKGROUND
#spg_bg = extract_lines('results/layered_simpeg.nc')
#print(f"\n= - = - =  :  {14*'= - '}=\n")
## 3D
#spg_tg = extract_lines('results/block_simpeg.nc')


# #### We plot data at offsets < min_offset

# In[10]:


min_offset = 500


# ## Compare 1D background

# # In[11]:


# # Calculate error
# error = {}
# for name, data in zip(['emg3d', 'custEM', 'PETGEM'], #, 'SimPEG'],
#                       [egd_bg, cst_bg, ptg_bg] #, spg_bg]
#                      ):
#     rerr = np.clip(100*abs((epm_1d.real-data.real)/epm_1d.real), 0.01, 100)
#     ierr = np.clip(100*abs((epm_1d.imag-data.imag)/epm_1d.imag), 0.01, 100)
#     error[name] = rerr + 1j*ierr


# # In[12]:


def get_pos_neg(resp, off, min_off):
    """Separate positive and negative values, enforce min_off."""
    resp_pos = np.array([x if x > 0 else np.nan for x in resp])
    resp_neg = np.array([-x if x < 0 else np.nan for x in resp])

    resp_pos[off < min_offset] = np.nan
    resp_neg[off < min_offset] = np.nan

    return resp_pos, resp_neg


# In[13]:


# marker = ['*', 'v', '^', 'o']

# for iy, y in enumerate(rec_y[:2]):
    
#     # Get offset
#     off = np.sqrt(rec_x**2 + y**2)

#     plt.figure(figsize=(9, 5))

#     # # Real
#     ax1 = plt.subplot(221)
#     plt.title('Real')

#     resp_pos, resp_neg = get_pos_neg(epm_1d[:, iy].real, off, min_offset)
#     plt.plot(rec_x/1e3, resp_pos, 'k-', label='empymod')
#     plt.plot(rec_x/1e3, resp_neg, 'k--')

#     plt.ylabel(r'$\Re(E_x)$ (V/m)')
#     ax1.set_xticklabels([])
#     plt.grid(axis='y', c='0.9')


#     # # Real Error
#     ax2 = plt.subplot(223)

#     for i, name in enumerate(error.keys()):
#         error[name][off < min_offset, iy] = np.nan + 1j*np.nan
#         plt.plot(rec_x/1e3, error[name][:, iy].real, f'C{i}{marker[i]}', ms=3)

#     plt.yscale('log')
#     plt.xlim(ax1.get_xlim())
#     plt.ylabel('Rel. error %')
#     plt.ylim([8e-3, 120])
#     plt.yticks([0.01, 0.1, 1, 10, 100], ('0.01', '0.1', '1', '10', '100'))
#     plt.grid(axis='y', c='0.9')
#     plt.xlabel('Offset (km)')


#     # # Imaginary
#     ax3 = plt.subplot(222, sharey=ax1)
#     plt.title('Imaginary')

#     resp_pos, resp_neg = get_pos_neg(epm_1d[:, iy].imag, off, min_offset)
#     plt.plot(rec_x/1e3, resp_pos, 'k-', label='empymod')
#     plt.plot(rec_x/1e3, resp_neg, 'k--')
    
#     plt.yscale('log')
#     plt.ylabel(r'$\Im(E_x)$ (V/m)')

#     ax3.set_xticklabels([])
#     ax3.yaxis.tick_right()
#     ax3.yaxis.set_label_position("right")
#     plt.grid(axis='y', c='0.9')


#     # # Imaginary Error
#     ax4 = plt.subplot(224, sharey=ax2)

#     for i, name in enumerate(error.keys()):
#         plt.plot(rec_x/1e3, error[name][:, iy].imag, f'C{i}{marker[i]}', ms=3)

#     # Legend
#     plt.plot(0, -1, 'k', label='empymod')
#     for i, name in enumerate(error.keys()):
#         plt.plot(0, -1, f'C{i}', label=name)
        
#     plt.yscale('log')
#     plt.xlim(ax1.get_xlim())
#     plt.xlabel('Offset (km)')
#     plt.ylabel('Rel. error (%)')
#     plt.ylim([8e-3, 120])
#     plt.yticks([0.01, 0.1, 1, 10, 100], ('0.01', '0.1', '1', '10', '100'))
#     ax4.yaxis.tick_right()
#     ax4.yaxis.set_label_position("right")
#     plt.grid(axis='y', c='0.9')

#     # Switch off spines
#     ax1.spines['top'].set_visible(False)
#     ax1.spines['right'].set_visible(False)
#     ax2.spines['top'].set_visible(False)
#     ax2.spines['right'].set_visible(False)
#     ax3.spines['top'].set_visible(False)
#     ax3.spines['left'].set_visible(False)
#     ax4.spines['top'].set_visible(False)
#     ax4.spines['left'].set_visible(False)

#     plt.tight_layout()
#     plt.legend(loc=2, ncol=2, bbox_to_anchor=(-0.4, 1.2), framealpha=1)
    
#     #plt.savefig(f'../manuscript/figures/results-layered-{int(y/1e3)}.pdf', bbox_inches='tight')
#     plt.suptitle(f'Receiver-line: {y/1e3} km')
#     plt.show()


# ## Compare 3D model

# In[14]:


# Collect data 
# ! HACKED so far not available SIMPEG data  !
    
spg_tg = np.zeros((101, 3), dtype=complex)
spg_tg[:, :].real = np.nan
spg_tg[:, :].imag = np.nan
data = [egd_tg, spg_tg, cst_tg, ptg_tg]

    
# In[15]:


# Calculate normalized difference between all models
nn = 4
medians = np.ones((nn+1, nn+1), dtype=float)
for i in range (4):
    for j in range(4):
        if i > j:
            medians[i, j] = np.median(200*abs(data[i].real - data[j].real) /
                             (abs(data[i].real) + abs(data[j].real)))
        elif j > i:
            medians[i, j] = np.median(200*abs(data[i].imag - data[j].imag) /
                             (abs(data[i].imag) + abs(data[j].imag)))
        else:
            medians[i, j] = np.nan

# In[16]:


M, N = np.meshgrid(np.arange(nn + 1), np.arange(nn + 1))
labels = ['EGD', 'SPG', 'CST', 'PTG']
cmap = plt.get_cmap('Oranges')
cmap.set_bad(color = '0.6', alpha = 1.) # main diagonal irrelevant

for iy, y in enumerate(rec_y):

    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(6, 6))

    obj = ax.pcolormesh(M, N, medians, cmap=cmap, norm=LogNorm(),
                        vmin=1e-1, vmax=1e1)

    ax.set_yticklabels(labels)
    ax.set_xticklabels(labels, rotation='vertical')
                                                               
    ax.set_xticks(np.arange(nn) + 0.5)
    ax.set_yticks(np.arange(nn) + 0.5)
    ax.xaxis.tick_top()
    ax.set_xlim([0., nn])
    ax.set_ylim([nn, 0.])
    ax.axis('equal')
    ax.set_adjustable('box')

    plt.colorbar(obj, ax=ax, label='median (error (%))',
                 orientation='vertical', extend='both')
    plt.savefig(f'../manuscript/figures/median-stats-block-{int(y/1e3)}.pdf',
                bbox_inches='tight')
    plt.suptitle(f'Receiver-line: {y/1e3} km')
    plt.show()

