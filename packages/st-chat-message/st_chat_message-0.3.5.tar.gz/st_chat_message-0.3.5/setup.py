# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['st_chat_message']

package_data = \
{'': ['*'],
 'st_chat_message': ['frontend/out/*',
                     'frontend/out/_next/static/Dg5cdAEY-RCHv3LVfP7Lo/*',
                     'frontend/out/_next/static/chunks/*',
                     'frontend/out/_next/static/chunks/pages/*',
                     'frontend/out/_next/static/css/*',
                     'frontend/out/_next/static/media/*']}

install_requires = \
['streamlit>=0.63']

setup_kwargs = {
    'name': 'st-chat-message',
    'version': '0.3.5',
    'description': 'A Streamlit component to display chat messages',
    'long_description': '# st-chat-message\n\n## Description\n\nThis is a simple chat message component for streamlit. It is based on the [streamlit-chat](https://github.com/AI-Yash/st-chat) component, trying to be as compatible as possible, but it adding a few features:\n\n- Markdown support\n- LaTeX support\n- Tables\n\n## Installation\n\n```bash\npip install st-chat-message\n```\n\nor\n\n```bash\npoetry add st-chat-message\n```\n## Usage\n\n```python\nimport streamlit as st\nfrom st_chat_message import message\n\nmessage("Hello world!", is_user=True)\nmessage("Hi")\n```\n\n![img.png](docs/img.png)\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Manolo Santos',
    'author_email': 'manolo.santos@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
