import os
import sys
import time
import fnmatch
import tempfile
import tarfile
from distutils import log

from site import USER_SITE
import subprocess


def _python_cmd(*args):
    args = (sys.executable,) + args
    return subprocess.call(args) == 0


DEFAULT_VERSION = "0.6.28"
DEFAULT_URL = "http://pypi.python.org/packages/source/d/distribute/"
SETUPTOOLS_FAKED_VERSION = "0.6c11"

SETUPTOOLS_PKG_INFO = """\
Metadata-Version: 1.0
Name: setuptools
Version: %s
Summary: xxxx
Home-page: xxx
Author: xxx
Author-email: xxx
License: xxx
Description: xxx
""" % SETUPTOOLS_FAKED_VERSION


def _install(tarball, install_args=()):
    tmpdir = tempfile.mktemp()
    log.warn(f"Extracting in {tmpdir}")
    old_wd = os.getcwd()
    try:
        os.chdir(tmpdir)
        log.warn(f"Working directory: {tmpdir}")
        tar = tarfile.open(tarball)
        _extractall(tar)
        tar.close()

        # Going inside the directory
        subdir = os.path.join(tmpdir, os.listdir(tmpdir)[0])
        os.chdir(subdir)
        log.warn(f"Working directory: {subdir}")

        # Install distribute
        log.warn("Installing distribute")
        if not _python_cmd("setup.py", "install", *install_args):
            log.warn("Something went wrong during the installation")
    finally:
        os.chdir(old_wd)


def _extractall():
    pass
