from setuptools import setup, find_packages


setup(
    name = "wsp_control",
    version = "0.1",
    description = "",
    author = "Eric George",
    author_email = "errkkgeorge@gmail.com",
    url = "https://wottonpool.co.uk",
    packages=['wsp_control'],
    install_requires=['RPi.GPIO', 'redis'],
    scripts=['src/main.py'],
)
