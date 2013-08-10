from setuptools import setup, find_packages


setup(
    name = "wsp_control",
    version = "0.1",
    description = "",
    author = "Eric George",
    author_email = "errkkgeorge@gmail.com",
    url = "https://wottonpool.co.uk",
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[ ],
    scripts=['src/main.py'],
)
