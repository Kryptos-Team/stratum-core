from setuptools import setup, find_packages
import os

package_root = os.path.abspath(os.path.dirname(__file__))
classifier_file = os.path.join(package_root, "classifiers.txt")
description_file = os.path.join(package_root, "README.md")
keyword_file = os.path.join(package_root, "keywords.txt")
requirement_file = os.path.join(package_root, "requirements.txt")
version_file = os.path.join(package_root, "stratum/version.py")

description = None
version = {}

with open(version_file) as fp:
    exec(fp.read(), version)
version = version["__version__"]

with open(description_file) as r:
    exec(r.read(), description)

with open(requirement_file) as r:
    # strip fixed version info from requirements file
    requirements = [line.split('~=', 1)[0] for line in r]

setup(
    name="stratum-core",
    url="https://github.com/Kryptos-Team/stratum-core.git",
    author="Abhimanyu Saharan",
    author_email="desk.abhimanyu@gmail.com",
    classifiers=classifier_file,
    license="MIT",
    description=description,
    long_description=description,
    long_description_content_type="text/markdown",
    keywords=keyword_file,
    install_requires=requirements,
    packages=find_packages(),
    version=version
)
