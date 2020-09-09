from pathlib import Path
import setuptools, datetime, sys, os
from setuptools.command.build_ext import build_ext


try:
    from jupyter_client.kernelspec import KernelSpecManager

    HAVE_JUPYTER = True
except ImportError:
    HAVE_JUPYTER = False


class kernelspec(build_ext):
    def run(self, *args, **kwargs):
        install_jupyter_hook()
        build_ext.run(self, *args, **kwargs)


def install_jupyter_hook():
    """Make pidgy available as a Jupyter kernel."""

    if not HAVE_JUPYTER:
        return print(
            "Could not install Jupyter kernel spec, please install " "Jupyter/IPython."
        )

    user = "--user" in sys.argv
    print("Installing Jupyter kernel spec:")
    try:
        KernelSpecManager().install_kernel_spec(
            "./pidgy/kernelspec", "pidgy", user=user
        )
    except:
        KernelSpecManager().install_kernel_spec(
            "./pidgy/kernelspec", "pidgy", user=not user
        )


name = "pidgy"

__version__ = None

here = Path(__file__).parent

setup_args = dict(
    name=name,
    version=datetime.datetime.now().strftime("%Y.%m.%d"),
    author="deathbeds",
    author_email="tony.fast@gmail.com",
    description="Literate computing for literate programming",
    long_description=((here / "README.md").read_text() + "\n\n"),
    long_description_content_type="text/markdown",
    url="https://github.com/deathbeds/pidgy",
    python_requires=">=3.6",
    license="BSD-3-Clause",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "hypothesis", "nbval"],
    install_requires=Path("requirements.txt").read_text().strip().splitlines(),
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={
        "pytest11": ["pytest-pidgy=pidgy.pytest_config"],
        "console_scripts": ["pidgy=pidgy.__main__:application"],
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Pytest",
    ],
    cmdclass={"build_ext": kernelspec},
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
