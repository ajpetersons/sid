from setuptools import setup, find_packages

setup(
    name='sid', 
    version='1.0.0', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sid = sid.cmd.main:cli'
        ]
    }
)
