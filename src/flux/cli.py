# Contains the command-line interface.


import os
import shutil
import argparse
from flux import template, sitetree, config, util
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


def cmd_create_post(title):

    # Get site path.
    site_path = os.getcwd()

    # Ensure working directory is a site tree.
    if not sitetree.is_site_tree(site_path):
        print("Working directory is not a site tree.")
        return -1

    # Ensure post does not exist already.
    if sitetree.post_exists(site_path, title):
        print("Post with the same name already exists.")
        return -1

    # Create post.
    if sitetree.create_post(site_path, title):
        print(f"Created post titled '{title}'.")
        return 0
    else:
        print("Could not create post.")
        return -1


def cmd_create_site(site_name):

    # Make sure site path does not exist.
    site_path = os.path.join(os.getcwd(), util.name_to_path(site_name))
    if os.path.exists(site_path):
        print(f"Site tree could not be created because '{site_path}' already exists.")
        return -1

    # Create site tree.
    if sitetree.create_site(site_path, site_name):
        print(f"Created a site tree at '{site_path}'.")
        return 0
    else:
        print("Could not create site tree.")
        return -1


def cmd_build_site(silent_success=False):
    try:
        # Get working directory.
        site_path = os.getcwd()

        # Ensure working directory is a site tree.
        if not sitetree.is_site_tree(site_path):
            print("Working directory is not a site tree.")
            return -1

        # Parse config file.
        if not config.init("site.cfg"):
            print("Could not load 'site.cfg' config file.")
            return -1

        # If .build directory is outdated, delete it.
        if sitetree.modified_since_build(site_path):
            if os.path.exists(".build"):
                shutil.rmtree(".build")
        else:
            if not silent_success:
                print("Site build already up to date.")
            return 0

        # Make .build directory and copy public directory into it.
        os.makedirs(".build/posts")
        shutil.copytree("public", ".build/public")

        # Load HTML templates and resolve file includes.
        os.chdir("templates")
        post_html = template.resolve_file_includes(util.read_file_text("post.html"))
        index_html = template.resolve_file_includes(util.read_file_text("index.html"))
        os.chdir("..")

        # Create posts.
        post_path_name_map = {}
        for file in os.listdir("posts"):
            if file.endswith(".md"):

                # Parse post markdown.
                post_metadata = template.markdown_to_post(
                    util.read_file_text(f"posts/{file}")
                )

                # Make sure title is provided.
                if not "title" in post_metadata:
                    print(f"Post '{file}' must contain metadata key 'title'.")
                    return -1

                # Build HTML post with template and metadata.
                post_html_file = file.replace(".md", ".html")
                util.write_file_text(
                    f".build/posts/{post_html_file}",
                    template.build(post_html, post_metadata),
                )

                # Insert post into path:name map for index.
                post_path_name_map[f"posts/{post_html_file}"] = post_metadata["title"]

        # Create index.
        index_metadata = template.posts_to_index(post_path_name_map)
        util.write_file_text(
            ".build/index.html", template.build(index_html, index_metadata)
        )

        if not silent_success:
            print("Site built successfully.")
        return 0
    except:
        print("Could not build site.")
        return -1


def cmd_serve_site():

    # Try to build the site.
    if cmd_build_site(silent_success=True) == -1:
        return -1

    # Get port from config.
    port = 5555
    if config.has("port"):
        port_string = config.get("port")
        if port_string.isnumeric() and 1 <= int(port_string) <= 65535:
            port = int(port_string)

    # Serve site.
    os.chdir(".build")
    with ThreadingHTTPServer(("", port), SimpleHTTPRequestHandler) as server:
        print(f"Serving at 'http://localhost:{port}', CTRL+C to stop.\n")
        try:
            server.serve_forever()
        except:
            return 0


def create_argument_parser():

    # Define argument parser and subparsers container.
    argument_parser = argparse.ArgumentParser(
        prog="flux", description="A blog engine in flux."
    )
    subparsers = argument_parser.add_subparsers(dest="command")

    # Configure the new command.
    create_parser = subparsers.add_parser("create", help="Create new content.")
    create_subparsers = create_parser.add_subparsers(
        dest="type", help="The type of content to create."
    )

    # Configure the new site sub-command.
    create_site_parser = create_subparsers.add_parser(
        "site", help="Create a new site directory."
    )
    create_site_parser.add_argument("name", help="The name of the new site.")
    create_site_parser.set_defaults(func=lambda args: cmd_create_site(args.name))

    # Configure the new post sub-command.
    create_article_parser = create_subparsers.add_parser(
        "post", help="Create a new post in the working site directory."
    )
    create_article_parser.add_argument("title", help="The title of the new post.")
    create_article_parser.set_defaults(func=lambda args: cmd_create_post(args.title))

    # Configure the build command.
    build_parser = subparsers.add_parser(
        "build", help="Build the site in the working directory."
    )
    build_parser.set_defaults(func=lambda _: cmd_build_site())

    # Configure the serve command.
    serve_parser = subparsers.add_parser(
        "serve", help="Serve the site in the working directory."
    )
    serve_parser.set_defaults(func=lambda _: cmd_serve_site())

    return argument_parser


def init():

    # Parse command line arguments.
    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    # Call the corresponding function based on the parsed arguments.
    if hasattr(args, "func"):
        return args.func(args)
    else:
        argument_parser.print_help()


if __name__ == "__main__":
    init()
