from setuptools import find_packages, setup

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
}

if __name__ == "__main__":
    setup(**setup_info)
