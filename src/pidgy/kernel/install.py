from pathlib import Path
from sys import argv

HERE = Path(__file__).parent
KERNELSPEC = HERE / "kernelspec"

try:
    from jupyter_client.kernelspec import KernelSpecManager

    HAVE_JUPYTER = True
except ImportError:
    HAVE_JUPYTER = False


def install_jupyter_hook():
    """Make pidgy available as a Jupyter kernel."""

    if not HAVE_JUPYTER:
        return print(
            "Could not install Jupyter kernel spec, please install " "Jupyter/IPython."
        )

    user = "--user" in argv
    print("Installing Jupyter kernel spec:")
    try:
        KernelSpecManager().install_kernel_spec(str(KERNELSPEC), "pidgy", user=user)
        return
    except:
        pass

    try:
        KernelSpecManager().install_kernel_spec(str(KERNELSPEC), "pidgy", user=not user)
        return
    except:
        pass


if __name__ == "__main__":
    # TODO: a better cli install/uninstall
    install_jupyter_hook()
