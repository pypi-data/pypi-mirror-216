import re
from bs4 import BeautifulSoup

IGNORE_ELEMENTS = [
    "script",
    "style",
    "iframe",
    "svg",
    "path",
    "aside",
    "footer",
    "link",
    "nav",
    "comment",
]


def filter_html(
    html: str,
    filter_elements: list[str] = IGNORE_ELEMENTS,
    use_main_selector: bool = True,
) -> str:
    """
    Filter out elements, comments and tabs from the html

    Args:
        html : str
            the webpage html
        filter_elements : list[str] (default=IGNORE_ELEMENTS)
            list of elements to filter out
        use_main_selector : bool (default=True)
            grab only the content inside the main selector, if false - body is used

    Returns:
        str: filtered content of the html
    """
    soup = BeautifulSoup(html, "html.parser")

    selector = "body"
    if use_main_selector:
        selector = "main"

    soup = soup.select(selector)[0]

    if filter_elements:
        for element in filter_elements:
            for tag in soup.find_all(element):
                tag.extract()

    content = str(soup)

    content = re.sub(r"<!--[\s\S]*?-->", "", content)
    content = content.replace("\t", "").replace("\n\n", "")

    return content
