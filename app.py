from flask import *
from model import *
from databases import *
from server_funcs import *
from flask_mail import *
from datetime import datetime
import threading
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'taskitMail'
app.config['MAIL_PASSWORD'] = 'mlsoybdtjnahqfmt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
db.app = app
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	default_subjects = ["אנגלית", "מתמטיקה", "מדעי המחשב", "מדעי החברה", "סייבר", "ביולוגיה", "פיזיקה", "אומנות"]
	notification_center() 
	# adding default sbjects to the DB.
	check_subjects = return_subjects()
	if not check_subjects:
		add_subjects(default_subjects)
	admin = return_user("taskitAdmin")
	if not admin:
		add_user("taskitAdmin", "taskitAdmin", "taskitmail@gmail.com")
	msg = ""
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		users_list = return_all_users()

		if username == "taskitAdmin" and password == "taskitAdmin":
			return redirect("/data")
		
		for user in users_list:
			if user.username == username and user.password == password:
				
				return redirect(url_for('projects', username = username))
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
			return redirect(url_for("index"))
	return render_template("signup.html", msg = msg)


@app.route('/manage_user_cookies', methods=['POST'])
def manage_user_cookies():
	username = request.form["user_ajax"]
	page = request.form["page"]
	if page == "projects":
		return redirect(url_for('projects', username = username))
	
	return redirect('/')


@app.route('/projects/<username>', methods=['GET', 'POST'])
def projects(username):
	current_user = return_user(username)
	update_proj_color(current_user.username)
	if request.method == 'POST':
		# Get the project out of the DB
		clicked_proj = request.form['project_name']
		# Redirect to '/current_proj'
		return redirect(url_for('current_proj', username = username, project_name = clicked_proj))

	# Pull from the project table all projects related to the user.
	# Put it in a list.
	# Get the date of the closest due date.
	# get the user's porjects and levels from the db.
	user_projects = return_user_projects(current_user.username)
	projects_due_dict = {}
	if current_user.total_porject_num != 0:
		# checking the percents of the project and levels.
		user_projects = verify_user_projects(current_user.username, user_projects)
		
		for project in user_projects:
			levels = return_project_levels(current_user.username, project.name)
			projects_due_dict[project] = return_closest_due(levels)
			
	return render_template("projects.html", user_projects = projects_due_dict, username = username)

@app.route('/new_project/<username>', methods=['GET', 'POST'])
def new_project(username):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	all_subjects = return_subjects()
	today = datetime.today().strftime('%Y-%m-%d')
	if request.method == 'POST':
		# Getting the form data - project info.
		p_name = request.form['name']
		subject = request.form['subject']
		p_start_date = request.form['start_val']
		p_end_date = request.form['end_val']
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
		return redirect(url_for("projects", username = current_user.username))
	# pulling all user's project from the DB into a hidden input in the html.
	user_projects = return_user_projects(current_user.username)
	all_projects_names = get_name_list(user_projects)
	return render_template("new_project.html", today = today, all_projects_names = all_projects_names,
	all_subjects = all_subjects, username = username)

@app.route('/current_proj/<username>/<project_name>', methods=['GET', 'POST'])
def current_proj(username, project_name):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# Updating the colors of the project's levels, pulling data from DB.
	update_level_color(current_user.username, project_name)
	project_object = return_project(current_user.username, project_name)
	project_levels = return_project_levels(current_user.username, project_object.name)
	# Presenting closest due date to the user. If there is none, the due is "-".
	due_date = "-"
	if project_object.percents_ready != 100:
		due_level = return_closest_due(project_levels)
		due_date = due_level.end_date
	return render_template("current_proj.html", project_object = project_object, due_date = due_date,
	levels_list = project_levels, username = username)


@app.route('/temp_edit', methods=['POST'])
def temp_edit():
	# Get the project name
	username = request.form['username']
	project_name = request.form['project_name']
	# Redirect to '/project_edit'
	return redirect(url_for('project_edit', username = username, project_name = project_name))
	

