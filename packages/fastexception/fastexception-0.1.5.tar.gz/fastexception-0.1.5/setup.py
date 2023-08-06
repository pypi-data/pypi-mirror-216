from setuptools import setup, find_packages
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
this_directory = Path(__file__).parent
setup(

    name='fastexception',
    version='0.1.5',
    license='MIT',
    author='Mojtaba',
    author_email='mojtabapaso@gamil.com',
    packages=find_packages(),
    url='https://github.com/mojtabapaso/fastexception',
    keywords='FastAPI Tools Fast Exception',

    install_requires=[
        'starlette',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'

)
