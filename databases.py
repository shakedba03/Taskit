from model import Base, Users, Projects, Levels, Subjects, Chats, Messages
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
    total_porject_num = 0)
    session.add(user_object)
    session.commit()


def delete_user(username):
    session = DBSession()
    session.query(Users).filter_by(username = username).delete()
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
    session = DBSession()
    user_object = session.query(Users).filter_by(username = username).first()
    user_object.active_projects += 1
    user_object.total_porject_num += 1
    session.commit()

def return_emails():
    session = DBSession()
    users = session.query(Users).all()
    emails = []
    for user in users:
        emails.append(user.email)
    return emails
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
    percents_ready = percents_ready,
    first_alert = False,
    second_alert = False,
    third_alert = False)
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

def update_percents(owner, name, percents):
    session = DBSession()
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    project.percents_ready = percents
    session.commit()

def update_p_color(owner, name, color):
    session = DBSession()
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    project.color = color
    session.commit()


def edit_project(username, name, new_name, s_date, e_date, subject, descrip):
    session = DBSession()
    project_object = session.query(Projects).filter_by(owner = username, name = name).first()
    if new_name:
        project_object.name = new_name
    if s_date:
        project_object.start_date = s_date
    if e_date:
        project_object.end_date = e_date
    if descrip:
        project_object.description = descrip
    if subject:
        project_object.subject = subject
    session.commit()
    

def update_project_duration(username, p_name, new_duration):
    session = DBSession()
    project_object = session.query(Projects).filter_by(owner = username, name = p_name).first()
    project_object.duration = new_duration
    session.commit()


def delete_project(owner, project_name):
    session = DBSession()
    session.query(Projects).filter_by(owner = owner, name = project_name).delete()
    session.commit()


def update_alert_status(owner, name, alert_num):
    session = DBSession()
    project_object = session.query(Projects).filter_by(owner = owner, name = name).first()
    if alert_num == 1:
        project_object.first_alert = True
    elif alert_num == 2:
        project_object.second_alert = True
    elif alert_num == 3:
        project_object.third_alert = True
    session.commit()
#############################################################################################################
def add_level(name, level_num, start_date, end_date, duration, description, from_project, owner, color):
    session = DBSession()
    level_object = Levels(
    name = name,
    level_num = level_num,
    start_date = start_date,
    end_date = end_date,
    duration = duration, 
    percent = 0,
    description = description,
    from_project = from_project,
    owner = owner,
    is_done = False,
    color = color,
    first_alert = False,
    second_alert = False,
    third_alert = False)
    session.add(level_object)
    session.commit()


def return_project_levels(owner, from_project):
    session = DBSession()
    levels = session.query(Levels).filter_by(owner = owner, from_project = from_project ).all()
    return levels


def return_level(owner, level_name, from_project):
    session = DBSession()
    level = session.query(Levels).filter_by(owner = owner, name = level_name, from_project = from_project).first()
    return level


def update_level_percents(owner, from_project, name, project_duration, new_duration):
    session = DBSession()
    level_object = session.query(Levels).filter_by(owner = owner, from_project = from_project, name = name).first()
    level_object.percent = round((new_duration / project_duration) * 100)
    print("FROM the DB func:")
    print(level_object.name + ": " + str(level_object.percent))
    session.commit()


def update_l_color(owner, from_project, name, color):
    session = DBSession()
    level = session.query(Levels).filter_by(owner = owner, from_project = from_project, name = name).first()
    level.color = color
    session.commit()


def update_from_proj(username, prev_name, new_name):
    levels_list = session.query(Levels).filter_by(owner = username, from_project = prev_name ).all()
    if new_name:
        for level in levels_list:
            level.from_project = new_name
        session.commit()

def update_level_alert_status(owner, name, from_project, alert_num):
    session = DBSession()
    project_object = session.query(Levels).filter_by(owner = owner, name = name, from_project = from_project).first()
    if alert_num == 1:
        project_object.first_alert = True
    elif alert_num == 2:
        project_object.second_alert = True
    elif alert_num == 3:
        project_object.third_alert = True
    session.commit()

def edit_level(owner, from_project, name, new_name, is_done, s_date, e_date, descrip):
    session = DBSession()
    level_object = session.query(Levels).filter_by(from_project = from_project, name = name, owner = owner).first()
    if new_name:
        level_object.name = new_name
    if s_date:
        level_object.start_date = s_date
    if e_date:
        level_object.end_date = e_date
    if descrip:
        level_object.description = descrip
    if is_done != level_object.is_done:
        level_object.is_done = is_done
    session.commit()


def delete_all_levels(owner, project_name):
    session = DBSession()
    session.query(Levels).filter_by(owner = owner, from_project = project_name).delete()
    session.commit()


def delete_level(owner, project_name, level_name, level_num):
    session = DBSession()
    session.query(Levels).filter_by(owner = owner, from_project = project_name, name = level_name,
    level_num = level_num).delete()
    session.commit()
############################################################################################################
def add_subjects(name_list):
    session = DBSession()
    for name in name_list:
        subject_object = Subjects(name = name)
        session.add(subject_object)
        session.commit()

def return_subjects():
    session = DBSession()
    subjects = session.query(Subjects).all()
    return subjects
#############################################################################################################

def open_new_chat(title, content, user, date, hour, subject):
    session = DBSession()
    chat_object = Chats(
        title = title,
        content = content,
        user = user,
        date = date,
        hour = hour,
        subject = subject,
        num_messages = 0)
    session.add(chat_object)
    session.commit()

heading_counter = 1
def return_chats_dict(subjects_list):
    global heading_counter
    session = DBSession()
    chats_dict = {}
    for subject in subjects_list:
        subjects_key = (subject, heading_counter)
        chats_dict[subjects_key] = session.query(Chats).filter_by(subject = subject).all()
        heading_counter += 1
    return chats_dict


def return_chat(chat_id):
    session = DBSession()
    chat = session.query(Chats).filter_by(id = chat_id).first()
    return chat


def return_chat_messages(from_chat, subject, chat_id):
    session = DBSession()
    message_list = session.query(Messages).filter_by(chat_id = chat_id, from_chat = from_chat, subject = subject).all()
    return message_list


def update_num_messages(id):
    session = DBSession()
    chat = session.query(Chats).filter_by(id = id).first()
    chat.num_messages += 1
    session.commit()
#############################################################################################################
def add_message(content, user, date, hour, subject, from_chat, chat_id):
    session = DBSession()
    message_object = Messages(
        content = content,
        user = user,
        date = date,
        hour = hour,
        subject = subject,
        from_chat = from_chat,
        chat_id = chat_id)
    session.add(message_object)
    session.commit()