import setuptools
from hypehd import __version__

# Read in the requirements.txt file
with open("requirements.txt") as f:
    requirements = []
    for library in f.read().splitlines():
        requirements.append(library)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hypehd",
    version=__version__,
    author="Jiayi Wang, Alieyeh Sarabandi Moghaddam",
    author_email="jw1289@exeter.ac.uk, as1724@exeter.ac.uk",
    license="The MIT License (MIT)",
    description="This package aims to be a tool for real-world and practical data analysis, assisting in reaching a "
                "quicker understanding of various health related data.",
    # read in from readme.md and will appear on PyPi
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alieyeh/hypehd",
    packages=setuptools.find_packages(),
    # if true look in MANIFEST.in for data files to include
    include_package_data=True,
    # 2nd approach to include data is include_package_data=False
    package_data={"hypehd": ["data/*.csv"]},
    # these are for documentation
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements,
)
