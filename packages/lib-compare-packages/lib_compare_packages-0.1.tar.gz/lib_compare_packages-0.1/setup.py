from setuptools import setup, find_packages

setup(
    name='lib_compare_packages',
    description='library for comparing two branches',
    version='0.1',
    packages=find_packages(),
    author="Alena Guseva",
    author_email="axenova.ale@mail.ru",
    url="https://github.com/aksalena/lib_compare_packages",
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'lib_compare_packages=lib_compare_packages.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)