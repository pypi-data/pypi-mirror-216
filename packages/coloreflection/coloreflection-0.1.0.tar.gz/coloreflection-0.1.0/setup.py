# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coloreflection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coloreflection',
    'version': '0.1.0',
    'description': 'Module for using colors for the terminal, based on reflection',
    'long_description': '![Coloreflection icon](https://github.com/Addefan/coloreflection/blob/main/images/logo.png?raw=true)\n\n# Coloreflection\n\nA tool with which you can use colors in your Python code to decorate terminal output.\n\n## Install\n\n```shell\npip install coloreflection\n```\n\nor,\n\n```shell\npoetry add coloreflection\n```\n\n## Capabilities\n\n### Dark PyCharm theme\n\n![Styles with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/styles_dark.png?raw=true)\n![Foreground colors with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/foreground_dark.png?raw=true)\n![Background colors with dark PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/background_dark.png?raw=true)\n\n### Light PyCharm theme\n\n![Styles with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/styles_light.png?raw=true)\n![Foreground colors with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/foreground_light.png?raw=true)\n![Background colors with light PyCharm theme](https://github.com/Addefan/coloreflection/blob/main/images/background_light.png?raw=true)\n\n## Usage\n\n```python\nfrom coloreflection import Color\n\nC = Color()\n\nprint(C.border(" Using style for text "))\nprint(C.FG.red("Changing text color"))\nprint(C.BG.green("Changing text background"))\n\nprint(C.border(C.bold(C.FG.pink("You can"))), "combine", \n      C.BG.blue(C.FG.yellow(f"different colors{C.reverse(\' and styles.\')}")))\n```\n![Usage examples](https://github.com/Addefan/coloreflection/blob/main/images/usage.png?raw=true)\n',
    'author': 'Vitaly Zorin',
    'author_email': 'addefan@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Addefan/coloreflection',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
