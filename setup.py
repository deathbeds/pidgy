__import__('setuptools').setup(
    name="rites",
    version="0.0.1",
    author="deathbes", author_email="tony.fast@gmail.com",
    description="Tools for writing, righting, and riting notebooks.", 
    license="BSD-3-Clause",
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-ipynb'],
    install_requires=['ipython', 'nbconvert', 'hypothesis'],
    include_package_data=True,
    packages=['rites'],
)