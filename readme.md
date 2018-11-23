
`pidgin` is a collection of `IPython` extensions for creating computable essays.

    #Execute this cell to install pidgin.
    #!pip install pidgin
    !pip install git+https://github.com/deathbeds/pidgin

Then load the `pidgin` extension.


<style>.highlight .hll { background-color: #ffffcc }
.highlight  { background: #f8f8f8; }
.highlight .c { color: #408080; font-style: italic } /* Comment */
.highlight .err { border: 1px solid #FF0000 } /* Error */
.highlight .k { color: #008000; font-weight: bold } /* Keyword */
.highlight .o { color: #666666 } /* Operator */
.highlight .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.highlight .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #BC7A00 } /* Comment.Preproc */
.highlight .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.highlight .c1 { color: #408080; font-style: italic } /* Comment.Single */
.highlight .cs { color: #408080; font-style: italic } /* Comment.Special */
.highlight .gd { color: #A00000 } /* Generic.Deleted */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gr { color: #FF0000 } /* Generic.Error */
.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.highlight .gi { color: #00A000 } /* Generic.Inserted */
.highlight .go { color: #888888 } /* Generic.Output */
.highlight .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.highlight .gt { color: #0044DD } /* Generic.Traceback */
.highlight .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.highlight .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.highlight .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.highlight .kp { color: #008000 } /* Keyword.Pseudo */
.highlight .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.highlight .kt { color: #B00040 } /* Keyword.Type */
.highlight .m { color: #666666 } /* Literal.Number */
.highlight .s { color: #BA2121 } /* Literal.String */
.highlight .na { color: #7D9029 } /* Name.Attribute */
.highlight .nb { color: #008000 } /* Name.Builtin */
.highlight .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.highlight .no { color: #880000 } /* Name.Constant */
.highlight .nd { color: #AA22FF } /* Name.Decorator */
.highlight .ni { color: #999999; font-weight: bold } /* Name.Entity */
.highlight .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
.highlight .nf { color: #0000FF } /* Name.Function */
.highlight .nl { color: #A0A000 } /* Name.Label */
.highlight .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.highlight .nt { color: #008000; font-weight: bold } /* Name.Tag */
.highlight .nv { color: #19177C } /* Name.Variable */
.highlight .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.highlight .w { color: #bbbbbb } /* Text.Whitespace */
.highlight .mb { color: #666666 } /* Literal.Number.Bin */
.highlight .mf { color: #666666 } /* Literal.Number.Float */
.highlight .mh { color: #666666 } /* Literal.Number.Hex */
.highlight .mi { color: #666666 } /* Literal.Number.Integer */
.highlight .mo { color: #666666 } /* Literal.Number.Oct */
.highlight .sa { color: #BA2121 } /* Literal.String.Affix */
.highlight .sb { color: #BA2121 } /* Literal.String.Backtick */
.highlight .sc { color: #BA2121 } /* Literal.String.Char */
.highlight .dl { color: #BA2121 } /* Literal.String.Delimiter */
.highlight .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.highlight .s2 { color: #BA2121 } /* Literal.String.Double */
.highlight .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
.highlight .sh { color: #BA2121 } /* Literal.String.Heredoc */
.highlight .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
.highlight .sx { color: #008000 } /* Literal.String.Other */
.highlight .sr { color: #BB6688 } /* Literal.String.Regex */
.highlight .s1 { color: #BA2121 } /* Literal.String.Single */
.highlight .ss { color: #19177C } /* Literal.String.Symbol */
.highlight .bp { color: #008000 } /* Name.Builtin.Pseudo */
.highlight .fm { color: #0000FF } /* Name.Function.Magic */
.highlight .vc { color: #19177C } /* Name.Variable.Class */
.highlight .vg { color: #19177C } /* Name.Variable.Global */
.highlight .vi { color: #19177C } /* Name.Variable.Instance */
.highlight .vm { color: #19177C } /* Name.Variable.Magic */
.highlight .il { color: #666666 } /* Literal.Number.Integer.Long */</style><div class="highlight"><pre><span></span>    <span class="kn">import</span> <span class="nn">pidgin</span><span class="o">,</span> <span class="nn">IPython</span>
</pre></div>
<p><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 allows <strong>Markdown</strong> as <strong>Code Cell</strong> source in <span class="highlight"><code><span></span><span class="n">IPython</span>
</code></span>
.</p>
<ol>
<li>The <strong>Markdown</strong> is converted to valid <strong>Python</strong> source.</li>
<li>The <strong>Python</strong> source is executed.</li>
<li>Any <span class="highlight"><code><span></span><span class="s2">&quot;doctest&quot;</span>
</code></span>
s are evaluated.</li>
<li>All inline code is evaluated.</li>
<li>The <strong>Markdown</strong> source is display with special rules defined in <span class="highlight"><code><span></span><span class="n">pidgin</span><span class="o">.</span><span class="n">display</span>
</code></span>
 including <span class="highlight"><code><span></span><span class="s2">&quot;jinja2&quot;</span>
</code></span>
 templates
for including data in the display.</li>
</ol>
<p>Each stuff must succeed without raising an <span class="highlight"><code><span></span><span class="ne">Exception</span>
</code></span>
.</p>



<h2>Benefits of <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
</h2>
<ul>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 requires that all code in a document is valid.</li>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 places tighter constraints on the <strong>Run All-ability</strong> of the document.</li>
<li><p><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 encourages tighter weaving of code and narrative.</p>
<div class="highlight"><pre><span></span>  <span class="kn">import</span> <span class="nn">jinja2</span>
</pre></div>
<p>Use <span class="highlight"><code><span></span><span class="n">jinja2</span>
</code></span>
 syntaxes in <strong>Code Cells</strong>.  On the last display step with include 
  pretty representations of template expression.  The <span class="highlight"><code><span></span><span class="n">jinja2</span><span class="o">.</span><span class="n">Environment</span>
</code></span>
 returns <strong>html</strong> formatted
  display <span class="highlight"><code><span></span><span class="nb">object</span>
</code></span>
s including <span class="highlight"><code><span></span><span class="s2">&quot;pandas&quot;</span>
</code></span>
 tables and <span class="highlight"><code><span></span><span class="s2">&quot;matplotlib&quot;</span>
</code></span>
 figures.</p>
</li>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 separates display statements from compute statements.</li>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 documents are importable because of <span class="highlight"><code><span></span><span class="kn">import</span> <span class="nn">importnb</span>
</code></span>
        </li>
</ul>
<div class="highlight"><pre><span></span><span class="k">with</span> <span class="n">pidgin</span><span class="o">.</span><span class="n">PidginImporter</span><span class="p">(</span><span class="n">position</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span>
    <span class="kn">import</span> <span class="nn">readme_pidgin</span> <span class="kn">as</span> <span class="nn">readme</span>
</pre></div>


`pidgin` introduces __.md.ipynb__, a hybird file extension, to identity __Markdown__ forward computational essays. When
this document (`readme`) is imported we can `assert readme.__file__.endswith('.md.ipynb')`.


<h2><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 works with</h2>
<ul>
<li><p><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a></p>
<p>Take <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 for a spin on <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><strong><em>Binder</em></strong></a>.</p>
</li>
<li><p><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a></p>
<p><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 works great with the <a href="https://github.com/computationalmodelling/nbval"><strong>nbval</strong></a> and <a href="https://github.com/deathbeds/importnb"><strong>importnb</strong></a> notebook specific pytest extensions.  <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 itself is a <span class="highlight"><code><span></span><span class="kn">import</span> <span class="nn">pytest</span>
</code></span>

  plugin that permits tests with <strong>.md.ipynb</strong> and <strong>.md</strong> extensions.</p>
<p><strong><em>Pro Tip</em></strong> test <span class="highlight"><code><span></span><span class="n">IPython</span>
</code></span>
 specific features using <strong>ipython</strong> as the <span class="highlight"><code><span></span><span class="n">pytest</span>
</code></span>
 runner instead of <strong>python</strong> <span class="highlight"><code><span></span><span class="ch">#!ipython -m pytest -- --collect-only</span>
</code></span>
</p>
</li>
<li><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a> </li>
<li><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a> </li>
<li><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></li>
<li><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></li>
</ul>



<h2>Architecture</h2>
<p>The <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 source is written almost entirely in Jupyter notebooks.  The hope is that the notebooks will serve as an important
interactive resourcing in the early development.  As the project matures, <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 will adopt different combinations of python
and notebook files.</p>
<div class="highlight"><pre><span></span><span class="n">ip</span> <span class="o">=</span> <span class="n">IPython</span><span class="o">.</span><span class="n">get_ipython</span><span class="p">()</span>
</pre></div>
<p><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 is architected as a collection of <span class="highlight"><code><span></span><span class="n">IPython</span>
</code></span>
 extensions that modify <span class="highlight"><code><span></span><span class="n">ip</span> <span class="o">=</span> <span class="n">IPython</span><span class="o">.</span><span class="n">get_ipython</span><span class="p">()</span>
</code></span>
 and <span class="highlight"><code><span></span><span class="n">ip</span><span class="o">.</span><span class="n">kernel</span>
</code></span>
.</p>
<div class="highlight"><pre><span></span><span class="k">if</span> <span class="mi">0</span><span class="p">:</span>
    <span class="o">%</span><span class="k">reload_ext</span> pidgin
</pre></div>
<p>Each component of <span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 can be loaded individually.</p>
<div class="highlight"><pre><span></span>    <span class="o">%</span><span class="k">reload_ext</span> pidgin.tangle
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.display
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.inspector
    <span class="o">%</span><span class="k">reload_ext</span> pidgin.post_run_cell
</pre></div>



<h2>Roadmap</h2>
<ul>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 should become an <span class="highlight"><code><span></span><span class="kn">import</span> <span class="nn">ipykernel</span>
</code></span>
.</li>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 should extend to other ipykernels.</li>
<li><span class="highlight"><code><span></span><span class="n">pidgin</span>
</code></span>
 should become an <span class="highlight"><code><span></span><span class="kn">import</span> <span class="nn">nbconvert.nbconvertapp</span>
</code></span>
 and <span class="highlight"><code><span></span><span class="n">nbconvert</span><span class="o">.</span><span class="n">preprocessors</span>
</code></span>
.</li>
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

