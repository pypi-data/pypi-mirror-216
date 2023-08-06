# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayes_lol_client']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.7,<2023.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'bayes-lol-client',
    'version': '1.0.3',
    'description': 'Wrapper for Bayes League of Legends API',
    'long_description': '# Bayes LoL Client\n\nThis library is used to make queries to the Bayes EMH API, which provides data for League of Legends esports games.\nThe (in progress) documentation can be found [here](https://bayes-lol-client.readthedocs.io).\n\n## Install\n```\npip install bayes_lol_client\n```\n\nIf you wish to install the latest development version:\n```\npip install -U git+https://github.com/arbolitoloco1/bayes_lol_client\n```\n\n## Bayes Credentials\nIn order to use the Bayes API, you must have login credentials, which will be prompted the first time you use the library.\nThese will be stored in a file in your user config path.\n\n## EMH Docs\nThe full documentation to use EMH can be found [here](https://docs.bayesesports.com/api/emh_riot).',
    'author': 'Santiago Kozak',
    'author_email': 'kozaksantiago@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arbolitoloco1/bayes_lol_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
