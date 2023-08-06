# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0',
 'pyinquirer>=1.0.3,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.4.2,<14.0.0',
 'textual[dev]>=0.28.0,<0.29.0',
 'typer[all]>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'linear-cli-ai',
    'version': '0.1.1',
    'description': 'A simple cli for interacting with linear',
    'long_description': '# linear-cli\nAn AI based CLI for the linear app\n\n# How to use\n\nJust install the package using the command pip install linear-cli-ai\n\n# Sample Usage\n\nCreate an issue with description \'Rewrite the print service with queue system\'\nand title as \'Print Service v2.0\' and team as \'engineering\' and assign it to \'Rohan\'\nand add labels \'bug\' and \'high priority\' and add it to project \'Print Service\'"""\n\n\n',
    'author': 'scar3crow',
    'author_email': 'rss.holmes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
