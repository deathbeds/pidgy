
`pidgin` is a collection of `IPython` extensions for creating computable essays.

    #Execute this cell to install pidgin.
    #!pip install pidgin
    !pip install git+https://github.com/deathbeds/pidgin

Then load the `pidgin` extension.


<pre><code>    import pidgin, IPython
</code></pre>
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
<pre><code>  import jinja2
</code></pre>
<p>Use <code>jinja2</code> syntaxes in <strong>Code Cells</strong>.  On the last display step with include 
  pretty representations of template expression.  The <code>jinja2.Environment</code> returns <strong>html</strong> formatted
  display <code>object</code>s including <code>"pandas"</code> tables and <code>"matplotlib"</code> figures.</p>
</li>
<li><code>pidgin</code> separates display statements from compute statements.</li>
<li><code>pidgin</code> documents are importable because of <code>import importnb</code>        </li>
</ul>
<pre><code class="lang-python">with pidgin.PidginImporter(position=1):
    import readme_pidgin as readme
</code></pre>


`pidgin` introduces __.md.ipynb__, a hybird file extension, to identity __Markdown__ forward computational essays. When
this document (`readme`) is imported we can `assert readme.__file__.endswith('.md.ipynb')`.


<h2><code>pidgin</code> works with</h2>
<ul>
<li><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a> </li>
<li><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a> </li>
<li><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a> </li>
<li><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a> </li>
<li><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></li>
<li><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></li>
</ul>


## Architecture

    ip = IPython.get_ipython()
`pidgin` is architected as a collection of `IPython` extensions that modify `ip = IPython.get_ipython()` and `ip.kernel`.
    
    %reload_ext pidgin
    
Each component of `pidgin` can be loaded individually.

    %reload_ext pidgin.tangle
    %reload_ext pidgin.display
    %reload_ext pidgin.inspector
    %reload_ext pidgin.post_run_cell


<h2>Roadmap</h2>
<ul>
<li><code>pidgin</code> should become an <code>import ipykernel</code>.</li>
<li><code>pidgin</code> should extend to other ipykernels.</li>
<li><code>pidgin</code> should become an <code>import nbconvert.nbconvertapp</code>.</li>
</ul>


## Developer
    

    !ipython -m readme -- --uml=True --nbconvert=True --test=True

### Test `pidgin`

    if __name__ == '__main__':
        !ipython -m pytest -- --nbval


<h3>Run tests</h3>
<pre><code>test = False
</code></pre>



<h3>UML diagrams</h3>
<pre><code>uml = False
</code></pre>



<h3>Convert to the <strong>readme.md</strong></h3>
<pre><code>nbconvert=False
</code></pre>

