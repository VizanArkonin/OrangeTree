"""
UserRoles table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, ForeignKey
from server.database import Base


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