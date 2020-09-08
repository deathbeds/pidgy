from pathlib import Path
import setuptools, datetime, sys, os
from setuptools.command.install import install


try:
    from jupyter_client.kernelspec import KernelSpecManager

    HAVE_JUPYTER = True
except ImportError:
    HAVE_JUPYTER = False


class kernelspec(install):
    def run(self):
        print("run")
        root = self.root if self.root else None
        prefix = self.prefix if self.prefix else None
        try:
            install_jupyter_hook(prefix=prefix, root=root)
        except Exception:
            import traceback

            traceback.print_exc()
            print("Installing Jupyter hook failed.")
        install.run(self)


def install_jupyter_hook(prefix=None, root=None):
    """Make pidgy available as a Jupyter kernel."""

    if not HAVE_JUPYTER:
        print(
            "Could not install Jupyter kernel spec, please install " "Jupyter/IPython."
        )
    return

    if "CONDA_BUILD" in os.environ:
        prefix = sys.prefix
        if sys.platform == "win32":
            prefix = prefix.replace(os.sep, os.altsep)
    user = "--user" in sys.argv
    print("Installing Jupyter kernel spec:")
    print("  root: {0!r}".format(root))
    print("  prefix: {0!r}".format(prefix))
    print("  as user: {0}".format(user))
    if root and prefix:
        # os.path.join isn't used since prefix is probably absolute
        prefix = root + prefix
        print("  combined prefix {0!r}".format(prefix))
    KernelSpecManager().install_kernel_spec(
        "./pidgy/kernelspec", "pidgy", user=user, replace=True, prefix=prefix
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
    cmdclass={"install": kernelspec},
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
