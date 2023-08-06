from dataclasses import dataclass
import re
from bs4 import BeautifulSoup


@dataclass
class Reference:
    # TODO: implement references
    pass


@dataclass
class Section:
    header: str
    content: str
    header_level: str


@dataclass
class Article:
    title: str
    content: list[Section]
    references: list[Reference] | None = None  # TODO: implement reference parsing

    def to_markdown(self) -> str:
        markdown = f"# {self.title}\n\n"
        for section in self.content:
            header_level = section.header_level
            markdown += f"\n{'#' * int(header_level[-1])} {section.header}\n\n"
            markdown += f"{section.content}\n"
        return markdown

    def save_md(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_markdown())


def parse_article(html: str) -> Article:
    """
    Parse a wikipedia article from html

    Args:
        html : str
            html of the webpage

    Returns:
        Article: parsed article object
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one(".mw-page-title-main").text
    main_content = soup.select_one("#mw-content-text").contents[0].contents
    contents = []
    header = "Main"
    text = []
    header_level = "h2"
    pattern = r"\[\d+\]|\[edit\]"
    # TODO: implement reference parsing
    for el in main_content:
        if el.name == "p":
            text.append(el.text)

        elif el.name == "ul":
            if "gallery" in el.attrs.get("class", []):
                continue
            for subel in el.contents:
                if subel.text == "\n":
                    continue
                text.append("- " + subel.text)

        elif el.name in ["h2", "h3", "h4", "h5", "h6"]:
            header = re.sub(pattern, "", header)
            joined_text = "\n".join(text)
            processed_text = re.sub(pattern, "", joined_text)
            contents.append(Section(header, processed_text, header_level=header_level))
            header = el.text
            header_level = el.name
            text = []

    return Article(
        title,
        content=contents,
    )
