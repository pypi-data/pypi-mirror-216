import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pineworkslabs",
    version="0.2.0",
    author="Pineworks Labs",
    author_email="shelby@pineworkslabs.com",
    description="An access layer for the Pineworks Labs RP2040 GPIO board",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pineworkslabs/rp-2040-gpio-board",
    project_urls={
        "Bug Tracker": "https://gitlab.com/pineworkslabs/rp-2040-gpio-board/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)