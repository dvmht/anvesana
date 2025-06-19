import json
import logging

from app.rag import EmbeddingModel
from app.config import RAW_DATA_PATH
from data.chunk import chunk_data
from data.ingest import get_all_data, get_all_pages


logger = logging.getLogger("data")


def save_raw_data(data: list[dict], file_path: str) -> None:
    """
    Saves the raw data to a JSON file.

    Args:
        data (list): The data to save.
        file_path (str): The path to the file where the data will be saved.
    """

    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def read_raw_data(file_path: str) -> list[dict]:
    """
    Reads the raw data from a JSON file.

    Args:
        file_path (str): The path to the file from which to read the data.

    Returns:
        list: The data read from the file.
    """

    try:
        logger.info(f"Reading raw data from {file_path}...")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        logger.info(f"Raw data read successfully from {file_path}.")
    except FileNotFoundError:
        logger.error(f"File {file_path} not found. Please run the data ingestion first.")
        return []


def main():
    # Get the raw data. Scrape it if it doesn't exist.
    if not (all_data := read_raw_data(RAW_DATA_PATH)):
        logger.warning("No raw data found. Starting data ingestion...")
        pages = get_all_pages()
        all_data = get_all_data(pages)
        save_raw_data(all_data, RAW_DATA_PATH)

    logger.debug(f"Dataset contains {len(all_data)} pages.")
    # Chunk the data into smaller pieces for processing.
    chunked_docs = chunk_data(all_data)

    # Save the chunked data to a file.
    model = EmbeddingModel()
    model.save_embeddings(docs=chunked_docs)


if __name__ == "__main__":
    main()
