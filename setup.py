from setuptools import setup
from src.version import __version__

setup(
    name="stratum-core",
    description="Stratum server implementation",
    author="Abhimanyu Saharan",
    author_email="desk.abhimanyu@gmail.com",
    url="https://github.com/Kryptos-Team/stratum-core.git",
    packages=["src"],
    zip_safe=False,
    install_requires=["twisted", "ecdsa", "autobahn"],
    version=__version__
)
