# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_fetcher_ops',
 'dbnomics_fetcher_ops.commands',
 'dbnomics_fetcher_ops.model',
 'dbnomics_fetcher_ops.model.fetcher_metadata',
 'dbnomics_fetcher_ops.model.pipeline_repo',
 'dbnomics_fetcher_ops.services']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'daiquiri>=3.0.1,<4.0.0',
 'dbnomics-solr>=1.1.13,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-gitlab>=3.11.0,<4.0.0',
 'requests>=2.24.0,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'validators>=0.20.0,<0.21.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['dbnomics-fetchers = dbnomics_fetcher_ops.cli:app']}

setup_kwargs = {
    'name': 'dbnomics-fetcher-ops',
    'version': '0.6.1',
    'description': 'Manage DBnomics fetchers',
    'long_description': '# DBnomics fetcher ops\n\nManage DBnomics fetchers: list, configure and run pipelines.\n\n## Install\n\n```bash\npip install dbnomics-fetcher-ops[cli]\n```\n\n## Usage\n\n### Configure a fetcher\n\nThe configure command needs write privileges. Create a GitLab [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) having the `api` scope, and pass it using the `--gitlab-private-token` option or the `GITLAB_PRIVATE_TOKEN` environment variable in `~/.config/dbnomics/dbnomics-fetchers.env`.\n\n```bash\ndbnomics-fetchers -v configure scsmich --dry-run\n# If everything seems OK, remove the --dry-run flag:\ndbnomics-fetchers -v configure scsmich\n```\n\n### List fetchers\n\n```bash\ndbnomics-fetchers -v list\n```\n\n### Run fetcher pipelines\n\n```bash\n# Replace PROVIDER_SLUG by the real value:\ndbnomics-fetchers -v run --provider-slug PROVIDER_SLUG\n\n# To run a pipeline for each fetcher:\ndbnomics-fetchers -v list --slug | xargs -I {} dbnomics-fetchers -v run --provider-slug {}\n```\n\n## Development\n\nInstall [Poetry](https://python-poetry.org/).\n\n```bash\n# git clone repo or fork\ncd dbnomics-fetcher-ops\npoetry install\ncp .env.example .env\n```\n\nRun commands with:\n\n```bash\npoetry shell\ndbnomics-fetchers COMMAND\n```\n',
    'author': 'Christophe Benz',
    'author_email': 'christophe.benz@nomics.world',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
