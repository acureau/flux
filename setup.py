from setuptools import setup, find_packages

setup(
    name="flux",
    description="A blog engine in flux.",
    version="1.0.0",
    author="Alec Cureau",
    author_email="alec.cureau@gmail.com",
    url="https://github.com/acureau/flux",
    install_requires=[
        "beautifulsoup4==4.12.3",
        "marko==2.1.2",
        "setuptools==75.2.0",
        "soupsieve==2.6"
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "flux = flux.cli:init",
        ]
    }
)