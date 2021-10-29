import os
from setuptools import setup, find_packages

root_dir = os.path.dirname(os.path.abspath(__file__))
req_file = os.path.join(root_dir, "requirements.txt")
with open(req_file) as f:
    requirements = f.read().splitlines()

version = __import__("ptms_finder").__version__

setup(
    name="ptms-finder",
    version=version,
    description="Post-translational modifications (PTMs) Finder",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ptms-finder=ptms_finder.app.cli:cli",
        ],
    },
    include_package_data=True,
    install_requires=requirements,
)
