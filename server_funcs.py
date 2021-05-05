import datetime as dt
from datetime import datetime
from databases import *
import sys

def format_date(date):
    # Gets a str of a date.
    # returns a date %d%m%Y format.
    if type(date) == str:
        str_date = date.split("-")
        str_date = str_date[2] + str_date[1] + str_date[0] 
        str_date = dt.datetime.strptime(str_date, "%d%m%Y").date()
        return str_date
    return date

def duration_calc(s_date, e_date):
    # Gets two dates and returns the days num between them.
    start = format_date(s_date)
    end = format_date(e_date)
    duration = end - start
    return duration.days + 1


def verify_user_projects(username, projects_list):
    # Gets a username and projects list, checks the percentage calc, returns a project list.

    for project in projects_list:
        levels_objects_list = return_project_levels(username, project.name)
       # fix_sum_percents(levels_objects_list, project.duration, project.name, username)
        project.percents_ready = percents_ready(levels_objects_list)
    
    return projects_list


def get_color(end_date):
    # Gets an ending date, retruns a color to show in the cards.
    color = "rgb(26, 168, 8)" # color = green
    today = datetime.today().strftime("%Y-%m-%d")
    days_gap = duration_calc(today, end_date)
    if days_gap < 0:
        color = "rgb(223, 2, 2)" # color = red
    elif days_gap <= 1:
        color = "rgb(250, 78, 10)" # color = orange
    return color

def percents_ready(levels_list):
    # Gets a list of a project's levels.
    # Returns how much of the project is done in percents. (int)
    percents = 0
    for level in levels_list:
        if level.is_done == True:
            percents += level.percent
    return percents

def fix_sum_percents(levels_list, p_duration, from_project, username):
    # Gets a list of a project's levels.
    # checks that the total sum of the percents = 100%.
    # If not, it fixes the percents.
    done_levels = []
    for level in levels_list:
        l_duration = duration_calc(level.start_date, level.end_date)
        update_level_percents(username, from_project, level.name, p_duration, l_duration)
        if level.is_done == True:
            updated_level = return_level(username, level.name, from_project)
            done_levels.append(updated_level)
    
    new_ready_percents = 0
    for item in done_levels:
        new_ready_percents += item.percent
    update_percents(username, from_project, new_ready_percents)


def return_closest_due(levels_list):
    # Gets a list of all levels, returns the closest due level.
    today = datetime.today()
    closest_due = None
    min_gap = sys.maxsize
    for level in levels_list:
        current_date = format_date(level.end_date)
        current_gap = duration_calc(today.date(), current_date)

        if current_date > today.date() and level.is_done == False and min_gap > current_gap and current_gap >= 0:
            closest_due = level
            min_gap = current_gap

        if current_date < today.date() and level.is_done == False:
            closest_due = level
            break
    return closest_due
        

def make_str_levels(levels):
    # Gets a levels list, returns a string for each level that contains the s_date, is_done and e_date.
    ret_list = []
    for level in levels:
        ret_list.append(level.start_date + "," + str(level.is_done) + "," + level.end_date)
    return ret_list

def make_str_project(project):
    # Gets a project, returns a string that contains the s_date and e_date.
    ret_str = project.start_date + "," + project.end_date
    return ret_str

def calc_new_duration(levels):
    new_duration = 0
    for level in levels:
        if not level.is_done:
            new_duration += level.duration
    return new_duration


def get_name_list(items):
    names_list = []
    for item in items:
        names_list.append(item.name)
    return names_list


def project_submission_alert(user):
    alerts_dict = {}
    today = datetime.today().strftime("%Y-%m-%d")
    print(today)
    user_projects = return_user_projects(user.username)
    for project in user_projects:
        if project.percents_ready < 100:
            end_date = format_date(project.end_date)
            if duration_calc(today, end_date) == 2:
                alerts_dict[project.name] = 1
            elif duration_calc(today, end_date) == 1:
                alerts_dict[project.name] = 2
            elif duration_calc(today, end_date) < 1:
                alerts_dict[project.name] = 3
    return alerts_dict

def level_submission_alert(user, levels):
    alerts_dict = {}
    today = datetime.today().strftime("%Y-%m-%d")

    for level in levels:
        if not level.is_done:
            end_date = format_date(level.end_date)
            if duration_calc(today, end_date) == 2:
                alerts_dict[level.name] = 1
            elif duration_calc(today, end_date) == 1:
                alerts_dict[level.name] = 2
            elif duration_calc(today, end_date) < 1:
                alerts_dict[level.name] = 3
    return alerts_dict

def update_proj_color(username):
    projects = return_user_projects(username)
    today = datetime.today().strftime("%Y-%m-%d")
    for project in projects:
        if project.percents_ready != 100:
            end_date = format_date(project.end_date)
            if duration_calc(today, end_date) == 2 or duration_calc(today, end_date) == 1:
                color = "rgb(250, 78, 10)" #orange
            elif duration_calc(today, end_date) < 0:
                color = "rgb(223, 2, 2)" #red
            else:
                color = "rgb(26, 168, 8)" #green
            update_p_color(username, project.name, color)


def update_level_color(username, project):
    levels = return_project_levels(username, project)
    today = datetime.today().strftime("%Y-%m-%d")
    for level in levels:
        end_date = format_date(level.end_date)
        if not level.is_done:
            if duration_calc(today, end_date) == 2 or duration_calc(today, end_date) == 1:
                color = "rgb(250, 78, 10)" #orange
            elif duration_calc(today, end_date) < 0:
                color = "rgb(223, 2, 2)" #red
            else:
                color = "rgb(26, 168, 8)" #green
            update_l_color(username, level.from_project, level.name, color)


def get_user_subjects(username):
    user_projects = return_user_projects(username)
    user_subjects = []
    for project in user_projects:
        user_subjects.append(project.subject)
    return user_subjects


def find_relevant_recipients(sender, subject):
    # Gets a subject and finds all the members of the forum.
    all_users_list = return_all_users()
    relevant_recipients = []
    for user in all_users_list:
        user_projects = return_user_projects(user.username)
        for project in user_projects:
            if project.subject == subject and user.username != sender:
                relevant_recipients.append(user)
    return relevant_recipients


def get_late_num():
    users = return_all_users()
    late_counter = 0
    today = format_date(datetime.today().strftime("%Y-%m-%d"))
    for user in users:
        user_projects = return_user_projects(user.username)
        for project in user_projects:
            end_date = format_date(project.end_date)
            if project.percents_ready < 100 and today > end_date:
                late_counter += 1
    return late_counter

def total_proj_num():
    users = return_all_users()
    proj_counter = 0
    for user in users:
        proj_counter += user.total_porject_num
    return proj_counter


def total_active_proj_num():
    users = return_all_users()
    proj_counter = 0
    for user in users:
        proj_counter += user.active_projects
    return proj_counter


def added_monthly():
    users = return_all_users()
    added_counter = 0
    today = date.today()
    month = today.month
    for user in users:
        user_projects = return_user_projects(user.username)
        for project in user_projects:
            if project.month_added == month:
                added_counter += 1
    return added_counter


def sent_monthly():
    messages = return_all_messages()
    sent_counter = 0
    today = date.today()
    month = today.month
    for message in messages:
        if message.month_added == month:
            sent_counter += 1
    return sent_counter
