# Contains functions for creating, verifying, and working with site trees.


import os
import util
import random


# The help text file.
_help_text = """todo: populate this with engine details."""


# The default config file.
_default_config_text = """; Site configuration.
[config]
port = 5555
index_element_id = index
post_element_id = post

; Globally scoped metadata.
[metadata]
site_name = {site_name}"""


# The default index.html template file.
_default_index_html_template = """<html lang=\"en\">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{site_name}</title>
    </head>
    <body>
        <div id=\"index\">

        </div>
    </body>
</html>"""


# The default post.html template file.
_default_post_html_template = """<html lang=\"en\">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <div id=\"post\">
            
        </div>
    </body>
</html>"""


# The default post markdown file.
_default_post_markdown_template = """<!--
[metadata]
title: {title}
-->

# {title}"""


# Creates a post in the given site tree.
def create_post(title):
    try:
        util.write_file_text(
            f"posts/{util.name_to_path(title)}.md",
            _default_post_markdown_template.format(title=title),
        )
        return True
    except:
        return False


# Checks if a post exists in the given site tree.
def post_exists(title):
    return os.path.exists(f"posts/{util.name_to_path(title)}.md")


# Creates a site tree at the given path.
def create_site(site_name, site_path):
    try:
        # Create site directories.
        os.makedirs(f"{site_path}/posts")
        os.makedirs(f"{site_path}/public")
        os.makedirs(f"{site_path}/templates")

        # Create site files.
        util.write_file_text(f"{site_path}/help.txt", _help_text)

        util.write_file_text(
            f"{site_path}/site.cfg",
            _default_config_text.format(site_name=site_name),
        )

        util.write_file_text(
            f"{site_path}/templates/index.html", _default_index_html_template
        )

        util.write_file_text(
            f"{site_path}/templates/post.html", _default_post_html_template
        )

        return True

    except:
        return False


# Determines whether a directory is a site tree.
def is_site_tree(path):
    required_dirs = ["posts", "public", "templates"]
    required_files = ["site.cfg", "templates/index.html", "templates/post.html"]

    # Check for required directories.
    for directory in required_dirs:
        if not os.path.isdir(os.path.join(path, directory)):
            return False

    # Check for required files.
    for file in required_files:
        if not os.path.isfile(os.path.join(path, file)):
            return False

    return True


# Determines whether any file in site tree has been modified since the given time.
def is_modified_since(path, time):
    pass
