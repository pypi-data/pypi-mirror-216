from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Saranya Narayansetti Package'
LONG_DESCRIPTION = 'This is the package dedicated to chinna'


setup(
     
        name="SaranyaNarayansetti", 
        version=VERSION,
        author="Sai Praneeth Renduchinthala",
        author_email="praneeth.renduchinthala210@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=[ 'SaranyaNarayansetti', 'SaranyaNarayansetti package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)