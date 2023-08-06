# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmcompact']

package_data = \
{'': ['*'], 'vmcompact': ['img/*']}

install_requires = \
['sv-ttk>=2.5.1,<3.0.0',
 'vban-cmd>=2.0.0,<3.0.0',
 'voicemeeter-api>=2.0.2,<3.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'voicemeeter-compact',
    'version': '1.8.2',
    'description': 'A Compact Voicemeeter Remote App',
    'long_description': '[![PyPI version](https://badge.fury.io/py/voicemeeter-compact.svg)](https://badge.fury.io/py/voicemeeter-compact)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/voicemeeter-compact/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![OS: Windows](https://img.shields.io/badge/os-windows-red)\n\n![Image of app/potato size comparison](./doc_imgs/potatocomparisonsmaller.png)\n\n# Voicemeeter Compact\n\nA compact Voicemeeter remote app, works locally and over LAN.\n\nFor an outline of past/future changes refer to: [CHANGELOG](CHANGELOG.md)\n\n## Prerequisites\n\n-   [Voicemeeter](https://voicemeeter.com/) (Basic v1.0.8.4), (Banana v2.0.6.4) or (Potato v3.0.2.4)\n-   Python 3.10 or greater\n\n## Installation\n\nFor a step-by-step guide [click here](INSTALLATION.md)\n\n```\npip install voicemeeter-compact\n```\n\n## Usage\n\nExample `__main__.py` file:\n\n```python\nimport voicemeeterlib\nimport vmcompact\n\n\ndef main():\n    # pass the kind_id and the vm object to the app\n    with voicemeeterlib.api(kind_id) as vm:\n        app = vmcompact.connect(kind_id, vm)\n        app.mainloop()\n\n\nif __name__ == "__main__":\n    # choose the kind of Voicemeeter (Local connection)\n    kind_id = "banana"\n\n    main()\n```\n\nIt\'s important to know that only labelled strips and buses will appear in the Channel frames. Removing a Channels label will cause the GUI to grow/shrink in real time.\n\n![Image of unlabelled app](./doc_imgs/nolabels.png)\n\nIf the GUI looks like the above when you first load it, then no channels are labelled. From the menu, `Configs->Load config` you may load an example config. Save your current Voicemeeter settings first :).\n\n### kind_id\n\nSet the kind of Voicemeeter, kind_id may be:\n\n-   `basic`\n-   `banana`\n-   `potato`\n\n## TOML Files\n\nThis is how your files should be organised. Wherever your `__main__.py` file is located (after install this can be any location), `configs` should be in the same location.\nDirectly inside of configs directory you may place an app.toml, vban.toml and a directory for each kind.\nInside each kind directory you may place as many custom toml configurations as you wish.\n\n.\n\n├── `__main__.py`\n\n├── configs\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── app.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── vban.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── basic\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── example.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── other_config.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── streaming_config.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── banana\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── example.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── other.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ...\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── potato\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── example.toml\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ...\n\n## Configs\n\n### app.toml\n\nConfigure certain startup states for the app.\n\n-   `configs`\n    Configure a user config to load on app startup. Don\'t include the .toml extension in the config name.\n\n-   `theme`\n    By default the app loads up the [Sun Valley light or dark theme](https://github.com/rdbende/Sun-Valley-ttk-theme) by @rdbende. You have the option to load up the app without any theme loaded. Simply set `enabled` to false and `mode` will take no effect.\n\n-   `extends`\n    Extending the app will show both strips and buses. In reduced mode only one or the other. This app will extend both horizontally and vertically, simply set `extends_horizontal` true or false accordingly.\n\n-   `channel`\n    For each channel labelframe the width and height may be adjusted which effects the spacing between widgets and the length of the scales and progressbars respectively.\n\n-   `mwscroll_step`\n    Sets the amount (in db) the gain slider moves with a single mousewheel step. Default 3.\n\n-   `submixes`\n    Select the default submix bus when Submix frame is shown. For example, a dedicated bus for OBS.\n\n### vban.toml\n\nConfigure as many vban connections as you wish. This allows the app to work over a LAN connection as well as with a local Voicemeeter installation.\n\nFor vban connections to work correctly VBAN TEXT incoming stream MUST be configured correctly on the remote machine. Both pcs ought to be connected to a local private network and should be able to ping one another.\n\nA valid `vban.toml` might look like this:\n\n```toml\n[connection-1]\nkind = \'banana\'\nip = \'192.168.1.2\'\nstreamname = \'worklaptop\'\nport = 6980\n\n[connection-2]\nkind = \'potato\'\nip = \'192.168.1.3\'\nstreamname = \'streampc\'\nport = 6990\n```\n\n### basic/ banana/ potato/\n\nThree example user configs are included with the package, one for each kind of Voicemeeter. Use these to configure parameter startup states. Any parameter supported by the underlying interfaces may be used. Check the \'multiple-parameters\' section for more info:\n\n[Python Interface for Voicemeeter API](https://github.com/onyx-and-iris/voicemeeter-api-python#multiple-parameters)\n\n[Python Interface for VBAN CMD](https://github.com/onyx-and-iris/vban-cmd-python#multiple-parameters)\n\nUser configs may be loaded at any time via the menu.\n\n## Special Thanks\n\n[Vincent Burel](https://github.com/vburel2018) for creating Voicemeeter, its SDK, the C Remote API, the RT Packet service and Streamer View app!\n\n[Rdbende](https://github.com/rdbende) for creating the beautiful Sun Valley Tkinter theme and adding it to Pypi!\n',
    'author': 'onyx-and-iris',
    'author_email': 'code@onyxandiris.online',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/onyx-and-iris/voicemeeter-compact',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
