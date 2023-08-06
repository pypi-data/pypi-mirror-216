# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryton_core',
 'cryton_core.cryton_app',
 'cryton_core.cryton_app.management',
 'cryton_core.cryton_app.management.commands',
 'cryton_core.cryton_app.migrations',
 'cryton_core.cryton_app.views',
 'cryton_core.etc',
 'cryton_core.lib',
 'cryton_core.lib.models',
 'cryton_core.lib.services',
 'cryton_core.lib.triggers',
 'cryton_core.lib.util']

package_data = \
{'': ['*'],
 'cryton_core': ['static/admin/css/*',
                 'static/admin/css/vendor/select2/*',
                 'static/admin/fonts/*',
                 'static/admin/img/*',
                 'static/admin/img/gis/*',
                 'static/admin/js/*',
                 'static/admin/js/admin/*',
                 'static/admin/js/vendor/jquery/*',
                 'static/admin/js/vendor/select2/*',
                 'static/admin/js/vendor/select2/i18n/*',
                 'static/admin/js/vendor/xregexp/*',
                 'static/drf_spectacular_sidecar/redoc/bundles/*',
                 'static/drf_spectacular_sidecar/swagger-ui-dist/*',
                 'static/rest_framework/css/*',
                 'static/rest_framework/docs/css/*',
                 'static/rest_framework/docs/img/*',
                 'static/rest_framework/docs/js/*',
                 'static/rest_framework/fonts/*',
                 'static/rest_framework/img/*',
                 'static/rest_framework/js/*']}

install_requires = \
['AMQPStorm>=2.10.4,<3.0.0',
 'APScheduler>=3.8.1,<4.0.0',
 'Django>=4.0.1,<5.0.0',
 'Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.29,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'django-cors-headers>=3.13.0,<4.0.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'drf-spectacular-sidecar>=2023.3.1,<2024.0.0',
 'drf-spectacular>=0.26.0,<0.27.0',
 'gunicorn>=20.1.0,<21.0.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'pytz>=2022.7,<2023.0',
 'rpyc>=5.3.0,<6.0.0',
 'schema>=0.7.5,<0.8.0',
 'structlog>=22.3.0,<23.0.0',
 'tzlocal>=4.1,<5.0',
 'uuid>=1.30,<2.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['cryton-core = cryton_core.manage:main']}

setup_kwargs = {
    'name': 'cryton-core',
    'version': '1.0.2',
    'description': 'Advanced scheduler for attack scenarios',
    'long_description': '![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-core/badges/master/coverage.svg)\n\n[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)\n\n# Cryton Core\nCryton Core is the center point of the Cryton toolset. It is used for:\n- Creating, planning, and scheduling attack scenarios\n- Generating reports from attack scenarios\n- Controlling Workers and scenarios execution\n\nCryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only \nthe latest version is supported** and issues regarding different OS or distributions may **not** be resolved.\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/core/).\n\n## Quick-start\nTo be able to execute attack scenarios, you also need to install **[Cryton Worker](https://gitlab.ics.muni.cz/cryton/cryton-worker)** \nand **[Cryton CLI](https://gitlab.ics.muni.cz/cryton/cryton-cli)** packages.  \nOptionally you can install [Cryton Frontend](https://gitlab.ics.muni.cz/cryton/cryton-frontend) for a non-command line experience.\n\nMake sure Git, Docker, and Docker Compose plugin are installed:\n- [Git](https://git-scm.com/)\n- [Docker Compose](https://docs.docker.com/compose/install/)\n\nOptionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).\n\nThe following script clones the repository and runs the Docker Compose configuration. The compose file contains the necessary prerequisites\n(Postgres, PgBouncer, RabbitMQ), Cryton Core itself (listener and REST API), and a proxy that allows access to the Cryton Core\'s REST API\nat http://0.0.0.0:8000/.\n```shell\ngit clone https://gitlab.ics.muni.cz/cryton/cryton-core.git\ncd cryton-core\nsed -i "s|CRYTON_CORE_RABBIT_HOST=127.0.0.1|CRYTON_CORE_RABBIT_HOST=cryton-rabbit|" .env\nsed -i "s|CRYTON_CORE_DB_HOST=127.0.0.1|CRYTON_CORE_DB_HOST=cryton-pgbouncer|" .env\nsed -i "s|CRYTON_CORE_API_USE_STATIC_FILES=false|CRYTON_CORE_API_USE_STATIC_FILES=true|" .env\ndocker compose up -d\n```\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/core/).\n\n## Contributing\nContributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-core)** on gitlab.com.\nFor more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).\n',
    'author': 'Ivo Nutár',
    'author_email': 'nutar@ics.muni.cz',
    'maintainer': 'Jiří Rája',
    'maintainer_email': 'raja@ics.muni.cz',
    'url': 'https://gitlab.ics.muni.cz/cryton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
