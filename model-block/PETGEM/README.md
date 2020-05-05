Calculate layered earth and block model results
===============================================

1. Run the mesh generation scripts:

   > ./gmsh -3 block_layered.geo

   Visit gmsh website to get more details about meshing tool
   (http://gmsh.info/)

2. Compute p2 solutions with a suitable number of mpi4py tasks (hybrid
   scheme with OpenMP is not supported). Recommended are 24 MPI tasks,

   With following input files:

    - params.yaml --> model parameters
    - block_layered.msh --> tetrahedral mesh
    - receiver_pos.h5 --> spatial receiver locations

   Run the following command:

   > mpirun -n 24 python3 kernel.py -options_file petsc.opts params.yaml

3. Access modeling results and save these data in the common NetCDF format
   in the results directory. Run:

   > python3 export_netcdf.py
