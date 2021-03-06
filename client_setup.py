from setuptools import setup, find_packages

requires = [
    "pycryptodome",
    "psutil"
]

setup(
    name="OrangeTree",
    version="0.1",
    description="Web-powered Orange PI controller and monitor - Client app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
