# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reps',
 'reps.templates.base.hooks',
 'reps.templates.base.{{cookiecutter.__project_slug}}.docs',
 'reps.templates.python.hooks',
 'reps.templates.python.{{cookiecutter.__project_slug}}.taskcluster.scripts',
 'reps.templates.python.{{cookiecutter.__project_slug}}.test']

package_data = \
{'': ['*'],
 'reps': ['templates/base/*',
          'templates/base/{{cookiecutter.__project_slug}}/*',
          'templates/base/{{cookiecutter.__project_slug}}/.github/*',
          'templates/base/{{cookiecutter.__project_slug}}/.github/workflows/*',
          'templates/python/*',
          'templates/python/{{cookiecutter.__project_slug}}/*',
          'templates/python/{{cookiecutter.__project_slug}}/taskcluster/ci/*',
          'templates/python/{{cookiecutter.__project_slug}}/taskcluster/ci/codecov/*',
          'templates/python/{{cookiecutter.__project_slug}}/taskcluster/ci/docker-image/*',
          'templates/python/{{cookiecutter.__project_slug}}/taskcluster/ci/fetch/*',
          'templates/python/{{cookiecutter.__project_slug}}/taskcluster/ci/test/*'],
 'reps.templates.base.{{cookiecutter.__project_slug}}.docs': ['concepts/*',
                                                              'howto/*',
                                                              'reference/*',
                                                              'tutorials/*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'pre-commit>=3.3.3,<4.0.0',
 'pyyaml>=6.0,<7.0',
 'taskcluster-taskgraph>=5.4.0,<6.0.0']

entry_points = \
{'console_scripts': ['reps-new = reps.console:run']}

setup_kwargs = {
    'name': 'reps-new',
    'version': '0.1.0',
    'description': 'Mozilla Release Engineering Project Standard',
    'long_description': '# Release Engineering Project Standard\n\nThis repository:\n\n1. Defines the standard tools and workflows that Mozilla Release Engineering\n   endeavours to use across its projects.\n2. Implements a `reps` binary that can be used to bootstrap new projects based\n   on the defined standard.\n\n## Usage\n\nThe `reps` tool can be used to bootstrap new projects that conform to this\nstandard. It is recommended to install and run it with\n[pipx](https://github.com/pypa/pipx) (so the most up to date version is always\nused):\n\n```bash\npipx run reps-new\n```\n\nand fill out the prompts. By default, the `python` project template is used.\nYou may optionally specify a different template to use with the `-t/--template` flag:\n\n```bash\npipx run reps-new -t base\n```\n\nAvailable templates can be found in the\n[templates directory](https://github.com/mozilla-releng/reps/tree/main/src/reps/templates).\n',
    'author': 'Mozilla Release Engineering',
    'author_email': 'release@mozilla.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
