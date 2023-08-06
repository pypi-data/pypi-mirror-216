from setuptools import setup

setup(
    name='NLPSimplified',
    version='1.0.2',
    description='A simple NLP pipeline using spaCy',
    long_description=open('README.md', 'r'),
    long_description_content_type='text/markdown',
    author='Avneh Singh Bhatia',
    author_email='avnehb@gmail.com',
    packages=['NLPSimplified'],
    install_requires=[
        'spacy>=3.0.0,<4.0.0',
    ],
)
