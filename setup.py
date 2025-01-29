from setuptools import setup, find_packages

setup(
    name="microsaas",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'python-dotenv',
        'pypdf2'
    ],
)
