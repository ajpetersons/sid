from setuptools import setup, find_packages
try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


setup(
    name='sid', 
    version='1.0.0', 
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'sid = sid.cmd.main:cli'
        ]
    },
    install_requires=load_requirements("requirements.txt")
)
