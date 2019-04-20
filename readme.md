
    !pip install pidgin ### Install `pidgin` from pypi.

Activate `pidgin` to start programming in __Markdown__.

    %load_ext pidgin


<blockquote><p>Programming in <strong>Markdown</strong> ⁉ What d🤔es that even mean❓</p>
</blockquote>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> executes code within indented <strong>Markdown</strong> code blocks.<a href="#" title="Special rules apply for ordered and unordered lists.">🎩</a><a href="https://coffeescript.org/#literate" title="Literate coffee is a significant inspiration for `pidgin`.">☕️</a></p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #BA2121">&quot;I am code! 👂 me rawrrrr🦁!&quot;</span>
</pre></div>
</td></tr></table><blockquote><p>An author will recoginize code by it's <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;monospaced&quot;</span>
</code></span> typesetting.</p>
</blockquote>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> encourages authors to capture computational thinking in human and computational logic.</p>
<ul>
<li><p>Human logic produces <strong>readable</strong> publications of a computational essay.</p>
</li>
<li><p>Computational logic ensures replicability; <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span>s specific focus on testing allows an author to reinforce their ideas.</p>
</li>
<li><p>Human and computational logic allows others to understand and <strong>reuse</strong> a program for what could be exciting new discoveries.</p>
</li>
</ul>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is a literate computing implementation that customizes the interactive <a href="https://jupyter.readthedocs.io/en/latest/"><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>jupyter
</code></span> <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>notebook
</code></span></a> experience.</p>
<p><a href="https://travis-ci.org/deathbeds/pidgin"><img src="https://travis-ci.org/deathbeds/pidgin.svg?branch=master" alt="Build Status"></a><a href="https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest" alt="Documentation Status"></a></p>




<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is a document-forward approach to <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>notebook
</code></span> authoring.  Authors will combine languages within cells to narrate the computational logic underlying the source code. Below is a list of <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> features 🔽</p>
<ul>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is <strong>Markdown</strong> first; <strong>indented code blocks</strong> execute as normal code.  _The only modification to your workflow is to indenting your code;
a notebook of indented code cells will execute with normal behavior.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> executes <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">all</span>
</code></span> code!  Inline code and code fences execute code, and it must work.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> promotes <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span>ing within cells.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span> is trigger by the familiar <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;&gt;&gt;&gt;&quot;</span> <span style="color: #AA22FF; font-weight: bold">and</span> <span style="color: #BA2121">&quot;...&quot;</span>
</code></span> syntax.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> documents are readable and reusable.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> uses <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>importnb
</code></span> to <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">__import__</span>
</code></span> documents as modules.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> uses <strong>YAML front matter</strong> to annotate output metadata and provide temporary variables for publishing.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> uses <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>jinja2
</code></span> -  a dependency of <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>nbconvert
</code></span> - to template <strong>Python</strong> variables into 
the published output.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> includes <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>graphviz
</code></span> support for typographically compising diagrams.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> has many other features (e.g. completion, inspection) that we hope you enjoy discovering along the way 😁.</p>
</li>
</ul>




<a href="#Writing-code-in-span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-code-span"><h3 id="Writing-code-in-span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-code-span">Writing code in <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span></h3></a><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #666666">...</span>
</code></span> is not much different than composing normal <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>notebook
</code></span>s; just indent the source code once.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #BA2121">&quot;I am code, 🦁, rawwwwrrr&quot;</span>
</pre></div>
</td></tr></table><blockquote><p>To reiterate, code objects are identified by their <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;monospace&quot;</span>
</code></span> typesetting.</p>
</blockquote>
<ul>
<li><p>If any other <strong>Markdown</strong> features exist, the cell is rendered as rich HTML; cells only containing code are not rendered.</p>
</li>
<li><p>A note: code in list blocks must be carry an extra indent to be registered.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">12</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #BA2121">&quot;Indented code within a list requires an extra for each level.&quot;</span>
</pre></div>
</td></tr></table></li>
<li><p>Indents are aligned to the first indented code block..  Specifically, the source for this cell is indented twice to avoid an <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #D2413A; font-weight: bold">IndentationError</span>
</code></span>.</p>
</li>
</ul>
<a href="#span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-span-style-color-BA2121-docstring-span-code-span-s-for-code-class-code-code-function-def-code-initions"><h4 id="span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-span-style-color-BA2121-docstring-span-code-span-s-for-code-class-code-code-function-def-code-initions"><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;docstring&quot;</span>
</code></span>s for <code>class</code> &amp; <code>function def</code>initions.</h4></a><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> converts all non-source code to strings so it is consumed by the python <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>ast
</code></span>.  When a <strong>_Markdown</strong> <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">str</span>
</code></span>ing following a <code>class</code> or <code>def</code> statement becomes the docstring; <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span>s included.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">21</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">def</span> <span style="color: #0000FF">a_function_with_a_markdown_docstring</span>():
</pre></div>
</td></tr></table><p>This is the <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;docstring&quot;</span>
</code></span> for <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>a_function_with_a_markdown_docstring
</code></span>.  It is a function that returns <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">None</span>
</code></span>.</p>
<pre><code>&gt;&gt;&gt; assert a_function_with_a_markdown_docstring() is None
</code></pre>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">26
27</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #666666">...</span> <span style="color: #408080; font-style: italic"># A line break is required above to define code</span>
<span style="color: #408080; font-style: italic"># otherwise Markdown assumes the paragraph is being continued</span>
</pre></div>
</td></tr></table><pre><code>&gt;&gt;&gt; a_function_with_a_markdown_docstring.__doc__
'This is the `"docstring"` for ... assert a_function_with_a_markdown_docstring() is None'
</code></pre>




