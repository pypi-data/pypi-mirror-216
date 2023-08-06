"""Installer for the collective.belowcontentportlets package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.belowcontentportlets",
    version="1.0.0a1",
    description="Content Type to show an belowcontentportlets",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/collective/collective.belowcontentportlets",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.belowcontentportlets/",
        "Source": "https://github.com/collective/collective.belowcontentportlets",
        "Tracker": "https://github.com/collective/collective.belowcontentportlets/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.api",
            "plone.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
