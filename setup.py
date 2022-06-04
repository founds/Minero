from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='minero',
    version='0.0.2',
    description='A tool for searching & extracting information...',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['Minero'],
    package_dir={'Minero':'Minero'},
    url='https://www.altsys.es',
    author='altsys',
    author_email='info@altsys.es',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='minero search extract text csv',
    python_requires=">=3.7, <4",
)
