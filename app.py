from flask import *
from model import *
from databases import *
from server_funcs import *
from flask_mail import *
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taskitMail'
app.config['MAIL_PASSWORD'] = 'cyberprojectpassword%'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


current_user = None
default_subjects = ["אנגלית", "מתמטיקה", "מדעי המחשב", "מדעי החברה", "סייבר", "ביולוגיה", "פיזיקה", "אומנות"]
project_name = ""
level_name = ""
clicked_chat_id = -1

@app.route('/', methods=['GET', 'POST'])
def index():
	global current_user, user_projects, default_subjects
	
	notification_center()
	admin = return_user("taskitAdmin")
	if not admin:
		add_user("taskitAdmin", "80261d757fbd1902559576f23a6c4968", "taskitmail@gmail.com")
	msg = ""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		users_list = return_all_users()

		if username == "taskitAdmin" and password == "80261d757fbd1902559576f23a6c4968":
			return redirect("/data")
		
		for user in users_list:
			if user.username == username and user.password == password:
				# get the user's porjects and levels from the db.
				current_user = return_user(username)
				user_projects = return_user_projects(current_user.username)
				# adding default sbjects to the DB.
				check_subjects = return_subjects()
				if not check_subjects:
					add_subjects(default_subjects)
				# print(current_user.username) ---> DELETE IT
				# print("after login: TOTAL PROJECTS NUM is " + str(current_user.total_porject_num)) ---> DELETE IT
				return redirect('/projects')
		msg = "פרטי הכניסה שגויים"
	return render_template("login.html", msg = msg)
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	msg = ""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']
		email = request.form['email']
		users_list = return_all_users()

		for user in users_list:
			if user.username == username:
				msg = "שם המשתמש שהוזן כבר קיים במערכת. אנא בחרו שם משתמש אחר!"

		if password != password2:
			msg = "אימות הסיסמה אינו תואם לסיסמה שהוזנה."
		if msg == "":
			add_user(username, password, email)
			return render_template("login.html")
	return render_template("signup.html", msg = msg)

@app.route('/projects', methods=['GET', 'POST'])
def projects():
	global current_user
	update_proj_color(current_user.username)
	if request.method == 'POST':
		# Get the project out of the DB
		clicked_proj = request.form['project_name']
		# Redirect to '/current_proj'
		return redirect(url_for('current_proj', project_name = clicked_proj))

	# Pull from the project table all projects related to the user.
	# Put it in a list.
	# Get the date of the closest due date.
	current_user = return_user(current_user.username)
	user_projects = return_user_projects(current_user.username)
	projects_due_dict = {}
	# print("at all projects: TOTAL PROJECTS NUM is " + str(current_user.total_porject_num)) ---> DELETE IT
	if current_user.total_porject_num != 0:
		# checking the percents of the project and levels.
		user_projects = verify_user_projects(current_user.username, user_projects)
		
		for project in user_projects:
			levels = return_project_levels(current_user.username, project.name)
			projects_due_dict[project] = return_closest_due(levels)
			
	return render_template("projects.html", user_projects = projects_due_dict)

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
	global current_user
	all_subjects = return_subjects()
	today = datetime.today().strftime('%Y-%m-%d')
	if request.method == 'POST':
		# Getting the form data - project info.
		p_name = request.form['name']
		subject = request.form['subject']
		p_start_date = request.form['start_val']
		p_end_date = request.form['end_val']
		# p_duration = duration_calc(p_start_date, p_end_date) ##################
		p_duration = 0
		p_descrip = request.form['message']
		owner = current_user.username
		color = get_color(p_end_date)
		percents_ready = 0
		# Adding a new project to the projects table.

		for i in range(1, 16):
			try:
				# Getting the form data - levels.
				level_name = request.form["level_name" + str(i)]
				level_start = request.form["level_start" + str(i)]
				level_end = request.form["level_end" + str(i)]
				level_descrip = request.form["level_descrip" + str(i)]
				level_num = i
				from_p = p_name
				level_duration = duration_calc(level_start, level_end)
				p_duration += level_duration
				level_color = get_color(level_end)
				# Adding the project's levels to the levels table.
				add_level(level_name, level_num, level_start,
				level_end, level_duration, level_descrip, from_p, owner, level_color)
			except:
				continue
		# adding the project to the Projects table.
		add_project(p_name, subject, p_start_date,
		p_end_date, p_duration, p_descrip, owner, color, percents_ready)
		# upadating the active projects of the user in the Users table.
		update_active_proj_num(current_user.username)
		levels = return_project_levels(current_user.username, p_name)
		# adjusting the percents of each level.
		fix_sum_percents(levels, p_duration, p_name, current_user.username)
		return redirect('/projects')
	# pulling all user's project from the DB into a hidden input in the html.
	user_projects = return_user_projects(current_user.username)
	all_projects_names = get_name_list(user_projects)
	return render_template("new_project.html", today = today, all_projects_names = all_projects_names,
	all_subjects = all_subjects)

