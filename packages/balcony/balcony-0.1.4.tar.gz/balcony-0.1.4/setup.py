# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['balcony', 'balcony.custom_nodes', 'balcony.terraform_import']

package_data = \
{'': ['*'], 'balcony': ['custom_tf_import_configs/*', 'custom_yamls/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'boto3>=1.24.80,<2.0.0',
 'inflect>=6.0.0,<7.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'mkdocs-autorefs>=0.4.1,<0.5.0',
 'mkdocs-material>=8.5.7,<10.0.0',
 'mkdocstrings[python]>=0.21.2,<0.22.0',
 'pydantic>=1.10.7,<2.0.0',
 'rich>=13.3.4,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['balcony = balcony.cli:run_app']}

setup_kwargs = {
    'name': 'balcony',
    'version': '0.1.4',
    'description': 'Read any resource in your AWS Account. You can generate terraform code for them, too.',
    'long_description': '# balcony\n\n\n<div style="display: flex;">\n  <a href="https://github.com/oguzhan-yilmaz/balcony/actions/workflows/docker-publish.yml"><img src="https://github.com/oguzhan-yilmaz/balcony/actions/workflows/docker-publish.yml/badge.svg" alt="Build and publish a Docker image to ghcr.io"></a>\n  <span style="width: 5px"></span>\n\n<a href="https://github.com/oguzhan-yilmaz/balcony/actions/workflows/pages/pages-build-deployment"><img src="https://github.com/oguzhan-yilmaz/balcony/actions/workflows/pages/pages-build-deployment/badge.svg" alt="Build and Deploy Documentation website"></a>\n</div>\n\n\n\nbalcony dynamically parses AWS SDK(`boto3` library) and analyzes required parameters for each operation. \n\nBy **establishing relations between operations over required parameters**, it\'s **able to auto-fill** them by reading the related operation beforehand.\n\nBy simply entering their name, balcony enables developers to easily list their AWS resources.\n\n\n## Installation & Documentation \n\n**[https://oguzhan-yilmaz.github.io/balcony/](https://oguzhan-yilmaz.github.io/balcony/quickstart)**\n\nBalcony\'s documentation website contains quickstart guide, usage cookbook and more.\n\n\n\n\n\n## Features & GIFs\n> click to play the videos\n### List Resource Nodes of an AWS Service \n`balcony aws <service-name>` to see every Resource Node of a service.\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/resource-node-list.gif)\n\n\n### Reading a Resource Node \n`balcony aws <service-name> <resource-node>` to read operations of a Resource Node.\n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/reading-a-resource-node.gif)\n\n\n### Documentation and Input & Output of Operations\nUse the `--list`, `-l` flag to print the given AWS API Operations documentation, input & output structure. \n \n\n![](https://github.com/oguzhan-yilmaz/balcony/blob/main/docs/visuals/list-option.gif)\n',
    'author': 'Oguzhan Yilmaz',
    'author_email': 'oguzhanylmz271@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
