from setuptools import setup, find_packages

requires = [
    "flask",
    "Flask-Security",
    "flask-socketio",
    "sqlalchemy",
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
