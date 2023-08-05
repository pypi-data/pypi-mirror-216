from setuptools import setup, find_packages

setup(
    name='vipes',
    version='0.0.5',
    author='Jhon',
    description='The most reliable script manager for crossplatform projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/flobbun/vipes',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    keywords=['script', 'manager', 'crossplatform', 'configuration'],
    packages=find_packages(),
    python_requires='>=3.7',
    entry_points='''
        [console_scripts]
        vipes=vipes.cli:main
    ''',
    include_package_data=False
)