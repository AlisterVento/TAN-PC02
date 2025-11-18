# Práctica Calificada 2 – Análisis ANOVA sobre el Dataset Ventas de Lácteos 2024

## 1. Selección y Descripción del proyecto
Este repositorio consolida un flujo reproducible de ingestión, limpieza y análisis exploratorio y prueba ANOVA utilizando el dataset **Ventas de Lácteos 2024**, siguiendo los lineamientos del documento de evaluación de la práctica calificada. El análisis combina herramientas de ingeniería de datos y estadística aplicada, integrando SPSS y Python para validar la coherencia de los resultados.



**Dataset:** Ventas de Lácteos 2024  
- **Origen**: Kaggle (https://www.kaggle.com/datasets/hectorconde/dataset-ventas-lacteos-2024).
- **Contenido**: El dataset contiene **10 000 registros de ventas simuladas** correspondientes al año 2024, provenientes de supermercados ubicados en distintos estados de Estados Unidos. Cada fila representa una transacción individual e incluye información suficiente para análisis descriptivos, modelamiento estadístico y evaluación comparativa entre categorías de productos lácteos.

### 1.1.Variables del dataset

| Variable | Tipo | Descripción |
|---------|------|-------------|
| IDOrden | Categórica | Identificador único por venta |
| Fecha | Fecha | Día de la venta |
| Estado / Ciudad | Categóricas | Localización geográfica |
| Categoria | Nominal | Cremas, Leche, Yogur, Quesos, Mantequilla, Otros |
| Producto | Categórica | Nombre del producto |
| Presentación | Categórica | Tipo de empaque |
| PrecioUnitarioUSD | Numérica | Precio unitario (USD) |
| CantidadComprada | Numérica | Número de unidades vendidas |
| ValorTotalUSD | Numérica | Monto total pagado por la transacción |


## 2.Objetivo del análisis
1. Registrar las ventas de lácteos con un pipeline ETL reproducible para facilitar auditorías y comparaciones con herramientas como SPSS.
2. Explorar patrones de valor total frente a categorías, precios y cantidades para identificar relaciones clave en la fuerza de ventas.
3. Generar gráficas y tablas que respalden una narrativa visual de las transacciones, facilitando posteriores pruebas estadísticas (ej.: ANOVA en `practica_calificada2.ipynb`).

## 3.Estructura del proyecto
```
├── data
│   ├── archives # descargas originales (Kaggle)
│   ├── processed # datos limpios para análisis
│   └── raw # archivos listos para procesar
├── src
│   ├── connections
│   │   └── kaggle_connections.py
│   ├── extract # ingestión desde Kaggle
│   │   └── download_and_ingest.py
│   ├── results # gráficos y tablas generadas por los notebooks
│   └── transform # limpieza y tipado (`procesamiento_data.py`)
│       └── procesamiento_data.py
├── .gitignore
├── EDA.ipynb # exploración descriptiva y gráficas
├── README.md
├── practica_calificada2.ipynb # prueba ANOVA y documentación estadística
└── requirements # dependencias del proyecto
         
```

## 4.Flujo ETL
1. **Extracción**
   - `src/extract/download_and_ingest.py` descarga el dataset con `kagglehub` y coloca las copias en `data/archives` y `data/raw`.
   - Se espera que el usuario provea la credencial `kaggle.json` en `/secrets/` o mediante la variable de entorno correspondiente.
2. **Transformación**
   - `src/transform/procesamiento_data.py` detecta el primer archivo CSV/XLSX en `data/raw`, normaliza nombres a snake_case, elimina columnas como `id` o `id_orden` y convierte los tipos de fecha, precio, cantidad y valores numéricos.
   - Los campos de texto limpian espacios y se compactan en columnas como `nombre_del_vendedor`, `producto`, `categoria` y `forma_pago`.
   - El resultado se guarda en `data/processed/ventas_lacteos_2024.csv` listo para el análisis exploratorio.
### 4.1.Resultados del procesamiento
   - No se encontraron valores perdidos en las variables de interés.
   - Las 10 000 observaciones fueron consideradas.
   - Se verificó consistencia tipológica:  
  - `ValorTotalUSD`: numérica–escala  
  - `Categoria`: categórica–nominal
3. **Exploración y análisis**
   - `EDA.ipynb` lee el dataset procesado, genera advertencias por nulos o duplicados, calcula estadísticas y guarda visualizaciones en `src/results/`.
   - `practica_calificada2.ipynb` resume la limpieza, propone una prueba ANOVA y rescata los hallazgos para comparar con SPSS.

## 5.Resultados generados
Las ejecuciones completas de los notebooks depositan los artefactos en `src/results/`. Cada imagen refleja un aspecto del análisis:
### 5.1 Distribución del valor total (USD)
[Histograma del valor total](src/results/hist_valor_total.jpg)
- La mayoría de las transacciones se concentran entre 200 y 1500 USD, típico de una distribución sesgada a la derecha.
### 5.2 Número de transacciones por categoría
[Barras por categoría](src/results/barras_categoria.jpg)
- Mantequilla y Leche muestran ligeramente más transacciones,sin embargo todas las categorías tienen volúmenes de transacciones muy similares (entre ~1600–1700), lo que sugiere una demanda balanceada en el portafolio.
### 5.3 Variabilidad del valor total por categoría
[Boxplot de categorías](src/results/boxplot_categoria.jpg)
- Los quesos y mantequilla presentan los valores totales más altos y mayor dispersión, lo que refleja tickets más elevados y compras más variables .  
- La leche y yogurt muestran valores más bajos y menos dispersos, característico de productos más básicos y de compra homogénea.
### 5.4 Relación entre precio unitario y cantidad comprada
[Gráfico de dispersión precio vs cantidad](src/results/scatter_precio_vs_cantidad.jpg)
- Los precios unitarios están muy concentrados en rangos específicos por categoría (bandas verticales), indicando precios estables y poco variables dentro de cada producto.
### 5.5 Distribución por forma de pago
[Conteo por forma de pago](src/results/count_forma_pago.jpg)
- No existe una forma de pago dominante: todas rondan las 1900–2000 transacciones. Esto indica un mix de pagos equilibrado.

### 5.6 Correlación entre variables numéricas
[Mapa de calor de correlación](src/results/heatmap_correlacion.jpg)
- La cantidad comprada tiene la correlación más fuerte con el valor total (0.71), lo que confirma que el volumen es el principal motor del gasto.
### 5.7 Tabla de estadísticas descriptivas por categoría
[Tabla HTML de estadísticas](src/results/tabla_estadisticas_categorias.html)
- tabla  con conteo, media, desviación, mínimo y máximo del valor total por categoría para informes detallados.
### 5.8 Síntesis de hallazgos del EDA

- Existen diferencias visibles entre las categorías de productos, especialmente en los valores promedio del monto total.
- Quesos y Mantequilla presentan montos más altos en sus transacciones.
- Yogur y Leche presentan menor monto promedio.
- La dispersión es heterogénea, evidenciando variabilidad considerable entre categorías.
- El valor total está altamente influenciado por la cantidad comprada y el precio unitario, confirmándose mediante correlaciones.
- El EDA sugiere que la aplicación de una prueba ANOVA es pertinente para evaluar diferencias estadísticas entre las categorías.

## 6. Tipo de prueba estadística

### 6.1.Prueba seleccionada  
**ANOVA de un factor** (paramétrica).

### 6.2.Objetivo  
Comparar si el valor total promedio (USD) difiere entre las seis categorías de productos lácteos.

### 6.3.Hipótesis
- **H₀:** Las medias del valor total son iguales entre las categorías.  
- **H₁:** Al menos una categoría tiene una media diferente.

### 6.4.Nivel de significancia  
α = 0.05

### 6.5Regla de decisión
- Si p < 0.05 → se rechaza H₀  
- Si p ≥ 0.05 → no se rechaza H₀

## 7. Resultados del ANOVA – SPSS

### 7.1.Descriptivos por categoría
[Resultados SPSS descriptivos](src/resultados_SPSS/resultados_descriptivos.jpg)
- Quesos y Mantequilla presentan los promedios más altos.
- Leche y Yogur presentan los valores más bajos.
- La media general del dataset es aproximadamente 1620 USD.

### 7.2.Prueba de homogeneidad de varianzas 
- p < 0.001  
Indica que no se cumple homogeneidad de varianzas, aunque con n=10 000 el ANOVA sigue siendo robusto.

### 7.3.Tabla ANOVA – SPSS
[Resultados SPSS descriptivos](src/resultados_SPSS/resultados_anova.jpg)
- F ≈ 573.843  
- p < 0.001

Interpretación: Se rechaza H₀. Existen diferencias significativas entre categorías.

---

## 7.5. Resultados del ANOVA – Python (SciPy)

```python
from scipy.stats import f_oneway

grupos = [
    df[df['categoria'] == cat]['valor_total_usd']
    for cat in df['categoria'].unique()
]

f, p = f_oneway(*grupos)
```

Resultados:
- p < 0.001  
- Se rechaza H₀  
- Existen diferencias significativas entre categorías

Los resultados de Python fueron consistentes con SPSS.

---

## 8. Conclusiones

El análisis ANOVA aplicado al valor total de ventas de productos lácteos ha demostrado que las categorías presentan diferencias estadísticamente significativas en sus montos promedio. Quesos y Mantequilla reflejan mejor rendimiento económico, mientras que Yogur y Leche muestran montos menores. La consistencia entre los resultados obtenidos en SPSS y Python confirma la validez del análisis y respalda el uso del modelo ANOVA en este contexto. Este hallazgo sugiere que la categoría del producto es un factor determinante en el desempeño económico y permite orientar estrategias comerciales diferenciadas según el tipo de producto.

---
## 9. Ejecución del proyecto

### 9.1.Pipeline ETL
```
python src/extract/download_and_ingest.py
python src/transform/procesamiento_data.py
```

### 9.2.Análisis exploratorio
Abrir:
```
EDA.ipynb
```

### 9.3.Prueba estadística ANOVA
Abrir:
```
practica_calificada2.ipynb
```

## 10.Requisitos
Instala las dependencias indicadas en `requirements/` con `python3 -m pip install -r requirements/requirements.txt`. Se requieren bibliotecas para herramientas para el trabajo con la plataforma de datos de Kaggle (`kaggle`, `kagglehub`, `python-dotenv`),manipulación y visualización (`pandas`, `numpy`, `matplotlib`, `seaborn`), estadística (`scipy`), automatización de notebooks (`ipykernel`, `loguru`) y acceso a archivos Excel (`openpyxl`).
