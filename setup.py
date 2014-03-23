from setuptools import setup, find_packages


setup(
    name = "wsp_control",
    version = "0.1",
    description = "",
    author = "Eric George",
    author_email = "errkkgeorge@gmail.com",
    url = "https://wottonpool.co.uk",
    package_dir={'wsp_control': 'src'},
    install_requires=['RPi.GPIO', 'redis', 'gspread', 'raven'],
    scripts=['src/runwsp.py'],
)
