from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Python Hello World Package'
LONG_DESCRIPTION = 'A Python Package that can print Hello, World'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="helloworld-rayaq", 
        version=VERSION,
        author="Rayaq Siddiqui",
        author_email="rayaq05@hotmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
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