<a href="#Writing-tests"><h3 id="Writing-tests">Writing tests</h3></a><blockquote><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">all</span>
</code></span> code are tests!</p>
</blockquote>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> provides <strong>3</strong> ways to run tests:</p>
<ol>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;Inline code is identified by a tick&quot;</span> <span style="color: #AA22FF; font-weight: bold">and</span> <span style="color: #BA2121">&quot;It must raise an Exception&quot;</span>
</code></span></p>
</li>
<li><p>Code fences without a language specification are evaluated.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">12
13
14</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">_document_</span>
 _document_<span style="color: #666666">.</span><span style="color: #19177C">__dict__</span><span style="color: #666666">.</span>update({<span style="color: #BA2121">&quot;I run&quot;</span>: <span style="color: #008000">None</span>})
 <span style="color: #008000; font-weight: bold">assert</span> <span style="color: #BA2121">&quot;I run&quot;</span> <span style="color: #AA22FF; font-weight: bold">in</span> _document_<span style="color: #666666">.</span><span style="color: #19177C">__dict__</span>
</pre></div>
</td></tr></table></li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span> are evaluated.</p>
</li>
</ol>
<pre><code>&gt;&gt;&gt; assert doctest
</code></pre>




<a href="#Templating-output"><h3 id="Templating-output">Templating output</h3></a><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> compiles and formats <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>jinja2
</code></span> template syntax during the <strong>Markdown</strong> rendering.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>jinja2<span style="color: #666666">.</span>Template
</code></span>s embed notebook variables as strings; <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is enhanced to use the <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>IPython<span style="color: #666666">.</span>display
</code></span>  to embed rich html objects.</p>



    The pidgin extension is already loaded. To reload it, use:
      %reload_ext pidgin



<a href="#Documents-as-modules"><h3 id="Documents-as-modules">Documents as modules</h3></a><p>It is a shame to write code that other documents can't use.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> subclasses <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>importnb
</code></span> to import notebooks as documents.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5
6
7</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">if</span> <span style="color: #19177C">__name__</span> <span style="color: #666666">==</span> <span style="color: #BA2121">&#39;__main__&#39;</span>:
    <span style="color: #008000; font-weight: bold">with</span> pidgin<span style="color: #666666">.</span>Pidgin():
        <span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">readme_pidgin</span>
</pre></div>
</td></tr></table><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> documents end with the hybird <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;.md.ipynb&quot;</span>
</code></span> extension.</p>
<pre><code>&gt;&gt;&gt; readme_pidgin
&lt;module 'readme_pidgin' from '...readme_pidgin.md.ipynb'&gt;
</code></pre>




<a href="#Ways-to-use-span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-code-span"><h4 id="Ways-to-use-span-class-highlight-code-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-code-span">Ways to use <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span></h4></a><ul>
<li><p><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme_pidgin.md.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a></p>
<p>Take <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> for a spin on <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><strong><em>Binder</em></strong></a>.</p>
</li>
<li><p><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a></p>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> works great with the <a href="https://github.com/computationalmodelling/nbval"><strong>nbval</strong></a> and <a href="https://github.com/deathbeds/importnb"><strong>importnb</strong></a> notebook specific pytest extensions.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> itself is a <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">pytest</span>
</code></span>
  plugin that permits tests with <strong>.md.ipynb</strong> and <strong>.md</strong> extensions.</p>
</li>
<li><p><strong><em>Jupyter</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/7388996?s=40" alt=""></a></p>
</li>
<li><p><strong><em>JupyterLab</em></strong> <a href="https://github.com/jupyterlab"><img src="https://avatars1.githubusercontent.com/u/22800682?s=40" alt=""></a></p>
</li>
<li><p><strong><em>Google Colaboratory</em></strong> <a href="https://colab.research.google.com/github/deathbeds/pidgin/blob/mistune/readme.ipynb"><img src="https://avatars0.githubusercontent.com/u/33467679?s=40" alt=""></a></p>
</li>
<li><p><strong><em>nteract</em></strong> <a href="https://nteract.io"><img src="https://avatars0.githubusercontent.com/u/12401040?s=40" alt=""></a></p>
</li>
</ul>




<a href="#Roadmap"><h2 id="Roadmap">Roadmap</h2></a><ul>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> should become an <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">ipykernel</span>
</code></span>.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> should have an application level interface to control features.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> should extend to other ipykernels.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> should become an <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">nbconvert.nbconvertapp</span>
</code></span> and <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>nbconvert<span style="color: #666666">.</span>preprocessors
</code></span>.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> should become python source code eventually.</p>
</li>
</ul>



## Developer
    

### Test `pidgin`

    if __name__ == '__main__':
        !ipython -m pytest -- --nbval


<a href="#Run-tests"><h3 id="Run-tests">Run tests</h3></a><table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">3</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span>test <span style="color: #666666">=</span> <span style="color: #008000">False</span>
</pre></div>
</td></tr></table>


    %%file sanitize.cfg
    [skip_graphviz]
    regex: <svg(.|\n)*</svg>w
    replace: ---
        
        


<a href="#UML-diagrams"><h3 id="UML-diagrams">UML diagrams</h3></a><table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">3</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span>uml <span style="color: #666666">=</span> <span style="color: #008000">False</span>
</pre></div>
</td></tr></table>



<a href="#Convert-to-the-strong-readme-md-strong"><h3 id="Convert-to-the-strong-readme-md-strong">Convert to the <strong>readme.md</strong></h3></a><table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">3</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span>convert<span style="color: #666666">=</span><span style="color: #008000">False</span>
</pre></div>
</td></tr></table>


    %%file markdown_readme.py
    c.MarkdownExporter.raw_mimetypes = ['text/markdown']
    c.TemplateExporter.exclude_input=True
