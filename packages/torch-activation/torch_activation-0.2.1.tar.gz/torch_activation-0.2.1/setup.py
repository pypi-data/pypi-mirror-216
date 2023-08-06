# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_activation']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.0.0']

setup_kwargs = {
    'name': 'torch-activation',
    'version': '0.2.1',
    'description': 'A library of new activation function implement in PyTorch to save time in experiment and have fun',
    'long_description': "# PyTorch Activations\n\nPyTorch Activations is a collection of activation functions for the PyTorch library. This project aims to provide an easy-to-use solution for experimenting with different activation functions or simply adding variety to your models.\n\n\n## Installation\n\nYou can install PyTorch Activations using pip:\n\n```bash\n$ pip install torch-activation\n```\n\n## Usage\n\nTo use the activation functions, import them from torch_activation. Here's an example:\n\n```python\nimport torch_activation as tac\n\nm = tac.ShiLU(inplace=True)\nx = torch.rand(16, 3, 384, 384)\nm(x)\n```\n\nOr in `nn.Sequential`:\n\n```python\nimport torch\nimport torch.nn as nn\nimport torch_activation as tac\n\nclass Net(nn.Module):\n    def __init__(self):\n        super(Net, self).__init__()\n        self.net = nn.Sequential(\n            nn.Conv2d(64, 32, 2),\n            tac.DELU(),\n            nn.ConvTranspose2d(32, 64, 2),\n            tac.ReLU(inplace=True),\n        )\n\n    def forward(self, x):\n        return self.net(x)\n```\n\nActivation functions can be imported directly from the package, such as `torch_activation.CoLU`, or from submodules, such as `torch_activation.non_linear.CoLU`.\n\nFor a comprehensive list of available functions, please refer to the [LIST_OF_FUNCTION](LIST_OF_FUNCTION.md) file.\n\nTo learn more about usage, please refer to [Documentation](https://torch-activation.readthedocs.io)\n\nWe hope you find PyTorch Activations useful for your experimentation and model development. Enjoy exploring different activation functions!\n\n## Contact\n\nAlan Huynh - [LinkedIn](https://www.linkedin.com/in/alan-huynh-64b357194/) - [hdmquan@outlook.com](mailto:hdmquan@outlook.com)\n\nProject Link: [https://github.com/alan191006/torch_activation](https://github.com/alan191006/torch_activation)\n\nDocumentation Link: [https://torch-activation.readthedocs.io](https://torch-activation.readthedocs.io)\n\nPyPI Link: [https://pypi.org/project/torch-activation/](https://pypi.org/project/torch-activation/)\n\n",
    'author': 'Alan Huynh',
    'author_email': 'hdmquan@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
