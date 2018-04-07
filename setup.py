__import__('setuptools').setup(
    name="rites",
    version="0.0.1",
    author="deathbes", author_email="tony.fast@gmail.com",
    description="Macros for computable essays.", 
    license="BSD-3-Clause",
    install_requires=['importnb', 'sweet'],
    include_package_data=True,
    packages=['rites'],
    dependency_links=[
        'https://github.com/deathbeds/importnb/archive/master.tar.gz#egg=importnb-0.0.1',
        'https://github.com/deathbeds/sweet/archive/master.tar.gz#egg=sweet-0.0.1'
    ]
    
)