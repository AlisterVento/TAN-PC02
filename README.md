# Ventas de Lácteos 2024

## Descripción del proyecto
Este repositorio consolida un flujo reproducible de ingestión, limpieza y análisis exploratorio para el dataset _Ventas de Lácteos 2024_. Se busca automatizar el procesamiento de los archivos crudos, documentar cada transformación con loggers en español y generar visualizaciones enfocadas en la calidad de las ventas y el comportamiento de cada categoría de lácteos.

## Dataset
- **Origen**: Kaggle (https://www.kaggle.com/datasets/hectorconde/dataset-ventas-lacteos-2024).
- **Contenido**: transacciones de productos lácteos durante el año 2024 que incluyen fecha, vendedor, supermercado, ciudad, categoría, producto, presentación, precio unitario (USD), cantidad, valor total (USD), forma de pago y estado. Permite contrastar segmentos (categoría, ciudad, forma de pago) y comparar tendencias de volumen frente a precio.
- **Notas**: el dataset original se almacena en `data/archives`, se normaliza en `data/raw` y el resultado procesado queda en `data/processed/ventas_lacteos_2024.csv` con columnas en snake_case y tipos consistentes.

## Objetivo del análisis
1. Registrar las ventas de lácteos con un pipeline ETL reproducible para facilitar auditorías y comparaciones con herramientas como SPSS.
2. Explorar patrones de valor total frente a categorías, precios y cantidades para identificar relaciones clave en la fuerza de ventas.
3. Generar gráficas y tablas que respalden una narrativa visual de las transacciones, facilitando posteriores pruebas estadísticas (ej.: ANOVA en `practica_calificada2.ipynb`).

## Estructura del proyecto
```
├── data
│   ├── archives # descargas originales (Kaggle)
│   │   └── dataset_ventas_lacteos_2024.csv
│   ├── processed # datos limpios para análisis
│   │   └── ventas_lacteos_2024.csv
│   └── raw # archivos listos para procesar
│       └── dataset_ventas_lacteos_2024.csv
├── src
│   ├── connections
│   │   └── kaggle_connections.py
│   ├── extract # ingestión desde Kaggle
│   │   └── download_and_ingest.py
│   ├── results # gráficos y tablas generadas por los notebooks
│   │   ├── barras_categoria.jpg
│   │   ├── boxplot_categoria.jpg
│   │   ├── count_forma_pago.jpg
│   │   ├── heatmap_correlacion.jpg
│   │   ├── hist_valor_total.jpg
│   │   ├── scatter_precio_vs_cantidad.jpg
│   │   └── tabla_estadisticas_categorias.html
│   └── transform # limpieza y tipado (`procesamiento_data.py`)
│       └── procesamiento_data.py
├── .gitignore
├── EDA.ipynb # exploración descriptiva y gráficas
├── README.md
├── practica_calificada2.ipynb # prueba ANOVA y documentación estadística
└── requirements # dependencias del proyecto
         
```

## Flujo ETL
1. **Extracción**
   - `src/extract/download_and_ingest.py` descarga el dataset con `kagglehub` y coloca las copias en `data/archives` y `data/raw`.
   - Se espera que el usuario provea la credencial `kaggle.json` en `/secrets/` o mediante la variable de entorno correspondiente.
2. **Transformación**
   - `src/transform/procesamiento_data.py` detecta el primer archivo CSV/XLSX en `data/raw`, normaliza nombres a snake_case, elimina columnas como `id` o `id_orden` y convierte los tipos de fecha, precio, cantidad y valores numéricos.
   - Los campos de texto limpian espacios y se compactan en columnas como `nombre_del_vendedor`, `producto`, `categoria` y `forma_pago`.
   - El resultado se guarda en `data/processed/ventas_lacteos_2024.csv` listo para el análisis exploratorio.
3. **Exploración y análisis**
   - `EDA.ipynb` lee el dataset procesado, genera advertencias por nulos o duplicados, calcula estadísticas y guarda visualizaciones en `src/results/`.
   - `practica_calificada2.ipynb` resume la limpieza, propone una prueba ANOVA y rescata los hallazgos para comparar con SPSS.

## Resultados generados
Las ejecuciones completas de los notebooks depositan los artefactos en `src/results/`. Cada imagen refleja un aspecto del análisis:
- `src/results/hist_valor_total.jpg`: histogramas del `valor_total_usd` para observar la dispersión y posibles sesgos en las transacciones.
- `src/results/barras_categoria.jpg`: barras ordenadas por número de transacciones por categoría, útil para identificar las categorías más activas.
- `src/results/boxplot_categoria.jpg`: rangos del valor total por categoría sin outliers para comparar la variabilidad relativa.
- `src/results/scatter_precio_vs_cantidad.jpg`: dispersión del precio unitario frente a la cantidad comprada por categoría, exponiendo comportamientos agrupados y posibles relaciones inversas.
- `src/results/count_forma_pago.jpg`: conteo de transacciones por forma de pago, ayudando a priorizar métodos más frecuentes.
- `src/results/heatmap_correlacion.jpg`: matriz de correlación entre precio unitario, cantidad comprada y valor total para destacar dependencias lineales.
- `src/results/tabla_estadisticas_categorias.html`: tabla HTML con conteo, media, desviación, mínimo y máximo del valor total por categoría para informes detallados.

## Requisitos
Instala las dependencias indicadas en `requirements/` con `python3 -m pip install -r requirements/requirements.txt`. Se requieren bibliotecas para manipulación y visualización (`pandas`, `numpy`, `matplotlib`, `seaborn`), estadística (`scipy`), automatización de notebooks (`ipykernel`, `loguru`) y acceso a archivos Excel (`openpyxl`).
