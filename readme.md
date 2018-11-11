
`pidgin` is a collection of `IPython` utilities for creating computable essays.

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/deathbeds/pidgin/master?filepath=readme.ipynb)


<div><pre><code>import pidgin
</code></pre><p><code>pidgin</code> contains IPython extensions for creating human readable inputs and outputs.  When <code>pidgin</code> is activated, all code cells accept Markdown as input.  The input code is converted to valid Python, non-code objects are included in the source as strings.</p><blockquote><p><code>pidgin</code> is designed to eventually be Jupyter kernel, just not yet.</p></blockquote></div>



<div><h2>Executing cells.</h2><ol start=""><li><p>A minimally lossly transform from <strong>Markdown</strong> to <strong>Python</strong> where markdown content is preserved in strings.</p></li><li><p>Any block code in the <strong>Markdown</strong> is evaluated as normal.  Evaluatation <strong>breaks</strong> if any <code>Exception</code>s are raised.</p><ul><li><p><strong>Code Fences</strong> are not executed, but may include <code>doctest</code>s.</p></li></ul></li><li><p>Any <code>doctest.Example</code> is evaluated; upon failure the evaluation breaks.</p></li><li><p>Expressions in the the inline code cells are evaluated.</p><ul><li><p><code>IPython.core.interactiveshell.InteractiveShell.user_expressions</code> inspires this step.  <code>pidgin</code> only allows for expressions except for <strong>assert</strong> statements; magic syntaxes may be used in inline expressions.</p></li><li><p>All code in code cells should work.</p></li></ul></li></ol><h3>Note on execution</h3><p>Statements and expressions in (1. and 2.) must suceed before evaluating the <code>doctest</code>s and inline expressions.</p><pre><code>import doctest, IPython
</code></pre></div>



<div><h2>Templates</h2><p><code>pidgin</code> has some really cool templating features; it allows <code>IPython</code> users to template the output the display system.  <code>jinja2</code> is the current templating engine because it
is a dependency of <code>nbconvert</code></p><pre><code>import jinja2, nbconvert
</code></pre></div>



<div><h2>Docstrings</h2><p>A latent feature of <code>pidgin</code> is the ability to compose docstrings as markdown.</p><pre><code>class MyClass:
</code></pre><p>This is the docstring for <code>MyClass</code>.  <code>pidgin</code> will automatically wrap this expression in quotes because it follows a class defintion.</p></div>



<div><pre><code>def my_function(x):
</code></pre><p>Functions may have their docstring written in markdown. <code>pidgin</code> now transparently tests doctests in the docstring.</p><h2><code>my_function</code> tests</h2><pre><code>&gt;&gt;&gt; assert my_function(10) == 10

</code></pre><pre><code>    return x
</code></pre><p>... and don&#x27;t forget that all inline functions must evaluate.</p></div>


    C:\Users\deathbeds\pidgin\tests
    C:\Users\deathbeds\pidgin
    popd -> ~\pidgin
    


<div><h2>Importing pidgin documents.</h2><pre><code>import jupyter
</code></pre><blockquote><p><code>pidgin</code> uses <code>jupyter</code> notebooks as source files, at least for the earliest proof-of-concept there are few python source files.</p></blockquote><p><code>pidgin</code> defines that conventional that literate documents have a complex files extension <strong>.md.ipynb</strong>; indicating that the code cells are support <strong>markdown</strong>.  <code>pidgin</code>&#x27;s literate documents are importable.</p><pre><code>%pushd tests
with pidgin.PidginImporter():
    import essay
%popd
assert essay.__file__.endswith(&#x27;.md.ipynb&#x27;), &quot;Something failed on importing.&quot;
</code></pre></div>



<div><h2>Conventions for pidgin</h2><ul><li><p>Documents should restart and run all.</p></li><li><p><strong>inline</strong> and <strong>block</strong> cells should evaluate.</p></li><li><p>All <strong>block</strong> code is indented.</p></li><li><p><strong>code</strong> &amp; <strong>markdown</strong> become <strong>on</strong> and <strong>off</strong> cells, respectively.</p></li><li><p>output is more important than input, <code>nbconvert</code> should be used with <span><code>TemplateExporter.exclude_input=True</code></span></p><pre><code>  import nbconvert
</code></pre></li></ul></div>


    !jupyter nbconvert --to markdown --TemplateExporter.exclude_input=True --execute readme.ipynb
