from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(

    name='graphnet',
    version='0.1.0',
    description='A python library for graph manipulation and visualization',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Fredpwol/graphnet',
    author='Fredrick Pwol',
    author_email='fredpwol@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=['numpy', "matplotlib"],
)