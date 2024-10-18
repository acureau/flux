# Contains functionality related to converting markdown and building templates.


# Resolves file inclusion in HTML templates.
def resolve_file_includes(html):
    # Find all bracket pairs {} in HTML string. For each:
    # Where value between brackets starts with @, check if the rest is a path.
    # If so load the string and recursively pass it to this function.
    # Return the result.
    pass


# Converts a list of paths to a metadata collection.
def paths_to_index(paths):
    # Build unordered list of a elements in HTML using bs4.
    # Insert html string into metadata dictionary with key "index".
    # Return dictionary.
    pass


# Converts a markdown post to a metadata collection.
def markdown_to_post(markdown):
    # Parse comment header, remove from MD.
    # Get metadata table using config method.
    # Convert markdown to HTML with marko, insert html string into metadata tag "post".
    # Return metadata table.
    pass


# Builds a template with HTML and metadata.
def build(html, metadata):
    # Find all bracket pairs {} in HTML string.
    # If value between them is a metadata key, replace the whole substring (brackets included) with the value.
    # Return HTML string.
    pass
