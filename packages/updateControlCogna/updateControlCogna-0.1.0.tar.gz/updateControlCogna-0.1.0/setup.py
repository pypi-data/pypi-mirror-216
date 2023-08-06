from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'Pacote Facilitador Para Acompanhamento de Atualizações'
LONG_DESCRIPTION = 'Pacote Facilitador Para Acompanhamento de Atualizações'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="updateControlCogna", 
        version=VERSION,
        author="Marco Rocha",
        author_email="<marco.rocha2@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas'],         
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