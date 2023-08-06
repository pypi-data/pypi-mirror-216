from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from pelican import ArticlesGenerator, PagesGenerator
from pelican.contents import Article, Page
import pelican.generators
from pelican.plugins import signals

LOGGER = logging.getLogger(__name__)

RE_CAPTION = re.compile(r"\[#([\w\d:\-]+)(?:=(.+))?\]")


def find_previous_sibling_tag(element: Tag) -> Tag | None:
    sibling: Tag | NavigableString | None = None

    while True:
        if not sibling:
            sibling = element.find_previous_sibling()
        else:
            sibling = sibling.find_previous_sibling()

        if not sibling:
            return None

        if isinstance(sibling, Tag):
            return sibling


def is_code_block(element: Tag) -> bool:
    if element.name != "table":
        return False

    if "class" not in element.attrs:
        return False

    if "highlighttable" not in element.attrs["class"]:
        return False

    return True


def is_table(element: Tag) -> bool:
    if element.name != "table":
        return False

    return True


def is_figure(element: Tag) -> bool:
    if element.name != "p":
        return False

    if not isinstance(element.findChild("img"), Tag):
        return False

    return True


def patch_code_block(
    counter: int,
    element: Tag,
    label: str,
    caption: str | None = None,
):
    element.attrs["id"] = label

    if caption:
        caption_element = Tag(name="caption")
        caption_element.string = f"Code {counter+1}: {caption}"
        element.append(caption_element)


def patch_table(counter: int, element: Tag, label: str, caption: str | None = None):
    element.attrs["id"] = label

    if caption:
        caption_element = Tag(name="caption")
        caption_element.string = f"Tab. {counter+1}: {caption}"
        element.append(caption_element)


def patch_figure(counter: int, element: Tag, label: str, caption: str | None = None):
    element.name = "figure"
    element.attrs["id"] = label

    img_element = element.findChild("img")
    if not isinstance(img_element, Tag):
        raise ValueError("invalid figure")

    if not caption:
        if "alt" in img_element.attrs:
            caption = img_element.attrs["alt"]

    if caption:
        caption_element = Tag(name="figcaption")
        caption_element.string = f"Fig. {counter+1}: {caption}"
        element.append(caption_element)


def patch_links(soup: BeautifulSoup, label_id_map: dict[str, int]):
    for tag in soup.find_all("a"):
        if not isinstance(tag, Tag):
            continue

        if "href" not in tag.attrs:
            continue

        if tag.string:
            continue

        if not tag.attrs["href"].startswith("#"):
            continue

        label = tag.attrs["href"][1:]

        tag.string = str(label_id_map[label])


def process_content(content: Article | Page):
    soup = BeautifulSoup(content._content, "html.parser")

    code_block_counter = 0
    table_counter = 0
    figure_counter = 0

    label_id_map: dict[str, int] = {}

    for tag in soup.find_all("p"):
        if not isinstance(tag, Tag):
            continue

        m = RE_CAPTION.match(tag.text)
        if not m:
            continue

        sibling = find_previous_sibling_tag(tag)
        if not sibling:
            tag.decompose()
            continue

        label: str = m.group(1)
        caption: str | None = m.group(2) if len(m.groups()) > 1 else None

        if is_code_block(sibling):
            patch_code_block(code_block_counter, sibling, label, caption)
            code_block_counter += 1
            label_id_map[label] = code_block_counter
        elif is_table(sibling):
            patch_table(table_counter, sibling, label, caption)
            table_counter += 1
            label_id_map[label] = table_counter
        elif is_figure(sibling):
            patch_figure(figure_counter, sibling, label, caption)
            figure_counter += 1
            label_id_map[label] = figure_counter

        tag.decompose()

    patch_links(soup, label_id_map)

    content._content = str(soup)


class CaptionsProcessor:
    def __init__(self, generators: list[pelican.generators.Generator]):
        self.generators: list[ArticlesGenerator | PagesGenerator] = [
            generator
            for generator in generators
            if isinstance(generator, ArticlesGenerator)
            or isinstance(generator, PagesGenerator)
        ]

    def process(self):
        for generator in self.generators:
            if isinstance(generator, ArticlesGenerator):
                articles: list[Article] = (
                    generator.articles
                    + generator.translations
                    + generator.drafts
                    + generator.drafts_translations
                )

                for article in articles:
                    process_content(article)

            elif isinstance(generator, PagesGenerator):
                pages: list[Page] = (
                    generator.pages
                    + generator.translations
                    + generator.draft_pages
                    + generator.draft_translations
                )

                for page in pages:
                    process_content(page)


def add_captions(generators: list[pelican.generators.Generator]):
    CaptionsProcessor(generators).process()


def register():
    signals.all_generators_finalized.connect(add_captions)
