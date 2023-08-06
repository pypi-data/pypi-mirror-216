import requests
from wikipyedia_md.html_filtering import filter_html
from wikipyedia_md.wiki_parser import parse_article


def articles_to_markdown(urls: list[str], output_dir: str):
    """
    Retrieves the wikipedia articles from the given urls, parses them into Markdown and saves them to the given output directory

    Args:
        urls : list[str]
            list of wikipedia article urls
        output_dir : str
            path to the output directory for the Markdown files
    """
    for url in urls:
        response = requests.get(url, timeout=10)
        content = response.text
        modified_html = filter_html(content)
        article = parse_article(modified_html)
        file_name = url.split("/")[-1] + ".md"
        article.save_md(f"{output_dir}/{file_name}")
