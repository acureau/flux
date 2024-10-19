# Contains functionality related to creating, verifying, and working with site trees.


import os
from flux import util


# The help text file.
_help_text = """This is your site directory. Flux commands must be executed at the root of this directory.
First, inspect the `site.cfg` file. This config file has two sections: config and metadata.
Config parameters change how flux works, a list of them can be found below.

port - The port the development server uses to host the site.
index_div_id = The ID of HTML div element containing the generated index.
post_div_id = The ID of HTML div element containing a generated post.

A metadata parameter is used by the templating engine to insert values in to your HTML. You 
can define any key-value pair here. Metadata values defined in the `site.cfg` file are global.
This means they're accessible by all templates and take precedence over local metadata. Have a 
look at how `site_name` is used in the default `index.html` template:

<title>{site_name}</title>

Get the jist? Local metadata values are defined in a comment header at the top of a markdown
file. Like so:

<!--
[metadata]
title: <title>
-->

One more helpful feature, HTML templates can insert file contents by providing a path instead
of a metadata key. Like so:

<body>
    {@navbar.html}
<body>

All of your HTML templates should live in the templates directory, `index.html` and `post.html`
must exist for flux to work. Put all public resources (images, CSS, etc.) in the public directory.

That's all there is to it. I've kept the code small and simple, so don't be afraid to jump in 
and fix a bug or add a feature. To create a new post, run the following command:

flux create post \"<post name>\"
"""


# The default config file.
_default_config_text = """; Site configuration.
[config]
port = 5555
index_div_id = index
post_div_id = post

; Globally scoped metadata.
[metadata]
site_name = {site_name}
"""


# The default index.html template file.
_default_index_html_template = """<html lang=\"en\">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{site_name}</title>
    </head>
    <h1>{site_name}</h1>
    <body>
        {index}
    </body>
</html>
"""


# The default post.html template file.
_default_post_html_template = """<html lang=\"en\">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        {post}
    </body>
</html>
"""


# The default post markdown file.
_default_post_markdown_template = """<!--
[metadata]
title: {title}
-->
"""


# Creates a post in the given site tree.
def create_post(site_path, title):
    try:
        util.write_file_text(
            f"{site_path}/posts/{util.name_to_path(title)}.md",
            _default_post_markdown_template.format(title=title),
        )
        return True
    except:
        return False


# Checks if a post exists in the given site tree.
def post_exists(site_path, title):
    return os.path.exists(f"{site_path}/posts/{util.name_to_path(title)}.md")


# Creates a site tree at the given path.
def create_site(site_path, site_name):
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
def is_site_tree(site_path):
    required_dirs = ["posts", "public", "templates"]
    required_files = ["site.cfg", "templates/index.html", "templates/post.html"]

    # Check for required directories.
    for directory in required_dirs:
        if not os.path.isdir(os.path.join(site_path, directory)):
            return False

    # Check for required files.
    for file in required_files:
        if not os.path.isfile(os.path.join(site_path, file)):
            return False

    return True


# Determines whether any file in site tree has been modified since the last build.
def modified_since_build(site_path):

    # If the .build directory exists get its modified time.
    if os.path.exists(f"{site_path}/.build"):
        build_modified_time = os.path.getmtime(f"{site_path}/.build")

        # Walk the site tree.
        for root, dirs, files in os.walk(site_path):

            # Exclude the .build directory.
            if ".build" in dirs:
                dirs.remove(".build")

            # Check each file for a more recent modified time.
            for file in files:
                if os.path.getmtime(os.path.join(root, file)) > build_modified_time:
                    return True

    # If it doesn't exist, the site has been modified since the last build.
    else:
        return True

    return False
