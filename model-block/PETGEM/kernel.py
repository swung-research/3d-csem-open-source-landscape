#!/usr/bin/env python3
# Author:  Octavio Castillo Reyes
# Contact: octavio.castillo@bsc.es
''' **PETGEM** kernel for 3D CSEM forward modelling using higg order
vector elements.
'''

if __name__ == '__main__':
    # ---------------------------------------------------------------
    # Load python modules
    # ---------------------------------------------------------------
    import sys
    import petsc4py
    import numpy as np
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
    # Initialize preprocessing and timers
    # ---------------------------------------------------------------
    Print.master(' ')
    Print.master('  Data preprocessing')

    # Create a preprocessing instance and output directory
    preprocessing = Preprocessing()

    # Run preprocessing
    preprocessing.run(inputSetup)

    # ---------------------------------------------------------------
    # Initialize and execute the solver
    # ---------------------------------------------------------------
    Print.master(' ')
    Print.master('  Run modelling')

    # Create a solver instance
    csem_solver = Solver()

    # Setup solver (import files from preprocessing stage)
    csem_solver.setup(inputSetup)

    # Assembly linear system
    csem_solver.assembly(inputSetup)

    # Set dirichlet boundary conditions
    csem_solver.solve()

    # Compute electromagnetic responses
    csem_solver.postprocess(inputSetup)

    # ---------------------------------------------------------------
    # End of PETGEM kernel
    # ---------------------------------------------------------------
