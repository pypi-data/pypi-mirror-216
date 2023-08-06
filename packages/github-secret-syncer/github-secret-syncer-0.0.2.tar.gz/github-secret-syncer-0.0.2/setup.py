import setuptools


setuptools.setup(
    name="github-secret-syncer",
    version="0.0.2",
    author="thejimmylin",
    author_email="b00502013@gmail.com",
    description="Github Secret Syncer.",
    long_description=(
        "# Github Secret Syncer..\n"
        "\n"
        "Synchronize Github secrets with local `.env` file.\n"
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/thejimmylin/github-secret-syncer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
