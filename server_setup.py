from setuptools import setup, find_packages

requires = [
    "eventlet",
    "Flask",
    "Flask-Security",
    "Flask-SQLAlchemy",
    "Flask-SocketIO",
    "SQLAlchemy",
    "mysql-connector",
    "bcrypt",
    "pycryptodome"
]

setup(
    name="OrangeTree",
    version="0.1",
    description="Web-powered Orange PI controller and monitor - Server app",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
