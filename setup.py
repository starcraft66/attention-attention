import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="attention-attention",
    version=1.0,
    author="Tristan Gosselin-Hane, Roch D'Amour",
    author_email="starcraft66@gmail.com, roch.damour@gmail.com",
    description="Plays attention-attention in voice chat early in the morning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/starcraft66/attention-attention",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
