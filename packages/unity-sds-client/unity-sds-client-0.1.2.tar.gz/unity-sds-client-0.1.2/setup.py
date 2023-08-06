# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unity_py', 'unity_py.resources', 'unity_py.services', 'unity_py.utils']

package_data = \
{'': ['*'], 'unity_py': ['envs/*']}

install_requires = \
['giturlparse>=0.10.0,<0.11.0',
 'pystac>=1.7.3,<2.0.0',
 'requests>=2.28.0,<3.0.0',
 'tenacity>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'unity-sds-client',
    'version': '0.1.2',
    'description': "Unity-Py is a Python client to simplify interactions with NASA's Unity Platform.",
    'long_description': '# Unity-Py\n\nUnity-Py is a Python client to simplify interactions with NASA\'s Unity Platform.\n\n## Installation\n\n### Install from Github\n```\npython -m pip install git+https://github.com/unity-sds/unity-py.git\n```\n\n### Building and installing locally using poetry\n\n```\ngit clone https://github.com/unity-sds/unity-py.git\ncd unity-py\npoetry install\n```\n\n## Getting Started\n\n### Authorization\n\nAuthorization can be handled interactively, in which case you will be prompted for a username/password when calling the Unity() method, or can be handled by way of environment variables:\n\n```\nexport UNITY_USER=MY_UNITY_USERNAME\nexport UNITY_PASSWORD=MY_UNITY_PASSWORD\n```\n\nThe order of Authentication Parameters is as follows:\n\n1. Environment variables\n2. Prompt for username and password\n\n### Running your first command\n\n```\nfrom unity_py.unity import Unity\nfrom unity_py.unity_session import UnitySession\nfrom unity_py.unity_services import UnityServices as services\n\ns = Unity()\ndataManager = s.client(services.DATA_SERVICE)\ncollections = dataManager.get_collections()\nprint(collections)\n\ncd = dataManager.get_collection_data(collections[0])\nfor dataset in cd:\n    print(f\'dataset name: {dataset.id}\' )\n    for f in dataset.datafiles:\n        print("\\t" + f.location)\n```\n\n## Testing\nTo run unit and regression tests:\n\n```\n# run all tests and include printouts:\npoetry run pytest -s\n\n# run non-regression tests:\npoetry run pytest -m "not regression"\n\n# run regression tests (and include logs)\n\n```\n',
    'author': 'Anil Natha, Mike Gangl',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unity-sds/unity-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
