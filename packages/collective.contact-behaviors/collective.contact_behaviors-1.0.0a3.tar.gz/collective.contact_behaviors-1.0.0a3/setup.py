"""Installer for the collective.contact_behaviors package."""
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""

short_description = (
    "A collection of contact information behaviors and vocabularies "
    "for Dexterity content types."
)


setup(
    name="collective.contact_behaviors",
    version="1.0.0a3",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
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
    author="Plone Community",
    author_email="ericof@plone.org",
    url="https://github.com/collective/collective.contact_behaviors",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.contact_behaviors",
        "Source": "https://github.com/collective/collective.contact_behaviors",
        "Tracker": "https://github.com/collective/collective.contact_behaviors/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.8",
    install_requires=["setuptools", "Plone>=6.0.0", "plone.api", "pycountry"],
    extras_require={
        "test": [
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "plone.app.testing",
            "plone.restapi[test]",
            "pytest",
            "pytest-cov",
            "pytest-plone>=0.2.0",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.contact_behaviors.locales.update:update_locale
    """,
)
