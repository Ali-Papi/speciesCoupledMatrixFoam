# 📌 Detailed Test Case Documentation: Heterogeneous Buckley-Leverett

## 🎯 Objective

The objective of this test case is to numerically verify the accuracy of capturing the saturation front in an **immiscible two-phase flow (water-oil displacement)** within a **heterogeneous** porous medium. In this scenario, **only porosity varies** across the domain. Numerical results are compared against a **Buckley-Leverett** analytical solution adapted for a piecewise-constant porosity distribution.

---

## ℹ️ How to Use This Guide

This guide describes how to set up, run, and post-process the **Heterogeneous Buckley-Leverett** test using **`coupledMatrixFoam`** in foam-extend 5.0:

1. **Files Overview** – Understand the main configuration files, especially how porosity is defined in `setFieldsDict`.
2. **Numerical Setup** – Learn about the porosity variation, other rock/fluid properties, and boundary conditions.
3. **Case Execution** – Steps to generate the mesh, apply heterogeneous porosity fields with `setFields`, run the solver, and post-process results.
4. **Post-processing and Validation** – Compare simulation results with the analytical solution.

By the end, you will have a clear sense of how well the solver captures the water-oil displacement front.

---

## 📖 Test Case Description

- **Domain:** 1D along the Y-axis, with:
  - **Length (Y):** `0.065 m`
  - **Width and Depth (X and Z):** `0.035 m × 0.035 m`
- **Heterogeneous Porosity:** The domain is split into different subregions (e.g., using `setFieldsDict`) with **piecewise-constant porosity**. For instance:
  - $\phi = 0.2$ for $0.0\,m \leq y \leq 0.0325 \,m$
  - $\phi = 0.1$ for $0.0325\,m < y \leq 0.065\,m$
- **Initial saturation:** The domain is initially fully saturated with oil (no water present at $t=0$).

By introducing spatially varying porosity, we check if the solver correctly handles changes in pore volume and captures how the water saturation front evolves in each subregion.

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
- **`alpha.oil`** and **`alpha.water`**: Oil and water phases volumetric fractions.
- **`alpha.rock`**: Rock phase volumetric fraction. In this case, it is defined as the complement of porosity ($\alpha_{rock} = 1 - \phi$).
- **`invK.rock`**: Normalized absolute permeability inverse (multiplied by `factor`).
- **`p`**: Normalized pressure field in the domain (multiplied by `factor`).
- **`U.oil`** and **`U.water`**: Oil and water phases interstitial velocities.

### 2. Property Files (folder `constant`)
- **`phaseProperties`**: Physical properties of the phases (density, viscosity), relative permeability model (e.g., Brooks-Corey), and normilized capillary pressure model (also normalized by `factor`).
- **`g`**: Normalized gravity vector (also normalized by `factor`).

### 3. Post Processing Files (folder `scripts`)
- **`analitic.csv`**: CSV file with the analytical solution.
- **`automation.py`**: Python script that compares the numerical solution with the analytical solution.

### 4. Configuration Files (folder `system`)
- **`controlDict`**: Controls simulation time parameters (start, end, deltaT) and output frequency.
- **`fvSolution`**: Sets tolerances and solvers (e.g., PCG, BiCGStab).
- **`fvSchemes`**: Specifies discretization (grad, div, laplacian) and interpolation schemes.
- **`sampleDict`**: Configures data extraction (e.g., saturation profiles) for later comparison.
- **`blockMeshDict`**: Configures the structured computational mesh (dimensions, number of cells).
- **`setFieldsDict`**: This is central to the heterogeneous test. It defines the subregions (by coordinate boxes) and assigns different porosity values accordingly. The `alpha.rock` and `alpha.oil` files must be modified by the setFields utility. The initial conditions for `0.orig/alpha.rock` and `0.orig/alpha.oil` are uniform, with values of 0.8 and 0.2, respectively. The `setFields` utility will modify these values based on the information defined in the `setFieldsDict` file:

```plaintext
regions
(
    boxToCell
    {
        box (-1e20 0.0325 -1e20) (1e20 1e20 1e20);

        fieldValues
        (
            volScalarFieldValue alpha.rock 0.9
            volScalarFieldValue alpha.oil  0.1
        );
    }
);
```

The `alpha.rock` `volScalarField` will have a value of 0.8 in $0m \leq y \leq 0.0325m$, as defined in `0.orig/alpha.rock`, and 0.9 in $0.0325m < y \leq 0.065m$, which is the region modified by the `setFields` utility. Similarly, the `alpha.oil` `volScalarField` will be 0.2 in $0m \leq y \leq 0.0325m$, as defined in `0.orig/alpha.oil`, and 0.1 in $0.0325m < y \leq 0.065m$, which is the region modified by the `setFields` utility.

