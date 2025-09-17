df_union <- read_csv("C:/Users/linar/Downloads/df_union.csv")
View(df_union)

library(dplyr)
library(ggplot2)
library(skimr)   # Para descripción general
library(janitor)


dim(df_union)
glimpse(df_union)
skim(df_union)


#Análisis Multivariado

# Variables categóricas: Departamento, Municipio, Régimen, Tipo de afiliado,
# Estado del afiliado, Zona de Afiliación, Género, Grupo etario, Nivel del Sisbén.

# Variables numéricas: Cantidad de registros, hash (identificador)

# Distribución por régimen
RegimenDist <- df_union %>% count(Régimen) %>% mutate(pct = n/sum(n)*100)
RegimenDist

# Hay mas personas del regimen subsidiado 1 millon hasta la fecha en Colombia

# Por género
GeneroDist <- df_union %>% count(Género) %>% mutate(pct = n/sum(n)*100)
GeneroDist

#Hay mas personas del género masculino.

# Por grupo etario
EdadDist<- df_union %>% count(`Grupo etario`) %>% arrange(desc(n))
EdadDist

# Hay mas personas en edad de trabajar 

# Régimen por género
RegimenG <- df_union %>% count(Régimen, Género)
RegimenG

# Régimen por zona
RegimenZ <- df_union %>% count(Régimen, `Zona de Afiliación`) %>% arrange(desc(n))
RegimenZ

# Régimen por Municipio
RegimenMun <- df_union %>% count(Régimen, `Departamento`)%>% arrange(desc(n))
RegimenMun

#  Estado del afiliado
EstadoAf <- df_union %>% count(Régimen, `Estado del afiliado`) 
EstadoAf


# Pirámide poblacional
Piramide <- df_union %>%
  count(Género, `Grupo etario`) %>%
  mutate(n = ifelse(Género=="Masculino", -n, n)) %>%
  ggplot(aes(`Grupo etario`, n, fill=Género)) +
  geom_col() +
  coord_flip() +
  labs(title="Pirámide de afiliados por grupo etario y género")

Piramide


# Distribución de afiliados: Predomina mas el regimen subsidiado

# Brechas territoriales: Los 5 departamentos con más cobertura son Antioquia (subsidiado), Cundianamrca (subsidiado), Antioquia (contributivo), Valle del cauca (subsidiado) y Cundianamrca (contributivo) 

# Composición etaria y de género: Hay más beneficiarios en la edad de trabajar.
  
# Zona de afiliación: hay mas subsidiados en urbana que en rural

# Estado del afiliado: activos




