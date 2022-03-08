from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['engine']
# 连接数据库
engine = create_engine('sqlite:///librarychoose.db', echo=True)

# 基本类
Base = declarative_base()


# 表要继承基本类
class User(Base):
    __tablename__ = 'users'  # 表的名字

    # 定义各字段
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __str__(self):
        return self.id


if __name__ == '__main__':
    Base.metadata.create_all(engine)
