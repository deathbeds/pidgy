from pathlib import Path
import setuptools

name = "pidgy"

__version__ = None

here = Path(__file__).parent

setup_args = dict(
    name=name,
    version='0.2.2',
    author="deathbeds",
    author_email="tony.fast@gmail.com",
    description="Conventions for writing code in the notebook.",
    long_description=(
        (here / "README.rst").read_text() + "\n\n"
    ),
    url="https://github.com/deathbeds/pidgy",
    python_requires=">=3.6",
    license="BSD-3-Clause",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', "hypothesis", 'nbval'],
    install_requires=[
        "nbconvert", "importnb", "IPython>7", 'dataclasses', "ruamel.yaml", "pyld", "jsonpointer", "jsonschema", "emoji", "htmlmin", "webcolors", "attrs>=17.4.0"
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points = {
        'pytest11': ['pidgy=pidgy.tests.plugin'],
        'console_scripts': ['pidgy=pidgy.app.__main__.cli:app'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",],
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
