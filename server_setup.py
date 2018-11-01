from setuptools import setup, find_packages

requires = [
    "eventlet",
    "Flask",
    "Flask-Security",
    "SQLAlchemy",
    "Flask-SocketIO",
    "SQLAlchemy",
    "bcrypt",
    "pycryptodome"
]

setup(
    name="Hephaestus",
    version="0.1",
    description="Web-powered Orange PI controller and monitor - Server app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
