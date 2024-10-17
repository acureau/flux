# Contains the flux command-line interface.

# We're going to need to pull out config parsing logic because each markdown file will have a comment header with metadata.

import os
import util
import config
import argparse
import sitetree
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler


def cmd_create_post(title):

    # Get working directory.
    working_directory = os.getcwd()

    # Ensure working directory is a site tree.
    if not sitetree.is_site_tree(working_directory):
        print("Working directory is not a site tree.")
        return -1

    # Ensure post does not exist already.
    if sitetree.post_exists(title):
        print("Post with the same name already exists.")
        return -1

    # Create post.
    if sitetree.create_post(title):
        print(f"Created post titled '{title}'.")
        return 0
    else:
        print("Could not create post.")
        return -1


def cmd_create_site(site_name):

    # Make sure site path does not exist.
    site_path = util.name_to_path(site_name)
    if os.path.exists(site_path):
        print(f"Site tree could not be created because '{site_path}' already exists.")
        return -1

    # Create site tree.
    if sitetree.create_site(site_name, site_path):
        print(f"Created a site tree at '{site_path}'.")
        return 0
    else:
        print("Could not create site tree.")
        return -1


def cmd_build_site(silent=False):

    # Get working directory.
    working_directory = os.getcwd()

    # Ensure working directory is a site tree.
    if not sitetree.is_site_tree(working_directory):
        print("Working directory is not a site tree.")
        return -1

    # Parse config file.
    if not config.init("site.cfg"):
        print("Could not load 'site.cfg' config file.")
        return -1


def cmd_serve_site():

    # Try to build the site.
    if cmd_build_site(silent=True) == -1:
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
