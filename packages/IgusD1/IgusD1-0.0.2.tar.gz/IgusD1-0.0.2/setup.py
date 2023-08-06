from setuptools import find_packages
from setuptools import setup


VERSION = '0.0.2'
DESCRIPTION = 'Package for Ingus D1 '
LONG_DESCRIPTION = 'file: README.md'

# Setting up
setup(
        # the name must match the folder name 'verysimplemodule'
        name="IgusD1",
        version=VERSION,
        author="Niklas Kuehnl",
        author_email="<niklas.kuehnl@beurer.de>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],  # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers=[
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Education",
                "Programming Language :: Python :: 2",
                "Programming Language :: Python :: 3",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: Microsoft :: Windows",
        ]
)