@app.route('/current_proj/<project_name>', methods=['GET', 'POST'])
def current_proj(project_name):
	global current_user
	update_level_color(current_user.username, project_name)
	project_object = return_project(current_user.username, project_name)
	project_levels = return_project_levels(current_user.username, project_object.name)
	due_date = "-"
	if project_object.percents_ready != 100:
		due_level = return_closest_due(project_levels)
		due_date = due_level.end_date
	return render_template("current_proj.html", project_object = project_object, due_date = due_date,
	levels_list = project_levels)


@app.route('/temp_edit', methods=['POST'])
def temp_edit():
	global project_name
	# Get the project name
	project_name = request.form['project_name']
	# Redirect to '/project_edit'
	return redirect('project_edit')
	

@app.route('/project_edit', methods=['GET', 'POST'])
def project_edit():
	global current_user, project_name
	today = datetime.today().strftime('%Y-%m-%d')
	all_levels = return_project_levels(current_user.username, project_name)
	levels_str = make_str_levels(all_levels)
	project_object = return_project(current_user.username, project_name)
	if request.method == 'POST':
		name = request.form["name"]
		start_date = request.form["start_date"]
		end_date = request.form["end_date"]
		subject = request.form["subject"]
		descrip = request.form["message"]

		update_from_proj(current_user.username, project_name, name)
		edit_project(current_user.username, project_name, name, start_date, end_date, subject, descrip)
		return redirect('/projects')
	
	# pulling all user's project from the DB into a hidden input in the html.
	user_projects = return_user_projects(current_user.username)
	all_projects_names = get_name_list(user_projects)	
	subjects = return_subjects()
	return render_template("project_edit.html", project = project_object, today = today,
	levels_str = levels_str, all_projects_names = all_projects_names, subjects = subjects)

@app.route('/temp_edit_level', methods=['POST'])
def temp_edit_level():
	global level_name, project_name
	# Get the level name
	level_name = request.form['level_name']
	project_name = request.form['p_name']
	# Redirect to '/project_edit'
	return redirect('/level_edit')
		
@app.route('/level_edit', methods=['GET', 'POST'])
def level_edit():
	global current_user, level_name, project_name
	today = datetime.today().strftime('%Y-%m-%d')
	project = return_project(current_user.username, project_name)
	project_str = make_str_project(project)
	levels = return_project_levels(current_user.username, project_name)
	if request.method == "POST":
		print(level_name)
		name = request.form["name"]
		start_date = request.form["start_date"]
		end_date = request.form["end_date"]
		descrip = request.form["message"]
		status = request.form["status"]
		is_done_changed = False
		print(status)
		level = return_level(current_user.username, level_name, project_name)
		
		if status != "none":
			is_done_changed  = True
		
			
		# Edit the level's info.
		edit_level(current_user.username, project_name, level_name, 
		name, is_done_changed , start_date, end_date, descrip)

		if format_date(start_date) != format_date(level.start_date)  or format_date(end_date) != format_date(level.end_date):
			new_duration = duration_calc(start_date, end_date)
			update_level_duration(current_user.username, project_name, level_name, new_duration)

			levels = return_project_levels(current_user.username, project_name)
			project = return_project(current_user.username, project_name)
			p_duration = calc_new_duration(levels)
			update_project_duration(current_user.username, project_name, p_duration)
			update_level_percents(current_user.username, project_name, level_name, project.duration, new_duration)
		# Updating the percents of the project.
		levels = return_project_levels(current_user.username, project_name)
		new_percents = percents_ready(levels)
		update_percents(current_user.username, project_name, new_percents)
		# redirect to projects.
		return redirect('/projects')
	level_object = return_level(current_user.username, level_name, project_name)
	return render_template("edit_level.html", level = level_object, today = today, project_str = project_str,
	)

