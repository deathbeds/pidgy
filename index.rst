*****
pidgy programming 
*****

|Binder| |Documentation Status| |Python package| |PyPI - Python Version|

.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/deathbeds/pidgy/master?urlpath=lab
.. |Documentation Status| image:: https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest
   :target: https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest
.. |Python package| image:: https://github.com/deathbeds/pidgy/workflows/Python%20package/badge.svg
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/pidgy

`pidgy` treats code as literature and programming as a literacy. It is an interactive programming workflow in Markdown that allows narrative and code to develop together.

`pidgy` has literary and computational qualities that:

-  Publish documentation and render PDFs using the
   `ReadTheDocs <https://pidgy.readthedocs.io/>`__ service.
-  Make it installable from `pip <https://pypi.org/project/pidgy>`__ and
   conda.

   .. code:: bash

      pip install pidgy

-  Formally test the literature and source code with `Github
   Actions <https://github.com/deathbeds/pidgy/actions>`__.
-  Reusable on
   `Binder <https://mybinder.org/v2/gh/deathbeds/pidgy/master>`__.
-  Import alternative source files into python like `notebooks and
   markdown <https://github.com/deathbeds/pidgy/tree/master/pidgy>`__.


.. toctree::
    :glob:
    
    README.md

pidgy paper
-----------

.. toctree::
    :glob:
    
    docs/intro.md
    
pidgy specification
===================

.. toctree::
    :glob:


    pidgy/shell.md
    
pidgy implementation
====================

.. toctree::
    :glob:

    pidgy/tangle.ipynb
    pidgy/extras.ipynb
    pidgy/loader.ipynb
    pidgy/weave.md    
    pidgy/testing.md
    pidgy/tests/test_pidgin_syntax.md.ipynb
    
pidgy applications
==================

.. toctree::
    :glob:
    
    pidgy/kernel.md
    pidgy/export.md
    pidgy/runpidgy.md
    pidgy/pytest_config/readme.md
    pidgy/readme.md
    docs/discussion.md.ipynb

pidgy tests
-----------

.. toctree::
    :glob:

    pidgy/tests/test_tangle.ipynb
    pidgy/tests/test_weave.md.ipynb
    pidgy/tests/test_runpidgy.md.ipynb
    pidgy/tests/test_magic.ipynb
    pidgy/tests/test_cli.ipynb
    pidgy/tests/test_3rd_party.ipynb
    docs/examples/fastapi_application.md
    docs/examples/working-within-dataframes.md.ipynb
    docs/figures.md.ipynb
    
Source
-----------

.. toctree::
    :glob:
    :maxdepth: 4

    
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


