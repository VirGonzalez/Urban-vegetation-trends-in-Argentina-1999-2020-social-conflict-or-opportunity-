# Librerías necesarias
library(sf)
library(dplyr)
library(purrr)
library(broom)
library(tibble)
library(ggplot2)
library(mgcv)
library(forestplot)
library(grid)
library(gamm4)

# Leer el shapefile
base <- st_read("datos/data_vf.shp")

# Seleccionar columnas a escalar
columns_to_scale <- c("final.weal", "Initial.Po", "final.educ", "Final.popu", 
                      "Final.Stru", "Initial.We", "Initial.Ed", "Initial.St")

# Escalar variables por ciudad
b_scaled <- base %>%
  group_by(City) %>%
  mutate(across(all_of(columns_to_scale), ~ scale(.x)))

# Calcular cambios escalados
b_scaled$Education. <- b_scaled$final.educ - b_scaled$Initial.Ed
b_scaled$Wealth.Cha <- b_scaled$final.weal - b_scaled$Initial.We
b_scaled$Structural <- b_scaled$Final.Stru - b_scaled$Initial.St
b_scaled$Population <- b_scaled$Final.popu - b_scaled$Initial.Po

# Guardar shapefile modificado
st_write(b_scaled, "data_scaled.shp")

# Crear modelos GAM por ciudad
models_by_city <- b_scaled %>%
  split(.$City) %>%
  map(~ list(
    model = gam(Relative.v ~ te(x, y) +
                  Population + Education. + 
                  Wealth.Cha + Structural + Initial.Po + Initial.We +
                  Initial.Ed + Initial.St,
                family = gaussian(), data = .x),
    city = unique(.x$City)
  ))

# Función para extraer coeficientes
extract_gam_coefs <- function(model) {
  model_summary <- summary(model)

  parametric_coefs <- model_summary$p.table %>%
    as.data.frame() %>%
    rownames_to_column(var = "term") %>%
    rename(estimate = Estimate, std.error = `Std. Error`, p.value = `Pr(>|t|)`)

  smooth_coefs <- model_summary$s.table %>%
    as.data.frame() %>%
    rownames_to_column(var = "term") %>%
    rename(estimate = edf, std.error = Ref.df, p.value = `p-value`)

  bind_rows(parametric_coefs, smooth_coefs)
}

# Aplicar función a cada modelo
coef_by_city <- models_by_city %>%
  map_df(~ {
    model <- .x$model
    city <- .x$city
    extract_gam_coefs(model) %>% mutate(City = city)
  })

# Añadir asteriscos según significancia
coef_by_city <- coef_by_city %>%
  mutate(significance = case_when(
    p.value < 0.001 ~ "***",
    p.value < 0.01 ~ "**",
    p.value < 0.05 ~ "*",
    TRUE ~ ""
  ))

# Combinar estimate con asteriscos
coef_by_city <- coef_by_city %>%
  mutate(estimate_with_sig = paste0(
    round(estimate, 3),
    case_when(
      p.value < 0.001 ~ "***",
      p.value < 0.01 ~ "**",
      p.value < 0.05 ~ "*",
      TRUE ~ ""
    )
  ))

# Intervalos de confianza
coef_by_city$Upper <- coef_by_city$estimate + coef_by_city$std.error
coef_by_city$Lower <- coef_by_city$estimate - coef_by_city$std.error

# Filtrar términos no deseados
coef_by_city <- subset(coef_by_city, term != 'te(x,y)')
coef_by_city <- coef_by_city[coef_by_city$term != "(Intercept)", ]

# Configuración para forestplot
coef_by_city %>%
  group_by(City) %>%
  forestplot(
    labeltext = c("term"),
    mean = estimate,
    lower = Lower,
    upper = Upper,
    is.summary = FALSE,
    xlab = "Effect size",
    xlog = FALSE,
    xticks = c(-0.00001, 0, 0.00001),
    lwd.ci = 3,
    lwd.zero = 2,
    col = fpColors(
      box = c("#E69F00", "#56B4E9", "#009E73", "#D55E00", "#CC79A7", "black"),
      zero = "grey"
    ),
    txt_gp = fpTxtGp(
      label = gpar(fontsize = 12),
      xlab = gpar(fontsize = 18, fontface = "bold"),
      title = gpar(fontsize = 16, fontface = "bold")
    ),
    zero = 0,
    boxsize = 0.05,
    lineheight = "auto"
  ) %>%
  fp_set_zebra_style("#EFEFEF")

# Reordenar factores y renombrar términos
coef_by_city$City <- factor(coef_by_city$City, 
                            levels = c("Great Salta", "Great San Miguel de Tucuman", 
                                       "Great Rosario", "Great Cordoba", "Great Buenos Aires"))

coef_by_city$term <- factor(coef_by_city$term,
                            levels = c("Education.", "Initial.Ed", "Wealth.Cha", "Initial.We",
                                       "Structural", "Initial.St", "Population", "Initial.Po"))

levels(coef_by_city$term) <- c("Education level change", "Initial Education", "Wealth Change",
                               "Initial Wealth", "Structural Poverty Change", 
                               "Initial Structural Poverty", "Population Density Change", 
                               "Initial Population Density")

# Gráfico con ggplot2
ggplot(coef_by_city, aes(x = estimate, y = City, color = City)) +
  geom_point(size = 3) +
  geom_errorbarh(aes(xmin = Lower, xmax = Upper), height = 0.2, size = 0.7) +
  geom_text(aes(label = significance), hjust = -0.5, vjust = 0, size = 5, color = "black") +
  geom_vline(xintercept = 0, color = "gray", linetype = "solid", size = 0.5) +
  facet_wrap(~ term, ncol = 2) +
  scale_color_manual(values = c("Great Salta" = "#E69F00",
                                "Great San Miguel de Tucuman" = "#56B4E9",
                                "Great Rosario" = "#009E73",
                                "Great Cordoba" = "#D55E00",
                                "Great Buenos Aires" = "#CC79A7")) +
  labs(
    x = "Estimate",
    y = NULL,
    color = "City"
  ) +
  theme_minimal() +
  theme(
    strip.text = element_text(size = 12, face = "bold"),
    axis.text.x = element_text(size = 10),
    axis.text.y = element_blank(),
    axis.title = element_text(size = 12, face = "bold"),
    legend.position = "top"
  )
