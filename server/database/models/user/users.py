"""
User table model and migration/creation events container
"""

from flask_security import UserMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String

from server.web import db as database
from common.general import get_time_formatter


class Users(database.Model, UserMixin):
    """
    User representation object
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Roles', secondary='user_roles',
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
            "last_login_at": self.last_login_at.strftime(get_time_formatter()) if self.last_login_at else None,
            "login_count": self.login_count,
            "active": self.active,
            "roles": [role.serialize() for role in self.roles]
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
