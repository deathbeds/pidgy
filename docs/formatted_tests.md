# `pidgy` test suite 

## A Markdown paragraph is a block string.

  ### Markdown Input 1

  ```
  This is a Markdown paragraph
  ```
  ### Python Output 1

  ```
  '''This is a Markdown paragraph''';
  ```
## Indented Markdown block code is Python.

  ### Markdown Input 2

  ```
      print('this is code')
  ```
  ### Python Output 2

  ```
  print('this is code')
  ```
## Markdown blocks care defined as variables using line continuations

  ### Markdown Input 3

  ```
       foo = \
  This is a Markdown paragraph.

  ```
  ### Python Output 3

  ```
  foo = \
  '''This is a Markdown paragraph.''';

  ```
## Parenthesis can group markdown blocks

  ### Markdown Input 4

  ```
      foo = (
  This is a Markdown paragraph.

      )

  ```
  ### Python Output 4

  ```
  foo = (
  '''This is a Markdown paragraph.'''

  )

  ```
## explict single quotes

  ### Markdown Input 5

  ```
      foo = '''
  This is a Markdown paragraph.

      '''.lower()

  ```
  ### Python Output 5

  ```
  foo = '''
  This is a Markdown paragraph.

  '''.lower()

  ```
## explict double quotes

  ### Markdown Input 6

  ```
      foo = """
  This is a Markdown paragraph.

      """.lower()

  ```
  ### Python Output 6

  ```
  foo = """
  This is a Markdown paragraph.

  """.lower()

  ```
## function docstring

  ### Markdown Input 7

  ```
      def func(x: object) -> None:
  A Markdown paragraph as a docstring

  ```
  ### Python Output 7

  ```
  def func(x: object) -> None:
      '''A Markdown paragraph as a docstring''';

  ```
## class docstring

  ### Markdown Input 8

  ```
      class Class(Object):
  A Markdown paragraph as a docstring

  ```
  ### Python Output 8

  ```
  class Class(Object):
      '''A Markdown paragraph as a docstring''';

  ```
