from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['engine']
# connect db
engine = create_engine('sqlite:///librarychoose.db', echo=True)

# base
Base = declarative_base()


# 表要继承基本类
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(11), unique=True)
    name = Column(String(55))
    password = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    iphone = Column(String(15))
    info = Column(Text) #可配置参数，例如头像等其他可变参数


class Permission(object):
    COMMENT = 0x02
    ADMINISTER = 0x80


if __name__ == '__main__':
    Base.metadata.create_all(engine)
