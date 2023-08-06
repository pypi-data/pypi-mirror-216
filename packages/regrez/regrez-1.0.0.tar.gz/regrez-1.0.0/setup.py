from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'Easiest way to implement linear regression.'
LONG_DESCRIPTION = 'This is a simple Python package that aims to make using linear regression easier for programmers.'

setup(
        name="regrez", 
        version=VERSION,
        author="Mehmet Utku OZTURK",
        author_email="<contact@ælphard.tk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["matplotlib", "sklearn", "numpy", "pandas"],
        
        keywords=['regression', 'machine learning'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Programming Language :: Python :: 3"
        ]
)