@app.route('/delete_proj', methods=['GET', 'POST'])
def delete_proj():
	global current_user
	# Get the delete name
	project_name = request.form['project_name']
	project = return_project(current_user.username, project_name)
	delete_project(current_user.username, project_name)
	# Delete the project's levels:
	delete_all_levels(current_user.username, project_name)
	
	return redirect('/projects')

@app.route('/del_level', methods=['POST'])
def del_level():
	global current_user
	# Get the delete info
	project_name = request.form['from_p']
	level_name = request.form['del_level_name']
	level_num = request.form["num"]
	# delete the requested level.
	delete_level(current_user.username, project_name, level_name, level_num)
	# check if there are other levels in the project. if not, delete the project.
	levels = return_project_levels(current_user.username, project_name)
	if not levels:
		delete_project(current_user.username, project_name)
		return redirect('/projects')
	# calc the new duration of the project, change the percents of other levels.
	new_proj_duration = calc_new_duration(levels)
	fix_sum_percents(levels, new_proj_duration, project_name, current_user.username)
	# update the duration of the project.
	update_project_duration(current_user.username, project_name, new_proj_duration)	
	return redirect('/projects')


@app.route('/forums', methods=['GET', 'POST'])
def forums():
	global current_user
	if request.method == 'POST':
		title = request.form["title"]
		content = request.form["content"]
		subject = request.form["forum_q_subject"]
		date = datetime.today().strftime("%Y-%m-%d")
		hour = str(datetime.today().hour) + ":" + str(datetime.today().minute)
		# Adding a new chat to a forum
		open_new_chat(title, content, current_user.username, date, hour, subject)
		# Notifying all members about the new question.
		forum_members = find_relevant_recipients(current_user.username, subject)
		for user in forum_members:
			sub_line = "התקבלה שאלה חדשה בפורום: " + subject
			msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user.email])
			msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> למישהו יש שאלה בפורום! תוכן השאלה: " + content + "</h3>"
			with app.app_context():
				mail.send(msg)
	open_subjects = get_user_subjects(current_user.username)
	open_chats = return_chats_dict(open_subjects) 
	return render_template("forums.html", open_chats = open_chats, user = current_user)


@app.route('/single_forum_temp', methods=['POST'])
def single_forum_temp():
	global clicked_chat_id
	clicked_chat_id = request.form["chat_id"]
	return redirect('/single_forum')


@app.route('/single_forum', methods=['GET','POST'])
def single_forum():
	global current_user, clicked_chat_id
	chat = return_chat(int(clicked_chat_id))
	if request.method == 'POST':
		content = request.form["reply"]
		date = datetime.today().strftime("%Y-%m-%d")
		hour = str(datetime.today().hour) + ":" + str(datetime.today().minute)
		# Adding the new reply to the DB
		add_message(content, current_user.username, date, hour, chat.subject, chat.title, chat.id)
		# Updating the num_messages by 1
		if current_user.username != chat.user:
			update_num_messages(chat.id)
		# Notifying the user who asked the question about a new reply
		if chat.num_messages < 3: #make sure to check who sent it
			user_sent = return_user(chat.user)
			sub_line = "התקבלה תשובה חדשה בפורום: " + chat.subject
			msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user_sent.email])
			msg.html = "<h3 dir='rtl'> תוכן התשובה: " + content + "</h3>"
			with app.app_context():
				mail.send(msg)
	messages = return_chat_messages(chat.title, chat.subject, chat.id)
	return render_template("single_forum.html", chat = chat, messages = messages)  


@app.route('/data', methods=['GET'])
def data():
	num_users = len(return_all_users())
	late_num = get_late_num()
	all_projects = total_proj_num()
	active_projects = total_active_proj_num()
	added = added_monthly()
	num_chats = len(return_all_chats())
	sent = sent_monthly()
	num_subjects = len(return_subjects())
	return render_template("admin_data.html", num_users = num_users, late_num = late_num,
	all_projects = all_projects, active_projects = active_projects, added = added, num_chats = num_chats, 
	sent = sent, num_subjects = num_subjects)


