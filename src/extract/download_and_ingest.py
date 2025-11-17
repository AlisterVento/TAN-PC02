from pathlib import Path
from src.connections.kaggle_connections import KaggleHubClient
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
def main():
    # 1) Define el slug del dataset (owner/dataset) -- actual: lácteos 2024
    slug = "hectorconde/dataset-ventas-lacteos-2024"

    client = KaggleHubClient()
    # 2) Descarga a la caché local de kagglehub y devuelve la carpeta
    cache_dir: Path = client.download_dataset(slug)

    # 3) Copia a archives y deja el contenido listo en raw (descomprime zips)
    created = client.copy_to_archives_then_raw(cache_dir)

    logger.info("Elementos creados en RAW:")
    for p in created:
        logger.info(" - %s", p)

if __name__ == "__main__":
    main()
