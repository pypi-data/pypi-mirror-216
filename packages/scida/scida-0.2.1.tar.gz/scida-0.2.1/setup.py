# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scida',
 'scida.configfiles',
 'scida.configfiles.units',
 'scida.customs',
 'scida.customs.arepo',
 'scida.customs.gizmo',
 'scida.customs.rockstar',
 'scida.interfaces',
 'scida.interfaces.mixins']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0',
 'dask[array,dataframe,distributed]>=2023,<2024',
 'distributed>=2023,<2024',
 'h5py>=3.7.0,<4.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'numba>=0.56,<0.57',
 'numpy>=1.21,<2.0',
 'pint>=0.22,<0.23',
 'pyyaml>=5.3.1',
 'requests>=2.31.0,<3.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'zarr>=v2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'scida',
    'version': '0.2.1',
    'description': 'Convenience wrapper around large scientific datasets to process with dask.',
    'long_description': '# scida\n\n![test status](https://github.com/cbyrohl/scida/actions/workflows/tests.yml/badge.svg)\n\nscida is an out-of-the-box analysis tool for large scientific datasets. It primarily supports the astrophysics community, focusing on cosmological and galaxy formation simulations using particles or unstructured meshes, as well as large observational datasets.\nThis tool uses dask, allowing analysis to scale up from your personal computer to HPC resources and the cloud.\n\n## Features\n\n- Unified, high-level interface to load and analyze large datasets from a variety of sources.\n- Parallel, task-based data processing with dask arrays.\n- Physical unit support via pint.\n- Easily extensible architecture.\n\n## Requirements\n\n- Python >= 3.9\n\n\n## Documentation\nThe documentation can be found [here](https://cbyrohl.github.io/scida/).\n\n## Install\n\n```\npip install scida\n```\n\n## First Steps\nAfter installing scida, follow the [tutorial](https://cbyrohl.github.io/scida/tutorial/).\n\n## License\n\nDistributed under the terms of the [MIT license](LICENSE),\n_scida_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue](https://github.com/cbyrohl/scida/issues/new) along with a detailed description.\n\n## Acknowledgements\n\nThe project structure was adapted from [Wolt](https://github.com/woltapp/wolt-python-package-cookiecutter) and [Hypermodern Python](https://github.com/cjolowicz/cookiecutter-hypermodern-python) cookiecutter templates.\n',
    'author': 'Chris Byrohl',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
