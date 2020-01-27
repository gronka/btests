import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

entry_points = {
    'console_scripts': [
        'btests = btests.__main__:main'
    ]
}

setuptools.setup(
    name="btests",
    version="0.0.1",
    author="Taylor Gronka",
    author_email="mr.gronka@gmail.com",
    description="Tests for bapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/gronka/btests",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Undetermined",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points=entry_points,
)
