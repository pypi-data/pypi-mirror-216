import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="checked-exception",
    version="0.0.5",
    author="thejimmylin",
    author_email="b00502013@gmail.com",
    description="Use checked exceptions in Python.",
    long_description=long_description,
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
