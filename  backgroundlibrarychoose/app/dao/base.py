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
    yield session
    session.commit()
    session.close()
    current_app.logger.info("exit connect")


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
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
    password = Column(String(50), nullable=True)
    email = Column(String(100), unique=True)
    iphone = Column(String(15))
    info = Column(Text)  # 可配置参数，例如头像等其他可变参数
    role_id = Column(Integer, nullable=True)

    def __init__(self, username, password, email, role_id, **kwargs):
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id
        self.name = kwargs.get("name", "")
        self.iphone = kwargs.get("iphone", "")
        self.info = kwargs.get("info", "")


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=True, comment="城市名称")


class Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=True, comment="图书馆名称")
    max_seat = Column(Integer, nullable=True, comment="最大可容纳人数")
    city_id = Column(Integer, ForeignKey("city.id"))


class Seat(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    library = Column(Integer, ForeignKey("library.id"))
    max_seat = Column(Integer, nullable=True, comment="最大可容纳人数")
    position = Column(String(10), nullable=True, comment="座位的定位")
    price = Column(String(100), nullable=True, comment="价格规则：如： 6点-10点：10元/小时, 10 -12 15元/小时 数据结构：{'1': 10, '2': 10}")


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(String(255), primary_key=True)
    seat = Column(Integer, ForeignKey("seat.id"))
    user = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, nullable=True, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         comment="订单创建时间,这里是支付方可创建订单")
    start_time = Column(DateTime, nullable=True, comment="坐位使用开始时间")
    end_time = Column(DateTime, nullable=True, comment="坐位使用结束时间")
    status = Column(Integer, nullable=True, comment="订单状态, 0 正常 1 已删除 2违约，相当于到点未签到")


class Permissions(object):
    """
    权限类
    """
    USER_MANAGE = 0X01
    UPDATE_PERMISSION = 0x02
    BADE_USER = 0x101

    path_permission = {
        USER_MANAGE: ["", ""],
        UPDATE_PERMISSION: [""],
        BADE_USER: []
    }


if __name__ == '__main__':
    Base.metadata.create_all(engine)
