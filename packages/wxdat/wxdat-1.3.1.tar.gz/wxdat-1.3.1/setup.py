# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wxdat', 'wxdat.providers', 'wxdat.units']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'gitpython>=3.1.31,<4.0.0',
 'prometheus-client>=0.17.0,<0.18.0',
 'psycopg2>=2.9.6,<3.0.0',
 'pydantic>=1.10.9,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'sqlalchemy>=2.0.17,<3.0.0']

entry_points = \
{'console_scripts': ['wxdat = wxdat.__main__:main']}

setup_kwargs = {
    'name': 'wxdat',
    'version': '1.3.1',
    'description': 'Weather data explorer.',
    'long_description': "# wxdat #\n\n[![PyPI](https://img.shields.io/pypi/v/wxdat.svg)](https://pypi.org/project/wxdat)\n[![LICENSE](https://img.shields.io/github/license/jheddings/wxdat)](LICENSE)\n[![Style](https://img.shields.io/badge/style-black-black)](https://github.com/ambv/black)\n\nA general purpose weather data recorder & explorer.\n\n![dashboard](docs/images/dashboard.png)\n\nWhile the primary purpose of this library is to record weather data, it can also be\nused as a framework for collecting weather information in other apps.\n\n## Installation ##\n\nInstall the published package using pip:\n\n```shell\npip3 install wxdat\n```\n\nThis project uses `poetry` to manage dependencies and a local virtual environment.  To\nget started, clone the repository and install the dependencies with the following:\n\n```shell\npoetry install\n```\n\n## Usage ##\n\nRun the module and tell it which config file to use.\n\n```shell\npython3 -m wxdat --config wxdat.yaml\n```\n\nIf you are using `poetry` to manage the virtual environment, use the following:\n\n```shell\npoetry run python -m wxdat --config wxdat.yaml\n```\n\n## Configuration ##\n\nThe configuration file is a YAML document with a list of stations to export.  See the\nincluded default file for more details.\n\nAll stations have the following configuration values:\n* name - must be unique\n* type - the support station type\n\n## Supported Stations ##\n\nEventually, I'd like to add local stations, not just online sources.  Please see\nthe example configuration file for details on each provider.\n\n* AccuWeather\n* Ambient Weather Network\n* OpenWeatherMap\n* National Weather Service (NOAA)\n* Weather Underground\n\n## Unit Conversion ##\n\n`wxdat` also includes a limited set of conversion helpers for working with units.  In\ngeneral, the pattern for using them is:\n\n```python\nfrom wxdat import units\n\n# convert 100.0 from celsius to fahrenheit\ntemp = units.degC(100).degf\n```\n\n## Contributing ##\n\nTo submit a new issue, please visit the [Issues](https://github.com/jheddings/wxdat/issues)\npage.\n\nIf you are unsure where to start, create a post in the\n[Discussions](https://github.com/jheddings/wxdat/discussions) area.\n\nAdditionally, [Pull Requests](https://github.com/jheddings/wxdat/pulls) are welcome.\n",
    'author': 'jheddings',
    'author_email': 'jheddings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
