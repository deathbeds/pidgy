

<style>
/**Sure we can write inline css.**/
p img, p svg {
    vertical-align: middle;
} 
/**vertical-align: baseline|length|sub|super|top|text-top|middle|bottom|text-bottom|initial|inherit;**/
</style>



<h1>What is <code>pidgin</code>?</h1>
<p><code>pidgin</code> is a multi-lingual, <strong>Markdown</strong> forward, interactive 
programming interface.  It is an implementation of a more general idea where 
multiple programming grammars are tangled within a <strong>Markdown</strong> narrative.  This approach to programming
applies to problems where neither the code nor the narrative is clear, but the concept
may be described as a woven hybrid of the <strong>2</strong>.</p>
<p><code>pidgin</code> is designed to interactively and incrementally create <a href="">literate programs</a> proposed by <a href="">Donald Knuth</a>.  <code>pidgin</code>
is a specific implementation that hot rods running <code>IPython</code> kernels in <strong>Jupyter</strong> notebook and lab.</p>
<pre><code>    import pidgin, jinja2, IPython, notebook; get_ipython = IPython.get_ipython
</code></pre>
<ol>
<li><strong>Tangle</strong> <strong>Markdown</strong> code into valid <strong>Python</strong> code.</li>
<li><strong>Weave</strong> <strong>Python</strong> <code>object</code>s and <code>jinja2</code> templates into the computational narrative.</li>
</ol>
<p>The resulting documents created by <code>pidgin</code> are <a href="https://blog.stephenwolfram.com/2017/11/what-is-a-computational-essay/">computational essays</a> that connect 
<svg width="63pt" height="44pt"viewBox="0.00 0.00 62.60 44.00" xmlns="http://www.w3.org/2000/svg" ><g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 40)"><title>%3</title><polygon fill="white" stroke="none" points="-4,4 -4,-40 58.5952,-40 58.5952,4 -4,4"/><!-- Text --><g id="node1" class="node"><title>Text</title><ellipse fill="none" stroke="black" cx="27.2976" cy="-18" rx="27.0966" ry="18"/><text text-anchor="middle" x="27.2976" y="-14.3" font-family="Times New Roman,serif" font-size="14.00">Text</text></g></g></svg> <svg width="68pt" height="44pt"viewBox="0.00 0.00 67.79 44.00" xmlns="http://www.w3.org/2000/svg" ><g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 40)"><title>%3</title><polygon fill="white" stroke="none" points="-4,4 -4,-40 63.7947,-40 63.7947,4 -4,4"/><!-- Input --><g id="node1" class="node"><title>Input</title><ellipse fill="none" stroke="black" cx="29.8973" cy="-18" rx="29.795" ry="18"/><text text-anchor="middle" x="29.8973" y="-14.3" font-family="Times New Roman,serif" font-size="14.00">Input</text></g></g></svg> and <svg width="81pt" height="44pt"viewBox="0.00 0.00 80.79 44.00" xmlns="http://www.w3.org/2000/svg" ><g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 40)"><title>%3</title><polygon fill="white" stroke="none" points="-4,4 -4,-40 76.7935,-40 76.7935,4 -4,4"/><!-- Output --><g id="node1" class="node"><title>Output</title><ellipse fill="none" stroke="black" cx="36.3968" cy="-18" rx="36.2938" ry="18"/><text text-anchor="middle" x="36.3968" y="-14.3" font-family="Times New Roman,serif" font-size="14.00">Output</text></g></g></svg> composed interactively in <code>IPython</code>.</p>
<p><svg width="365pt" height="150pt"viewBox="0.00 0.00 365.39 150.00" xmlns="http://www.w3.org/2000/svg" ><g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 146)"><title>%3</title><polygon fill="white" stroke="none" points="-4,4 -4,-146 361.389,-146 361.389,4 -4,4"/><g id="clust1" class="cluster"><title>cluster</title><polygon fill="none" stroke="black" points="8,-8 8,-134 349.389,-134 349.389,-8 8,-8"/><text text-anchor="middle" x="178.694" y="-118.8" font-family="Times New Roman,serif" font-size="14.00">Computational Essays</text></g><!-- Text --><g id="node1" class="node"><title>Text</title><ellipse fill="none" stroke="black" cx="43.2976" cy="-60" rx="27.0966" ry="18"/><text text-anchor="middle" x="43.2976" y="-56.3" font-family="Times New Roman,serif" font-size="14.00">Text</text></g><!-- Input --><g id="node2" class="node"><title>Input</title><ellipse fill="none" stroke="black" cx="169.595" cy="-34" rx="29.795" ry="18"/><text text-anchor="middle" x="169.595" y="-30.3" font-family="Times New Roman,serif" font-size="14.00">Input</text></g><!-- Text&#45;&gt;Input --><g id="edge1" class="edge"><title>Text&#45;&gt;Input</title><path fill="none" stroke="black" d="M69.451,-54.7385C87.0902,-51.0488 110.981,-46.0516 130.89,-41.887"/><polygon fill="black" stroke="black" points="131.813,-45.2699 140.884,-39.7965 130.379,-38.4181 131.813,-45.2699"/></g><!-- Output --><g id="node3" class="node"><title>Output</title><ellipse fill="none" stroke="black" cx="304.992" cy="-59" rx="36.2938" ry="18"/><text text-anchor="middle" x="304.992" y="-55.3" font-family="Times New Roman,serif" font-size="14.00">Output</text></g><!-- Input&#45;&gt;Output --><g id="edge2" class="edge"><title>Input&#45;&gt;Output</title><path fill="none" stroke="black" d="M198.235,-39.18C216.253,-42.5569 240.144,-47.0342 260.658,-50.8788"/><polygon fill="black" stroke="black" points="260.249,-54.363 270.723,-52.765 261.539,-47.4828 260.249,-54.363"/></g><!-- Output&#45;&gt;Text --><g id="edge3" class="edge"><title>Output&#45;&gt;Text</title><path fill="none" stroke="black" d="M268.646,-60.1719C256.863,-60.5104 243.665,-60.8333 231.595,-61 176.489,-61.761 162.705,-61.4353 107.595,-61 99.0005,-60.9321 89.75,-60.8124 81.0464,-60.6788"/><polygon fill="black" stroke="black" points="80.8377,-57.1751 70.782,-60.5116 80.7236,-64.1741 80.8377,-57.1751"/><text text-anchor="middle" x="169.595" y="-64.8" font-family="Times New Roman,serif" font-size="14.00">Interactive Computing</text></g></g></svg></p>



