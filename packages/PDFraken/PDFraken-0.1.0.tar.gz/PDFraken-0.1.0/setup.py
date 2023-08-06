from setuptools import setup, find_packages

setup(
    name='PDFraken',
    version='0.1.0',
    url='https://github.com/patrickfleith/PDFraken',
    author='Patrick Fleith',
    author_email='',
    description='Split your PDF from command line instead of sending your data to third parties',
    packages=find_packages(),    
    install_requires=[
        'typer',
        'PyPDF2'
     ],
    entry_points={
        'console_scripts': [
            'splitpdf=PDFraken.cli:app',
        ],
    }
)
