from setuptools import setup, find_packages
from pathlib import Path

with Path('README.md').open() as readme:
    readme = readme.read()

version = 1.0

setup(
    name='paperbnf',
    version=version if isinstance(version, str) else str(version),
    keywords="LaTex, BNF",
    # keywords of your project that separated by comma ","
    description="",  # a conceise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.7.0',
    url='https://github.com/thautwarm/paperbnf',
    author='thautwarm',
    author_email='twshere@outlook.com',
    packages=find_packages(),
    py_modules=['paperbnf_lex', 'paperbnf_parser', 'paperbnf'],
    install_requires=[],
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)

