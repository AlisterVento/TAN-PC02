from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable

import pandas as pd
from loguru import logger


SUPPORTED_EXTENSIONS = (".xlsx", ".xls", ".csv")


def _configurar_logger() -> None:
    """Prepara el logger en español para mejorar el trazado del pipeline."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="[ {time:YYYY-MM-DD HH:mm:ss} ] {level} - {message}",
        level="INFO",
    )


def obtener_rutas_default() -> tuple[Path, Path]:
    """Encuentra el archivo raw y define la ruta de salida procesada.

    Returns:
        tuple[Path, Path]: ruta de origen encontrada y archivo CSV de salida.
    Raises:
        FileNotFoundError: si no se encuentra ningún archivo compatible en raw/.
    """
    proyecto = Path(__file__).resolve().parents[2]
    raw_dir = proyecto / "data" / "raw"
    destino = proyecto / "data" / "processed" / "ventas_lacteos_2024.csv"
    archivo_origen = _encontrar_archivo_raw(raw_dir)
    return archivo_origen, destino


def _encontrar_archivo_raw(raw_dir: Path) -> Path:
    """Busca el primer archivo compatible dentro de data/raw."""
    if not raw_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta raw: {raw_dir}")
    candidatos = sorted(
        archivo
        for archivo in raw_dir.iterdir()
        if archivo.is_file() and archivo.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not candidatos:
        raise FileNotFoundError(
            f"No se encontraron archivos con extensiones {SUPPORTED_EXTENSIONS} en {raw_dir}"
        )
    seleccionado = candidatos[0]
    logger.info(f"Archivo raw seleccionado para transformación: {seleccionado.name}")
    return seleccionado


def cargar_datos(ruta_origen: Path) -> pd.DataFrame:
    """Carga el archivo raw que puede ser XLSX o CSV.

    Args:
        ruta_origen (Path): Archivo raw detectado en data/raw.

    Returns:
        pd.DataFrame: DataFrame sin procesar que mantiene texto.
    """
    logger.info(f"Cargando datos desde {ruta_origen}")
    extension = ruta_origen.suffix.lower()
    if extension in (".xlsx", ".xls"):
        return pd.read_excel(ruta_origen, dtype=str)
    if extension == ".csv":
        return pd.read_csv(ruta_origen, dtype=str)
    raise ValueError(f"Extensión no soportada: {extension}")


def normalizar_columnas(data: pd.DataFrame) -> pd.DataFrame:
    """Renombra columnas usando snake_case y removiendo acentos/puntuación."""

    def sanitized(columna: str) -> str:
        columna_ascii = unicodedata.normalize("NFKD", columna).encode("ascii", "ignore").decode(
            "ascii"
        )
        columna_ascii = re.sub(r"[^\w\s]", "", columna_ascii)
        columna_ascii = re.sub(r"\s+", "_", columna_ascii.strip().lower())
        return columna_ascii or columna

    nuevo_nombre = {col: sanitized(col) for col in data.columns}
    return data.rename(columns=nuevo_nombre)


def convertir_tipos(data: pd.DataFrame) -> pd.DataFrame:
    """Construye un DataFrame tipado para el dataset de ventas de lácteos.

    Args:
        data (pd.DataFrame): DataFrame sin normalizar.

    Returns:
        pd.DataFrame: DataFrame con columnas claves tipadas y normalizadas.
    """
    logger.info("Normalizando columnas y convirtiendo tipos para el dataset de lácteos")
    df = normalizar_columnas(data)
    columnas_borrar = {"id", "id_orden", "orden"}
    df = df.drop(columns=[col for col in df.columns if col in columnas_borrar], errors="ignore")
    df = df.drop_duplicates().reset_index(drop=True)

    df = df.rename(columns={"forma_de_pago": "forma_pago"})

    texto_cols = [
        "nombre_del_vendedor",
        "nombre_del_supermercado",
        "representante_de_compras",
        "ciudad",
        "estado",
        "categoria",
        "producto",
        "presentacion",
        "forma_pago",
    ]
    for col in texto_cols:
        if col in df:
            df[col] = df[col].astype(str).str.strip()

    if "categoria" in df:
        df["categoria"] = df["categoria"].replace("", "sin_categoria")
    else:
        df["categoria"] = "sin_categoria"

    if "fecha" in df:
        df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce")
    else:
        df["fecha"] = pd.NaT
    df["mes_venta"] = df["fecha"].dt.to_period("M").astype(str)

    for col in ("precio_unitario_usd", "cantidad_comprada", "valor_total_usd"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "valor_total_usd" not in df or df["valor_total_usd"].isna().all():
        valor_col = _buscar_columna(df, {"valor", "total", "usd"})
        cantidad_col = _buscar_columna(df, {"cantidad", "qty", "unidades", "volumen"})
        precio_col = _buscar_columna(df, {"precio", "unit_price", "price"})
        if valor_col:
            df["valor_total_usd"] = pd.to_numeric(df[valor_col], errors="coerce")
        elif cantidad_col and precio_col:
            df["valor_total_usd"] = (
                pd.to_numeric(df[cantidad_col], errors="coerce")
                * pd.to_numeric(df[precio_col], errors="coerce")
            )
        else:
            df["valor_total_usd"] = pd.to_numeric(df.iloc[:, 0], errors="coerce")
            logger.warning(
                "No se detectó columna de valor total; se aplica la primera numérica disponible."
            )

    df = df.assign(
        tipo_producto=df.get("producto", "lacteo"),

    )


    columna_orden = [
        "fecha",
        "mes_venta",
        "nombre_del_vendedor",
        "nombre_del_supermercado",
        "representante_de_compras",
        "estado",
        "ciudad",
        "categoria",
        "producto",
        "presentacion",
        "precio_unitario_usd",
        "cantidad_comprada",
        "valor_total_usd",
        "forma_pago",
        "tipo_producto",
        "region",
    ]
    columnas_finales = [col for col in columna_orden if col in df.columns]
    df = df[columnas_finales]

    return df


def _buscar_columna(data: pd.DataFrame, palabras_clave: Iterable[str]) -> str | None:
    """Busca la primera columna que contenga alguna de las palabras clave."""
    columnas = {col: col for col in data.columns}
    for clave in palabras_clave:
        for columna in columnas:
            if clave in columna:
                return columna
    return None


def exportar_datos(df: pd.DataFrame, ruta_destino: Path) -> Path:
    """Guarda el CSV procesado en la carpeta processed."""
    logger.info(f"Exportando datos procesados a {ruta_destino}")
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_destino, index=False)
    logger.info("Exportación finalizada")
    return ruta_destino


def procesar_datos(archivo_raw: Path | None = None, destino: Path | None = None) -> Path:
    """Orquesta la transformación completa del dataset.

    Args:
        archivo_raw (Path | None): Ruta opcional de origen.
        destino (Path | None): Ruta opcional de destino.
    """
    _configurar_logger()
    ruta_origen_default, ruta_destino_default = obtener_rutas_default()
    ruta_origen_efectiva = archivo_raw or ruta_origen_default
    ruta_destino_efectiva = destino or ruta_destino_default
    datos_crudos = cargar_datos(ruta_origen_efectiva)
    datos_procesados = convertir_tipos(datos_crudos)
    return exportar_datos(datos_procesados, ruta_destino_efectiva)


if __name__ == "__main__":
    procesar_datos()
