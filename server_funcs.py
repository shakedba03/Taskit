import datetime as dt
from datetime import datetime
from databases import return_project_levels, update_level_percents

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


def user_projects_levels_full(username, projects_list):
    # Gets a username and projects list, returns a dictionary that connects the project to its levels.
    print(projects_list)
    data_dict = {}

    for project in projects_list:
        levels_objects_list = return_project_levels(username, project.name)
        fix_sum_percents(levels_objects_list, project.start_date, project.end_date, project.duration, project.name, username)
        project.percents_ready = percents_ready(levels_objects_list)
        data_dict[project] = levels_objects_list
    
    return data_dict


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
    # Gets a list of a projct's levels.
    # Returns how much of the project is done in percents. (int)
    percents = 0
    for level in levels_list:
        if level.is_done == True:
            percents += level.percent
    return percents

def fix_sum_percents(levels_list, p_start, p_end, p_duration, from_project, username):
    # Gets a list of a projct's levels.
    # checks that the total sum of the percents = 100%.
    # If not, it fixes the percents.
    total_percent_sum = 0
    for level in levels_list:
        total_percent_sum += level.percent

    if total_percent_sum < 100:
        first_level_start = format_date(levels_list[0].start_date)
        project_start = format_date(p_start)
        last_level_end = format_date(levels_list[len(levels_list) - 1].end_date)
        project_end = format_date(p_end)

        if first_level_start != project_start:
            duration_start = levels_list[0].duration + duration_calc(project_start, first_level_start)
            # update the level's percent in the DB
            update_level_percents(username, from_project, levels_list[0].level_num, p_duration, duration_start)

        if last_level_end != p_end:
            duration_end = levels_list[len(levels_list) - 1].duration + duration_calc(project_end, last_level_end)
            # update the level's percent in the DB
            update_level_percents(username, from_project, levels_list[len(levels_list) - 1].level_num, p_duration, duration_end)
        
