# 📌 speciesCoupledMatrixFoam Repository

# 🚀 Overview
The `speciesCoupledMatrixFoam` repository, developed by the team led by Ali Papi (Gabriel Marcos Magalhaes, Amir Jahanbakhsh and Mercedes M. Maroto-Valer), is a development to `coupledMatrixFoam` solver by Lange et al. (2025)(1). `coupledMatrixFoam` solves the pressure and phase fraction equations of multiphase fluid flows in porous media. This repository simulates species transport in porous media by assuming a binary system (CO2 and H2O).
The coupling of the new code with `coupledMatrixFoam` is as follows: initially, the pressure and phase fraction values of the phases are calculated using the fully coupled approach of the `coupledMatrixFoam` solver. Then, the calculated values of pressure and phase fractions are transferred to the species transport equations (two species per each phase: 4 equations in total) in the same timestep outside of the coupled loop. So, species transport equations are decoupled from pressure and phase fraction equations to reduce the size of the coupled matrix and decrease the memory overhead. 

🔬 This project is intended for researchers, engineers, and developers working on numerical modeling of multiphase flow in porous media using OpenFOAM. It is applicable in CO2 Storage, Oil&Gas Engineering, Environmental Engineering (Underground and Soil Contamination Modelling), and Geothermal Energies.

This solver has been developed based on OpenFOAM/foam-extend ecosystem and hence has compatibility with foam-extend (OpenFOAM) version 5.0.

# ⚙️ Installation Instructions
Requirements
foam-extend-5.0 (foam-extend installation)
Python libraries:
numpy
pandas
matplotlib
Installation Steps
Source the foam-extend environment:
source /path/to/foam-extend-5.0/etc/bashrc
Navigate to the coupledMatrixFoam directory and compile the solver:
./Allwmake -jX
💡 Replace X with the number of processors to use (e.g., -j4). Leave blank to use all available processors.

Executables and libraries:
Dynamic libraries are installed in $FOAM_USER_LIBBIN
The solver executable is installed in $FOAM_USER_APPBIN
Test the solver installation by executing provided test cases in their respective directories:
./Allrun
To clean the solver compilation and temporary files:
./Allwclean


# 🧪 Test Cases
Multiple test cases have been created in the ↳ [tutorials](tutorials).

# 📄 License
This project is licensed under the terms of the GNU General Public License v3.0. It is derived from foam-extend, which is distributed under the same license.

You are free to use, modify, and distribute this software under the conditions described in the license, provided that any derivative work remains under the same terms.



(1) Lange, R.; Magalhães, G. M.; Rocha, F. F.; Ribeiro Neto, H. (2025). coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend. arXiv:2501.19076 — DOI: 10.48550/arXiv.2501.19076
