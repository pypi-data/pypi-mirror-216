import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="croqueta", # Replace with your own username
    version="0.2.3",
    author="juanluisrto",
    author_email="juanluis.rto@gmail.com",
    description="A bunch of utilities to code even faster.",
    url="https://github.com/juanluisrto/croqueta",
    packages= setuptools.find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=[

      ]
)
 