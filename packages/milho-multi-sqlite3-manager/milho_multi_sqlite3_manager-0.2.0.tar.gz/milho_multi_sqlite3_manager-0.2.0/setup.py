# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multisqlite3manager', 'multisqlite3manager.tests']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.2,<3.0.0', 'sqlalchemy>=2.0.16,<3.0.0', 'sqlglot>=16.3.1,<17.0.0']

setup_kwargs = {
    'name': 'milho-multi-sqlite3-manager',
    'version': '0.2.0',
    'description': '',
    'long_description': '# milho-multi-sqlite3-manager\n\n## Description\n\nThe idea is to have an environment with multiple SQLITE3 files, aiming at ease of access and use.\nThe inspiration for creating this module came from the ease of working with Spark in BigData environments where, generally, everything is integrated, without the need to make several explicit connections in the code.\n\nIf you want an integrated environment on your machine, create an environment variable called "MULTISQLITE3MANAGER_FOLDER_PATH" with the directory of your folder. You will need to make sure that all files in this folder are SQLITE3 databases.\n\nWhen "to_dataframe" is used, the result is a Pandas DataFrame. The query is previously parsed to map all the databases used in the SQL. Then the module create a sqlalchemy connection and attach that databases to the connection. After that, the query is executed and the result is a Pandas DataFrame. \n\n## Code Samples\n\n```python\n\nfrom multisqlite3manager import print_databases, print_tables, to_dataframe\n\nprint_databases()\nprint_tables("DB_NAME")\n\ndf = to_dataframe("SELECT * FROM db_1.tMisto")\ndf2 = to_dataframe("SELECT * FROM db_2_copy.tMisto")\n\n```\n',
    'author': 'Guilherme S. Magalhães',
    'author_email': '40049979+Guisilcol@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
