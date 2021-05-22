from model import Base, Users, Projects, Levels, Subjects, Chats, Messages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

try:
    engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
except:
    print("###################################################################################\n************************")
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

def add_user(username, password, email):
    user_object = Users(
    username = username,
    password = password,
    email = email,
    active_projects = 0,
    total_porject_num = 0,
    is_blocked = False)
    session.add(user_object)
    session.commit()


def delete_user_from_db(id):
    
    session.query(Users).filter_by(id = id).delete()
    session.commit()


def return_all_users():
    
    users = session.query(Users).all()
    return users


def return_user(username):
    
    user = session.query(Users).filter_by(username = username).first()
    return user


def return_user_by_id(id):
    
    user = session.query(Users).filter_by(id = id).first()
    return user


def update_active_proj_num(username):
    
    user_object = session.query(Users).filter_by(username = username).first()
    user_object.active_projects += 1
    user_object.total_porject_num += 1
    session.commit()


def reduce_active_projects(username):
    
    user_object = session.query(Users).filter_by(username = username).first()
    user_object.active_projects -= 1
    session.commit()


def reduce_total_proj_num(username):
    
    user_object = session.query(Users).filter_by(username = username).first()
    user_object.total_porject_num -= 1
    session.commit()


def block_user_forums(id):
    
    user_object = session.query(Users).filter_by(id = id).first()
    user_object.is_blocked = True
    session.commit()


def unblock_user(id):
    
    user_object = session.query(Users).filter_by(id = id).first()
    user_object.is_blocked = False
    session.commit()


def return_emails():
    
    users = session.query(Users).all()
    emails = []
    for user in users:
        emails.append(user.email)
    return emails
#############################################################################################################
def add_project(name, subject, start_date, end_date, duration, description, owner, color, percents_ready):
    
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
    third_alert = False,
    month_added = date.today().month)
    session.add(project_object)
    session.commit()


def return_user_projects(owner):
    
    projects = session.query(Projects).filter_by(owner = owner).all()
    return projects


def return_project(owner, name):
    
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    return project


def update_percents(owner, name, percents):
    
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    if project.percents_ready + percents > 100:
        project.percents_ready = 100
        reduce_active_projects(owner)
    else:
        project.percents_ready = percents
    session.commit()


def update_p_color(owner, name, color):
    
    project = session.query(Projects).filter_by(owner = owner, name = name).first()
    project.color = color
    session.commit()


def edit_project(username, name, new_name, s_date, e_date, subject, descrip):
    
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
    
    project_object = session.query(Projects).filter_by(owner = username, name = p_name).first()
    project_object.duration = new_duration
    session.commit()


def delete_project(owner, project_name):
    
    reduce_total_proj_num(owner)
    project = return_project(owner, project_name)
    user = return_user(owner)
    if project.percents_ready < 100 or user.total_porject_num == 1:
        reduce_active_projects(owner)
    session.query(Projects).filter_by(owner = owner, name = project_name).delete()
    session.commit()


def delete_all_projects(owner):
    
    session.query(Projects).filter_by(owner = owner).delete()
    session.commit()


def update_alert_status(owner, name, alert_num):
    
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
    
    levels = session.query(Levels).filter_by(owner = owner, from_project = from_project ).all()
    return levels


def return_level(owner, level_name, from_project):
    
    level = session.query(Levels).filter_by(owner = owner, name = level_name, from_project = from_project).first()
    return level


def update_level_percents(owner, from_project, name, project_duration, new_duration):
    
    level_object = session.query(Levels).filter_by(owner = owner, from_project = from_project, name = name).first()
    level_object.percent = round((new_duration / project_duration) * 100)
    session.commit()

def update_level_duration(owner, from_project, name, new_level_duration):
    
    level_object = session.query(Levels).filter_by(owner = owner, from_project = from_project, name = name).first()
    level_object.duration = new_level_duration
    session.commit()

def update_l_color(owner, from_project, name, color):
    
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
    
    project_object = session.query(Levels).filter_by(owner = owner, name = name, from_project = from_project).first()
    if alert_num == 1:
        project_object.first_alert = True
    elif alert_num == 2:
        project_object.second_alert = True
    elif alert_num == 3:
        project_object.third_alert = True
    session.commit()

def edit_level(owner, from_project, name, new_name, is_done_changed , s_date, e_date, descrip):
    
    level_object = session.query(Levels).filter_by(from_project = from_project, name = name, owner = owner).first()
    if new_name != "":
        level_object.name = new_name
    if s_date != "":
        level_object.start_date = s_date
    if e_date != "":
        level_object.end_date = e_date
    if descrip != "":
        level_object.description = descrip
    if is_done_changed:
        level_object.is_done = not level_object.is_done
    session.commit()


def delete_all_levels(owner, project_name):
    
    session.query(Levels).filter_by(owner = owner, from_project = project_name).delete()
    session.commit()


def delete_all_user_levels(owner):
    
    session.query(Levels).filter_by(owner = owner).delete()
    session.commit()


def delete_level(owner, project_name, level_name, level_num):
    
    session.query(Levels).filter_by(owner = owner, from_project = project_name, name = level_name,
    level_num = level_num).delete()
    session.commit()
############################################################################################################
def add_subjects(name_list):
    
    for name in name_list:
        subject_object = Subjects(name = name)
        session.add(subject_object)
        session.commit()


def add_subject(name):
    
    all_subjects = return_subjects()
    existed = False
    for subject in all_subjects:
        if subject.name == name:
            existed = True
    if not existed:
        subject_object = Subjects(name = name)
        session.add(subject_object)
        session.commit()


def return_subjects():
    
    subjects = session.query(Subjects).all()
    return subjects


def delete_subject(id):
    
    session.query(Subjects).filter_by(id = id).delete()
    session.commit()
#############################################################################################################

def open_new_chat(title, content, user, date, hour, subject):
    
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
    
    chats_dict = {}
    for subject in subjects_list:
        subjects_key = (subject, heading_counter)
        chats_dict[subjects_key] = return_all_chats()
        heading_counter += 1
    return chats_dict


def return_chat(chat_id):
    
    chat = session.query(Chats).filter_by(id = chat_id).first()
    return chat


def return_chat_messages(from_chat, subject, chat_id):
    
    message_list = session.query(Messages).filter_by(chat_id = chat_id, from_chat = from_chat, subject = subject).all()
    return message_list


def return_all_chats():
    
    list = session.query(Chats).all()
    chats = [x for x in list[::-1]]
    return chats


def delete_chat_DB(id, chat_name):
    
    session.query(Messages).filter_by(from_chat = chat_name, chat_id = id).delete()
    session.query(Chats).filter_by(id = id).delete()
    session.commit()


def update_num_messages(id):
    
    chat = session.query(Chats).filter_by(id = id).first()
    chat.num_messages += 1
    session.commit()
#############################################################################################################
def add_message(content, user, date_input, hour, subject, from_chat, chat_id):
    
    message_object = Messages(
        content = content,
        user = user,
        date = date_input,
        hour = hour,
        subject = subject,
        from_chat = from_chat,
        chat_id = chat_id,
        month_added = date.today().month)
    session.add(message_object)
    session.commit()


def return_all_messages():
    
    messages = session.query(Messages).all()
    return messages
