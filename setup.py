from setuptools import setup, find_packages

setup(
    name="whatsnium",
    version="0.1.0",
    description="Automate WhatsApp Web messaging using Selenium with with multi-language support.",
    author="Jonathan Silva",
    author_email="jeas560@gmail.com",
    url="https://github.com/jeas560/whatsnium",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
        "PyYAML>=6.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
