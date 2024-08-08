from setuptools import setup, find_packages

setup(
    name='MarCell',
    packages=find_packages(),
    install_requires=[
        'pandas==1.5.3',
        'numpy==1.23.5',
        'seaborn==0.12.2',
        'matplotlib==3.7.2',
        'plotly==5.18.0',
        'scipy==1.10.1',
        'cellpose==2.1.1'],
    url='https://github.com/julienf1249/MarCell',
    author='Julien Ferragu',
    author_email='julien.ferragu@inserm.fr',
     
)
