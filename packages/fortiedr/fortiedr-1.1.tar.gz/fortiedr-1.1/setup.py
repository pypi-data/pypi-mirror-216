from setuptools import find_packages, setup
from setuptools.command.install import install

setup(
    name="fortiedr",
    version="1.1",
    description="Open-source python package intended to help on interacting with FortiEDR API.",
    author="Rafael Foster",
    author_email="fosterr@fortinet.com",
    project_urls={
        "GitHub": "https://github.com/rafaelfoster/FortiEDR_API",
    },
    python_requires=">=3.5",
    packages=find_packages(),
    install_requires=[
	'requests>=2.22.0',
	'setuptools>=45.2.0'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
    ]
)

