# Urban_Greening_ms

# Socioeconomic Change Analysis Using GAM Models by City

This project analyzes socioeconomic changes across major Argentine cities using Generalized Additive Models (GAM). It uses spatial `.shp` data to model changes in education, wealth, structural poverty, and population density—scaled by city—along with visualizations of model coefficients and their statistical significance.

---

## 📁 Files

- `gam_effects_by_city.R`: Main R script containing the complete data processing, modeling, and visualization pipeline.
- `data_scaled.shp`: Scaled shapefile with transformed variables by city (generated during script execution).
- `datos/data_vf.shp`: Original input shapefile (not included for size or licensing reasons; place manually in the `datos/` folder).

---

## 🔧 Requirements

The following R packages are required:

---

## ▶️ How to Run
Ensure that the input shapefile data_vf.shp is located inside a datos/ folder.

Open the gam_effects_by_city.R script in RStudio or your preferred R environment.

Run the script. It will:

Load and scale the data by city.

Compute changes (delta) in variables between initial and final states.

Fit GAM models for each city separately.

Extract model coefficients and assess significance.

Generate forest plots and facet plots to visualize results.
---
## 📊 Expected Output
GAM models fitted per city.

A tidy table with coefficients, standard errors, p-values, and significance indicators.

Visual plots showing the effect size of each variable on Relative.v, stratified by city.
---
## 🌆 Cities Analyzed
Great Buenos Aires

Great Córdoba

Great Rosario

Great San Miguel de Tucumán

Great Salta
---
## 📝 Notes
Non-informative terms like te(x,y) and intercepts are excluded from plots.

It's recommended to run the script in a clean R session to avoid object conflicts.
---
## 📬 Contact
For questions, comments, or collaborations, contact virginiagonzalez782@gmail.com.
