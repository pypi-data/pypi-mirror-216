from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="email-finder-website",
    version="0.4",
    description="A Python library to crawl websites and collect emails",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Sav Cal",
    author_email="savadamcal@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "lxml",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'emailfinder=email_crawler.crawler:main',
        ],
    },
)
