# Wikipyedia_md

A python package for converting Wikipedia articles to Markdown format.

## Usage

Install the package

```shell
pip install wikipyedia-md
```

Fetch, parse and save a list of articles from urls as .md files in the output dirrectory

```python
from wikipyedia_md import articles_to_markdown

    urls = [
            "https://en.wikipedia.org/wiki/Computer_science",
            # ...
        ]
        articles_to_markdown(urls, output_dir="./articles")
```

Or you can do it manually

```python
import requests
from wikipyedia_md.html_filtering import filter_html
from wikipyedia_md.wiki_parser import parse_article

urls = [
    "https://en.wikipedia.org/wiki/Computer_science",
    # ...
]

for url in urls:
    response = requests.get(url, timeout=10)
    content = response.text
    modified_html = filter_html(content)
    article = parse_article(modified_html)
    file_name = url.split("/")[-1] + ".md"
    article.save_md(f"{output_dir}/{file_name}")

```

By default filter_html filters out common html elements that would mess with the markdown output, you can modify the elements if you want by passing a list of elements

```python
from wikipyedia_md import IGNORE_ELEMENTS

custom_elements = IGNORE_ELEMENTS
custom_elements.extend([
    "img",
    # ...
])
modified_html = filter_html(content, filter_elements=custom_elements)
```

## Contributing

Contributions to this package are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## References

- [Github Repository](https://github.com/t4skmanag3r/wikipyedia-md)
- [PyPI package](https://pypi.org/project/wikipyedia-md/)
