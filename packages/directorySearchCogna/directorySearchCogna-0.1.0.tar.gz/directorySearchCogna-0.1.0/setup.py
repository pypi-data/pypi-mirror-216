from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'Pacote Utilizado para Localizar o Diretorio de Determinada Pasta'
LONG_DESCRIPTION = 'Pacote Utilizado para Localizar o Diretorio de Determinada Pasta'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="directorySearchCogna", 
        version=VERSION,
        author="Marco Rocha",
        author_email="<marco.rocha2@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[''],         
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