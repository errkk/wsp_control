from setuptools import setup, find_packages


setup(
    name = "wsp_control",
    version = "0.1",
    description = "",
    author = "Eric George",
    author_email = "errkkgeorge@gmail.com",
    url = "https://wottonpool.co.uk",
    packages=['wsp_control'],
    install_requires=['RPi.GPIO', 'requests'],
    scripts=['src/runwsp.py'],
    entry_points = {
        'console_scripts': [
            'wcheck = wsp_control.functions:check',
            'wtoggle = wsp_control.functions:toggle',
            'woverride = wsp_control.functions:override',
        ]
    },
)
