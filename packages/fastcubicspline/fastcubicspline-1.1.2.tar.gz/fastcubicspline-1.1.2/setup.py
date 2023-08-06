# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastcubicspline']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.3,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'fastcubicspline',
    'version': '1.1.2',
    'description': 'A fast cubic spline interpolator for real and complex data.',
    'long_description': '# fastcubicspline\na fast cubic spline interpolator for equally spaced values and complex data\n\n# Why not using scipy\'s Cubic Spline?\n\nThere are two reasons why fcSpline should be used instead \nof [scipy.interpolate.CubicSpline](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html#scipy.interpolate.CubicSpline).\n\n1) When called in a loop, fcSpline it 3 to 5 time faster than CubicSpline (see `fcs_timing.py`).\n2) Natively handles complex data.\n\nWhat are the drawbacks? Well, fcSpline works on equally spaced data only.\n\n# Example\n\n```python\nfrom fastcubicspline import FCS\n# set up x-limits\nx_low = 1\nx_high = 5\n\n# set up the y-data, here complex values\ny_data = [9+9j, 4+4j, 0, 6+6j, 2+2j]\n\n# class init\nfcs = FCS(x_low, x_high, y_data)\n\n# simply call the FCS-object like a regular function\n# to get interpolated values\nprint(fcs(2.5))\n# (0.921875+0.921875j)\n```\n\n# Install\n\n`fastcubicspline` is on PyPi. So you can simply install the latest release with\n\n    pip install fastcubicspline\n\n## From Source\n\nFetch the latest version (or check any previous stage) \nby cloning from https://github.com/cimatosa/fcSpline.\n\n### pip\n\nMake sure [pip](https://pip.pypa.io/en/stable/installation/) is installed.\nChange into the fcSpline package directory and run:\n\n    python -m pip install .\n\nSee the option `--user` if you don\'t have the appropriate permission\nfor an installation to the standard location.\n\n### poetry\n\nChange into the fcSpline package directory.\nInstall `fastcubicspline` and its dependencies into a virtual environment with\n\n    poetry install\n\nand spawn a shell using that environment `poetry shell`.\nNow you can check if the tests pass with `pytest`.\n`poetry install` should build the cython extension which you cen check with `pytest -v -k cython`. \n\nIn case of poetry errors, you might want to get the latest poetry version\nwith `poetry self update`.\n\n### Manually Build Cython Extension\n\nSome distutils magic is contained in `build_ext.py` so you can simply call\n\n    python3 build_ext.py\n\nto build the Cython extension inplace.\nRun `pytest -v -k cython` to verify that the Cython extension is available.\n\nClean the build files by calling\n\n    python3 build_ext.py clean\n\n\n# Testing\n\nRun and list all tests with\n\n    pytest -v\n\n\n\n### MIT licence\nCopyright (c) 2023 Richard Hartmann\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n',
    'author': 'Richard Hartmann',
    'author_email': 'richard.hartmann@tu-dresden.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cimatosa/fcSpline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}
from build_ext import *
build(setup_kwargs)

setup(**setup_kwargs)
