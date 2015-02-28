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
    entry_points = {
        'my_ep_group_id': [
            'check = wsp_control.functions:check',
            'toggle = wsp_control.functions:toggle',
            'override = wsp_control.functions:override',
        ]
    },
)
