# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryton_worker',
 'cryton_worker.etc',
 'cryton_worker.lib',
 'cryton_worker.lib.triggers',
 'cryton_worker.lib.util']

package_data = \
{'': ['*'], 'cryton_worker.etc': ['systemd-service/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'amqpstorm>=2.10.4,<3.0.0',
 'bottle>=0.12.19,<0.13.0',
 'click>=8.1.2,<9.0.0',
 'paramiko>=3.0.0,<4.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pymetasploit3>=1.0.3,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'schema>=0.7.5,<0.8.0',
 'structlog>=22.3.0,<23.0.0',
 'utinni-fork>=0.5.1,<0.6.0']

entry_points = \
{'console_scripts': ['cryton-worker = cryton_worker.lib.cli:cli']}

setup_kwargs = {
    'name': 'cryton-worker',
    'version': '1.0.1',
    'description': 'Attack scenario orchestrator for Cryton',
    'long_description': '![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-worker/badges/master/coverage.svg)\n\n[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)\n\n# Cryton Worker\nCryton Worker is used for executing attack modules remotely. It utilizes [RabbitMQ](https://www.rabbitmq.com/) \nas its asynchronous remote procedures call protocol. It connects to the Rabbit MQ server and consumes messages from \nthe Core component or any other app that implements its RabbitMQ API.\n\nCryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only \nthe latest version is supported** and issues regarding different OS or distributions may **not** be resolved.\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/worker/).\n\n## Quick-start\nTo be able to execute attack scenarios, you also need to install **[Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core)**.  \nModules provided by Cryton can be found [here](https://gitlab.ics.muni.cz/cryton/cryton-modules). **Their installation will\nbe covered in this section**.\n\nMake sure Git, Docker, and Docker Compose plugin are installed:\n- [Git](https://git-scm.com/)\n- [Docker Compose](https://docs.docker.com/compose/install/)\n\nOptionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).\n\nThe following script clones the Worker repository and runs the Docker Compose configuration which starts \nthe Worker (with preinstalled modules), and its prerequisites (Metasploit and Empire framework).\n```shell\ngit clone https://gitlab.ics.muni.cz/cryton/cryton-worker.git\ncd cryton-worker\ndocker compose up -d\n```\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/worker/).\n\n## Contributing\nContributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-worker)** on gitlab.com.\nFor more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).\n',
    'author': 'Ivo Nutár',
    'author_email': 'nutar@ics.muni.cz',
    'maintainer': 'Jiří Rája',
    'maintainer_email': 'raja@ics.muni.cz',
    'url': 'https://gitlab.ics.muni.cz/cryton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
