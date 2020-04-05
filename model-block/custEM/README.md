Calculate layered earth and block model results
===============================================

1. Run the mesh generation scripts:

   > python mesh_layered.py
   > python mesh_block.py

2. compute p1 and p2 solutions with a suitable number of mpi4py processes 
   (additional OpenMP threads led not to speed-up for these problem sizes)
   Rcommended are 24 MPI processes, but less is also fine without 
   increasing the computation times significantly. With this recommended
   setup, 2-5 min time per frequency and overall less than 200 GB RAM
   are required. Run the following commands (choose given default or
   your own of OMP and MPI processes):
   
   > export OMP_NUM_THREADS=1   # no OpenMP threading
   > mpirun -n 24 python -u run_layered.py
   > mpirun -n 24 python -u run_block.py
   
3. Access modeling statistics and interpolated results and save these
   data in the common NetCDF format in the results directory. Run:
   
   > python export_netcdf.py