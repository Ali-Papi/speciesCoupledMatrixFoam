
# 📌 porousMedia Repository Documentation
[![DOI](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2501.19076-blue)](https://doi.org/10.48550/arXiv.2501.19076)
[![BibTeX](https://img.shields.io/badge/BibTeX-citation.bib-orange)](citation.bib)

## 🚀 Overview

The **porousMedia** repository, developed by **WIKKI Brasil**, contains a set of computational tools and test cases designed for advanced simulations of multiphase flows in porous media. It employs robust numerical methods for scenarios involving complex physics such as capillary pressure effects, gravity, and heterogeneous media properties.

This project is intended for researchers, engineers, and developers working on numerical modeling of multiphase flow in porous media using the OpenFOAM/foam-extend ecosystem.

---

## 🔬 CoupledMatrixFoam Solver

The repository introduces `coupledMatrixFoam`, an advanced fully implicit solver based on the Euler-Euler multifluid formulation combined with Darcy’s law. Key features of this solver include:

- **Implicit coupling** of phase fraction and pressure equations.
- Enhanced **numerical stability** allowing significantly larger time steps.
- Compatibility with `foam-extend` **(OpenFOAM) version 5.0**.
- **Implicit treatment** of Darcy and capillary pressure terms.
- Modeling of the porous medium as a stationary phase within the Euler-Euler framework.
- Linearization of nonlinear terms using Taylor series expansions for robust numerical solutions.

For in-depth details regarding mathematical modeling, numerical formulations, and validations, consult the related reference:

- **Lange, R. et al. (2025).** *coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend.*

---

## ⚙️ Installation Instructions

### Requirements

- **foam-extend-5.0** ([foam-extend installation](http://wikki.co.uk/index.php/foam-extend-5-0/))
- Python libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`

### Installation Steps


1. Source the foam-extend environment:

```bash
source /path/to/foam-extend-5.0/etc/bashrc
```

2. Navigate to the `coupledMatrixFoam` directory and compile the solver:

```bash
./Allwmake -jX
```
> 💡 Replace `X` with the number of processors to use (e.g., `-j4`). Leave blank to use all available processors.

3. Executables and libraries:

- Dynamic libraries are installed in `$FOAM_USER_LIBBIN`
- The solver executable is installed in `$FOAM_USER_APPBIN`

4. Test the solver installation by executing provided test cases in their respective directories:

```bash
./Allrun
```
5. To clean the solver compilation and temporary files:

```bash
./Allwclean
```

---

## 📚 Generate C++ Documentation with Doxygen

Follow these steps to generate the C++ code documentation along with integrated test case pages using Doxygen:

1. Install Doxygen and dependencies (Debian-based systems):

```bash
sudo apt update && sudo apt install doxygen graphviz pandoc
```

> 🧠 `pandoc` is required to convert test case `README.md` files into HTML fragments embedded in the documentation.

2. Load the `foam-extend-5.0` environment and repository-specific settings:

```bash
source /path/to/foam-extend-5.0/etc/bashrc
source /path/to/porous-media/etc/bashrc
```

3. Navigate to the documentation directory:

```bash
cd doc/Doxygen
```

> ⚠️ Ensure scripts are executable. If needed:

```bash
chmod +x Allwmake Allwclean
```

4. Generate the documentation:

```bash
./Allwmake -j
```

This script will:
- Convert each test case `README.md` into embedded Doxygen pages using Pandoc.
- Generate `.dox` files under `doc/pages/` with rich HTML content, including MathJax equations.
- Build the full documentation using Doxygen, including solver internals and test case descriptions.

5. Open the generated documentation in a browser:

```bash
xdg-open html/index.html
```

6. (Optional) Clean generated documentation and intermediate files:

```bash
./Allwclean
```

---

## 🧪 Test Case Documentation

Detailed descriptions of individual test cases can be found in the following files:


- 📄 Heterogeneous Buckley-Leverett
  ↳ [View Markdown](tests/BuckleyLeverett/heterogeneous/README.md)

- 📄 Homogeneous Buckley-Leverett
  ↳ [View Markdown](tests/BuckleyLeverett/homogeneous/README.md)

- 📄 Buckley-Leverett with Capillarity
  ↳ [View Markdown](tests/BuckleyLeverett/homogeneousCapillarity/README.md)

- 📄 Capillary-Gravity Equilibrium
  ↳ [View Markdown](tests/capillarityGravityEquilibrium/README.md)

- 📄 Core Case with Capillarity
  ↳ [View Markdown](tests/coreCase/README.md)

---

## 📑 References

- **Lange, R. et al. (2025).** *coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend.* [arXiv:2501.19076](https://arxiv.org/abs/2501.19076)

---

## 🧾 Citation

Please cite the following article when using this software in research:

> Lange, R.; Magalhães, G. M.; Rocha, F. F.; Ribeiro Neto, H. (2025).
> *coupledMatrixFoam: an advanced fully-implicit solver for heterogeneous porous media based on foam-extend.*
> [arXiv:2501.19076](https://arxiv.org/abs/2501.19076) — DOI: [10.48550/arXiv.2501.19076](https://doi.org/10.48550/arXiv.2501.19076)

📚 BibTeX entry available at [citation.bib](citation.bib)

---

## 📄 License

This project is licensed under the terms of the
[GNU General Public License v3.0](./LICENSE).
It is derived from `foam-extend`, which is distributed under the same license.

You are free to use, modify, and distribute this software under the conditions described in the license, provided that any derivative work remains under the same terms.

---

## 📞 Support and Contributions

We welcome questions, bug reports, feature suggestions, and contributions from the community.

- 💬 **Support:** If you encounter issues or have questions, please use the [GitLab issue tracker](https://gitlab.com/wikki.brasil/porousmedia/issues) to report them. Make sure to provide enough context (logs, system info, steps to reproduce).
- 👷 **Contributions:** Contributions are highly appreciated! Please read our [CONTRIBUTING](CONTRIBUTING) guidelines before submitting a merge request.
- 🧪 **How you can help:**
  - Report bugs or unexpected behavior.
  - Propose or implement new test cases.
  - Improve documentation, including test case descriptions.
  - Review and test open merge requests.

📋 See our [Code of Conduct](CODE_OF_CONDUCT.md) and [Changelog](CHANGELOG.md) for community standards and release history.

Let’s build robust porous media simulation tools together!