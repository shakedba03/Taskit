from model import Base, Users, Projects, Levels
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_user(username, password, email):
    session = DBSession()
    user_object = Users(
    username = username,
    password = password,
    email = email,
    active_projects = 0,
    submited_projects = 0,
    total_porject_num = 0)
    session.add(user_object)
    session.commit()

def del_user(id):
    session = DBSession()
    session.query(Users).filter_by(id = id).delete()
    session.commit()

def return_all_users():
    session = DBSession()
    users = session.query(Users).all()
    return users

def return_user(username):
    session = DBSession()
    user = session.query(Users).filter_by(username = username).first()
    return user

#############################################################################################################
def add_project(name, subject, start_date, end_date, duration, description, owner):
    session = DBSession()
    project_object = Projects(
    name = name,
    subject = subject,
    start_date = start_date,
    end_date = end_date,
    duration = duration, 
    description = description,
    owner = owner)
    session.add(project_object)
    session.commit()


def return_user_projects(owner):
    session = DBSession()
    projects = session.query(Projects).filter_by(owner = owner).all()
    return projects


def return_project(owner):
    session = DBSession()
    project = session.query(Projects).filter_by(owner = owner).first()
    return project
#############################################################################################################
def add_level(name, level_num, start_date, end_date, duration, percent, description, from_project, owner):
    session = DBSession()
    level_object = Levels(
    name = name,
    level_num = level_num,
    start_date = start_date,
    end_date = end_date,
    duration = duration, 
    percent = percent,
    description = description,
    from_project = from_project,
    owner = owner,
    is_done = False)
    session.add(level_object)
    session.commit()


def return_project_levels(owner, project_name):
    session = DBSession()
    levels = session.query(Projects).filter_by(owner = owner, project_name = project_name).all()
    return levels


def return_level(owner, project_name):
    session = DBSession()
    level = session.query(Projects).filter_by(owner = owner, project_name = project_name).first()
    return level