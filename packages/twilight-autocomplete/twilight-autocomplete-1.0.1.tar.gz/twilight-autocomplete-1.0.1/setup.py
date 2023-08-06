from setuptools import setup, find_packages

setup(
    name='twilight-autocomplete',
    version='1.0.1',
    description='Autocomplete Package built using NLTK for the twilight messaging client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Avneh Singh Bhatia',
    author_email='avnehb@gmail.com',
    packages=find_packages(),
    install_requires=[
        'nltk'
    ],
)
