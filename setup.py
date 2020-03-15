from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name = "lcagg",
    version = "0.1",

    description = "Liquid chromatography (LC) aggregation and processing",
    url = "https://github.com/rnelsonchem/lcagg",
    long_description = long_description,

    author = "Ryan Nelson",
    author_email = "rnelsonchem@gmail.com",

    license = "MIT",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU License',
        'Programming Language :: Python :: 3',
    ],

    keywords = "Liquid Chromatography LC HPLC",

    packages = find_packages(),
    install_requires = [
        'numpy>=1.17',
        'pandas>=1.0',
        ]

)


