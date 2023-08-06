import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="teamanchorhello",
    version="0.0.6",
    author="fanis",
    description="teamanchor say hello using Pypi package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["teamanchorhello"],
    package_dir={'':'teamanchorhello/src'},
    install_requires=[]
)