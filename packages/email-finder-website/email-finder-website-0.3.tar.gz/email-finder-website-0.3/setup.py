from setuptools import setup, find_packages

setup(
    name="email-finder-website",
    version="0.3",
    description="A Python library to crawl websites and collect emails",
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
