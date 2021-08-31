import os
import subprocess

import setuptools
from setuptools.command.sdist import sdist

with open("README.md", "r") as fh:
    long_description = fh.read()

# The CSS file
package_resources = ["securedrop_client/resources/css/sdclient.css"]

# All other graphics used in the client
for name in os.listdir("./securedrop_client/resources/images/"):
    package_resources.append(os.path.join("./securedrop_client/resources/images", name))


class SdistWithTranslationCatalogs(sdist):
    def run(self):
        """Call out to `make compile-translation-catalogs`, then run the rest of
        the rest of the normal `sdist` routine.
        """

        cmd = ["make", "compile-translation-catalogs"]
        if subprocess.call(cmd) != 0:
            raise EnvironmentError(f"error calling {cmd}")

        super().run()


setuptools.setup(
    name="securedrop-client",
    version="0.5.0",
    author="Freedom of the Press Foundation",
    author_email="securedrop@freedom.press",
    description="SecureDrop Workstation client application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    install_requires=["SQLALchemy", "alembic", "securedrop-sdk", "python-dateutil", "arrow"],
    python_requires=">=3.5",
    url="https://github.com/freedomofpress/securedrop-proxy",
    packages=["securedrop_client", "securedrop_client.gui", "securedrop_client.resources"],
    include_package_data=True,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["sd-client = securedrop_client.app:run"]},
    # Override "sdist" to compile gettext gettext POs to MOs for inclusion in
    # built distributions.
    cmdclass={"sdist": SdistWithTranslationCatalogs},
    package_data={"": ["locale/*/*/*.mo", "locale/*/*/*.po"]},
    setup_requires=["babel"],
)
