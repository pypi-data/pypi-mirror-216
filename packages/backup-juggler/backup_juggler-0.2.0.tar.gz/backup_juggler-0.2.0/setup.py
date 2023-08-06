# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backup_juggler']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.4.2,<14.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.65.0,<5.0.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['bj = backup_juggler.juggler_cli:app']}

setup_kwargs = {
    'name': 'backup-juggler',
    'version': '0.2.0',
    'description': 'Multiple copies of files and directories simultaneously made easy',
    'long_description': "# Backup Juggler: Multiple copies of files and directories simultaneously made easy\n[![Stable Version](https://img.shields.io/pypi/v/backup-juggler?label=stable)][PyPI Releases]\n[![Python Versions](https://img.shields.io/pypi/pyversions/backup-juggler)][PyPI]\n[![Download Stats](https://img.shields.io/pypi/dm/backup-juggler)](https://pypistats.org/packages/backup-juggler)\n\nBackup Juggler is a command-line tool that allows you to perform multiple copies of files and directories simultaneously. The whole application is based on a command called `bj`. This command has a subcommand related to each action that the application can perform. Like `do-backups` and `get-size`.\n\n## Installation\nTo install the Backup Juggler CLI, we recommend that you use `pipx`, although this is just a recommendation! You can also install the project with the manager of your choice, like `pip`. For full instalation instructions see the [instalation documentation][Tutorial]\n\n## Documentation\nThe goal of this project is to help users who need to make multiple copies of files and directories simultaneously. See the [quick start guide][Documentation] or for full instructions of the current version of Backup Juggler see the [tutorial documentation][Tutorial].\n\n## Contribute\nThe full [contributing documentation][Contributing Documentation] provides useful guidance, but if you have any questions or need help during the contribution process, feel free to open an [issue on the project's GitHub repository][Issue Tracker] and ask for help. We're happy to assist you.\n\n## Resources\n\n- [Releases][PyPI Releases]\n- [Documentation]\n- [Issue Tracker]\n\n  [PyPI]: https://pypi.org/project/backup-juggler/\n  [PyPI Releases]: https://pypi.org/project/backup-juggler/#history\n  [Documentation]: https://backup-juggler.readthedocs.io/en/latest/\n  [Tutorial]: https://backup-juggler.readthedocs.io/en/latest/tutorial/\n  [Issue Tracker]: https://github.com/Raulin0/backup-juggler/issues\n  [Contributing Documentation]: https://backup-juggler.readthedocs.io/en/latest/contribute/",
    'author': 'Marcos Raulino',
    'author_email': 'marcosfsraulino@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
