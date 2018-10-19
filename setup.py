from setuptools import setup, find_packages

requires = [
    "Flask",
    "Flask-Security",
    "SQLAlchemy",
    "Flask-SocketIO",
    "SQLAlchemy",
    "bcrypt"
]

setup(
    name="Hephaestus",
    version="0.1",
    description="Web-powered Orange PI controller and monitor",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