<h2>Literate Programming</h2>
<blockquote><p>By coining the phrase “literate programming,” I am imposing a moral commitment
on everyone who hears the term; surely nobody wants to admit writing an illiterate program.</p>
</blockquote>
<p>There are quite a few tools for literate programming that model Knuth's original Pascal implementation of <a href="http://www.literateprogramming.com/knuthweb.pdf"><strong>WEB</strong></a>.  <code>pidgin</code> does not try to be an exact copy of <strong>WEB</strong> because computing, 
and most specifically interactive computing, has changed significantly.  Other contemporaries of <code>pidgin</code> are <strong>RMarkdown</strong>
and <strong>Mathematica</strong> computational essays.</p>
<p><code>pidgin</code> focuses on the core value of <strong>literate programming</strong> that one should <em>never write an illiterate program</em>.</p>



<h2>Language</h2>
<blockquote><p>Let us change our traditional attitude to the construction of programs: Instead of imagining that our
main task is to instruct a computer what to do, let us concentrate rather on explaining to human beings what
we want a computer to do.</p>
</blockquote>
<p>Literate programs are readable documents composed in human logic; <a href="">imperative</a>/<a href="">declarative</a> 
programs are for the computer. Literate programs will use combinations of 
imperative and declarative tools to express human logic.  This approach to programming is ideal for domain experts that 
speak a hybrid languages of human and computer language.</p>
<p>The distinct overlap between literate programming and science is they are multi-lingual.  Open
source software and scientific computing are causing an evolution scientific communication.  Communities are 
organizing to understand increasingly complex systems.  The collision of scientific interests rise <code>pidgin</code> languages.
The hope is that these languages will contribute to a scientific <strong>creole</strong>, rather than the increasing tribalism 
in scientific, technology, engineering, art and mathematics.</p>
<h2><code>pidgin</code> is just an implementation.</h2>
<p>To reiterate, like <strong>WEB</strong>, <code>pidgin</code> is just an implementation.  <code>pidgin</code> promotes an multi-objective and multi-lingual approach to 
programming.  <code>pidgin</code> assists authors during the act of literate computing by readability and reproducability.</p>
<p><code>pidgin</code> uses <code>IPython</code> and <code>notebook</code>s as a substrate for modifying the interactive programming experience.</p>



