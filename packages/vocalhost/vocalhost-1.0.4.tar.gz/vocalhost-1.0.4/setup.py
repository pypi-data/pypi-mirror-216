from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vocalhost',
    version='1.0.4',
    py_modules=['receiver', 'request'],
    install_requires=[
        'websockets',
        'certifi',
        'requests'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)