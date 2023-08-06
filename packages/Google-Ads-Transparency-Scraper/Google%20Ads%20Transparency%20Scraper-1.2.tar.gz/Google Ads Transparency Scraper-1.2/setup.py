"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

setup(
    name="Google Ads Transparency Scraper",
    author="Farhan Ahmed",
    author_email="jattfarhan10@gmail.com",
    url="https://github.com/faniAhmed/GoogleAdsTransparencyScraper",
    description="A scraper for getting Ads from Google Transparency",
    version="1.2",
    packages=find_packages(where=".", exclude=["tests"]),
    download_url= 'https://github.com/faniAhmed/GoogleAdsTransparencyScraper/archive/refs/tags/v1.2.tar.gz',
    keywords= ['Google', 'Transparency', 'Scraper', 'API', 'Google Ads', 'Ads', 'Google Transparency', 'Google Transparency Scraper', 'Google Ads Scrapre'],
    license='Securely Incorporation',
    install_requires=[
        "setuptools>=45.0",
        "beautifulsoup4>=4.12.2",
        "Requests>=2.31.0",
        "lxml>=4.6.3",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Natural Language :: Urdu",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
)