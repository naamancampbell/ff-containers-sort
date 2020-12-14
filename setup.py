import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ff-containers-sort",
    version="1.5.1",
    author="Naaman Campbell",
    author_email="naaman@clancampbell.id.au",
    description="Sorts and re-numbers Firefox Containers config objects in Firefox containers.json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naamancampbell/ff-containers-sort",
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            'ff-containers-sort=ff_containers_sort.ff_containers_sort:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
)