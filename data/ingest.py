import requests
from tqdm import tqdm

from app.config import API_URL


def get_all_pages(limit: int = 500, api_url: str = API_URL) -> list:
    """
    Fetches all page titles from the MediaWiki API.

    Args:
        limit (int): The maximum number of titles to fetch per request.
        api_url (str): The URL of the MediaWiki API. Default: API_URL set in .env file.

    Returns:
        list: A list of page titles.
    """

    if not api_url:
        raise ValueError("API URL is not set. Please check environment variables.")

    print(f"Fetching all page titles from {api_url} ...")
    titles = []
    apcontinue = ""
    i = 0
    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": limit,
            "format": "json",
        }
        if apcontinue:
            params["apcontinue"] = apcontinue

        res = requests.get(api_url, params=params)
        data = res.json()
        pages = data["query"]["allpages"]
        titles.extend([p["title"] for p in pages])

        i += 1
        print(f"{i}/?. Fetched {len(pages)} titles (Total: {len(titles)}).")
        apcontinue = data.get("continue", {}).get("apcontinue")
        if not apcontinue:
            break
    print(f"{i}/{i}. Fetched total of {len(titles)} titles.")
    return titles


def get_all_data(pages: list[str], api_url: str = API_URL) -> list[dict[str, str]]:
    """
    Fetches the text content of all pages from a list of page titles.

    Args:
        pages (list): A list of page titles to fetch.
        api_url (str): The URL of the MediaWiki API. Default: API_URL set in .env file.

    Returns:
        list: A list of dictionaries containing page titles and their content.
    """

    all_page_data = []
    print(f"Extracting text content from {len(pages)} pages...")
    for title in tqdm(pages):
        text, url = get_page_text_and_url(title, api_url)
        if text.strip():  # skip empty pages
            all_page_data.append({"title": title, "content": text, "link": url})
    return all_page_data


def get_page_text_and_url(title, api_url: str = API_URL) -> tuple[str, str]:
    """
    Fetches the text content and URL of a specific page from the MediaWiki API.

    Args:
        title (str): The title of the page to fetch.
        api_url (str): The URL of the MediaWiki API. Default: API_URL set in .env file.

    Returns:
        tuple: A tuple containing the text content of the page and its URL.
        If the page does not exist, returns an empty string and an empty URL.
    """

    params = {
        "action": "query",
        "prop": "extracts|info",
        "explaintext": 1,
        "titles": title,
        "format": "json",
        "inprop": "url",
    }
    res = requests.get(api_url, params=params)
    data = res.json()
    page = next(iter(data["query"]["pages"].values()))
    text = page.get("extract", "")
    url = page.get("fullurl", "")
    return text, url


if __name__ == "__main__":
    api_url = "https://test.wikipedia.org/w/api.php"
    pages = get_all_pages(api_url)
    all_data = get_all_data(api_url, pages)
