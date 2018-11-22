
`pidgin` is a collection of `IPython` extensions for creating computable essays.

    #Execute this cell to install pidgin.
    #!pip install pidgin
    !pip install git+https://github.com/deathbeds/pidgin@mistune

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
<li><p><code>pidgin</code> documents are importable because of <code>import importnb</code></p>
<pre><code>  with pidgin.PidginImporter():
      import readme
</code></pre>
<p><code>pidgin</code> introduces <strong>.md.ipynb</strong>, a hybird file extension, to identity <strong>Markdown</strong> forward computational essays. When
  this document (<code>readme</code>) is imported we can <code>assert readme.__file__.endswith('.md.ipynb')</code>.</p>
</li>
</ul>



<h2><code>pidgin</code> works on</h2>
<ul>
<li><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a> </li>
<li><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a> </li>
<li><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a> </li>
<li><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></li>
<li><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></li>
</ul>


## Architecture
    
    %reload_ext pidgin
    
Is equivalent to 

    %reload_ext pidgin.tangle
    %reload_ext pidgin.display
    %reload_ext pidgin.inspector
    %reload_ext pidgin.post_run_cell


<h2>Roadmap</h2>
<ul>
<li><code>pidgin</code> should become an <code>import ipykernel</code>.</li>
<li><code>pidgin</code> should extend to other ipykernels.</li>
<li><code>pidgin</code> should become an <code>import nbconvert.nbconvertapp</code>.</li>
<li><code>pidgin</code> should work with <code>import pytest</code></li>
</ul>


## Developer

    # Uncomment this cell the convert the readme file.
    !jupyter nbconvert --to markdown --execute --stdout --TemplateExporter.exclude_input=True readme.md.ipynb > readme.md
