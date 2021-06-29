# tangling `pidgy`

`tyrm` tangles markdown code to source by applying heuristics to block tokens in the CommonMark spec* that convert markdown to:

1. python scripts

    the current program only applies to python. different languages require different heuristics.

2. notebook formats
3. [todo] other code formats

### markdown rules

in processing markdown code to execute our main goal is to separate _code_ and _non-code_, or things cause execution and things that don't.

#### front matter _code_

front matter is the only convention we uphold outside of the CommonMark spec. `tyrm` uses front matter to define document level metadata. a block of `yaml` or `toml` is expected; `yaml` is delimited by `---` and `toml` is delimited by `+++` as per the hugo convention.

objects in the front matter are available in your namespace for quick reuse and defining key variables.

#### themactic breaks _non-code_

when a markdown document is saved as notebook, the themactic breaks are used to identify individual cells.  `---` begin code blocks and `~~~` begin markdown cells. this rule does not apply to thematic breaks nested in blocks like list items.

#### indented _code_

indented code is executed by python, and hopefully other languages in the future. in between themactic breaks.

##### using markdown objects in _code_

###### markdown docstrings _code/non-code_

all _non-code_ objects are wrapped as block strings

###### line continuations acroos indented _code_

#### code fences 

popular literate programming tools in markdown, like rmarkdown or pyweave, use the language string to apply directives to executed the enclosed. in `tyrm`, we take no opinions about the language string of the code fence. in `tyrm`, code fences are treated a _non-code_ objects by default. instead we rely on indented code blocks to delineate _code_ and _non-code_ objects; this approach inspired by coffeescript.

#### doctests

i told a non-truth earlier, doctests are another convention we add to markdown. these blocks are verified after each execution.

##### the `__test__` variable

#### `jinja2` templating

`tyrm` uses `jinja2` templates to allow authors insert variables defined by code that has been executed.    