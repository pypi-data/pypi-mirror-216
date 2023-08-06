# Auteur : Esteban COLLARD, Nordine EL AMMARI
# Modifications : Reda ID TALEB & Manal LAGHMICH

from setuptools import setup
import os.path

import thonnycontrib
thonnycontrib_path = os.path.dirname(os.path.abspath(thonnycontrib.__file__))

def get_packages_under_thonnycontrib(directory:str, module_name:str):
    packages = []
    for root, dirs, files in os.walk(directory):
        if "__init__.py" in files:
            splitted: list[str] = root.split(os.sep)
            try:
                index = splitted.index(module_name)
                sub_module = ".".join(splitted[index:])
                packages.append(sub_module)
            except:pass
    return packages

packages = get_packages_under_thonnycontrib(thonnycontrib_path, thonnycontrib.__name__)

def get_packages_data(packages: list[str]=packages):
    py_packs = dict([(p, ["*.py"]) for p in packages if not p.endswith("docs")])
    other_packs = dict([(p, ["res/*"]) for p in packages if p.endswith("docs")])
    return py_packs | other_packs

setupdir = os.path.dirname(__file__)


setup(
    name="UpyTest",
    version="3.1.5",
    author="Réda Id-taleb",
    description="A plug-in which adds a test framework",
    long_description="""A plug-in for Thonny which allows you to test your doc examples
 
More info: https://gitlab.univ-lille.fr/reda.idtaleb.etu/thonny_test_framework""",
    url="https://gitlab.univ-lille.fr/reda.idtaleb.etu/thonny_test_framework",
#    keywords="IDE education programming tests in documentation",
    classifiers=[
        "Topic :: Education :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education"
        ],
    platforms=["Windows", "macOS", "Linux"],
    python_requires=">=3.9",
    package_data=get_packages_data(),
    install_requires=["thonny>=4.0.0"],
    packages=packages,
)

