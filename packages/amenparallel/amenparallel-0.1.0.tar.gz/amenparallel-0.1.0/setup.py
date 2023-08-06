from setuptools import setup, find_packages

setup(
    name='amenparallel',
    version='0.1.0',
    description='Library to process parallel Amharic-English texts',
    author='Hizkiel',
    author_email='hizkiel.alemayehu@uni-paderborn.de',
    url='https://github.com/dice-group/Amharic_English_Parallal_Corpus/tree/main',
    packages=find_packages(),
    install_requires=[
        'pyonmttok',
        'truecase',
        'pycld2',
        'nltk',
        'amseg',
        'regex' 
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
