"""URL Reader Tool for the AI Research Assistant."""
import requests
from bs4 import BeautifulSoup

def read_url_content(url: str) -> str:
    """
    Reads and extracts the primary text content from a given URL.

    Args:
        url: The URL to read from.

    Returns:
        The text content of the URL, or an error message if reading fails.
    """
    print(f"TOOL: Reading content from URL '{url}'")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        return " ".join(soup.stripped_strings)
    except requests.exceptions.RequestException as e:
        return f"Error reading URL: {e}"