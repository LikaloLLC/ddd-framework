from setuptools import setup, find_packages

setup(
    name='docsie-ddd-framework',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/LikaloLLC/ddd-framework',
    license='Apache License',
    author='Docsie',
    author_email='',
    description='The package includes helper methods and types for working in DDD',
    include_package_data=True,
    install_requires=[
        "cattrs~=22.2.0",
        "attrs~=22.2.0",
        "pymongo~=4.3.3",
    ]
)
