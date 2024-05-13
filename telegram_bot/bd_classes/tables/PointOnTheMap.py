from sqlalchemy import Column, BigInteger, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from bd_classes.tables.Base import Base


class PointOnTheMapTable(Base):
    __tablename__ = 'point_on_the_map'
    __table_args__ = {'schema': 'public'}

    message_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    photo_path = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    message = Column(String)
    user_id = Column(BigInteger, ForeignKey('public.user.user_id'), nullable=False)

    user_relationship = relationship("UserTable")

    def __repr__(self):
        return f"<PointOnTheMapTable(message_id={self.message_id}, photo_path={self.photo_path}, location_id={self.location_id}, message={self.message}, user={self.user})>"
