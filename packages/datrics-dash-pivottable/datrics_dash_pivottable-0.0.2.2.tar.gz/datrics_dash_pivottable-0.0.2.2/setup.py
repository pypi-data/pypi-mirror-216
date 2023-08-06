import json
import os
from setuptools import setup


with open(os.path.join('datrics_dash_pivottable', 'package.json')) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name = 'datrics_dash_pivottable',
    description = 'Fixed version of the dash_pivottable=0.0.2',
    version = '0.0.2.2',
    author='Roman Malkevych',
    author_email='rm@datrics.ai',
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    install_requires=['dash']
)
