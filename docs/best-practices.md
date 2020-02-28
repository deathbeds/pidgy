# Best practices for literate programming

The first obligation of the literate programmer, defined by [Donald Knuth](ie.
the prophet of _[Literate Programming]_), is a core moral commitment to write
literate programs, because:

> ...; surely nobody wants to admit writing an illiterate program.
>
> > - [Donald Knuth] _[Literate Programming]_

The following best practices for literate programming have emerged while
desiging `pidgy`.

## List of best practices

- Restart and run all or it didn't happen.

  A document should be literate in all readable, reproducible, and reusable
  contexts.

- When in doubt, abide [Web Content Accessibility Guidelines][wcag] so that
  information can be accessed by differently abled audiences.

- [Markdown] documents are sufficient for single units of thought.

  Markdown documents that translate to python can encode literate programs in a
  form that is better if version control systems that the `json` format that
  encodes notebooks.

- All code should compute.

  Testing code in a narrative provides supplemental meaning to the `"code"`
  signifiers. They provide a test of veracity at least for the computational
  literacy.

- [`readme.md`] is a good default name for a program.

  Eventually authors will compose [`"readme.md"`] documents that act as both the
  `"__init__"` method and `"__main__"` methods of the program.

- Each document should stand alone,
  [despite all possibilities to fall.](http://ing.univaq.it/continenza/Corso%20di%20Disegno%20dell'Architettura%202/TESTI%20D'AUTORE/Paul-klee-Pedagogical-Sketchbook.pdf#page=6)
- Use code, data, and visualization to fill the voids of natural language.
- Find pleasure in writing.

[wcag]: https://www.w3.org/WAI/standards-guidelines/wcag/
[donald knuth]: #
[literate programming]: #
[markdown]: #
[`readme.md`]: #
