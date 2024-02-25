from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PointOnTheMapTable(Base):
    __tablename__ = 'point_on_the_map'
    __table_args__ = {'schema': 'public'}

    message_id = Column(Integer, primary_key=True, nullable=False)
    photo_path = Column(String)
    location_id = Column(Integer, nullable=False)
    message = Column(String)
    user = Column(Integer, ForeignKey('public.users.user_id'), nullable=False)

    user_relationship = relationship("UserTable", back_populates="points_on_the_map")

    def __repr__(self):
        return f"<PointOnTheMapTable(message_id={self.message_id}, photo_path={self.photo_path}, location_id={self.location_id}, message={self.message}, user={self.user})>"
