"""
Database models definitions library.
We use SQLAlchemy as primary ORM, adding in elements of Flask-Security features.
"""

from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey

from database import Base


class UserRoles(Base):
    """
    Maps roles from Role table to a given user
    """
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    """
    Defines the list of available roles
    """
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


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
