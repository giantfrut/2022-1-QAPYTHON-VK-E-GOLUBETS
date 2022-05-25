from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TotalRequests(Base):
    __tablename__ = 'TotalRequests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TotalRequests(" \
               f"id='{self.id}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=False)


class CountTypes(Base):
    __tablename__ = 'CountTypes'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<CountTypes(" \
               f"id='{self.id}'," \
               f"method='{self.method}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(length=400), nullable=False)
    count = Column(Integer, nullable=False)


class FrequentRequests(Base):
    __tablename__ = 'FrequentRequests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<FrequentRequests(" \
               f"id='{self.id}'," \
               f"request='{self.request}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(String(length=400), nullable=False)
    count = Column(Integer, nullable=False)


class UserErrors(Base):
    __tablename__ = 'UserErrors'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<UserErrors(" \
               f"id='{self.id}'," \
               f"request='{self.request}'," \
               f"status='{self.status}'," \
               f"bytes='{self.bytes}'," \
               f"ip_addr='{self.ip_addr}'," \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request = Column(String(length=400), nullable=False)
    status = Column(Integer, nullable=False)
    bytes = Column(Integer, nullable=False)
    ip_addr = Column(String(length=50), nullable=False)


class ServerErrors(Base):
    __tablename__ = 'ServerErrors'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<ServerErrors(" \
               f"id='{self.id}'," \
               f"ip_addr='{self.ip_addr}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_addr = Column(String(length=50), nullable=False)
    count = Column(Integer, nullable=False)
