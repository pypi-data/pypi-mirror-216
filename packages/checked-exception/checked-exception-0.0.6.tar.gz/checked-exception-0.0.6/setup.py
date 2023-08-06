import setuptools


setuptools.setup(
    name="checked-exception",
    version="0.0.6",
    author="thejimmylin",
    author_email="b00502013@gmail.com",
    description="Use checked exceptions in Python.",
    long_description=(
        "# Use checked exceptions in Python.\n"
        "\n"
        "This package makes you use checked exceptions in Python.\n"
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/thejimmylin/checked-exception",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
