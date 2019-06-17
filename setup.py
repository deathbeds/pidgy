from pathlib import Path
import setuptools

name = "pidgin"

__version__ = None

here = Path(__file__).parent

setup_args = dict(
    name=name,
    version='0.1.0',
    author="deathbeds",
    author_email="tony.fast@gmail.com",
    description="Conventions for writing code in the notebook.",
    long_description=(
        (here / "readme.md").read_text() + "\n\n"
    ),
    long_description_content_type='text/markdown',
    url="https://github.com/deathbeds/pidgin",
    python_requires=">=3.6",
    license="BSD-3-Clause",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', "hypothesis", 'nbval'],
    install_requires=[
        "nbconvert", "importnb", "IPython>7", 'dataclasses', "ruamel.yaml", "pyld", "jsonpointer", "jsonschema", "emoji", "htmlmin", "webcolors", "attrs>=17.4.0"
    ],
    include_package_data=True,
    py_modules=['pidgin'],
    #packages=setuptools.find_packages(where='src'),
    #package_dir={'':'src',},
    entry_points = {
        'pytest11': [],
    },
    classifiers=(
        "Development Status :: 4 - Beta",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",),
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
