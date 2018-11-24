
`pidgin` is a collection of `IPython` extensions for creating computable essays.

    #Execute this cell to install pidgin.
    #!pip install pidgin
    !pip install git+https://github.com/deathbeds/pidgin

Then load the `pidgin` extension.


<div class="highlight"><pre><span></span>    <span class="kn">import</span> <span class="nn">pidgin</span><span class="o">,</span> <span class="nn">IPython</span>
</pre></div>
<p><code>pidgin</code> allows <strong>Markdown</strong> as <strong>Code Cell</strong> source in <code>IPython</code>.</p>
<ol>
<li>The <strong>Markdown</strong> is converted to valid <strong>Python</strong> source.</li>
<li>The <strong>Python</strong> source is executed.</li>
<li>Any <code>"doctest"</code>s are evaluated.</li>
<li>All inline code is evaluated.</li>
<li>The <strong>Markdown</strong> source is display with special rules defined in <code>pidgin.display</code> including <code>"jinja2"</code> templates
for including data in the display.</li>
</ol>
<p>Each stuff must succeed without raising an <code>Exception</code>.</p>



<h2>Benefits of <code>pidgin</code></h2>
<ul>
<li><code>pidgin</code> requires that all code in a document is valid.</li>
<li><code>pidgin</code> places tighter constraints on the <strong>Run All-ability</strong> of the document.</li>
<li><p><code>pidgin</code> encourages tighter weaving of code and narrative.</p>
<div class="highlight"><pre><span></span>  <span class="kn">import</span> <span class="nn">jinja2</span>
</pre></div>
<p>Use <code>jinja2</code> syntaxes in <strong>Code Cells</strong>.  On the last display step with include 
  pretty representations of template expression.  The <code>jinja2.Environment</code> returns <strong>html</strong> formatted
  display <code>object</code>s including <code>"pandas"</code> tables and <code>"matplotlib"</code> figures.</p>
</li>
<li><code>pidgin</code> separates display statements from compute statements.</li>
<li><code>pidgin</code> documents are importable because of <code>import importnb</code>        </li>
</ul>
<div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">pidgin</span><span class="o">.</span><span class="n">PidginImporter</span><span class="p">(</span><span class="n">position</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span>
    <span class="kn">import</span> <span class="nn">readme_pidgin</span> <span class="kn">as</span> <span class="nn">readme</span>
</pre></div>


`pidgin` introduces __.md.ipynb__, a hybird file extension, to identity __Markdown__ forward computational essays. When
this document (`readme`) is imported we can `assert readme.__file__.endswith('.md.ipynb')`.


<h2><code>pidgin</code> works with</h2>
<ul>
<li><p><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a></p>
<p>Take <code>pidgin</code> for a spin on <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><strong><em>Binder</em></strong></a>.</p>
</li>
<li><p><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a></p>
<p><code>pidgin</code> works great with the <a href="https://github.com/computationalmodelling/nbval"><strong>nbval</strong></a> and <a href="https://github.com/deathbeds/importnb"><strong>importnb</strong></a> notebook specific pytest extensions.  <code>pidgin</code> itself is a <code>import pytest</code>
  plugin that permits tests with <strong>.md.ipynb</strong> and <strong>.md</strong> extensions.</p>
<p><strong><em>Pro Tip</em></strong> test <code>IPython</code> specific features using <strong>ipython</strong> as the <code>pytest</code> runner instead of <strong>python</strong> <code>#!ipython -m pytest -- --collect-only</code></p>
</li>
<li><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a> </li>
<li><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a> </li>
<li><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></li>
<li><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></li>
</ul>



<h2>Architecture</h2>
<p>The <code>pidgin</code> source is written almost entirely in Jupyter notebooks.  The hope is that the notebooks will serve as an important
interactive resourcing in the early development.  As the project matures, <code>pidgin</code> will adopt different combinations of python
and notebook files.</p>
<div class="highlight"><pre><span></span><span class="n">ip</span> <span class="o">=</span> <span class="n">IPython</span><span class="o">.</span><span class="n">get_ipython</span><span class="p">()</span>
</pre></div>
<p><code>pidgin</code> is architected as a collection of <code>IPython</code> extensions that modify <code>ip = IPython.get_ipython()</code> and <code>ip.kernel</code>.</p>
<div class="highlight"><pre><span></span><span class="k">if</span> <span class="mi">0</span><span class="p">:</span>
    <span class="o">%</span><span class="k">reload_ext</span> pidgin
</pre></div>
<p>Each component of <code>pidgin</code> can be loaded individually.</p>
<div class="highlight"><pre><span></span>    <span class="o">%</span><span class="k">reload_ext</span> pidgin.tangle
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.display
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.inspector
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.post_run_cell
</pre></div>


    C:\Anaconda3\lib\site-packages\nbconvert\exporters\exporter_locator.py:28: DeprecationWarning: `nbconvert.exporters.exporter_locator` is deprecated in favor of `nbconvert.exporters.base` since nbconvert 5.0.
      DeprecationWarning)
    C:\Anaconda3\lib\site-packages\nbconvert\preprocessors\regexremove.py:41: DeprecationWarning: Traits should be given as instances, not types (for example, `Int()`, not `Int`). Passing types is deprecated in traitlets 4.1.
      patterns = List(Unicode, default_value=[r'\Z']).tag(config=True)
    C:\Anaconda3\lib\site-packages\traitlets\traitlets.py:2367: DeprecationWarning: Traits should be given as instances, not types (for example, `Int()`, not `Int`). Passing types is deprecated in traitlets 4.1.
      super(Set, self).__init__(trait, default_value, minlen, maxlen, **kwargs)
    C:\Anaconda3\lib\site-packages\tornado\web.py:1747: DeprecationWarning: @asynchronous is deprecated, use coroutines instead
      DeprecationWarning)
    


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
<div class="highlight"><pre><span></span><span class="n">test</span> <span class="o">=</span> <span class="bp">False</span>
</pre></div>



<h3>UML diagrams</h3>
<div class="highlight"><pre><span></span><span class="n">uml</span> <span class="o">=</span> <span class="bp">False</span>
</pre></div>



<h3>Convert to the <strong>readme.md</strong></h3>
<div class="highlight"><pre><span></span><span class="n">nbconvert</span><span class="o">=</span><span class="bp">False</span>
</pre></div>


    %%file markdown_readme.py
    c.MarkdownExporter.raw_mimetypes = ['text/markdown']
    c.TemplateExporter.exclude_input=True
