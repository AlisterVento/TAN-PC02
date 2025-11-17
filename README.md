# Ventas de Lácteos 2024

## Descripción del proyecto
Este repositorio automatiza el flujo completo de extracción, transformación y análisis para el dataset _Ventas de Lácteos 2024_ (Kaggle), enfocándose en documentar la limpieza con Google Style, generar visualizaciones mediante `seaborn`, realizar una prueba ANOVA y dejar evidencia para comparar los resultados con SPSS.

## Dataset
- **Fuente**: [https://www.kaggle.com/datasets/hectorconde/dataset-ventas-lacteos-2024](https://www.kaggle.com/datasets/hectorconde/dataset-ventas-lacteos-2024)
- **Dimensiones esperadas**: miles de transacciones de productos lácteos con las columnas principales como `Fecha`, `Categoria`, `Producto`, `Valor total (USD)`, `Cantidad`, `Precio unitario`, `Region`, `Sucursal`. Cubre el primer semestre de 2024 y permite comparar categorías como cremas, quesos, yogur y mantequilla.
- **Notas**: la variable `Valor total (USD)` es el objetivo de los análisis descriptivos e inferenciales, y `Categoria` sirve para segmentar la prueba de hipótesis (ANOVA de un factor).

## Objetivo del análisis
1. Registrar un flujo reproducible de descarga desde Kaggle y almacenamiento en `data/archives` y `data/raw`.
2. Procesar los datos en `src/transform/procesamiento_data.py` usando `Path`, loggers en español y docstrings Google Style.
3. Explorar el dataset en `EDA.ipynb`, guardar gráficas en `src/results/*.jpg` y tablas en `src/results/*.html`.
4. Ejecutar `practica_calificada2.ipynb` para resumir el EDA, documentar la limpieza y aplicar una prueba ANOVA (con formulación de hipótesis, nivel de significancia, valor p y conclusión).
5. Preparar un informe de apoyo para comparar estos resultados con SPSS siguiendo el esquema de prueba de hipótesis establecido.

## Flujo ETL
1. **Extracción**
   - Descarga y prepara el dataset con `python3 -m src.extract.download_and_ingest`. `KaggleHubClient`:
     - Usa tu `kaggle.json` (debe estar en `/secrets/` o en la variable de entorno).
     - Descarga `hectorconde/dataset-ventas-lacteos-2024` y copia los archivos a `data/archives` y `data/raw`.
2. **Transformación**
   - Ejecuta `python3 -m src.transform.procesamiento_data`. El módulo:
     - Detecta el primer archivo XLSX o CSV en `data/raw`.
     - Normaliza nombres (snake_case) sin espacios ni acentos.
     - Convierte `valor_total_usd`, `cantidad`, `precio_unitario`, `fecha_venta` y crea campos como `mes_venta`.
     - Guarda `data/processed/ventas_lacteos_2024.csv`, listando los registros ya limpios listos para análisis.
3. **Notebooks**
   - `EDA.ipynb`: utiliza `Path`, describe dimensiones/tipos/nulos/duplicados, genera gráficas y tablas, y guarda los resultados en `src/results`.
   - `practica_calificada2.ipynb`: incluye descripción del dataset y la prueba ANOVA (H₀ vs H₁, α = 0.05, tipo de prueba paramétrica, código `scipy.stats.f_oneway`, valor p y conclusión). También indica que se contrastará con SPSS.

## Resultados generados
- Las siguientes salidas se guardan en `src/results/` cuando ejecutas los notebooks después de procesar `data/processed/ventas_lacteos_2024.csv`:
  - `hist_valor_total.jpg`
  - `barras_categoria.jpg`
  - `boxplot_categoria.jpg`
  - `tabla_estadisticas_categorias.html`
  - `anova_valor_total.html`
- Si aún no existen, corre primero `EDA.ipynb` y `practica_calificada2.ipynb`; en caso de que el sistema no pueda crearlos, adjunta la explicación en el informe usando el formato ["descripcion"] para indicar la ausencia.

## Estructura del proyecto

```
├── README.md
├── data/
│   ├── archives/
│   ├── processed/
│   └── raw/
├── EDA.ipynb
├── practica_calificada2.ipynb
├── requirements
└── src/
    ├── connections/
    │   └── kaggle_connections.py
    ├── extract/
    │   └── download_and_ingest.py
    ├── results/
    │   └── README.md
    └── transform/
        └── procesamiento_data.py
```

## Estándares de documentación
- Las funciones de `src/transform/procesamiento_data.py` usan docstrings Google Style (`Args`, `Returns`, `Raises` cuando aplica).
- Toda manipulación de archivos usa `pathlib.Path`.
- Los loggers del pipeline están en español gracias a `loguru`.

## Notas sobre SPSS
Los hallazgos descriptivos y el resultado de la ANOVA serán la base para replicarlo en SPSS: documenta la transformación de `valor_total_usd`, la segmentación por `categoria` y el esquema de prueba de hipótesis (tipo paramétrico, α = 0.05, p-valor, conclusión) para comparar consistencia entre herramientas.

## Requisitos
Instala todas las dependencias con `python3 -m pip install -r requirements`. El archivo incluye bibliotecas para manipulación de datos (`pandas`, `numpy`), estadística (`scipy`), visualización (`matplotlib`, `seaborn`), ejecución de notebooks (`ipykernel`, `loguru`), autenticación con Kaggle (`kaggle`, `kagglehub`) y lectura de Excel (`openpyxl`).
