import os
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys


class CMakeExtension(Extension):
    def __init__(self, name, cmakelists_dir=".", **kwargs):
        super().__init__(name, sources=[], **kwargs)
        self.cmakelists_dir = os.path.abspath(cmakelists_dir)

class CmakeBuild(build_ext):
    def build_extensions(self) -> None:
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cmake not found!')

        for ext in self.extensions:
            os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
            build_type = 'Debug' if os.environ.get('DEBUG', 'OFF') == 'ON' else 'Release'

            cmake_args = [
                    '-DCMAKE_BUILD_TYPE = %s'%build_type,
                    '-DCMAKE_EXPORT_COMPILE_COMMANDS=1',
                    '-DPYTHON_EXECUTABLE={}'.format(sys.executable)
                    ]

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config
            subprocess.check_call(['cmake', ext.cmakelists_dir] + cmake_args, cwd=self.build_temp)

            # Build
            subprocess.check_call(['cmake', '--build', '.', '--config', build_type], cwd=self.build_temp)



with open("VERSION", "r") as f:
    version = f.read().strip()

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()

setup_info = {
    "name": "lmptools",
    "packages": find_packages(exclude=["tests"]),
    "version": version,
    "maintainer": "Venkat Bala",
    "url": "https://github.com/venkatBala/lmptools",
    "license": "MIT License",
    "author": "Venkat Bala",
    "author_email": "balavk89@gmail.com",
    "description": """lmptools is python module to facilitate post
        processing of LAMMPS simulation output files""",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "zip_safe": False,
    "install_requires": required,
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Adaptive Technologies",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
    ],
    "ext_modules":[CMakeExtension(name='lmptools_')],
    "cmdclass":{'build_ext': CmakeBuild}
}

if __name__ == "__main__":
    setup(**setup_info)
