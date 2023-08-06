from distutils.core import setup

try:
   import pypandoc
   long_desc = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
   long_desc = open('README.md').read()


#this_directory = Path(__file__).parent
#long_desc = (this_directory / "README").read_text()

setup(
    name='SpecLab',
    version='4.0.7',
    author='A. F. Kowalski',
    author_email='adam.f.kowalski@colorado.edu',
    packages=['SpecLab','SpecLab.aux','SpecLab.aux.param_files','SpecLab.imXam','SpecLab.doc','SpecLab.gen',],
    package_data = {'':['*.tar.gz', '*.txt', '*.dat'],},
   # include_package_data=True,
   # package_dir={"": ""},
    scripts=['SpecLab/cfg/SpecLab_config.py','SpecLab/imXam/imXam.py','SpecLab/cfg/epar_imXam.py',],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    description='IRAF imexam+DS9 replacement for Python',long_description_content_type='text/markdown',
    long_description=long_desc,
    install_requires=['numpy', 'plotly>=5.2.1', 'pandas','astropy>=4.0.2','scipy','matplotlib','PyQt5>=5.15.6', 'photutils',]
)

# python setup.py sdist
# python -m twine upload --repository testpypi dist/*
# pip install -i https://test.pypi.org/simple/ speclab-imXam==3.1.2
# pip uninstall speclab-imXam==3.1.2
#  I neeeded to put the #! crap at the top of any of the scripts=
# put alias for imXam.py -f 

#https://test.pypi.org/project/SpecLab/3.1.3/
#https://test.pypi.org/project/SpecLab/3.1.12/
