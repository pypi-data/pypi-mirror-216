import setuptools


setuptools.setup(
    name="f5project",
    version="0.0.1",
    author="thejimmylin",
    author_email="b00502013@gmail.com",
    description="F5 project",
    long_description=(
        "# F5 project\n"
        "\n"
        "This package makes you use F5 project in Python.\n"
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/thejimmylin/f5project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
