# `pidgy` test suite 

## A Markdown paragraph is a block string.

  ### Markdown Input 1

    This is a Markdown paragraph
  ### Python Output 1

    '''This is a Markdown paragraph''';
## Indented Markdown block code is Python.

  ### Markdown Input 2

        print('this is code')
  ### Python Output 2

    print('this is code')
## code fence is block string

  ### Markdown Input 3

    ```{code} fence
    code shenanigans
    ```

  ### Python Output 3

    '''```{code} fence
    code shenanigans
    ```''';

## Markdown blocks care defined as variables using line continuations

  ### Markdown Input 4

         foo = \
    This is a Markdown paragraph.

  ### Python Output 4

    foo = \
    '''This is a Markdown paragraph.''';

## Parenthesis can group markdown blocks

  ### Markdown Input 5

        foo = (
    This is a Markdown paragraph.

        )

  ### Python Output 5

    foo = (
    '''This is a Markdown paragraph.'''

    )

## explict single quotes

  ### Markdown Input 6

        foo = '''
    This is a Markdown paragraph.

        '''.lower()

  ### Python Output 6

    foo = '''
    This is a Markdown paragraph.

    '''.lower()

## explict double quotes

  ### Markdown Input 7

        foo = """
    This is a Markdown paragraph.

        """.lower()

  ### Python Output 7

    foo = """
    This is a Markdown paragraph.

    """.lower()

## function docstring

  ### Markdown Input 8

        def func(x: object) -> None:
    A Markdown paragraph as a docstring

  ### Python Output 8

    def func(x: object) -> None:
        '''A Markdown paragraph as a docstring''';

## function docstring extra trailing indent

  ### Markdown Input 9

        def func(x: object) -> None:
    A Markdown paragraph as a docstring
             
                    ...

  ### Python Output 9

    def func(x: object) -> None:
                '''A Markdown paragraph as a docstring'''

                ...

## class docstring

  ### Markdown Input 10

        class Class(Object):
    A Markdown paragraph as a docstring

  ### Python Output 10

    class Class(Object):
        '''A Markdown paragraph as a docstring''';

## class docstring extra indent

  ### Markdown Input 11

            class Class(Object):
    A Markdown paragraph as a docstring

                                def prop(self):
                                    pass

  ### Python Output 11

    class Class(Object):
                        '''A Markdown paragraph as a docstring'''

                        def prop(self):
                            pass

## class method docstring

  ### Markdown Input 12

            class Class(Object):
    A Markdown paragraph as a docstring

                                def prop(self):
      A Markdown paragraph as a method docstring

                                            pass

  ### Python Output 12

    class Class(Object):
                        '''A Markdown paragraph as a docstring'''

                        def prop(self):
                                    '''A Markdown paragraph as a method docstring'''

                                    pass

## single indent is paragraph in a markdown list

  ### Markdown Input 13

    *  A Markdown List

        This line is not code

    * Another item in the list

            # This line IS code

  ### Python Output 13

    '''*  A Markdown List

        This line is not code

    * Another item in the list'''

    # This line IS code

