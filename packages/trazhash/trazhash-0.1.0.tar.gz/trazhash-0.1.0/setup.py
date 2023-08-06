from setuptools import setup, find_packages

setup(
    name='trazhash',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your library dependencies here
    ],
    author='TrazTech',
    author_email='contact@traztech.ca',
    description="TrazHash is a Python library designed to hash data strings or file contents using a combination of your system's specific values and cryptographic hash functions.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/traztech/trazhash',
)
