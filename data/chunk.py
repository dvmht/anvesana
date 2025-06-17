from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)


def chunk_data(all_data: list[dict[str, str]]) -> list[Document]:
    """
    Splits the content of all of the text into smaller chunks for processing.

    Args:
        all_data (list): List of dictionaries containing page titles, content, and links.

    Returns:
        list: List of documents with metadata.
    """

    if not all_data:
        print("No data to chunk. Returning empty list.")
        return []

    print("Chunking data into smaller pieces...")
    # Create documents from the content of each page
    contents = [page["content"] for page in all_data]
    metadatas = [
        {
            "title": page["title"],
            "link": page["link"],
        }
        for page in all_data
    ]
    documents = splitter.create_documents(contents, metadatas=metadatas)
    print(f"Chunked data into {len(documents)} documents.")
    return documents
