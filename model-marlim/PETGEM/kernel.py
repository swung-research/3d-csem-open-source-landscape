#!/usr/bin/env python3
# Author:  Octavio Castillo Reyes
# Contact: octavio.castillo@bsc.es
''' **PETGEM** kernel for 3D CSEM forward modelling using high order
vector elements.
'''

if __name__ == '__main__':
    # ---------------------------------------------------------------
    # Load python modules
    # ---------------------------------------------------------------
    import sys
    import petsc4py
    import numpy as np
    import meshio
    # ---------------------------------------------------------------
    # PETSc init
    # ---------------------------------------------------------------
    petsc4py.init(sys.argv)
    # ---------------------------------------------------------------
    # Load python modules
    # ---------------------------------------------------------------
    from petsc4py import PETSc
    # ---------------------------------------------------------------
    # Load petgem modules (BSC)
    # ---------------------------------------------------------------
    from petgem.common import Print, InputParameters, Timers
    from petgem.parallel import MPIEnvironment
    from petgem.preprocessing import Preprocessing
    from petgem.solver import Solver

    # ---------------------------------------------------------------
    # Load system setup (both parameters and dataset configuration)
    # ---------------------------------------------------------------
    # Obtain the MPI environment
    parEnv = MPIEnvironment()

    # Import parameters file
    inputSetup = InputParameters(sys.argv[3], parEnv)

    # Initialize timers
    Timers(inputSetup.output.directory)

    # ---------------------------------------------------------------
    # Print header
    # ---------------------------------------------------------------
    Print.header()

    # ---------------------------------------------------------------
    # Initialize and execute the solver
    # ---------------------------------------------------------------
    Print.master(' ')
    Print.master('  Run modelling')

    # Create a solver instance
    frequencies = inputSetup.model.frequency

    for i in np.arange(len(frequencies)):
        inputSetup.model.frequency = frequencies[i]
        csem_solver = Solver()

        # Setup solver (import files from preprocessing stage)
        csem_solver.setup(inputSetup)

        # Assembly linear system
        csem_solver.assembly(inputSetup)

        # Set dirichlet boundary conditions
        csem_solver.solve()

        # Compute electromagnetic responses
        csem_solver.postprocess(inputSetup)

        if parEnv.rank==0:
            if i==0:
                # Create file to store measures for all frequencies
                fileID_out = h5py.File(inputSetup.output.directory+'/results.h5', 'w')

                # Open file to read measures for frequency i
                fileID_in = h5py.File(inputSetup.output.directory+'/electric_fields.h5', 'r')

                data_i = fileID_in.get('electric_fields')[()].conjugate()

                # Create dataset for frequency i
                dset = fileID.create_dataset('freq'+str(frequencies[i]), data=data_i)

                fileID_out.close()
                fileID_in.close()
            else:
                # Create file to store measures for all frequencies
                fileID_out = h5py.File(inputSetup.output.directory+'/results.h5', 'r')

                # Open file to read measures for frequency i
                fileID_in = h5py.File(inputSetup.output.directory+'/electric_fields.h5', 'r')

                data_i = fileID_in.get('electric_fields')[()].conjugate()

                # Create dataset for frequency i
                dset = fileID.create_dataset('freq'+str(frequencies[i]), data=data_i)

                fileID_out.close()
                fileID_in.close()

    # ---------------------------------------------------------------
    # End of PETGEM kernel
    # ---------------------------------------------------------------
