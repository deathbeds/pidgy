import datetime
import os
import sys
from pathlib import Path

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

try:
    from jupyter_client.kernelspec import KernelSpecManager

    HAVE_JUPYTER = True
except ImportError:
    HAVE_JUPYTER = False


class kernelspec:
    def run(self, *args, **kwargs):
        install_jupyter_hook()
        print("install jupyter")
        install.run(self, *args, **kwargs)


class install_hook(install, kernelspec):
    pass


class develop_hook(develop, kernelspec):
    pass


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
            "./src/pidgy/kernel/kernelspec", "pidgy", user=user
        )
        return
    except:
        pass

    try:
        KernelSpecManager().install_kernel_spec(
            "./src/pidgy/kernel/kernelspec", "pidgy", user=not user
        )
        return
    except:
        pass


setup_args = dict(
    setup_cfg=True,
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
    cmdclass={"install": install_hook, "develop": develop_hook},
    zip_safe=False,
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
