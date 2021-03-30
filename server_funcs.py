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
    return duration.days


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
        print(f'BEFORE update: {level.percent}')
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

    user_projects = return_user_projects(user.username)
    for project in user_projects:
        end_date = format_date(project.end_date)
        if duration_calc(today, end_date) == 1:
            alerts_dict[project.name] = 1
        elif duration_calc(today, end_date) == 0:
            alerts_dict[project.name] = 2
        elif duration_calc(today, end_date) < 0:
            alerts_dict[project.name] = 3
    return alerts_dict
# def level_submission_alert():
#     users = return_all_users()
#     if not users:
#         return
#     for user in users:
#         user_projects = return_user_projects(user.username)
#         for project in user_projects:
#             levels = return_project_levels(user.username, project.name)
#             due_level = return_closest_due(levels)
            
        
        