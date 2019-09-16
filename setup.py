import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def get_long_description():
    try:
        with open('README.md', encoding='utf8') as fd:
            return fd.read()
    except TypeError:
        with open('README.md') as fd:
            return fd.read()


setup(name='oval_graph',
      version='0.0.5',
      description='Client for visualization of SCAP rule evaluation results',
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      url='https://github.com/OpenSCAP/OVAL-visualization-as-graph',
      author='Jan Rodak',
      author_email='jrodak@redhat.com',
      license='Apache-2.0',
      packages=find_packages(),
      install_requires=[
          'lxml',
      ],
      extras_require={
          'niceCli': [
              'inquirer',
          ],
      },
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': ['arf-to-graph=oval_graph.command_line:main'],
      },
      python_requires='>=3.6',
      )
