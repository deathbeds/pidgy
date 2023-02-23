# `pidgy` literate computing interface

![pidgy logo](pidgy.png "PIDGY written in large lower case sans serif text with the word WEAVE written in capital letters underneath the letters PID")

`pidgy` is a fun, literate and interactive style of programming in markdown & python. together, these languages offer an exciting new experience to rapidly co-develop of code and narrative in Jupyter computational notebooks.

## writing with `pidgy`

<figure markdown>

```bash
pip install pidgy
```
<figcaption>install <code>pidgy</code> with `pip`</figcaption>
</figure>


<figure markdown>

```ipython
%reload_ext pidgy
```
<figcaption markdown>

1. 🪐 open a jupyter notebook
2. 🔌 activate the <code>pidgy</code> extension
3. ✏️ program in markdown
 
</figcaption> 
</figure>

<figure markdown>

<figcaption markdown style="font-size: 1.5rem;">

[💡 try `pidgy` in jupyterlite without any installation][pidgy lite][^lite] 

</figcaption>
</figure>

## programming in markdown

markdown is inclusive AF![^a11y] it is a plain-text format that never fails [^violate].
further markdown can include any programming language within its contents.
effectively, markdown files are literate programs that really on code and narrative to cooperate. markdown is a global minimum for teams of people with different language literacies.

a <kbd>Tab</kbd> separates markdown code and narrative, `pidgy` uses this nearness to create python representations of the markdown. with code and narrative so close, an author can fluidly switch between the writing modes capturing more of their process.

## learn more

* [try `pidgy`, without installing it, in `jupyterlite`.][pidgy lite]
* learn more from the `pidgy` documentation.
* [learn how CommonMark markdown converts to python][midgy]
* [contributing and development]

## development

[midgy]: https://github.com/deathbeds/midgy "midgy tangles markdown to python from pidgy"
[pip]: https://pypi.org/ "python package index"
[improving accessibility of markdown]: https://www.smashingmagazine.com/2021/09/improving-accessibility-of-markdown/
[With Markdown, Even the Blind Can Write]: https://tidbits.com/2013/06/18/with-markdown-even-the-blind-can-write/
[pidgy lite]: https://deathbeds.github.io/pidgy/run/
[jupyterlite]: https://github.com/jupyterlite/jupyterlite
[contributing and development]: #

[^a11y]: there are techniques for [improving accessibility of markdown] and abiding best practices.
[^violate]: markdown WILL violate expectation through implementation inconsistencies. over time we learn to navigate the nuances across products.
[^lite]: [jupyterlite] is a new in-the-browser jupyter experience that requires zero installation.