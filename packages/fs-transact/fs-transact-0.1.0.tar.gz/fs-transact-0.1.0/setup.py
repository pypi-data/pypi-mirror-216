from setuptools import setup

setup(
    name='fs-transact',
    version='0.1.0',
    packages=['transact'],
    url='https://git.sr.ht/~martijnbraam/transact',
    license='GPL3',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Run a shell in an isolated filesystem transaction',
    entry_points={
        'console_scripts': [
            'transact=transact.__main__:main'
        ]
    }
)
