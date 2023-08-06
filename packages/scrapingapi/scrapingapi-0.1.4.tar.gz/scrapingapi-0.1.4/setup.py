# read the contents of your README file
from collections import OrderedDict
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='scrapingapi',
    packages=['scrapingapi'],
    version='0.1.4',
    url='https://scrapingapi.net/',
    project_urls=OrderedDict((
        ('Documentation', 'https://scrapingapi.net/documentation'),
        ('Code', 'https://github.com/ScrapingApi/python-client'),
        ('Issue tracker', 'https://github.com/ScrapingApi/python-client/issues'),
    )),
    license='MIT',
    description='The official python client of ScrapingApi, website scraping API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Timothée Jeannin',
    author_email='tjeannin@scrapingapi.net',
    keywords=[
        "scraping",
        "proxy",
        "phantomjs",
        "scraping",
        "website",
        "headless",
        "chrome",
        "render",
        "page",
        "webkit",
    ],
    install_requires=[],
    extras_require={
        'dev': [
            'setuptools',
            'twine',
            'wheel'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
