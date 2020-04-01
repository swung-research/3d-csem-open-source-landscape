Reproduce the results by Correa and Menezes (2018) with custEM
==============================================================

1. download the resistivity data, topography information, and survey data 
   without noise from 

   https://zenodo.org/record/400233
   
   The following files are required to be stored in the "mode-marlim/DATA"
   direcgtory (or "../DATA") as relative path from the custEM files location.

   Sea_Bottom-mr3d.xyz
   Miocene-mr3d.xyz
   Oligocene-mr3d.xyz
   Blue_mark-mr3d.xyz
   Top_of_Salt-mr3d.xyz
   Base_of_salt-mr3d.xyz
    
   Horizontal_resistivity.sgy
   Vertical_Resistivity.sgy
   EW_nonoise.zip  # extract zip file in the directory `EW_nonoise`!
   
2. Run: 

   > python modify_marlim_input_data.py
    
3. Run:
    
   > python mesh_marlim_reciprocal.py

4. compute p2 solutions with a suitable number of mpi4py processes and
   OpenMP threads, recommended are 16 x 4, but less is also fine without 
   increasing the computation times significantly. With this recommended
   setup, ~20 min time per frequency and overall less than 700 GB RAM
   are required. Run the following commands (choose given default or
   your own customized number of OMP and MPI processes):
   
   > export OMP_NUM_THREADS=4
   > mpirun -n 16 python -u run_marlim_reciprocal.py

5. Access modeling statistics and interpolated results and save these
   data in the common NetCDF format in the results directory. Run:
   
   > python export_netcdf.py