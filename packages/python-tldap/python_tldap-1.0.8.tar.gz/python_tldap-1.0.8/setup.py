# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tldap',
 'tldap.backend',
 'tldap.database',
 'tldap.django',
 'tldap.django.migrations',
 'tldap.test']

package_data = \
{'': ['*'], 'tldap.test': ['ldap_schemas/*']}

install_requires = \
['ldap3', 'passlib', 'pip', 'pyasn1', 'six']

extras_require = \
{'docs': ['django', 'sphinx', 'furo']}

setup_kwargs = {
    'name': 'python-tldap',
    'version': '1.0.8',
    'description': 'High level python LDAP Library',
    'long_description': 'python-tldap\n============\nTLDAP is a high level LDAP library for Python that uses Ecto like models\nto define LDAP schemas that can then be used in an easy way from Python code.\nIt also supports fake LDAP transactions, to try and ensure LDAP database\nremains in a consistent state, even if there are errors that cause the\ntransaction to fail.\n\nDocumentation can be found at http://python-tldap.readthedocs.org/\n',
    'author': 'Brian May',
    'author_email': 'brian@linuxpenguins.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Karaage-Cluster/python-tldap/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
