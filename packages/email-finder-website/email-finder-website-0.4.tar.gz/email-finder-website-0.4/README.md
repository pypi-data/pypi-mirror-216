# email_finder_website

## Introduction

`email_finder` is a Python library that crawls a specified website and finds all the emails on that website.

## Installation

You can install `email_finder` from PyPI:

```
pip install email-finder-website
```
The library requires Python 3.6 or later.




## Usage

Once you have the package installed, you can use it in your Python code or from the command line.

### Using in Python code:


```
from email_crawler import EmailCrawler

crawler = EmailCrawler('https://example.com')  # replace with the website you want to crawl
crawler.crawl()
```

### Using from the command line:

```
email_crawler https://example.com  # replace with the website you want to crawl
```

You can also specify the maximum number of pages to crawl:

```
email_crawler https://example.com --max-pages 10  # replace with the website you want to crawl and maximum pages to crawl
```


## License
This project is licensed under the terms of the MIT license.