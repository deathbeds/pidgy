``pidgy`` literate ``notebook`` programming
===========================================

|Binder| |Documentation Status|

``pidgy`` is literate programming kernel and shell for ``IPython``. When
``pidgy`` is enabled: \* Write code in ``markdown``, indented and fenced
are executed. \* ``doctest``\ s in ``markdown`` are tested. \* Include
``object``\ s in ``markdown`` with ``jinja2`` ``template`` syntax. \*
``notebook``\ s can be woven and tangled as documentation and code. \*
``notebook``\ s can be reproduced as tests. \* ``".md.ipynb"`` is a
composite extension that indicates ``pidgy`` ``notebook``\ s primarly
written in ``markdown``

The ``pidgy`` programming paper.
--------------------------------

``pidgy`` is written as literate programming in ``notebook``\ s; the
narrative develop together into a cohesive program that serves dually as
literature and reusable source code.

.. |Binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/deathbeds/pidgy/master
.. |Documentation Status| image:: https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest
   :target: https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest




::

   import pidgy




``pidgy`` command line application
----------------------------------




Install the ``IPython`` kernels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the ``pidgy`` kernel so you can use whenever you want.

.. code:: bash

   pidgy kernel install




Load the ``IPython`` extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Otherwise, using the ``pidgy`` ``IPython`` extension any ``jupyter``
``notebook``.

.. code:: bash

   %load_ext pidgy

Likely, the only other paper of the api you made need is the
``pidgy.pidgyLoader`` that allows ``pidgy`` documents to be imported as
normal source code. The loader searches for ``notebook``\ s with the
``".md.ipynb"`` extension and adds them to the python import system.




reuse ``pidgy`` documents as modules
------------------------------------

::

   with pidgy.pidgyLoader():
       import readme
   assert readme.__file__.endswith('.md.ipynb')




The plurality of ``pidgy``
--------------------------

Above we’ve highlight a few outcomes of ``pidgy`` programming. ``pidgy``
is written as both documentation and source code therefore it can be
viewed by the following tools.

-  `nbviewer <https://nbviewer.jupyter.org/github/deathbeds/pidgy/blob/master/readme.md.ipynb>`__
-  `github pages <https://deathbeds.github.io/pidgy/>`__
-  `readthedocs <https://pidgin-notebook.readthedocs.io/en/latest/>`__
-  `binder <https://mybinder.org/v2/gh/deathbeds/pidgy/master>`__
-  `actions <https://github.com/deathbeds/pidgy/actions>`__

