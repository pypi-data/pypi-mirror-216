import setuptools

long_description = '123'

setuptools.setup(
    name="meta-edc-demo",
    version="0.0.2",
    author="Erik van Widenfelt",
    author_email="ew2789@gmail.com",
    description="Testing META Trial EDC (http://www.isrctn.com/ISRCTN76157257)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meta-trial/meta-edc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
)
