
`pidgin` is a literate computing tool for composing computational essays and documents with IPython/Jupyter notebooks. 

[![Build Status](https://travis-ci.org/deathbeds/pidgin.svg?branch=master)](https://travis-ci.org/deathbeds/pidgin)[![Documentation Status](https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)

#### [References](src/pidgin/docs/references.md.ipynb)

    !pip install pidgin ### Install `pidgin` from pypi.

Activate `pidgin` to start programming in [__Markdown__][]


<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is a document-forward approach to writing in <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>IPython
</code></span> where authors combine narrative and code within notebook cells.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> relies
on several common syntax opinions to create computational essays and literate programs.</p>
<a href="#Features"><h2 id="Features">Features</h2></a><ul>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> is <strong>Markdown</strong> first; <strong>indented code blocks</strong> execute as normal code.  _The only modification to your workflow is to indenting your code;
a notebook of indented code cells will execute with normal behavior.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> promotes <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span>ing within cells.  <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span> is trigger by the familiar <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #BA2121">&quot;&gt;&gt;&gt;&quot;</span> <span style="color: #AA22FF; font-weight: bold">and</span> <span style="color: #BA2121">&quot;...&quot;</span>
</code></span> syntax.</p>
</li>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> executes <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">all</span>
</code></span> code!  Inline code and code fences execute code, and it must work.</p>
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
</code></span></h3></a><table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">3</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #BA2121">&quot;I am code, 🦁, rawwwwrrr&quot;</span>
</pre></div>
</td></tr></table><ul>
<li><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> cells tangle standard <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>IPython
</code></span> from indented <strong>Markdown</strong> code.</p>
</li>
<li><p>If any other <strong>Markdown</strong> features exist, the cell is rendered as rich HTML.</p>
</li>
<li><p>A note: code in list blocks must be carry an extra indent to be registered.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">10</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #BA2121">&quot;Indented code within a list requires an extra for each level.&quot;</span>
</pre></div>
</td></tr></table></li>
<li><p>Indents are aligned to the first indented code block..  Spwcifically, the source for this cell is indented twice to avoid an <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #D2413A; font-weight: bold">IndentationError</span>
</code></span>.</p>
</li>
</ul>




<a href="#Writing-tests"><h3 id="Writing-tests">Writing tests</h3></a><blockquote><p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span><span style="color: #008000">all</span>
</code></span> code are tests!</p>
</blockquote>
<p><span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>pidgin
</code></span> provides <strong>3</strong> ways to run tests: inline code is execute, code fences are executed, and <span class="highlight"><code style="display: inline-block; vertical-align: middle; line-height: 125%"><span></span>doctest
</code></span>s are evaluated.  Heavy use of code woven within a document will create more reliable documentation over time.</p>




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




<a href="#Documents-as-documents"><h4 id="Documents-as-documents">Documents as documents</h4></a><ul>
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
</ul>



## Developer
    

    !ipython -m readme_pidgin.md.ipynb -- --uml=True --nbconvert=True --test=True

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
