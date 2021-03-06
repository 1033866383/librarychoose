import datetime
import json
from contextlib import contextmanager

from flask import current_app
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///librarychoose.db', echo=True)
Session = sessionmaker(engine)
# base
Base = declarative_base()


@contextmanager
def connect():
    current_app.logger.info("open connect")
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        current_app.logger.info("exit connect")


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if isinstance(obj, User) and field == "info" and data:
                    data = json.loads(data)
                if isinstance(obj, Seat) and (field == "position" or field == "price") and data:
                    data = json.loads(data)
                if isinstance(data, datetime.datetime):
                    data = data.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def alchemy2json(obj):
    data = json.dumps(obj, cls=AlchemyEncoder)
    data = json.loads(data)
    return data


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(11), unique=True)
    name = Column(String(55))
    password = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    iphone = Column(String(15))
    info = Column(Text)  # ???????????????????????????????????????????????????
    role_id = Column(Integer, nullable=False)

    def __init__(self, username, password, email, role_id, **kwargs):
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id
        self.name = kwargs.get("name", "")
        self.iphone = kwargs.get("iphone", "")
        self.info = kwargs.get("info", "")


class Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, comment="???????????????")
    max_seat = Column(Integer, nullable=False, comment="?????????????????????")
    position = Column(String(255), nullable=False, comment="??????????????????")


class Seat(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    library = Column(Integer, ForeignKey("library.id"))
    position = Column(String(10), nullable=False, comment="???????????????")
    price = Column(String(100), nullable=False, comment="????????????????????? 6???-10??????10???/??????, 10 -12 15???/?????? ???????????????{'1': 10, '2': 10}")


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(String(255), primary_key=True)
    seat = Column(Integer, ForeignKey("seat.id"))
    user = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now(),
                         comment="??????????????????,?????????????????????????????????")
    start_time = Column(DateTime, nullable=False, comment="????????????????????????")
    end_time = Column(DateTime, nullable=False, comment="????????????????????????")
    status = Column(Integer, nullable=False, comment="????????????, 0 ?????? 1 ?????????")
    price = Column(Integer, nullable=False, comment="????????????????????????")


class Permissions(object):
    """
    ?????????
    """
    USER_MANAGE = 0X01
    NORMAL_USER = 0x02
    BADE_USER = 0x101

    path_permission = {
        USER_MANAGE: ["", ""],
        NORMAL_USER: [""],
        BADE_USER: []
    }


if __name__ == '__main__':
    Base.metadata.create_all(engine)
