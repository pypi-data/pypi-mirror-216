from setuptools import setup, find_packages

setup(
    name='vipes',
    version='0.0.1',
    author='Jhon',
    description='The most reliable script manager for crossplatform projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/flobbun',
    packages=find_packages(),
    python_requires='>=3.7',
    include_package_data=False
)