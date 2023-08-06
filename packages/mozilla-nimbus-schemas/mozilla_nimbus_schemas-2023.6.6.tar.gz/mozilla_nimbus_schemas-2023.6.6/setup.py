# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozilla_nimbus_schemas',
 'mozilla_nimbus_schemas.jetstream',
 'mozilla_nimbus_schemas.tests.jetstream']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'mozilla-nimbus-schemas',
    'version': '2023.6.6',
    'description': 'Schemas used by Mozilla Nimbus and related projects.',
    'long_description': '# Nimbus Schemas\n\nThis directory contains a published package of schemas used by different parts of the Mozilla Nimbus experimentation ecosystem.\n\n## Versioning\n`mozilla-nimbus-schemas` uses a date-based versioning scheme. The format is `yyyy.m.#`, where `m` is the non-zero-padded month, and `#` is an incrementing number starting from 1 for each month. For example, the second release in June of 2023 would have a version of `2023.6.2`.\n\n## Installation/Usage\n### Prerequisites\n- python ^3.10\n- poetry ^1.2.2\n\nFrom project root (i.e., parent to this directory)\n- Install: `make schemas_install`\n- Run linting and tests: `make schemas_check`\n- Code formatting: `make schemas_code_format`\n\n## Schemas\n### Jetstream\n\nContains schemas describing analysis results, metadata, and errors from [Jetstream](https://github.com/mozilla/jetstream).\n',
    'author': 'mikewilli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
