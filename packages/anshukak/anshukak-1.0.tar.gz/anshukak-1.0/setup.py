from setuptools import setup

setup(
    name='anshukak',
    version='1.0',
    packages=['anshukak'],
    entry_points={
        'console_scripts': [
            'anshukak = anshukak.main:main'
        ]
    },
    install_requires=[
        'requests',
        'pyperclip'
    ],
)
