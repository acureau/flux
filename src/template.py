# Contains functionality related to converting markdown and building templates.


import re
import os
import util
import marko
import config
from bs4 import BeautifulSoup


# The marko markdown instance used for HTML conversion.
markdown_converter = marko.Markdown()


# Gets all unique bracket pairs from the HTML string.
def _get_bracket_pairs(html):
    return set(re.findall(r"\{[^{}]*\}", html))


# Resolves file inclusion in HTML templates.
def resolve_file_includes(html):

    # For each file include bracket pair, replace with file contents.
    for bracket_pair in _get_bracket_pairs(html):
        if bracket_pair.startswith("{@"):
            content_path = bracket_pair.split("{@")[1].split("}")[0]
            if os.path.exists(content_path):
                content = resolve_file_includes(util.read_file_text(content_path))
                html = html.replace(bracket_pair, content)
            else:
                print(f"Could not resolve include at '{content_path}'.")

    return html


# Converts a list of paths to a metadata collection.
def paths_to_index(paths):

    # Get global metadata from config.
    metadata = config.get_metadata()

    # Get index div id from config file.
    index_div_id = "index"
    if config.has("index_div_id"):
        index_div_id = config.get("index_div_id")

    # Create index div and unordered list.
    html_builder = BeautifulSoup("", "html.parser")
    index_div = html_builder.new_tag("div", id=index_div_id)
    ul = html_builder.new_tag("ul")

    # Build link list items.
    for path in paths:
        li = html_builder.new_tag("li")
        a = html_builder.new_tag("a", href=path)
        a.string = "PLACEHOLDER"  # need to pass name of post too
        li.append(a)
        ul.append(li)

    # Insert list into the div, convert to a string, insert into metadata.
    index_div.append(ul)
    metadata[index_div_id] = str(index_div)

    return metadata


# Converts a markdown post to a metadata collection.
def markdown_to_post(markdown):
    metadata = {}

    # Remove leading and trailing whitespace.
    markdown = markdown.strip()

    # If metadata header is present, parse it out.
    if markdown.startswith("<!--") and "-->" in markdown:
        post_metadata = markdown.split("<!--")[1].split("-->")[0]
        metadata = config.get_metadata(post_metadata)
        markdown = markdown.replace(f"<!--{post_metadata}-->", "")

    # Get post div id from config file.
    post_div_id = "post"
    if config.has("post_div_id"):
        post_div_id = config.get("post_div_id")

    # Convert markdown to html, insert into metadata.
    metadata[post_div_id] = (
        f'<div id="{post_div_id}">{markdown_converter.convert(markdown)}</div>'
    )

    return metadata


# Builds a template with HTML and metadata.
def build(html, metadata):

    # For each bracket pair, parse key and replace with metadata contents.
    for bracket_pair in _get_bracket_pairs(html):
        key = bracket_pair.split("{")[1].split("}")[0]
        if key in metadata:
            html = html.replace(bracket_pair, metadata[key])
        else:
            html = html.replace(bracket_pair, "")
            print(f"No metadata provided for '{key}'.")

    return BeautifulSoup(html, "html.parser").prettify()
