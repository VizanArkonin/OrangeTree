"""
Database models definitions library.
We use SQLAlchemy as primary ORM, adding in elements of Flask-Security features.
"""

from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey

from database import Base
from utils.general import get_time_formatter


class UserRoles(Base):
    """
    Maps roles from Role table to a given user
    """
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

    def serialize(self):
        """
        Serializes given object into dict
        :return: Dict with data
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id
        }


class Role(Base, RoleMixin):
    """
    Defines the list of available roles
    """
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    def serialize(self):
        """
        Serializes object to dict object
        :return: Dict with data
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class User(Base, UserMixin):
    """
    User representation object
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='user_roles',
                         backref=backref('users', lazy='dynamic'))

    def serialize_general_data(self):
        """
        Serializes non-sensual information about the device (i.e. excluding password and roles)
        :return: Dict with data
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "last_login_at": self.last_login_at.strftime(get_time_formatter()),
            "login_count": self.login_count,
            "active": self.active
        }

    def serialize_all(self):
        """
        Serializes all variables, providing full information about user.
        :return: Dict with data
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "last_login_at": self.last_login_at.strftime(get_time_formatter()),
            "login_count": self.login_count,
            "active": self.active,
            "roles": [role.serialize() for role in self.roles]
        }
