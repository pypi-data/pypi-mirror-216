# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drive',
 'drive.cluster',
 'drive.factory',
 'drive.filters',
 'drive.log',
 'drive.models',
 'drive.plugins',
 'drive.utilities',
 'drive.utilities.callbacks',
 'drive.utilities.parser',
 'factory']

package_data = \
{'': ['*']}

install_requires = \
['igraph>=0.10.4,<0.11.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['drive = drive.drive:app']}

setup_kwargs = {
    'name': 'drive-ibd',
    'version': '2.0.3',
    'description': 'cli tool to identify networks of individuals who share IBD segments overlapping loci of interest',
    'long_description': '# DRIVE:\n\nThis repository contains the source code for the tool DRIVE v1.0.0. Distant Relatedness for Identification and Variant Evaluation (DRIVE) is a novel approach to IBD-based genotype inference used to identify shared chromosomal segments in dense genetic arrays. DRIVE implemented a random walk algorithm that identifies clusters of individuals who pairwise share an IBD segment overlapping a locus of interest. This tool was developed in python by the Below Lab at Vanderbilt University. The documentation for how to use this tool can be found here [DRIVE documentation](https://belowlab.github.io/drive/)\n\n## Installing DRIVE:\nDRIVE is available on PYPI and can easily be installed using the following command:\n\n```bash\npip install drive-ibd\n```\n\nIf the user wishes to develop DRIVE or install the program from source then they can clone the repository. This process is described under the section called "Github Installation" in the documentation.\n\n### Reporting issues:\nIf you wish to report a bug or propose a feature you can find templates under the .github/ISSUE_TEMPLATE directory.',
    'author': 'James Baker',
    'author_email': 'james.baker@vanderbilt.edu',
    'maintainer': 'James Baker',
    'maintainer_email': 'james.baker@vanderbilt.edu',
    'url': 'https://belowlab.github.io/drive/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
