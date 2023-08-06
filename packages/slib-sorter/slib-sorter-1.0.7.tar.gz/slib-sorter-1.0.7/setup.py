from setuptools import setup, find_packages

setup(
    name="slib-sorter",
    version="1.0.7",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "slib-sorter = src.__main__:sort_files",
        ]
    },
    install_requires=[
        "termcolor"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
)