# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edsteva',
 'edsteva.io',
 'edsteva.io.synthetic',
 'edsteva.metrics',
 'edsteva.models',
 'edsteva.models.rectangle_function',
 'edsteva.models.rectangle_function.algos',
 'edsteva.models.rectangle_function.viz_configs',
 'edsteva.models.step_function',
 'edsteva.models.step_function.algos',
 'edsteva.models.step_function.viz_configs',
 'edsteva.probes',
 'edsteva.probes.biology',
 'edsteva.probes.biology.completeness_predictors',
 'edsteva.probes.biology.viz_configs',
 'edsteva.probes.biology.viz_configs.n_measurement',
 'edsteva.probes.biology.viz_configs.per_measurement',
 'edsteva.probes.biology.viz_configs.per_visit',
 'edsteva.probes.condition',
 'edsteva.probes.condition.completeness_predictors',
 'edsteva.probes.condition.viz_configs',
 'edsteva.probes.condition.viz_configs.n_condition',
 'edsteva.probes.condition.viz_configs.per_condition',
 'edsteva.probes.condition.viz_configs.per_visit',
 'edsteva.probes.note',
 'edsteva.probes.note.completeness_predictors',
 'edsteva.probes.note.viz_configs',
 'edsteva.probes.note.viz_configs.n_note',
 'edsteva.probes.note.viz_configs.per_note',
 'edsteva.probes.note.viz_configs.per_visit',
 'edsteva.probes.utils',
 'edsteva.probes.visit',
 'edsteva.probes.visit.completeness_predictors',
 'edsteva.probes.visit.viz_configs',
 'edsteva.probes.visit.viz_configs.n_visit',
 'edsteva.probes.visit.viz_configs.per_visit',
 'edsteva.utils',
 'edsteva.viz',
 'edsteva.viz.dashboards',
 'edsteva.viz.dashboards.normalized_probe',
 'edsteva.viz.dashboards.probe',
 'edsteva.viz.plots',
 'edsteva.viz.plots.estimates_densities',
 'edsteva.viz.plots.normalized_probe',
 'edsteva.viz.plots.probe']

package_data = \
{'': ['*']}

install_requires = \
['altair>=5.0,<6.0',
 'catalogue>=2.0.8,<3.0.0',
 'ipython>=7.31.0,<8.0.0',
 'koalas>=1.8.2,<2.0.0',
 'loguru==0.7.0',
 'numpy<1.20.0',
 'pandas>=1.3,<2.0',
 'pgpasslib>=1.1.0,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyarrow>=0.15,<0.17.0',
 'pyspark>=2.4.3,<2.5.0']

setup_kwargs = {
    'name': 'edsteva',
    'version': '0.2.0',
    'description': 'EDS-TeVa provides a set of tools that aims at modeling the adoption over time and across space of the Electronic Health Records.',
    'long_description': '<p align="center">\n<b>DISCLAIMER: </b>EDS-TeVa is intended to be a module of <a href="https://github.com/aphp/EDS-Scikit">EDS-Scikit</a>\n</p>\n\n<div align="center">\n\n<p align="center">\n  <a href="https://aphp.github.io/edsteva/latest/"><img src="https://aphp.github.io/edsteva/latest/assets/logo/edsteva_logo_small.svg" alt="EDS-TeVa"></a>\n</p>\n\n# EDS-TeVa [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aphp/edsteva/HEAD?labpath=notebooks%2Fsynthetic_data.ipynb)\n\n<p align="center">\n<a href="https://aphp.github.io/edsteva/latest/" target="_blank">\n    <img src="https://img.shields.io/github/actions/workflow/status/aphp/edsteva/documentation.yaml?branch=main&label=docs&style=flat" alt="Documentation">\n</a>\n<a href="https://pypi.org/project/edsteva/" target="_blank">\n    <img src="https://img.shields.io/pypi/v/edsteva?color=blue&style=flat" alt="PyPI">\n</a>\n<a href="https://codecov.io/github/aphp/edsteva?branch=main" target="_blank">\n    <img src="https://codecov.io/github/aphp/edsteva/coverage.svg?branch=main" alt="Codecov">\n</a>\n<a href="https://github.com/psf/black" target="_blank">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">\n</a>\n<a href="https://python-poetry.org/" target="_blank">\n    <img src="https://img.shields.io/badge/reproducibility-poetry-blue" alt="Poetry">\n</a>\n<a href="https://www.python.org/" target="_blank">\n    <img src="https://img.shields.io/badge/python-~3.7.1-brightgreen" alt="Supported Python versions">\n</a>\n</p>\n</div>\n\n**Documentation**: <a href="https://aphp.github.io/edsteva/latest/" target="_blank">https://aphp.github.io/edsteva/latest/</a>\n\n**Source Code**: <a href="https://github.com/aphp/edsteva" target="_blank">https://github.com/aphp/edsteva</a>\n\n---\n\nEDS-TeVa provides a set of tools that aims at modeling the adoption over time and across space of the Electronic Health Records.\n\n## Requirements\nEDS-TeVa stands on the shoulders of [Spark 2.4](https://spark.apache.org/docs/2.4.8/index.html) which requires:\n\n- Python ~3.7.1\n- Java 8\n\n## Installation\n\nYou can install EDS-TeVa through ``pip``:\n\n```shell\npip install edsteva\n```\nWe recommend pinning the library version in your projects, or use a strict package manager like [Poetry](https://python-poetry.org/).\n\n```\npip install edsteva==0.2.0\n```\n## Example\n\nA scientific paper is currently being written that describes extensively the use of the library on the study of pulmonary embolism of cancer patients.\n\n## Contributing\n\nContributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.\n\n## Acknowledgement\n\nWe would like to thank [Assistance Publique – Hôpitaux de Paris](https://www.aphp.fr/) and [AP-HP Foundation](https://fondationrechercheaphp.fr/) for funding this project.\n',
    'author': 'Adam Remaki',
    'author_email': 'adam.remaki@aphp.fr',
    'maintainer': 'Adam Remaki',
    'maintainer_email': 'adam.remaki@aphp.fr',
    'url': 'https://github.com/aphp/edsteva',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.8.0',
}


setup(**setup_kwargs)
