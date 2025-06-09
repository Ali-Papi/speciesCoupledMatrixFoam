# 📚 Automated Doxygen Documentation Pipeline for porousMedia Test Cases

> This documentation system is part of the **porousMedia** repository, a collection of test cases and solvers designed for porous media simulation using OpenFOAM.

This folder contains a set of scripts, templates, and configurations to automate the generation of styled Doxygen documentation pages for the **porousMedia repository**, using Pandoc, a custom HTML-to-Doxygen conversion workflow, and Doxygen itself.

---

## 🎯 Objectives

- Automatically generate human-readable documentation from test cases.
- Ensure each test folder is documented consistently using Markdown.
- Maintain styled and interactive HTML documentation using Doxygen.

---


## 📁 Folder Structure

```
.
├── Allwmake                        # Main build script: generates documentation
├── Allwclean                      # Cleanup script: removes generated files
├── Doxyfile                       # Doxygen configuration
├── generate_dox_indexes.py       # Recursively generates index pages for test folders
├── generate_doxygen_page_from_html.py  # Converts HTML (from Pandoc) to .dox pages
├── style/                         # Custom CSS/JS for styling Doxygen output
│   ├── custom-alternative.css
│   ├── doxygen-awesome.css
│   ├── doxygen-awesome-darkmode-toggle.js
│   ├── doxygen-awesome-fragment-copy-button.js
│   ├── doxygen-awesome-interactive-toc.js
│   ├── doxygen-awesome-paragraph-link.js
│   ├── doxygen-awesome-tabs.js
│   ├── toggle-alternative-theme.js
│   ├── header.html
│   ├── mathjax-template.html      # Template used by Pandoc
│   └── Logo.png
```

---

## 🚀 Workflow Overview

### 1. **Convert README.md to HTML**
Using `pandoc` and a custom template (`style/mathjax-template.html`), each `README.md` is converted to a clean HTML fragment.

### 2. **Convert HTML to Doxygen**
The HTML is passed to `generate_doxygen_page_from_html.py`, which performs the following:
- Extracts the title from the `<h1>` tag (marked with 📌)
- Wraps it in a Doxygen `\page` block
- Embeds the HTML inside a `\htmlonly` section

### 3. **Generate Index Pages**
The script `generate_dox_indexes.py` recursively walks through the test directories:
- Creates a `.dox` page for each folder (if no `README.md` exists)
- Adds `\subpage` references for subdirectories

### 4. **Generate Final Docs with Doxygen**
The [`Allwmake`](./Allwmake) script:
- Runs all conversions
- Calls Doxygen to generate the final HTML documentation
- Applies the styles from the `style/` folder

---

## 📜 Script Descriptions

### 🔧 [`Allwmake`](./Allwmake)
Main automation script. It:
- Checks for required tools and environment
- Converts all test `README.md` files
- Runs `generate_dox_indexes.py`
- Runs `doxygen`

### 🔧 [`Allwclean`](./Allwclean)
Cleans up generated `.dox` pages and Doxygen output.

### 🧠 [`generate_doxygen_page_from_html.py`](./generate_doxygen_page_from_html.py)
Takes raw HTML (string) and wraps it into a valid `.dox` file with proper Doxygen formatting and title detection.

### 📂 [`generate_dox_indexes.py`](./generate_dox_indexes.py)
Recursively generates index `.dox` files for directories without `README.md`, linking subpages using `\subpage`.

---

## 🎨 Custom Styling (style/)

The `style/` folder contains CSS and JS plugins to enhance Doxygen with:
- Dark mode toggle
- Copy buttons
- Interactive TOC
- Custom math rendering with MathJax
- A personalized logo and theme

---

## ✅ Requirements

- `pandoc`
- `doxygen`
- `python3`
- `OpenFOAM` environment (for `WM_PROJECT_DIR`)

---

## 🧪 Usage

```bash
# Make sure the OpenFOAM environment is loaded
source /path/to/OpenFOAM/etc/bashrc
./Allwmake
```

To clean:

```bash
./Allwclean
```

---

## 📝 Notes

- Test case folders must include a `README.md` file with a top-level `<h1>` marked like:
  ```markdown
  # 📌 Detailed Test Case Documentation: My Cool Simulation
  ```

- The `📌` marker is used to extract the title automatically.

---

## 📬 Output

After execution, the documentation is generated in the output directory specified in the `Doxyfile` (typically `html/`).

