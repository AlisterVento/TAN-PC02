# Data Coffee Shop Sales:

## Descreipcion del proyecto

Este proyecto tiene como objetivo realizar un análisis estadístico descriptivo de las ventas de una cadena de cafeterías, utilizando un dataset público de Kaggle.
*https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales*  
A través de un flujo ETL (Extract, Transform, Load), se automatiza la descarga, procesamiento y análisis de los datos, garantizando consistencia, limpieza y trazabilidad del proceso.

## Fuente de datos

Dataset: Coffee Sales Dataset – Kaggle

Autor: Ahmed Abbas

Licencia: Open Data (uso libre con atribución)

Descripción original:
Contiene transacciones diarias de ventas en una tienda de café, incluyendo información de productos, categorías, precios, tiendas y fechas. 


## File Tree: Estadistica

```
├── 📁 data/
│   ├── 📁 archives/
│   │   └── Coffee_Shop_Sales.xlsx
│   ├── 📁 processed/
│   │   └── Coffee_Shop_Sales.csv
│   └── 📁 raw/
│       └── Coffee_Shop_Sales.xlsx
├── 📁 src/
│   ├── 📁 connections/
│   │   └── kaggle_connections.py
│   ├── 📁 extract/
│   │   └── download_and_ingest.py
│   ├── 📁results/
│   │   ├── estadisticos_descriptivos.html
│   │   └── intervalos_confianza.html
│   └── 📁 transform/
│       └── procesamiento_data.py
├── README.md
└── estadistica.ipynb
```

## Proceso 

### 1. Conexión y extracción (Kaggle Connections)

El módulo src/connections/kaggle_connections.py implementa la clase KaggleHubClient, encargada de:

Autenticar la sesión mediante kaggle.json (ubicado en /secrets/).

Descargar automáticamente datasets públicos usando la API de Kaggle.

Guardar los archivos originales en la carpeta /data/archives/.

Una vez descargado, el módulo download_and_ingest.py copia o descomprime el archivo fuente hacia /data/raw/, asegurando nombres limpios (sin espacios) y verificando la integridad del archivo.

### 2. Transformación (procesamiento_data.py)

El módulo procesamiento_data.py realiza:

Conversión de tipos (int, float, datetime).

Limpieza de campos con espacios o formatos inconsistentes.

Creación del campo total_venta como producto entre cantidad y precio.

Generación de la variable tiempo_transaccion (combinación de fecha + hora).

Estandarización de nombres y exportación a CSV en /data/processed/.


## Data Previa
### Descripción de los datos raw:

El dataset contiene información de transacciones diarias en una tienda de café, incluyendo variables como fecha, hora, producto, categoría, precio unitario, cantidad vendida, tienda y ubicación.

---

### Variables principales  

| Tipo | Nombre | Descripción |
|------|---------|-------------|
| **Categórica** | `transaction_id` | Identificador único de cada transacción. |
| **Fecha** | `transaction_date` | Fecha de la transacción. |
| **Hora** | `transaction_time` | Hora de la transacción. |
| **Numérica** | `unit_price` | Precio unitario del producto. |
| **Categórica** | `product_category` | Categoría del producto (por ejemplo, *Bebidas*, *Comidas*, etc.). |
| **Categórica** | `product_type` | Tipo específico del producto (por ejemplo, *Latte*, *Espresso*, *Sandwich*, etc.). |
| **Categórica** | `store_location` | Ubicación de la tienda (por ciudad o zona). |


## Data Procesada:  

### Descripcion  de los datos procesados:  
El dataset procesado contiene información depurada y estructurada sobre las transacciones realizadas en una cadena de cafeterías.
A diferencia de la versión original (RAW), este dataset estandariza los tipos de datos, corrige inconsistencias en formato de fechas y horas, y agrega una variable derivada que consolida la fecha y hora de cada transacción.

Cada registro representa una venta única de un producto específico, identificada por su transacción y asociada a una tienda y categoría de producto.

---

### Variables principales (procesadas):
| Tipo | Nombre | Descripción |
|------|---------|-------------|
| **Categórica** | `transaction_id` | Identificador único de cada transacción en el sistema. |
| **Fecha** | `fecha_transaccion` | Fecha exacta en la que ocurrió la transacción (`YYYY-MM-DD`). |
| **Hora** | `hora_transaccion` | Hora del día en la que se realizó la transacción (`HH:MM:SS`). |
| **Datetime** | `tiempo_transaccion` | Combinación de la fecha y hora de la transacción, útil para análisis temporales precisos. |
| **Numérica** | `cantidad_transaccion` | Cantidad de unidades de producto vendidas en la transacción. |
| **Numérica** | `precio_unitario` | Precio unitario del producto en la venta, expresado en la moneda local. |
| **Numérica (derivada)** | `total_venta` | Monto total de la venta (calculado como `cantidad_transaccion × precio_unitario`). |
| **Numérica / Categórica** | `id_tienda` | Identificador único de la tienda donde se realizó la venta. |
| **Categórica** | `ubicacion_tienda` | Ciudad o ubicación geográfica de la tienda. |
| **Numérica / Categórica** | `id_producto` | Identificador único del producto vendido. |
| **Categórica** | `categoria_producto` | Categoría general del producto (por ejemplo, *Bebidas*, *Comidas*, *Postres*, etc.). |
| **Categórica** | `tipo_producto` | Tipo o subcategoría del producto (por ejemplo, *Latte*, *Espresso*, *Sandwich*, etc.). |


