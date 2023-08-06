from setuptools import setup

setup(
    name='NLPSimplified',
    version='1.0.1',
    description='A simple NLP pipeline using spaCy',
    author='Avneh Singh Bhatia',
    author_email='avnehb@gmail.com',
    packages=['NLPSimplified'],
    install_requires=[
        'spacy>=3.0.0,<4.0.0',
    ],
)
