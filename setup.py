import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="particle_analyzer",
    version="0.0.2.dev0",
    author="Nick Machairas",
    author_email="machairas@nyu.edu",
    description="A simple program that analyzes soil particle data and "
                "produces plots and particle images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickmachairas/particle_analyzer",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy==1.14.3',
        'pandas==0.23.0',
        'matplotlib==2.2.2',
        'tqdm==4.23.3',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
