from setuptools import find_packages, setup

import oval_graph


def get_long_description():
    try:
        with open('README.md', encoding='utf8') as fd:
            return fd.read()
    except TypeError:
        with open('README.md') as fd:
            return fd.read()


setup(name='oval_graph',
      version=oval_graph.__version__,
      description='Tool for visualization of SCAP rule evaluation results',
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      url='https://github.com/OpenSCAP/OVAL-visualization-as-graph',
      author='Jan Rodak',
      author_email='jrodak@redhat.com',
      license='Apache-2.0',
      packages=find_packages(exclude=["tests_oval_graph", "tests_oval_graph.*"]),
      install_requires=[
          'lxml',
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'arf-to-graph=oval_graph.command_line:arf_to_graph',
              'arf-to-json=oval_graph.command_line:arf_to_json',
              'json-to-graph=oval_graph.command_line:json_to_graph',
          ],
      },
      python_requires='>=3.6',
      )
