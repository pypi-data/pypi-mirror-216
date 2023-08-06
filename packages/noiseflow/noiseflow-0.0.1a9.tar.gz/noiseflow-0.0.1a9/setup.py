# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noiseflow',
 'noiseflow.app',
 'noiseflow.cc',
 'noiseflow.cc.python',
 'noiseflow.client',
 'noiseflow.dispersion',
 'noiseflow.dvv',
 'noiseflow.real_time',
 'noiseflow.signal',
 'noiseflow.signal.python',
 'noiseflow.tests']

package_data = \
{'': ['*'],
 'noiseflow.cc': ['include/*', 'src/*'],
 'noiseflow.signal': ['include/*', 'src/*']}

install_requires = \
['faker>=18.11.2,<19.0.0',
 'h5py>=3.9.0,<4.0.0',
 'joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numba>=0.57.1,<0.58.0',
 'numpy>=1.24.0,<2.0.0',
 'obspy>=1.4.0,<2.0.0',
 'retry>=0.9.2,<0.10.0',
 'scipy>=1.11.0,<2.0.0',
 'setuptools>=58.0.4,<59.0.0',
 'stockwell>=1.1,<2.0',
 'tqdm>=4.65.0,<5.0.0',
 'tslearn>=0.5.3.2,<0.6.0.0']

setup_kwargs = {
    'name': 'noiseflow',
    'version': '0.0.1a9',
    'description': 'An ambient noise package',
    'long_description': '# NoiseFlow\n\n\n## Prerequisites\n\nNoiseFlow now supports `Clang` and `GCC` compiler in MacOS and Linux system separately, and all installation processes are under the `conda` environment, and we recommend to use miniconda. Make sure to install the following pre-packages before installing noiseflow:\n\n\nIf you use `Clang` in Mac, please install `OpenMP` via `brew` as following:\n\n```bash\nbrew install openmp\n```\n\nAnd use `pip` and `conda` to install the following packages:\n\n```bash\npip install joblib\n\nconda install -c conda-forge numpy scipy matplotlib \nconda install -c conda-forge obspy\nconda install -c conda-forge fftw (动态库)\nconda install -c conda-forge pybind11 (头文件)\nconda install -c conda-forge xtensor xsimd xtl xtensor-blas xtensor-python (可能是静态库)\nconda install -c conda-forge xtensor-fftw  #(usually failed at most time)  \n```\n\nThe `xtensor-fftw` and `KFR` need to be installed from source, first download them:\n\n\n```bash\ngit clone https://github.com/OUCyf/noiseflow.git\ncd noiseflow\ngit submodule init\ngit submodule update\n```\n\n\n\nNote the `xtensor-fftw` do not support M1 chip, and if it is failed to install via conda, you can install it from source into conda environment as `$CONDA_PREFIX`\n\n```bash\ncd ./extern/xtensor-fftw\nmkdir build && cd build\ncmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX\nmake install\n```\n\n\n\nThe `KFR` package is C++ DSP framework, should be installed in `./extern/kfr` from source\n\n```bash\ncd ./extern/kfr\nmkdir build && cd build\ncmake ..\nmake install\n```\n\n\n\n\n## Installation\n\nNow you can install `NoiseFlow`. If you use `MacOS`, please make sure to use Clang as the complier\n\n```bash\nexport CXX=clang++\n# unset CXX\npython setup.py install\n```\n\nIf you use `Linux`, please use GCC as the compiler\n\n```bash\nexport CXX=g++-13\npython setup.py install\n```\n\n\nIf you use `HPC` with `module` tool, you can use both Clang and GCC, for example using NOTS in Rice University.\n\n```bash\n# use gcc\nmodule load GCC/13.1.0\nexport CXX=g++\npython setup.py install\nINCLUDE_CMAKE_EXTENSION=1 pip install .\n\n# use clang\nmodule load GCCcore/11.2.0\nmodule load Clang/13.0.1\nexport CXX=clang++\npython setup.py install\n```\n\n```bash\nconda install -c conda-forge stockwell\n\nNOISEFLOW_USE_CPP=1 pip install --no-binary :all: noiseflow --no-cache-dir\n\ngit submodule add https://gitclone.com/github.com/kfrlib/kfr.git extern/kfr\n```\n\n\n\n##\nNoiseflow is dual-licensed, available under both commercial and apache license.\n\nIf you want to use noiseflow in a commercial product or a closed-source project, you need to purchase a Commercial License.\n',
    'author': 'Fu Yin',
    'author_email': 'oucyinfu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
