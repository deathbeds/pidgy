__import__('setuptools').setup(
    name="pidgin",
    version="0.0.1",
    author="deathbes", author_email="tony.fast@gmail.com",
    description="Macros for computable essays.",
    license="BSD-3-Clause",
    install_requires=['importnb', 'sweet'],
    include_package_data=True,
    packages=['pidgin'],
    dependency_links=[
        'https://github.com/deathbeds/importnb/tarball/master#egg=importnb',
        'https://github.com/deathbeds/sweet/tarball/master#egg=sweet'
    ])
