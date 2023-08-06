"""
This code defines the script required by setuptools.
"""

# Non-standard imports.
from setuptools import setup

# Local constants.
PACKAGE_NAME = "hoskerlatch"
VERSION = "1.0.0"
DESCRIPTION = "Encrypt and decrypt folders to a medium standard of security"
GIT_URL_STEM = "https://github.com/tomhosker"
AUTHOR = "Tom Hosker"
AUTHOR_EMAIL = "tomdothosker@gmail.com"
SCRIPT_PATHS = ("scripts/hoskerlatch", "scripts/hoskerunlatch")
INSTALL_REQUIRES = ("cryptography", "hosker-utils")
INCLUDE_PACKAGE_DATA = True

###################################
# THIS IS WHERE THE MAGIC HAPPENS #
###################################

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=GIT_URL_STEM+"/"+PACKAGE_NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    package_dir={ PACKAGE_NAME: "source" },
    packages=[PACKAGE_NAME],
    scripts=SCRIPT_PATHS,
    install_requires=INSTALL_REQUIRES,
    include_package_data=INCLUDE_PACKAGE_DATA
)
