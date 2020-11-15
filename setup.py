from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools import setup, find_packages
import subprocess
import distutils.cmd
import os

class ServiceCommand(distutils.cmd.Command):
    """A custom command to install systemd service """

    description = 'Install systemd service'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""

    def finalize_options(self):
        """Post-process options."""

    def run(self):
        """Run command."""
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        create_service_script_path = os.path.join(current_dir_path, 'inst_scripts', 'create_service.sh')
        subprocess.check_output([create_service_script_path])

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PiPlot2D",
    version="0.0.1",
    author="sinseman44",
    author_email="sinseman44@gmail.com",
    description="Control PiPlot2D system",
    long_description="Control PiPlot2D system",
    long_description_content_type="text/markdown",
    url="https://github.com/sinseman44/PiPlot2D",
    scripts=['piplotter'],
    cmdclass={
        'install_service': ServiceCommand
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    install_requires=[
        'RPi.GPIO',
        'RPLCD',
        'PyCNC<=2.0.0'
    ],
    dependency_links=[
        "https://github.com/sinseman44/PyCNC/archive/v2.0.0.zip#egg=pycnc-2.0.0",
    ],
    python_requires='>=3.6',
)
