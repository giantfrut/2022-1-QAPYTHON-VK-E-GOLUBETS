from sqlalchemy import Column, Integer, String, SmallInteger, Date
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UsersTest(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<test_users(" \
               f"id='{self.id}'," \
               f"name='{self.name}'," \
               f"surname='{self.surname}'," \
               f"middle_name='{self.middle_name}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=255), nullable=False)
    surname = Column(String(length=255), nullable=False)
    middle_name = Column(String(length=255), default=None)
    username = Column(String(length=16), default=None, unique=True)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=64), nullable=False, unique=True)
    access = Column(SmallInteger, default=None)
    active = Column(SmallInteger, default=None)
    start_active_time = Column(Date, default=None)
