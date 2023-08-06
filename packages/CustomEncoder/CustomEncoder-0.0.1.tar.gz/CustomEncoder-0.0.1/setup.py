from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A custom LabelEncoder implementation'


# Setting up
setup(
    name="CustomEncoder",
    version=VERSION,
    author="Tanmay Chakraborty",
    author_email="chakrabortytanmay326@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'encoder', 'machine-learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)