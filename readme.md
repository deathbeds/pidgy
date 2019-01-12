
`pidgin` is a collection of `IPython` extensions for creating computable essays.

[![Build Status](https://travis-ci.org/deathbeds/pidgin.svg?branch=master)](https://travis-ci.org/deathbeds/pidgin)[![Documentation Status](https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)


    #Install pidgin
    !pip install pidgin

Load the `pidgin` extension.

Write code in __Markdown__.


<pre><code>    %reload_ext pidgin
</code></pre>
<p><code>import pidgin</code> allows <strong>Markdown</strong> as <strong>Code Cell</strong> source in <code>IPython</code>.</p>
<ol>
<li>The <strong>Markdown</strong> is converted to valid <strong>Python</strong> source.</li>
<li>The <strong>Python</strong> source is executed.</li>
<li>Any <code>"doctest"</code>s are evaluated.</li>
<li>All inline code is evaluated.</li>
<li><p>The <strong>Markdown</strong> source is display with special rules defined in <code>pidgin.display</code> including <code>"jinja2"</code> templates
for including data in the display.</p>

</li>
</ol>
<p>Each of the above steps must succeed without raising an <code>Exception</code>.</p>



<h2>Benefits of <code>pidgin</code></h2>
<ul>
<li><code>pidgin</code> requires that all code in a document is valid.</li>
<li><code>pidgin</code> places tighter constraints on the <strong>Run All-ability</strong> of the document.</li>
<li><p><code>pidgin</code> encourages tighter weaving of code and narrative.</p>

<p>Use <code>jinja2</code> syntax in <strong>Code Cells</strong>.  On the last display step with include
  pretty representations of template expression.  The <code>jinja2.Environment</code> returns <strong>html</strong> formatted
  display <code>object</code>s including <code>"pandas"</code> tables and <code>"matplotlib"</code> figures.</p>
</li>
<li><code>pidgin</code> separates display statements from compute statements.</li>
<li><code>pidgin</code> documents are importable because of <code>import importnb</code>        </li>
</ul>


`pidgin` introduces __.md.ipynb__, a hybrid file extension, to identify __Markdown__-forward computational essays. When
this document (`readme`) is imported without
<pre><code class="lang-ipython">with pidgin.PidginImporter(position=1):
    from . import readme as readme
</code></pre>
we can `assert readme.__file__.endswith('.md.ipynb')`.


<h2><code>pidgin</code> works with</h2>
<ul>
<li><p><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme_pidgin.md.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a></p>
<p>Take <code>pidgin</code> for a spin on <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><strong><em>Binder</em></strong></a>.</p>
</li>
<li><p><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a></p>
<p><code>pidgin</code> works great with the <a href="https://github.com/computationalmodelling/nbval"><strong>nbval</strong></a> and <a href="https://github.com/deathbeds/importnb"><strong>importnb</strong></a> notebook specific pytest extensions.  <code>pidgin</code> itself is a <code>import pytest</code>
  plugin that permits tests with <strong>.md.ipynb</strong> and <strong>.md</strong> extensions.</p>
<p><strong><em>Pro Tip</em></strong>: test <code>IPython</code>-specific features using <strong>ipython</strong> as the <code>pytest</code> runner instead of <strong>python</strong> <code>#!ipython -m pytest -- --collect-only</code></p>
</li>
<li><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a> </li>
<li><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a> </li>
<li><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></li>
<li><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></li>
</ul>



<h2>Architecture</h2>
<p>The <code>pidgin</code> source is written almost entirely in Jupyter notebooks.  The hope is that the notebooks will serve as an important
interactive resource in the early development.  As the project matures, <code>pidgin</code> will adopt different combinations of python
and notebook files.</p>
<pre><code>ip = IPython.get_ipython()
</code></pre>
<p><code>pidgin</code> is architected as a collection of <code>IPython</code> extensions that modify <code>ip = IPython.get_ipython()</code> and <code>ip.kernel</code>.</p>

<p>Each component of <code>pidgin</code> can be loaded individually.</p>
<pre><code>    %reload_ext pidgin.tangle
    %reload_ext pidgin.display
    %reload_ext pidgin.inspector
    %reload_ext pidgin.post_run_cell
</code></pre>



<h2>Roadmap</h2>
<ul>
<li><code>pidgin</code> should become an <code>import ipykernel</code>.</li>
<li><code>pidgin</code> should extend to other ipykernels.</li>
<li><code>pidgin</code> should become an <code>import nbconvert.nbconvertapp</code> and <code>nbconvert.preprocessors</code>.</li>
</ul>


## Developer


    !ipython -m readme_pidgin.md.ipynb -- --uml=True --nbconvert=True --test=True

### Test `pidgin`

    if __name__ == '__main__':
        !ipython -m pytest -- --nbval


<h3>Run tests</h3>
<pre><code>test = False
</code></pre>


    %%file sanitize.cfg
    [skip_graphviz]
    regex: <svg(.|\n)*</svg>w
    replace: ---




<h3>UML diagrams</h3>
<pre><code>uml = False
</code></pre>



<h3>Convert to the <strong>readme.md</strong></h3>
<pre><code>convert=False
</code></pre>


    %%file markdown_readme.py
    c.MarkdownExporter.raw_mimetypes = ['text/markdown']
    c.TemplateExporter.exclude_input=True
