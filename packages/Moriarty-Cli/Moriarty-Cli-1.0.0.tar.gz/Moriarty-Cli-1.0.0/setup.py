from setuptools import setup, find_packages

setup(
    name='Moriarty-Cli',
    version='1.0.0',
    author='Moriarty',
    description='a cli for init .tsx from yapi',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Moriarty = Moriarty.module:main',
        ],
    },
)
