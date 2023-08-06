# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curcheck_manager',
 'curcheck_manager.templates.full.app',
 'curcheck_manager.templates.full.app.{{ cookiecutter.app_name }}',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name }}',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name }}.src',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name '
 '}}.src.apps',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name '
 '}}.src.apps.main',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name '
 '}}.src.core',
 'curcheck_manager.templates.full.project.{{ cookiecutter.project_name '
 '}}.src.core.models',
 'curcheck_manager.templates.mini.project.{{ cookiecutter.project_name }}',
 'curcheck_manager.templates.mini.project.{{ cookiecutter.project_name }}.src',
 'curcheck_manager.templates.mini.project.{{ cookiecutter.project_name '
 '}}.src.core',
 'curcheck_manager.templates.mini.project.{{ cookiecutter.project_name '
 '}}.src.core.models']

package_data = \
{'': ['*'],
 'curcheck_manager': ['templates/full/project/*', 'templates/mini/project/*']}

install_requires = \
['changecode>=0.0.1b',
 'click>=8.1.3',
 'cookiecutter>=2.1.1',
 'curcheck>=1.1.3b',
 'loguru>=0.6.0',
 'pydantic>=1.10.4']

entry_points = \
{'console_scripts': ['curcheckmanager = curcheck_manager.app:cli']}

setup_kwargs = {
    'name': 'curcheck-manager',
    'version': '1.0.0',
    'description': 'Managing curcheck projects',
    'long_description': '# Curcheck-manager\n___\n\n\nManager for curcheck library\n',
    'author': 'BulatXam',
    'author_email': 'Khamdbulat@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