### 5. Execution Scripts
- **`Allrun`**: Main script that:
  - Generates the mesh (`blockMesh`).
  - Runs the `coupledMatrixFoam` solver.
  - Post-processes results (e.g., `sample`).
- **`Allclean`**: Removes previous execution results, cleaning the directory for a new run.

---

## 🔨 Detailed Numerical Setup

### 1. Porous Medium Properties

- **Porosity** ($\phi$):    Defined via `setFieldsDict`:
   - Region A: $0.0 m \leq y \leq 0.0325m$: $\phi = 0.2$
   - Region B: $0.0325m < y \leq0.065m$: $\phi = 0.1$

- **Absolute Permeability** ($K$): $1\times10^{-13}\,\mathrm{m}^2$
- Defined in `invK.rock` as:
  $$
  invK_{rock} = \frac{1}{K} \times factor \\
  $$
  with a normalization factor of $1\times10^{-6}$. This normalization factor is used to bring the pressure values closer to the phase volume fraction values, as they are being resolved in the coupled nonlinear system.

- The rock volume fraction is defined in `alpha.rock` as:
  $$
  alpha.rock = 1 - \phi \\
  $$

### 2. Relative Permeability Model

A **Brooks-Corey** model consistent with the homogeneous Buckley-Leverett approach was used:

- **Water relative permeability**: $k_{rw} = S_w^2$
- **Oil relative permeability**: $k_{ro} = S_o^2$

This is set on `constant/phaseProperties`.

> In a Buckley-Leverett test, these exponents produce a characteristic shock front progression.

### 3. Fluid Physical Properties

Water has a density of 1000 kg/m³ and a dynamic viscosity of 0.001 Pa·s, while
 oil has a lower density of 800 kg/m³ and a higher viscosity of 0.002 Pa·s.

These values are typical for laboratory-scale water-oil displacement experiments.
This is set on `constant/phaseProperties`.

### 4. Initial Conditions

- Oil volume fraction (`alpha.oil`) = `0.2`
- Water volume fraction (`alpha.water`) = `0`

Hence, the entire domain is initially 100% oil saturated.

### 5. Boundary Conditions

**Inlet (Y=0):**

- A constant **superficial volumetric flow rate** of water:
  $$
  U_w = 2.7102 \times 10^{-6} \, m/s \\
  $$
- Since the solver uses an interstitial flux in `U.water`, we convert:
  $$
  U_{w,interstitial} = \frac{U_w}{\phi} = 1.3551 \times 10^{-5} \text{ m}^3/s \\
  $$

**Outlet (Y=0.065 m):**

- Fixed pressure boundary condition:
  $$
  p_{real} = 1 \times 10^5 \text{ Pa} \\
  $$
- Since permeability was normalized, pressure must also be normalized by the same factor:
  $$
  p_{normalized} = p_{real} \times factor \\
  $$

### 6. Gravity

- The gravity vector is set in `constant/g`. In standard Buckley-Leverett cases, gravity is typically negligible.

---

## 🚀 Case Execution

1. **Enable the environment**
   Make sure to run, for example:
   ```bash
   source /path/to/foam-extend-5.0/etc/bashrc
   ```
2. **Run `Allrun`**
   - Generates the mesh with `blockMesh`.
   - Applies heterogeneous porosity with `setFields`.
   - Executes the solver `coupledMatrixFoam`.
   - Performs data extraction for comparison with `sample`.

3. **Clean**
   To remove previous results and start fresh, run:
   ```bash
   ./Allclean
   ```

---

## 📊 Post-processing and Validation

- **sampleDict**: Extracts water saturation values along the domain (e.g., `acrossFlow_S.water.xy`).
- **Quantitative Error Metrics**
  We suggest computing mean and maximum absolute errors compared to the analytical solution to quantify accuracy.
- **automation.py**
  This Python script (in the `scripts` folder) compares the simulation output (e.g., `../postProcessing/sets/<time>/acrossFlow_S.water.xy`) with the analytical data in `analitic.csv`, producing a saturation plot (`comp.png`).


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

By varying **only porosity** via `setFieldsDict`, this Heterogeneous Buckley-Leverett test verifies whether the solver accurately handles discontinuities in pore volume while capturing the advancing saturation front. Compare results to an adapted analytical solution that accounts for subregions of different porosity to confirm accuracy.

---

## 📑 References

- **Lange, R. et al. (2025).** *coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend*.
- **Wu, Y.-S. (2016).** “Appendix B — Program of Buckley–Leverett Solution in a Radial System and Linear and Radial Composite Systems.” *Multiphase Fluid Flow in Porous and Fractured Reservoirs*, Gulf Professional Publishing, pp. 333–355, ISBN: 978-0-12-803848-2, [doi](https://doi.org/10.1016/B978-0-12-803848-2.15002-0).
