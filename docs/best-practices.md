# Best practices for literate programming

[Donald Knuth], the prophet of _[Literate Programming]_, asks for a core moral
commitment to write literate programs, because:

> ...; surely nobody wants to admit writing an illiterate program.
>
> > - [Donald Knuth] _[Literate Programming]_

The following best practices for literate programming have emerged while
desigined `pidgy`.

## List of best practices

- Restart and run all or it didn't happen.

  A useful document, as both literature and python program, must be literate in
  all readable, reproducible and reusable contexts.

- One `"h1"` or major heading per page.

  Abide [Web Content Accessibility Guidelines][wcag] so that information can be
  accessed by differently abled audiences. This constraint indicates that one
  subject should be discussed in each document.

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

- Use code, data, and visualization to fill the voids of natural language.
- When writing narrative include one unit of meaning per line.

      A sentence represents the maximum unit that can be broken up into

  smaller diffable units. This approach with create cleaner histories in
  revision control systems.

[wcag]: https://www.w3.org/WAI/standards-guidelines/wcag/
[donald knuth]: #
[literate programming]: #
[markdown]: #
[`readme.md`]: #
