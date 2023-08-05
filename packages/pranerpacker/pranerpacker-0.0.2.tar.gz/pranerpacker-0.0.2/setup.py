from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Praneeths first Python package'
LONG_DESCRIPTION = 'praneeths first package with a slightly longer description'


setup(
     
        name="pranerpacker", 
        version=VERSION,
        author="Sai Praneeth Renduchinthala",
        author_email="praneeth.renduchinthala210@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=[ 'pranerpacker'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)