# 📌 Detailed Test Case Documentation: Capillary-Gravity Equilibrium

## 🎯 Objective

The objective of this test case is to verify numerically the correct behavior of the **capillary pressure and gravity** terms in a multiphase flow through porous media. Specifically, the test aims to validate the solver's ability to capture the **equilibrium** between gravitational and capillary forces in a vertical, one-dimensional porous medium domain. Results obtained from the numerical simulation are compared against an **analytical equilibrium solution** and a **numerical solution obtained using `impesFoam`**.

---

## ℹ️ How to Use This Guide

This guide describes how to set up, run, and post-process the **Capillary-Gravity Equilibrium** test using **`coupledMatrixFoam`** in foam-extend 5.0:

1. **Files Overview** – Understand the main configuration files, especially how water and gas saturation are defined in `setFieldsDict`.
2. **Numerical Setup** – Learn about the saturation variation, other rock/fluid properties, and boundary conditions.
3. **Case Execution** – Steps to generate the mesh, apply piecewise water and gas saturation fields using `setFields`, run the solver, and post-process the results.
4. **Post-processing and Validation** – Compare simulation results with the analytical and reference solutions.

By the end, you will have a clear sense of how well the solver captures the capillary-gravity equilibrium.

---

## 📖 Test Case Description

- **Domain:** 1D along the Y-axis, with:
  - **Length (Y):** `1.0 m`
  - **Width and Depth (X and Z):** `0.05 m × 0.05 m`
- **Initial saturation:** The domain is split into different subregions (e.g., using `setFieldsDict`) with **piecewise-constant saturations**. For instance:
  - Lower half (`0 ≤ y ≤ 0.5 m`): partially saturated with water (`Sw = 0.5`, `Sg = 0.5`)
  - Upper half (`0.5 < y ≤ 1.0 m`): initially dry (`Sw = 0`, `Sg = 1`)

The test evaluates if the solver achieves the expected equilibrium between gravity (which tends to pull water downwards) and capillary forces (which tend to move water upwards).

---

## 🛠️ Solver Description

The case uses **`coupledMatrixFoam`**, a fully implicit solver based on an Euler-Euler multifluid formulation and Darcy’s law for each phase flowing through the porous medium. Key features include:

- **Implicit coupling** of phase-fraction and pressure equations.
- **Numerical stability** even for relatively large time steps.
- **Based on foam-extend (OpenFOAM) 5.0**.

For more details on the solver’s formulation and block-coupled approach, see the references at the end.

---

## ⚙️ Files Overview

### 1. Initial and Boundary Condition Files (folder `0.orig`)
- **`alpha.gas`** and **`alpha.water`**: Gas and water phases volumetric fractions.
- **`alpha.rock`**: Rock phase volumetric fraction. In this case, it is defined as the complement of porosity ($\alpha_{rock} = 1 - \phi$).
- **`invK.rock`**: Normalized absolute permeability inverse (multiplied by `factor`).
- **`p`**: Normalized pressure field in the domain (multiplied by `factor`).
- **`U.gas`** and **`U.water`**: Gas and water phases interstitial velocities.

### 2. Property Files (folder `constant`)
- **`phaseProperties`**: Physical properties of the phases (density, viscosity), relative permeability model (e.g., Brooks-Corey), and normilized capillary pressure model (also normalized by `factor`).
- **`g`**: Normalized gravity vector (also normalized by `factor`).

### 3. Post Processing Files (folder `scripts`)
- **`impes.csv`**: CSV file with the reference solution obained using `impesFoam`.
- **`postProc.py`**: Python script that compares the numerical solution with the analytical and reference solution.

### 4. Configuration Files (folder `system`)
- **`controlDict`**: Controls simulation time parameters (start, end, deltaT) and output frequency.
- **`fvSolution`**: Sets tolerances and solvers (e.g., PCG, BiCGStab).
- **`fvSchemes`**: Specifies discretization (grad, div, laplacian) and interpolation schemes.
- **`sampleDict`**: Configures data extraction (e.g., saturation profiles) for later comparison.
- **`blockMeshDict`**: Configures the structured computational mesh (dimensions, number of cells).
- **`setFieldsDict`**: This is central to the initial saturation definition. It defines the subregions (by coordinate boxes) and assigns different phase volume fractions values accordingly. The `alpha.gas` and `alpha.water` files must be modified by the setFields utility. The initial conditions defined on `0.orig/alpha.gas` and `0.orig/alpha.water` will be completely modified by `setFields` utility based on the information defined in the `setFieldsDict` file:

```plaintext
regions
(
    boxToCell
    {
        box                           (-1e20 -1e20 -1e20) ( 1e20 0.5 1e20);
        fieldValues
        (
            volScalarFieldValue alpha.gas 0.25
            volScalarFieldValue alpha.water 0.25
        );
    }
    boxToCell
    {
        box                           (-1e20 0.5 -1e20 ) ( 1e20 1e20 1e20);
        fieldValues
        (
            volScalarFieldValue alpha.gas 0.499
            volScalarFieldValue alpha.water 0.001
        );
    }
);
```

The `alpha.gas` `volScalarField` will have a value of 0.25 ($S_g=0.5$) in $0m \leq y \leq 0.5m$, and 0.499 ($S_g=0.998$) in $0.5m < y \leq 1.0m$, which are the region modified by the `setFields` utility. Similarly, the `alpha.water` `volScalarField` will be 0.25 ($S_w=0.5$) in $0m \leq y \leq 0.5m$, and 0.001 ($S_w=0.002$) in $0.5m < y \leq 1.0m$.

