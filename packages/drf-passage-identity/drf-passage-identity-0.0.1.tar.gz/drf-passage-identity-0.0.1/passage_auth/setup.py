from setuptools import setup, find_packages

setup(
    name='drf-passage-identity',
    version='0.1',
    description='Description of your package',
    author='Prem',
    author_email='kothawleprem@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Django',
        'djangorestframework',
        'passage-identity'
    ],
)
