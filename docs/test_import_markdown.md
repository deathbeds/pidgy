# Reusing markdown documents as code.
    
    import pidgy
In `pidgy`, `markdown` documents are transformed
into programs that can be imported. 
This document tests that ability.


    try: from . import test_import_markdown
    except: import test_import_markdown
    assert test_import_markdown.__file__.endswith('.md')
