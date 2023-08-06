import subprocess, os

try:
  from setuptools import setup, find_packages
except ImportError:
  subprocess.call(["pip","install","setuptools"])
  from setuptools import setup, find_packages

with open( (os.path.dirname(__file__)+"/e2e_cli/docs/PyPi_description.md") , 'r') as f:
      pypi_text=f.read()

setup(
    name='e2e_cli',
    version='0.9.9.9',
    description="This a E2E CLI tool for myAccount",
    author="Sajal&Aman@E2E_Networks_Ltd",
    packages=find_packages(),
    install_requires=['prettytable', 'requests', 'setuptools', 'chardet'],
    
    long_description_content_type="text/markdown",
    long_description=pypi_text,
    
    include_package_data = True,
    package_data = {
        '': ['*.1'],
        '': ['docs/*.1'],
        'docs': ['*.1'],
    },

    entry_points={
        'console_scripts': [
            'e2e_cli=e2e_cli.main:run_main_class'
        ]
    },
)

# from  install_man import runcls
# runcls().run()