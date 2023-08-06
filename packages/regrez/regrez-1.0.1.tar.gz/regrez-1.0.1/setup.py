from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'Easiest way to implement linear regression.'

with open('README.md') as f:
    long = f.read()
setup(
        name="regrez", 
        version=VERSION,
        author="Mehmet Utku OZTURK",
        author_email="<contact@ælphard.tk>",
        description=DESCRIPTION,
        long_description=long,
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