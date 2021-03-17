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

def update_active_proj_num(username):
    user_object = session.query(Users).filter_by(username = username).first()
    user_object.active_projects += 1
    user_object.total_porject_num += 1
    print("UPDATED USER ACTIVES")
    session.commit()

#############################################################################################################
def add_project(name, subject, start_date, end_date, duration, description, owner, color, percents_ready):
    session = DBSession()
    project_object = Projects(
    name = name,
    subject = subject,
    start_date = start_date,
    end_date = end_date,
    duration = duration, 
    description = description,
    owner = owner, 
    is_active = True,
    color = color,
    percents_ready = percents_ready)
    session.add(project_object)
    session.commit()


def return_user_projects(owner):
    session = DBSession()
    projects = session.query(Projects).filter_by(owner = owner).all()
    return projects


def return_project(owner, name):
    session = DBSession()
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    return project
#############################################################################################################
def add_level(name, level_num, start_date, end_date, duration, percent, description, from_project, owner, color):
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
    is_done = False,
    color = color)
    session.add(level_object)
    session.commit()


def return_project_levels(owner, from_project):
    session = DBSession()
    levels = session.query(Levels).filter_by(owner = owner, from_project = from_project ).all()
    return levels


def return_level(owner, project_name):
    session = DBSession()
    level = session.query(Levels).filter_by(owner = owner, project_name = project_name).first()
    return level

def update_level_percents(owner, from_project, level_num, project_duration, new_duration):
    level_object = session.query(Levels).filter_by(owner = owner, from_project = from_project, level_num = level_num).first()
    level_object.percent = (new_duration / project_duration) * 100
    print("UPDATED PERCENTS%")
    session.commit()



