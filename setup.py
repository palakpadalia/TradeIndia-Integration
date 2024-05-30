from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in trade_india_integration/__init__.py
from trade_india_integration import __version__ as version

setup(
	name="trade_india_integration",
	version=version,
	description="Trade India Integration",
	author="Sanskar Technolab",
	author_email="palak@sanskartechnolab.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
