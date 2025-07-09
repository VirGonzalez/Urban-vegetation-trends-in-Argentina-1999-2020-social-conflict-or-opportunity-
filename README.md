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

```r
install.packages(c("sf", "dplyr", "purrr", "broom", "tibble", 
                   "ggplot2", "mgcv", "gamm4", "forestplot"))
