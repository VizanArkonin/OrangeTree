"""
Role table model and migration/creation events container
"""
from flask_security import RoleMixin
from sqlalchemy import Column, Integer, String, event
from server.database import Base, db_session


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


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(Role.__table__, "after_create")
def populate_default_user_roles(*args, **kwargs):
    db_session.add(Role(id=1, name="admin", description="Admin role"))
    db_session.add(Role(id=2, name="user", description="Regular user"))
    db_session.commit()
