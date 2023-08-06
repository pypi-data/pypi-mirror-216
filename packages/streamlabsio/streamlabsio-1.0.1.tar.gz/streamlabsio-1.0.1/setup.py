# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlabsio']

package_data = \
{'': ['*']}

install_requires = \
['observable>=1.0.3,<2.0.0',
 'python-engineio==3.14.2',
 'python-socketio[client]==4.6.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['debug = scripts:ex_debug']}

setup_kwargs = {
    'name': 'streamlabsio',
    'version': '1.0.1',
    'description': 'Get real time Twitch/Youtube events through Streamlabs SocketIO API',
    'long_description': '[![PyPI version](https://badge.fury.io/py/streamlabsio.svg)](https://badge.fury.io/py/streamlabsio)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/streamlabs-socketio-py/blob/dev/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n# A Python client for Streamlabs Socket API\n\nFor an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)\n\n### Requirements\n\n-   A Streamlabs Socket API key.\n    -   You can acquire this by logging into your Streamlabs.com dashboard then `Settings->Api Settings->API Tokens`\n\n-   Python 3.8 or greater\n\n### How to install using pip\n\n```\npip install streamlabsio\n```\n\n### How to Use\n\nYou may store your api key in a `config.toml` file, its contents should resemble:\n\n```toml\n[streamlabs]\ntoken = "<apikey>"\n```\n\nPlace it next to your `__main__.py` file.\n\n#### Otherwise:\n\nYou may pass it as a keyword argument.\n\nExample `__main__.py`:\n\n```python\nimport streamlabsio\n\n\ndef on_twitch_event(event, data):\n    print(f"{event}: {data.attrs()}")\n\n\ndef main():\n    with streamlabsio.connect(token="<apikey>") as client:\n        client.obs.on("streamlabs", on_twitch_event)\n        client.obs.on("twitch_account", on_twitch_event)\n\n        # run for 30 seconds then disconnect client from server\n        client.sio.sleep(30)\n\n\nif __name__ == "__main__":\n    main()\n```\n\n#### note\n\nFrom the [SocketIO docs](https://python-socketio.readthedocs.io/en/latest/client.html#managing-background-tasks), `client.sio.wait()` may be used if your application has nothing to do in the main thread.\n\n### Client class\n`streamlabsio.connect(token="<apikey>", raw=False)`\n\nThe following keyword arguments may be passed:\n\n-   `token`: str   Streamlabs SocketIO api token.\n-   `raw`: boolean=False    Receive raw json objects.\n\n### Attributes\n\nFor event data you may inspect the available attributes using `attrs()`.\n\nexample:\n\n```python\ndef on_twitch_event(event, data):\n    print(f"{event}: {data.attrs()}")\n```\n\n### Errors\n\n-   `SteamlabsSIOConnectionError`: Exception raised when connection errors occur\n\n### Logging\n\nTo view raw incoming event data set logging level to DEBUG. Check `debug` example.\n\n### Official Documentation\n\n-   [Streamlabs Socket API](https://dev.streamlabs.com/docs/socket-api)\n',
    'author': 'onyx-and-iris',
    'author_email': 'code@onyxandiris.online',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/onyx-and-iris/streamlabs-socketio-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