@app.route('/project_edit/<username>/<project_name>', methods=['GET', 'POST'])
def project_edit(username, project_name):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# Pulling data from DB.
	today = datetime.today().strftime('%Y-%m-%d')
	all_levels = return_project_levels(current_user.username, project_name)
	levels_str = make_str_levels(all_levels)
	project_object = return_project(current_user.username, project_name)
	# When the user edits the project:
	if request.method == 'POST':
		name = request.form["name"]
		start_date = request.form["start_date"]
		end_date = request.form["end_date"]
		subject = request.form["subject"]
		descrip = request.form["message"]

		update_from_proj(current_user.username, project_name, name)
		edit_project(current_user.username, project_name, name, start_date, end_date, subject, descrip)

	
	# Pulling all user's project from the DB into a hidden input in the html.
	user_projects = return_user_projects(current_user.username)
	all_projects_names = get_name_list(user_projects)	
	subjects = return_subjects()
	return render_template("project_edit.html", project = project_object, today = today,
	levels_str = levels_str, all_projects_names = all_projects_names, subjects = subjects, username = username)

@app.route('/temp_edit_level', methods=['GET','POST'])
def temp_edit_level():
	# Get the level name
	level_name = request.form['level_name']
	project_name = request.form['p_name']
	username = request.form["username"]
	# Redirect to '/level_edit'
	return redirect(url_for('level_edit', username = username, level_name = level_name, project_name = project_name))
		
@app.route('/level_edit/<username>/<level_name>/<project_name>', methods=['GET', 'POST'])
def level_edit(username, level_name, project_name):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# Pulling data from DB.
	today = datetime.today().strftime('%Y-%m-%d')
	project = return_project(current_user.username, project_name)
	project_str = make_str_project(project)
	levels = return_project_levels(current_user.username, project_name)
	# When the user edits a level:
	if request.method == "POST":
		name = request.form["name"]
		start_date = request.form["start_date"]
		end_date = request.form["end_date"]
		descrip = request.form["message"]
		status = request.form["status"]
		is_done_changed = False
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
	level_object = return_level(current_user.username, level_name, project_name)
	return render_template("edit_level.html", level = level_object, today = today, project_str = project_str,
	username = username, project_name = project_name)

@app.route('/delete_proj', methods=['POST'])
def delete_proj():
	username = request.form["username"]
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# Get the delete name
	project_name = request.form['project_name']
	delete_project(current_user.username, project_name)
	# Delete the project's levels:
	delete_all_levels(current_user.username, project_name)
	return redirect(url_for('projects', username = username))


@app.route('/del_level', methods=['POST'])
def del_level():
	username = request.form["username"]
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# Get the delete info
	project_name = request.form['from_p']
	level_name = request.form['del_level_name']
	level_num = request.form["num"]
	# delete the requested level.
	delete_level(current_user.username, project_name, level_name, level_num)
	# check if there are other levels in the project. if not, delete the project.
	levels = return_project_levels(current_user.username, project_name)
	if not levels:
		if current_user == None:
			return redirect('/')
		delete_project(current_user.username, project_name)
		return redirect(url_for('projects', username = username))
	# calc the new duration of the project, change the percents of other levels.
	new_proj_duration = calc_new_duration(levels)
	fix_sum_percents(levels, new_proj_duration, project_name, current_user.username)
	# update the duration of the project.
	update_project_duration(current_user.username, project_name, new_proj_duration)	
	return redirect(url_for('projects', username = username))


@app.route('/forums/<username>', methods=['GET', 'POST'])
def forums(username):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	# When a new question is sent:
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
	return render_template("forums.html", open_chats = open_chats, user = current_user, username = username)


@app.route('/single_forum_temp', methods=['POST'])
def single_forum_temp():
	# Finding the relevant chat to open
	clicked_chat_id = request.form["chat_id"]
	username = request.form["username"]
	# Redirect to /single_forum
	return redirect(url_for('single_forum', username = username, clicked_chat_id = clicked_chat_id))


