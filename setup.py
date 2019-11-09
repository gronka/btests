import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

entry_points = {
    'console_scripts': [
        'ftests = ftests.__main__:main'
    ]
}

setuptools.setup(
    name="ftests",
    version="0.0.1",
    author="Taylor Gronka",
    author_email="mr.gronka@gmail.com",
    description="Functional tests for flick",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gronka/ftests",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Click",
        "requests",
    ],
    entry_points=entry_points,
)