@app.route('/delete_user', methods=['POST'])
def delete_user():
	user_id = request.form["user_id"]
	user = return_user_by_id(user_id)
	delete_all_projects(user.username)
	delete_all_user_levels(user.username)
	delete_user_from_db(user_id)
	return redirect('/users_table')


@app.route('/block_user', methods=['POST'])
def block_user():
	user_id = request.form["user_id"]
	user = return_user_by_id(user_id)
	if user.is_blocked:
		unblock_user(user_id)
		return redirect('/users_table')
	block_user_forums(user_id)
	return redirect('/users_table')


@app.route('/users_table', methods=['GET', 'POST'])
def users_table():
	users = return_all_users()
	return render_template("admin_users.html", users = users)

@app.route('/admin_subjects', methods=['GET', 'POST'])
def admin_subjects():
	subjects = return_subjects()
	return render_template("admin_subjects.html", subjects = subjects)


def notification_center():
	users = return_all_users()
	for user in users:
		user_alerts = project_submission_alert(user)
		if len(user_alerts.keys()) > 0:
			for project in user_alerts:
				project_object = return_project(user.username, project)
				if not project_object.first_alert and user_alerts[project] == 1: 
					msg = Message("תאריך הגשה של פרוייקט מתקרב", sender = 'taskitMail@gmail.com', recipients = [user.email])
					msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של הפרוייקט: " + project + " הוא מחר! " + "</h3>"
					with app.app_context():
						mail.send(msg)
					update_alert_status(user.username, project_object.name, 1)
				elif not project_object.second_alert and user_alerts[project] == 2: 
					msg = Message("תאריך הגשה של פרוייקט", sender = 'taskitMail@gmail.com', recipients = [user.email])
					msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של הפרוייקט: " + project + "הוא היום!" + "</h3>"
					with app.app_context():
						mail.send(msg)
					update_alert_status(user.username, project_object.name, 2)
				elif not project_object.third_alert and user_alerts[project] == 3: 
					msg = Message("תאריך הגשה של פרוייקט חלף...", sender = 'taskitMail@gmail.com', recipients = [user.email])
					msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של הפרוייקט: " + project + " היה אתמול והפרוייקט לא הוגש." + "</h3>"
					with app.app_context():
						mail.send(msg)	
					update_alert_status(user.username, project_object.name, 3)	


		# levels nontifications.
		user_total_projects = return_user_projects(user.username)
		for project_object in user_total_projects:
			levels = return_project_levels(user.username, project_object.name)	
			levels_alerts = level_submission_alert(user, levels)
			if len(levels_alerts.keys()) > 0:
				for level in levels_alerts:
					level_object = return_level(user.username, level, project_object.name)
					if not level_object.first_alert and levels_alerts[level] == 1: 
						msg = Message("תאריך הגשה של שלב מתקרב", sender = 'taskitMail@gmail.com', recipients = [user.email])
						msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של השלב: " + level + " הוא מחר! " + "</h3>"
						with app.app_context():
							mail.send(msg)
						update_level_alert_status(user.username, level_object.name, project_object.name, 1)
					elif not level_object.second_alert and levels_alerts[level] == 2: 
						msg = Message("תאריך הגשה של שלב", sender = 'taskitMail@gmail.com', recipients = [user.email])
						msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של השלב: " + level + "הוא היום!" + "</h3>"
						with app.app_context():
							mail.send(msg)
						update_level_alert_status(user.username, level_object.name, project_object.name, 2)
					elif not level_object.third_alert and levels_alerts[level] == 3: 
						msg = Message("תאריך הגשה של שלב חלף...", sender = 'taskitMail@gmail.com', recipients = [user.email])
						msg.html = "<h1 dir='rtl'>" + user.username + ",</h1> <h3 dir='rtl'> תאריך ההגשה של הפרוייקט: " + level + " היה אתמול והשלב לא הוגש." + "</h3>"
						with app.app_context():
							mail.send(msg)	
						update_level_alert_status(user.username, level_object.name, project_object.name, 3)	

	threading.Timer(60.0, notification_center).start()
	


if __name__ == '__main__':
# check date, send messages?
	app.run(debug = False)
	#, ssl_context = "adhoc"