@app.route('/single_forum/<username>/<clicked_chat_id>', methods=['GET','POST'])
def single_forum(username, clicked_chat_id):
	current_user = return_user(username)
	if current_user == None:
		return redirect('/')
	chat = return_chat(int(clicked_chat_id))
	if request.method == 'POST':
		chat = return_chat(int(clicked_chat_id))
		content = request.form["reply"]
		date = datetime.today().strftime("%Y-%m-%d")
		hour = str(datetime.today().hour) + ":" + str(datetime.today().minute)
		# Adding the new reply to the DB
		add_message(content, current_user.username, date, hour, chat.subject, chat.title, chat.id)
		# Updating the num_messages by 1
		if current_user.username != chat.user:
			update_num_messages(chat.id)
		# Notifying the user who asked the question about a new reply
		user_sent = return_user(chat.user)
		if chat.num_messages < 3 and current_user.username != user_sent.username: 
			sub_line = "התקבלה תשובה חדשה בפורום: " + chat.subject
			msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user_sent.email])
			msg.html = "<h3 dir='rtl'> תוכן התשובה: " + content + "</h3>"
			with app.app_context():
				mail.send(msg)
	messages = return_chat_messages(chat.title, chat.subject, chat.id)
	return render_template("single_forum.html", chat = chat, messages = messages, username = username, 
	clicked_chat_id = clicked_chat_id)  


@app.route('/data', methods=['GET'])
def data():
	# Calculating usage data of the website
	num_users = len(return_all_users()) - 1
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
	# Deleting a user by the Admin
	user_id = request.form["user_id"]
	user = return_user_by_id(user_id)
	delete_all_projects(user.username)
	delete_all_user_levels(user.username)
	delete_user_from_db(user_id)
	# Notifying the user 
	sub_line = "הודעה על הסרת חשבון"
	msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user.email])
	msg.html = "<h3 dir='rtl'> זוהי הודעה על מחיקת חשבונך על ידי מנהל האתר. במידה ומדובר בטעות, השב להודעה זו.</h3>"
	with app.app_context():
		mail.send(msg)
	return redirect('/users_table')


@app.route('/block_user', methods=['POST'])
def block_user():
	user_id = request.form["user_id"]
	user = return_user_by_id(user_id)
	# Unblocking a user from all forums
	if user.is_blocked:
		unblock_user(user_id)
		# Notifying the user
		sub_line = "הודעה על ביטול חסימה מפורומים"
		msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user.email])
		msg.html = "<h3 dir='rtl'> זוהי הודעה על ביטול חסימת חשבונך מכל הפורומים, על ידי מנהל האתר. במידה ומדובר בטעות, השב להודעה זו.</h3>"
		with app.app_context():
			mail.send(msg)
		return redirect('/users_table')
	# Blocking a user from all forums
	block_user_forums(user_id)
	# Notifying the user
	sub_line = "הודעה על חסימה מפורומים"
	msg = Message(sub_line, sender = 'taskitMail@gmail.com', recipients = [user.email])
	msg.html = "<h3 dir='rtl'> זוהי הודעה על חסימת חשבונך מכל הפורומים, על ידי מנהל האתר. במידה ומדובר בטעות, השב להודעה זו.</h3>"
	with app.app_context():
		mail.send(msg)
	return redirect('/users_table')


@app.route('/users_table', methods=['GET'])
def users_table():
	# Showing the Admin 2 tables - users and chats.
	users = return_all_users()
	chats = return_all_chats()
	return render_template("admin_users.html", users = users, chats = chats)


@app.route('/delete_chat', methods=['POST'])
def delete_chat():
	# Deleting a chat
	chat_id = request.form["chat_id"]
	chat = return_chat(int(chat_id))
	delete_chat_DB(chat_id, chat.title)
	return redirect('/users_table')


@app.route('/admin_subjects', methods=['GET', 'POST'])
def admin_subjects():
	subjects = return_subjects()
	# adding a new subject to the list:
	if request.method == 'POST':
		new_subject = request.form["new_subject"]
		add_subject(new_subject)
		subjects = return_subjects()
	return render_template("admin_subjects.html", subjects = subjects)


@app.route('/admin_subjects_delete', methods=['POST'])
def admin_subjects_delete():
	# Deleting a subject
	subject_id = request.form["subject_id"]
	delete_subject(subject_id)
	return redirect('/admin_subjects')


def notification_center():
	users = return_all_users()
	# Looping through all users, sending relevant emails about due dates of projects and levels
	for user in users:
		user_alerts = project_submission_alert(user)
		# Projects notifications
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


		# levels notifications.
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

	threading.Timer(30.0, notification_center).start()
	


if __name__ == '__main__':
	db.create_all()
	app.run(debug = False)
