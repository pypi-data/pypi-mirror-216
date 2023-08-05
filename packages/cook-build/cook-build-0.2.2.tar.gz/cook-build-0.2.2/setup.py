from setuptools import find_packages, setup


with open("README.rst") as fp:
    long_description = fp.read()
long_description = long_description \
    .replace(":func:", ":code:") \
    .replace(".. doctest::", ".. code-block::\n") \
    .replace(".. shtest::", ".. code-block::\n") \
    .replace(":class:", ":code:") \
    .replace(".. toctree::", "..") \
    .replace(".. sh::", "..")


setup(
    name="cook-build",
    version="0.2.2",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    python_requires=">=3.8",
    install_requires=[
        "colorama",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cook = cook.__main__:__main__",
        ],
    },
)
