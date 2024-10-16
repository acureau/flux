# This file will be the command line interface. It will:
#  - Serve a blog directory.
#  - Create a new blog directory.
#  - Create a new article.

import argparse

def create_article(name):
    pass

def create_site(directory):
    pass

def build_site(directory):
    pass

def serve_site(directory):
    pass

def create_argument_parser():

    # Define argument parser and subparsers container.
    argument_parser = argparse.ArgumentParser(
        prog = "flux",
        description = "A blog engine in flux."
    )
    subparsers = argument_parser.add_subparsers(dest="command")

    # Configure the new command.
    new_parser = subparsers.add_parser("new", help="Create new content.")
    new_subparsers = new_parser.add_subparsers(dest="type", help="The type of content to create.")
    new_article_parser = new_subparsers.add_parser("article", help="Create a new article.")
    new_article_parser.add_argument("name", help="The name of the new article.")
    new_article_parser.set_defaults(func=lambda args: create_article(args.name))
    new_site_parser = new_subparsers.add_parser("site", help="Create a new site.")
    new_site_parser.add_argument("directory", help="The directory for the new site.")
    new_site_parser.set_defaults(func=lambda args: create_site(args.directory))

    # Configure the build command.
    build_parser = subparsers.add_parser("build", help="Build the blog site.")
    build_parser.add_argument("directory", help="The directory of the site to build")
    build_parser.set_defaults(func=lambda args: build_site(args.directory))

    # Configure the serve command.
    serve_parser = subparsers.add_parser("serve", help="Serve the blog site.")
    serve_parser.add_argument("directory", help="The directory of the site to serve")
    serve_parser.set_defaults(func=lambda args: serve_site(args.directory))

    return argument_parser

def init():

    # Parse command line arguments.
    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    # Call the corresponding function based on the parsed arguments.
    if hasattr(args, 'func'):
        args.func(args)
    else:
        argument_parser.print_help()

if (__name__ == "__main__"):
    init()