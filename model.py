from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime, insert
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    active_projects = Column(Integer)
    submited_projects = Column(Integer)
    total_porject_num = Column(Integer)

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key = True)
    name = Column(String) #
    subject = Column(String) #
    start_date = Column(String) #
    end_date = Column(String) #
    duration = Column(Integer) #
    description = Column(String) #
    owner = Column(String) #
    is_active = Column(Boolean) #
    color = Column(String) #
    percents_ready = Column(Integer)#


class Levels(Base):
    __tablename__ = 'levels'
    id = Column(Integer, primary_key = True)
    name = Column(String) #
    level_num = Column(Integer) #
    start_date = Column(String) #
    end_date = Column(String) #
    duration = Column(Integer) #
    percent = Column(Integer) #
    description = Column(String) #
    from_project = Column(String) #
    owner = Column(String) #
    is_done = Column(Boolean) #
    color = Column(String) #
    
# class Subjects(Base):
#     __tablename__ = 'subjects'
#     id = Column(Integer, primary_key = True)
#     name = Column("name", Integer, server_default= "50")