<h2>Literate Computing vs. Literate Programming</h2>
<p>In <a href="http://blog.fperez.org/2013/04/literate-computing-and-computational.html"><strong>"Literate computing" and computational reproducibility: IPython in the age of data-driven journalism</strong></a>, Fernando Perez comments on <strong>Literate Programming</strong>:</p>
<blockquote><p>I don't take any issue with this approach per se, but I don't personally use it because it's not
very well suited to the kinds of workflows that I need in practice. These require the frequent
execution of small fragments of code, in an iterative cycle where code is run to obtain partial 
exploratory computing, which is the bread and butter of many practicing scientists.</p>
</blockquote>
<p><code>pidgin</code>'s goal is create bring <strong>Literate Programs</strong> and <strong>Literate Computing</strong> closer together. 
It is not sufficient for practicing scientist to focus on exploratory computing without creating
publishable material.  <code>pidgin</code> modifies features to <code>IPython</code> that bring document, testing, and 
publication closer to a <code>IPython</code> author.</p>


    The process cannot access the file because it is being used by another process.
    


<h3>Readability: publishing <code>pidgin</code> documents.</h3>
<p>A <code>pidgin</code> author is composing their compute and portions (or <a href="http://nytlabs.com/blog/2015/10/20/particles/">particles</a>) of the published document
while interactively computing.  <code>import nbconvert</code> can be used against a <code>pidgin</code> <code>notebook</code>.</p>
<pre><code>if __name__ == '__main__':
    output = !jupyter nbconvert --to markdown --TemplateExporter.exclude_input=True --stdout readme.md.ipynb &gt; readme.md
    print(output[0])
</code></pre>
<p>The hybrid <strong>Markdown</strong>, templates, and <strong>Python</strong> in code cells encourage authors to encode 
the final layout in the output.  The input cells are excluded in the published document.</p>



<h3>reusability</h3>
<p>Computational thinking evolves over different time scales.  An author of a computational
essay should be the first consumer of their work.  <code>pidgin</code> extends <code>import importnb</code> to
<strong>import</strong> them as modules.</p>
<pre><code>with pidgin.PidginImporter(): 
    if __import__('os').environ.get('PYTEST_CURRENT_TEST', None):
        from docs import readme
    else:
        from . import readme
</code></pre>
<p>Importing essays will allow authors to consume their work as software.  When authors
reuse their own tools and code then will be motivated to make them more usable by
adding documentation and testing.</p>



<h3>reproducibility</h3>
<p><code>import importnb, \</code> and <code>pidgin, \</code> have <code>pytest, \</code> extensions complement the <code>nbval</code> tool.  These extensions together
encourage notebooks to be reused as tests; literate computing tests computational ideas thereby they ought
to be used as tests.  They provide targets for the quality of a notebook.</p>
<ul>
<li><code>nbval</code> ensures that the display for an output is the same a the 🥇 standard.</li>
<li><code>importnb</code> permits authors to write test functions in notebooks that are discoverable through the traditional <code>pytest</code> configurations.</li>
<li><code>pidgin</code> tests <strong>Markdown</strong> files.  It is important for code in documentation to work. <code>pidgin</code>
tests file as literate programs that should evaluated.</li>
</ul>
<h4><a href="https://github.com/noffle/art-of-readme">The Art of the README</a></h4>
<p>The <strong>README</strong> is a modern convention that is a literate program.  <strong>README</strong>'s generally require human intervention
to create compute.  It is critical for user facing code to work.  <code>pidgin</code> considers 
the <strong>README</strong> to be a critical test for the success of a computational technology.</p>
<blockquote><p><a href="https://github.com/noffle/art-of-readme">The Art of the README</a> can be used as a useful style guide for writing readable computational essays.</p>
<p><a href="http://liber118.com/pxn/">Paco Nathan</a>'s <a href="http://nbviewer.jupyter.org/github/jupyterday-atlanta-2016/oriole_jupyterday_atl/blob/master/oriole_talk.ipynb"><em>Oriole: a new learning medium based on Jupyter + Docker</em></a> 
given at <a href="https://jupyterday-atlanta-2016.github.io">Jupyter Day Atlanta 2016</a>. In Paco's <em>unofficial</em> <a href="http://nbviewer.jupyter.org/github/jupyterday-atlanta-2016/oriole_jupyterday_atl/blob/master/oriole_talk.ipynb#What-we-learned-about-teaching-with-notebooks">styleguide for authoring Jupyter notebooks</a> 
he reminds of a valuable principle for <code>notebook</code> authors:</p>
<blockquote><h2>clear all output then "Run All" -- or it didn't happen</h2>
</blockquote>
</blockquote>

