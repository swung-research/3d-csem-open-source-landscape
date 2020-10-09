Reproduce the results by Correa and Menezes (2018) with PETGEM
==============================================================

1. Download the resistivity data, topography information, and survey data
   without noise from

   https://zenodo.org/record/400233

   The following files are required to be stored in the "DATA"
   directory as relative path from the PETGEM files location.

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

3. Run Tetgen for mesh generation (vtk output format):

   > ./tetgen -pq1.6aAk marlim.poly

4. Compute p2 solutions with a suitable number of mpi4py tasks (hybrid
   scheme with OpenMP is not supported). Recommended are 96 MPI tasks,

   With following input files:

    - params.yaml --> model parameters
    - marlim.vtk --> tetrahedral mesh

   Run the preprocessing (sequential task):

   > python run_preprocessing.py params.yaml

   Run modeling (parallel task):

   > mpirun -n 96 python3 kernel.py -options_file petsc.opts params.yaml


5. Access modeling results and save these data in the common NetCDF format
   in the results directory. Run:

   > python3 export_netcdf.py