## Interpretación:

- Tabla de estadísticas descriptivas:
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Variable</th>
      <th>Media</th>
      <th>Mediana</th>
      <th>Moda</th>
      <th>Varianza</th>
      <th>Desviación estándar</th>
      <th>Rango</th>
      <th>Q25</th>
      <th>Q50</th>
      <th>Q75</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>cantidad_transaccion</td>
      <td>1.44</td>
      <td>1.00</td>
      <td>1.0</td>
      <td>0.29</td>
      <td>0.54</td>
      <td>7.0</td>
      <td>1.0</td>
      <td>1.00</td>
      <td>2.00</td>
    </tr>
    <tr>
      <td>precio_unitario</td>
      <td>3.38</td>
      <td>3.00</td>
      <td>3.0</td>
      <td>7.07</td>
      <td>2.66</td>
      <td>44.2</td>
      <td>2.5</td>
      <td>3.00</td>
      <td>3.75</td>
    </tr>
    <tr>
      <td>total_venta</td>
      <td>4.69</td>
      <td>3.75</td>
      <td>3.0</td>
      <td>17.87</td>
      <td>4.23</td>
      <td>359.2</td>
      <td>3.0</td>
      <td>3.75</td>
      <td>6.00</td>
    </tr>
  </tbody>
</table>

- Tabla de intervalos de confianza:

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Variable</th>
      <th>Rango</th>
      <th>IC 95% Inferior</th>
      <th>IC 95% Superior</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>cantidad_transaccion</td>
      <td>7.0</td>
      <td>1.44</td>
      <td>1.44</td>
    </tr>
    <tr>
      <td>precio_unitario</td>
      <td>44.2</td>
      <td>3.37</td>
      <td>3.40</td>
    </tr>
    <tr>
      <td>total_venta</td>
      <td>359.2</td>
      <td>4.66</td>
      <td>4.71</td>
    </tr>
  </tbody>
</table>
Las medias estimadas son precisas y estables, con intervalos estrechos.

### Cantidad de transacción
La mayoría de las transacciones son de una sola unidad, lo cual se confirma porque la media, mediana y moda están muy cerca (1.0–1.4).
La dispersión baja (0.54) indica homogeneidad, es decir, casi todas las compras son pequeñas.
Solo algunas pocas transacciones son más grandes (lo que explica el rango amplio de 7).
El intervalo es extremadamente estrecho (sin variación entre los límites), lo que indica muy baja variabilidad y una media estable.

### Precio unitario
La mayoría de precios se concentran alrededor de 3 unidades monetarias, pero el rango alto (44.2) y la varianza elevada (7.07) muestran alta dispersión y posibles valores atípicos (productos con precios mucho mayores).
Esto podría indicar un menu con algunos productos de alto valor  (granos de cafe) que sesgan la media hacia arriba.
El rango de precios es alto (productos entre valores bajos y muy altos), pero la media está estimada con gran precisión, dado que el IC apenas varía 0.03 unidades.
Esto implica que el tamaño de muestra fue suficientemente grande y que la media (~3.38) es un estimador confiable del precio promedio.

### Total venta
El total de venta promedio es de 4.69, pero con una gran dispersión (σ = 4.23) similar ala media y un rango enorme (359.2).
Esto sugiere que, aunque la mayoría de ventas son pequeñas, existen algunas transacciones de alto valor que elevan la media 

El rango de precios es alto (productos entre valores bajos y muy altos), pero la media está estimada con gran precisión, dado que el IC apenas varía 0.03 unidades.
Esto implica que el tamaño de muestra fue suficientemente grande y que la media (~3.38) es un estimador confiable del precio promedio.
## Resultados globales

- La distribución de total_venta muestra asimetría ligera a la derecha, con algunas transacciones de alto valor.

- Para las ventas se observa que el rango intercuartil se encuentra entre 3 y 6 unidades monetarias.

- Los resultados reflejan un comportamiento típico de cafeterías: alta frecuencia de ventas pequeñas con productos económicos y pocas ventas de alto valor.

- A pesar de la estabilidad en la media, precio_unitario y total_venta tienen grandes rangos, lo que refleja alta variabilidad entre observaciones individual