### 5. Execution Scripts
- **`Allrun`**: Main script that:
  - Generates the mesh (`blockMesh`).
  - Applies piecewise initial saturation (`setFields`).
  - Runs the `coupledMatrixFoam` solver.
  - Post-processes results (`sample` and Python script).
- **`Allclean`**: Removes previous execution results, cleaning the directory for a new run.

---

## 🔨 Detailed Numerical Setup

### 1. Porous Medium Properties
- **Porosity**: $\phi = 0.5$
- **Absolute Permeability** ($K$): $1\times10^{-11}\,\mathrm{m}^2$
- Defined in `invK.rock` as:
  $$
  invK_{rock} = \frac{1}{K} \times factor \\
  $$
  with a normalization factor of $1\times10^{-7}$. This normalization factor is used to bring the pressure values closer to the phase volume fraction values, as they are being resolved in the coupled nonlinear system.

- The rock volume fraction is defined in `alpha.rock` as:
  $$
  alpha.rock = 1 - \phi \\
  $$

### 2. Relative Permeability Model

A **Brooks-Corey** model consistent with the homogeneous Buckley-Leverett approach was used:

- **Water relative permeability**: $k_{rw} = S_w^3$
- **Oil relative permeability**: $k_{ro} = S_o^3$

This is set on `constant/phaseProperties`.

### 3. Capillarity Model

A **Brooks-Corey** model was used:

$$
  p_{c,ow} = p_{c,0} \left(\frac{\alpha_i}{\alpha_{void}}\right)^{-\beta}, \\
$$
where $p_{c,0} = 1000 Pa$ and $\beta = 0.5$.

Since the capillary pressure must also be multiplied by $factor$, we set it in `constant/phaseProperties` as follows:

$$
  p_{c,0,normalized} = p_{c,0} \times factor. \\
$$

### 4. Fluid Physical Properties

Water has a density of 1000 kg/m³ and a dynamic viscosity of 0.001 Pa·s, while
 gas has a lower density of 1 kg/m³ and a lower viscosity of 1.76e-05 Pa·s.

This is set on `constant/phaseProperties`.

### 5. Boundary Conditions

**Bottom (Y=0.0 m):**

- This is a surface where a wall is defined. So the water and gas intersticial velocities are defined as zero:
  $$
    U_w = U_g = 0.0 m/s \\
  $$

**Top (Y=1.0 m):**

- Fixed pressure boundary condition:
  $$
  p_{real} = 1 \times 10^6 \text{ Pa} \\
  $$
- Since permeability was normalized, pressure must also be normalized by the same factor:
  $$
  p_{normalized} = p_{real} \times factor \\
  $$

### 6. Gravity

- The gravity vector is set in `constant/g`. Since the permeability and the pressure were normalized, the gravity must also be normalized by the same factor:
  $$
  g_{normalized} = g_{real} \times factor \\
  $$

---

## 🚀 Case Execution

1. **Enable the environment**
   Make sure to run, for example:
   ```bash
   source /path/to/foam-extend-5.0/etc/bashrc
   ```
2. **Run `Allrun`**
   - Generates the mesh with `blockMesh`.
   - Applies heterogeneous staturations intial condition with `setFields`.
   - Executes the solver `coupledMatrixFoam`.
   - Performs data extraction for comparison with `sample`.
   - Performs comparison with `scripts/postProc.py`.


3. **Clean**
   To remove previous results and start fresh, run:
   ```bash
   ./Allclean
   ```

---

## 📊 Post-processing and Validation

- Results are post-processed with `postProc.py`. This script compares simulation results with analytical solutions, computes validation metrics (e.g., mean and max absolute errors), and generates plots for:
  - **Water Saturation (`Sw.png`)**
  - **Saturation Gradient (`dSdy.png`)**

The analytical solution for equilibrium is:

\[\frac{\partial S_w}{\partial y} = \frac{(\rho_{g}-\rho_{w}) g_y}{\frac{\partial p_c}{\partial S_w}}\]

Quantitative validation includes:
- Mean absolute error in `dS/dy`
- Max absolute error in `dS/dy`

These values are printed in the terminal after the post-processing script execution (`postProc.py`).

---

## 🧮 Analytical Reference Result

The analytical solution represents the steady-state equilibrium between gravity and capillary forces, used to verify numerical accuracy.

---

## 🧮 Model Equations (Summary)

1. **Darcy’s Law for phase $i$**:
   $$
   \alpha_i U_i = -\frac{k_{r,i}}{\mu_i} K (\nabla p_i - \rho_i g) \\
   $$
2. **Phase Mass Conservation**:
   $$
   \frac{\partial \alpha_i}{\partial t} + \nabla \cdot (\alpha_i U_i) = 0 \\
   $$
3. **Closure condition**:
   $$
   \sum_{i=1}^{n} \alpha_i = 1 \\
   $$

---

## 🏁 Conclusion

By replicating the **Capillary-Gravity Equilibrium** problem in a 1D domain, this test provides a straightforward yet robust verification of the solver’s capability to accurately capture the correct behavior of the **capillary pressure and gravity** terms in a multiphase flow through porous media.

---

## 📑 References

- **Multiphase flow modeling in multiscale porous media: An open-source micro-continuum approach** ([doi](https://doi.org/10.1016/j.jcpx.2020.100073))
- **An open-source toolbox for multiphase flow in porous media** ([doi](https://doi.org/10.1016/j.cpc.2014.10.005))
- **Lange et al. (2025)**. *coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend*.
