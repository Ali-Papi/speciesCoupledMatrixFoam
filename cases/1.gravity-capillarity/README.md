## Capillary pressure verification  ##

### Introduction ###

Through this tutorial case, it is possible to verify the correct behavior of capillary pressure and gravity terms. In this tutorial, a unidimensional domain representing a simplified porous media is used to evaluate the equilibrium between capillary pressure and gravity. This case is based on the results of the following papers:

- [Multiphase flow modeling in multiscale porous media: An open-source micro-continuum approach](https://doi.org/10.1016/j.jcpx.2020.100073)
- [An open-source toolbox for multiphase flow in porous media](https://doi.org/10.1016/j.cpc.2014.10.005)

### Metodology ###

For this verification, it will be simulated a linear unidimensional case without injection to evaluate the equilibrium between capillary pressure and gravity.

The physical system is composed of two phases: gas and water. The properties of the fluid phases are given by:

- Gas:
   - $`\mu`$ = 1.76e-5 Pa.s
   - $`\rho`$ = 1 kg/m³
- Water
   - $`\mu`$ = 1.0e-3 Pa.s
   - $`\rho`$ = 1000 kg/m³

It is used a rectangular domain with dimensions of 0.05 x 1.0 x 0.05 m, discretized by a grid with 1 x 1500 x 1 cells. In the initial condition, the domain is divided into two sections with length $`L_1=L_2=0.5`$ m. In the first section, the water saturation $`(S_w)`$ and the gas saturation $`(S_g)`$ are equal to 0.5. In the second section is used $`S_w=0`$ e $`S_g=1`$.
The initial water saturation is defined far from the thermodynamic equilibrium. The section $`L_1`$ is partially saturated with water $`(S_w=0.5)`$ while the section $`L_2`$ is initially dry.

To guarantee adequate equilibrium, both fluid phases can flow freely through the superior limit of the column but not through the bottom limit. For this simplified case, the theoretical steady state can be described as the equilibrium between the capillary force and gravitational force, where gravity promotes a downside flow for the water while the capillary pressure promotes an upside flow for the water phase.

The system porosity is constant and homogeneous, defined as 0.2. The scalar absolute permeability in the y-axis (main flow direction) is constant and homogeneous, given by $`k = 1 \times 10^{-11}m^2`$ (10132.5 millidarcys).

The Brooks and Corey model is used for the capillary pressure, whit the following parameters:

$`p_c(S_w) = p_{c,0} S_w^{-\alpha} `$

| Model                   | pc,0  | $`\alpha`$ |
|-------------------------|-------|------------|
| Brooks and Corey (1964) | 1000  |     0.5    |

### Reference result ###

In this context, the analytical solution will be determined using the simplified momentum equation for a scenario where the steady state can be considered. This relation is mathematically described by:

$`\dfrac{\partial S_w}{\partial y} = \dfrac{\left(\rho_{g}-\rho_{w}\right) g_y}{\dfrac{\partial p_c}{\partial S_w} }`$

where:

- $`S_w`$: water saturation $`[m^3/m^3]`$
- $`y`$: main direction of flow $`[m]`$
- $`\rho_{g}`$: specif mass of gas $`[kg/m^3]`$
- $`\rho_{w}`$: specif mass of water $`[kg/m^3]`$
- $`g_y`$: gravity in the flow direction $`[m/s^2]`$
- $`p_c`$: capillary pressure $`[Pa]`$


It is important to explain that permeability, gravity, and pressure (including capillary pressure) values need to be rescaled. In this case, the scale factor that was applied is $`10^{-7}`$.

### Case execution

To run this tutorial it is necessary to source the foam-extend 5.0 and execute the Allrun script. In the Allrun it will be run the mesh generation, the solver calculations, and the post-process of the results. After the Allrun execution, it will be in the root of case two graphs (water saturation and dS/dy). Additionally, it will be printed in the terminal the mean and maximum absolute error for dS/dy.

The file [postProc.py](./postProc.py) contains the script to generate the graphs of water saturation and dS/dy. For the dS/dy result the analytical result is generated to compare graphically and to evaluate the mean and maximum absolute error between the numerical result and the analytical solution.
