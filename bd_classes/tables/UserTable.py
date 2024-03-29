from sqlalchemy import Column, String, BigInteger

from bd_classes.tables.Base import Base


class UserTable(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'public'}

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    user_name = Column(String(100), nullable=False)
    user_photo_path = Column(String)

    def __repr__(self):
        return f"<UserTable(user_id={self.user_id}, user_name={self.user_name}, user_photo_path={self.user_photo_path})>"
