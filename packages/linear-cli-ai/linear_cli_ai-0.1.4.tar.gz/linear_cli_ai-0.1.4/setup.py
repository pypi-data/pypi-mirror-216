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

entry_points = \
{'console_scripts': ['linear = src.main:app']}

setup_kwargs = {
    'name': 'linear-cli-ai',
    'version': '0.1.4',
    'description': 'A simple cli for interacting with linear',
    'long_description': "# linear-cli\nAn AI based CLI for the linear app\n\n# Installation\n\nInstallation of linear-cli-ai and its dependencies require ``python`` and ``pip``. To ensure smooth installation,\nit's recommended to use:\n\n- ``python``: 3.8.10 or greater\n- ``pip``: 9.0.2 or greater\n\nThe safest way to install globally is to use\n\n```\n\n   $ python -m pip install linear-cli-ai\n\n```\n\nor for your user:\n\n```\n\n   $ python -m pip install --user linear-cli-ai\n\n```\n\nIf you have the linear-cli-ai package installed and want to upgrade to the\nlatest version, you can run:\n\n```\n\n   $ python -m pip install --upgrade linear-cli-ai\n\n```\n\n# Configuration\n\nBefore using linear-cli-ai, you need to configure a few keys.\nYou can do this in several ways:\n\n-  Configuration command\n-  Environment variables\n-  Config file\n\nThe quickest way to get started is to run the ``linear configure`` command:\n\n```\n$ linear configure\n  Provide the following details : \n   Linear API Token : MY_LINEAR_TOKEN\n   OpenAI API Key : MY_OPENAI_KEY\n   Select the model you will use : gpt4 or gpt-3.5-turbo-0613\n\n```\n\nTo use environment variables, do the following:\n\n```\n\n   $ export LINEAR_TOKEN=<linear_token>\n   $ export GPT_MODEL=<gpt_model>\n   $ export OPENAI_API_KEY=<openai_api_key>\n\n```\n\nTo use a config file, create an INI formatted file like this:\n\n```\n\n  [linear]\n  token = <linear_token>\n  \n  [gpt]\n  token = <openai_api_key>\n  model = <gpt_model>\n\n```\nand place it in ``~/.linear-cli-ai.ini`` (or in ``%UserProfile%\\.linear-cli-ai.ini`` on Windows).\n\n# Sample Usage\n\nlinear-cli-api is available in the commandline with the command ``linear``\n\nTo view help documentation type :\n\n```\n$ linear help\n```\n\nTo use ai to perform actions on linear:\n\n```\n$ linear ai\n```\n\nTo create an issue via options on linear :\n\n```\n$ linear create-issue\n```\n### Sample ai prompt for creating an issue on linear\nCreate an issue with description 'Rewrite the print service with queue system'\nand title as 'Print Service v2.0' and team as 'engineering' and assign it to 'Rohan'\nand add labels 'bug' and 'high priority' and add it to project 'Print Service'\n\n\n",
    'author': 'scar3crow',
    'author_email': 'rss.holmes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.8.10',
}


setup(**setup_kwargs)
