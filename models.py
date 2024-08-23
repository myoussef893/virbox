from sqlalchemy import Column,Integer,Float,create_engine,String
from sqlalchemy.orm import declarative_base,sessionmaker
from flask_login import UserMixin

engine  = create_engine('sqlite:///database.db')
Base = declarative_base()

Session = sessionmaker(engine)
db_session = Session()




class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer,primary_key = True)
    creation_date = Column(String,nullable=False)
    full_name = Column(String)
    username = Column(String,unique=True)
    password = Column(String,nullable=False)
    email = Column(String,nullable=False)
    phone = Column(String,nullable=False,unique=True)
    locker = Column(String,nullable=False,unique=True,default=' ')
    group = Column(String,nullable=False) # set the type of user if Customer or Employee, and if the later the group belongs to. 


class Package(Base):
    __tablename__ = 'packages'
    scanning_date = Column(String, nullable=False)
    id = Column(Integer, primary_key = True)
    tracking_number = Column(String, nullable=False)
    items_count = Column(Integer, nullable=False)
    weight = Column(Float)
    locker = Column(String)

class Items(Base): 
    __tablename__ = 'items'
    id = Column(Integer,primary_key = True)
    scanning_date = Column(String,nullable=False)
    tracking_number = Column(String,nullable=False)
    item_weight = Column(Float)
    item_clearnace = Column(Integer)
    item_category = Column(String)
    item_quantity = Column(Integer,nullable=False)
    locker = Column(String)
    status = Column(String,nullable=False)

class IntBox(Base):
    __tablename__ = 'international_box'
    id = Column(Integer,primary_key = True)
    tracking_number = Column(String,nullable=False)
    total_weight = Column(Float,nullable=False)
    creation_date = Column(String,nullable=False)
    items_count = Column(String,nullable=False)
    shipping_company = Column(String,nullable=False)
    box_value = Column(Float)

Base.metadata.create_all(engine)

