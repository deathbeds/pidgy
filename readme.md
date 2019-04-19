
`pidgin` is a literate computing tool for composing computational essays and documents with IPython/Jupyter notebooks. 

[![Build Status](https://travis-ci.org/deathbeds/pidgin.svg?branch=master)](https://travis-ci.org/deathbeds/pidgin)[![Documentation Status](https://readthedocs.org/projects/pidgin-notebook/badge/?version=latest)](https://pidgin-notebook.readthedocs.io/en/latest/?badge=latest)

#### [References](src/pidgin/docs/references.md.ipynb)

    !pip install pidgin ### Install `pidgin` from pypi.

Activate `pidgin` to start programming in [__Markdown__][]


<p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> is a document-forward approach to writing in <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>IPython
</pre></span> where authors combine narrative and code within notebook cells.  <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> relies
on several common syntax opinions to create computational essays and literate programs.</p>
<a href="#Features"><h2 id="Features">Features</h2></a><ul>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> is <strong>Markdown</strong> first; <strong>indented code blocks</strong> execute as normal code.  _The only modification to your workflow is to indenting your code;
a notebook of indented code cells will execute with normal behavior.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> promotes <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>doctest
</pre></span>ing within cells.  <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>doctest
</pre></span> is trigger by the familiar <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #BA2121">&quot;&gt;&gt;&gt;&quot;</span> <span style="color: #AA22FF; font-weight: bold">and</span> <span style="color: #BA2121">&quot;...&quot;</span>
</pre></span> syntax.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> executes <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000">all</span>
</pre></span> code!  Inline code and code fences execute code, and it must work.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> documents are readable and reusable.  <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> uses <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>importnb
</pre></span> to <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000">__import__</span>
</pre></span> documents as modules.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> uses <strong>YAML front matter</strong> to annotate output metadata and provide temporary variables for publishing.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> uses <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>jinja2
</pre></span> -  a dependency of <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>nbconvert
</pre></span> - to template <strong>Python</strong> variables into 
the published output.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> includes <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>graphviz
</pre></span> support for typographically compising diagrams.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> has many other features (e.g. completion, inspection) that we hope you enjoy discovering along the way 😁.</p>
</li>
</ul>




<a href="#Writing-code-in-span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span"><h3 id="Writing-code-in-span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span">Writing code in <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span></h3></a><ul>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> cells tangle standard <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>IPython
</pre></span> from indented <strong>Markdown</strong> code.</p>
</li>
<li><p>If any other <strong>Markdown</strong> features exist, the cell is rendered as rich HTML.</p>
</li>
</ul>




<a href="#Writing-tests"><h3 id="Writing-tests">Writing tests</h3></a><blockquote><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000">all</span>
</pre></span> code is are tests!</p>
</blockquote>
<p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> provides <strong>x</strong> ways to run tests: inline code is execute, code fences are executed, and <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>doctest
</pre></span>s are evaluated.  Heavy use of code woven within a document will create more reliable documentation over time.</p>




<a href="#Templating-output"><h3 id="Templating-output">Templating output</h3></a>



<a href="#Documents-as-modules"><h3 id="Documents-as-modules">Documents as modules</h3></a>



<a href="#Documents-as-documents"><h3 id="Documents-as-documents">Documents as documents</h3></a>



<a href="#Importing-span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span-documents"><h2 id="Importing-span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span-documents">Importing <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> documents.</h2></a><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> documents are notebooks that can be imported as <strong>Python</strong> modules.</p>
<pre><code>&gt;&gt;&gt; with pidgin.Pidgin(): None
</code></pre>
<p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> documents are recognized <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #BA2121">&quot;.md.ipynb&quot;</span>
</pre></span> extension.
<span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> documents render on <a href="#">nbviewer</a>.  Get in the habit of creaitng reusable
notebooks with <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>importnb
</pre></span>.</p>




<a href="#span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span-works-with"><h2 id="span-class-highlight-pre-style-display-inline-block-vertical-align-middle-line-height-125-span-span-pidgin-pre-span-works-with"><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> works with</h2></a><ul>
<li><p><strong><em>Binder</em></strong> <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme_pidgin.md.ipynb"><img src="https://mybinder.org/badge.svg" alt="Binder"></a></p>
<p>Take <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> for a spin on <a href="https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb"><strong><em>Binder</em></strong></a>.</p>
</li>
<li><p><strong><em>Pytest</em></strong> <a href="https://github.com/pytest-dev"><img src="https://avatars1.githubusercontent.com/u/8897583?s=40&amp;v=4" alt=""></a></p>
<p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> works great with the <a href="https://github.com/computationalmodelling/nbval"><strong>nbval</strong></a> and <a href="https://github.com/deathbeds/importnb"><strong>importnb</strong></a> notebook specific pytest extensions.  <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> itself is a <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">pytest</span>
</pre></span>
  plugin that permits tests with <strong>.md.ipynb</strong> and <strong>.md</strong> extensions.</p>
<p><strong><em>Pro Tip</em></strong> test <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>IPython
</pre></span> specific features using <strong>ipython</strong> as the <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pytest
</pre></span> runner instead of <strong>python</strong> <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #408080; font-style: italic">#!ipython -m pytest -- --collect-only</span>
</pre></span></p>
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




<a href="#Architecture"><h2 id="Architecture">Architecture</h2></a><p>The <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> source is written almost entirely in Jupyter notebooks.  The hope is that the notebooks will serve as an important
interactive resourcing in the early development.  As the project matures, <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> will adopt different combinations of python
and notebook files.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">7</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span>ip <span style="color: #666666">=</span> IPython<span style="color: #666666">.</span>get_ipython()
</pre></div>
</td></tr></table><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> is architected as a collection of <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>IPython
</pre></span> extensions that modify <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>ip <span style="color: #666666">=</span> IPython<span style="color: #666666">.</span>get_ipython()
</pre></span> and <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>ip<span style="color: #666666">.</span>kernel
</pre></span>.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">10
11</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">if</span> <span style="color: #666666">0</span>:
    <span style="color: #666666">%</span>reload_ext pidgin
</pre></div>
</td></tr></table><p>Each component of <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> can be loaded individually.</p>
<table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">15
16
17
18</pre></div></td><td style="text-align: left;" class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span></span><span style="color: #666666">%</span>reload_ext pidgin<span style="color: #666666">.</span>tangle
    <span style="color: #666666">%</span>reload_ext pidgin<span style="color: #666666">.</span>display
    <span style="color: #666666">%</span>reload_ext pidgin<span style="color: #666666">.</span>inspector
    <span style="color: #666666">%</span>reload_ext pidgin<span style="color: #666666">.</span>post_run_cell
</pre></div>
</td></tr></table>



<a href="#Roadmap"><h2 id="Roadmap">Roadmap</h2></a><ul>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> should become an <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">ipykernel</span>
</pre></span>.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> should extend to other ipykernels.</p>
</li>
<li><p><span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>pidgin
</pre></span> should become an <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span><span style="color: #008000; font-weight: bold">import</span> <span style="color: #0000FF; font-weight: bold">nbconvert.nbconvertapp</span>
</pre></span> and <span class="highlight"><pre style="display: inline-block; vertical-align: middle;; line-height: 125%"><span></span>nbconvert<span style="color: #666666">.</span>preprocessors
</pre></span>.</p>
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
