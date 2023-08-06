from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'String treatment package'
LONG_DESCRIPTION = '''
Method to treat strings with inconsistencies in your data

Github: https://github.com/guilhermehuther/string_treatment
'''

setup(
        scripts=['string_treatment.py'],
        name="string_treatment", 
        version=VERSION,
        author="Guilherme Huther Baldo",
        author_email="guilhermehuther@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['jellyfish', 'numpy', 'pandas'],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)