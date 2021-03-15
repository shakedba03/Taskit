from flask import *
from model import *
from databases import *
from server_funcs import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

current_user = None


@app.route('/', methods=['GET', 'POST'])
def index():
	global current_user, user_projects
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		users_list = return_all_users()

		for user in users_list:
			if user.username == username and user.password == password:
				# get the user's porjects and levels from the db.
				current_user = return_user(username)
				user_projects = return_user_projects(current_user.username)
				# print(current_user.username) ---> DELETE IT
				# print("after login: TOTAL PROJECTS NUM is " + str(current_user.total_porject_num)) ---> DELETE IT
				return redirect('/projects')
	return render_template("index.html")
	
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
				# if the emails are the same - what happens? can someone have 2 users?---> DELETE IT
				msg = "שם המשתמש שהוזן כבר קיים במערכת. אנא בחרו שם משתמש אחר!"

		if password != password2:
			msg = "אימות הסיסמה אינו תואם לסיסמה שהוזנה."
		if msg == "":
			add_user(username, password, email)
			return render_template("index.html")
	return render_template("signup.html", msg = msg)

@app.route('/projects')
def projects():
	global current_user
	all_levels_projects_dict = {}
	# Pull from the project table all projects related to the user.
	# Put it in a list.
	# Get the date of the closest due date.
	current_user = return_user(current_user.username)
	user_projects = return_user_projects(current_user.username)
	# print("at all projects: TOTAL PROJECTS NUM is " + str(current_user.total_porject_num)) ---> DELETE IT
	if current_user.total_porject_num != 0:
		all_levels_projects_dict = user_projects_levels_full(current_user.username, user_projects)
		print(all_levels_projects_dict)
	return render_template("projects.html", all_levels_projects_dict = all_levels_projects_dict)

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
	global current_user
	today = datetime.today().strftime('%Y-%m-%d')
	if request.method == 'POST':
		# Getting the form data - project info.
		p_name = request.form['name']
		subject = request.form['subject']
		p_start_date = request.form['start_val']
		p_end_date = request.form['end_val']
		p_duration = duration_calc(p_start_date, p_end_date)
		p_descrip = request.form['message']
		owner = current_user.username
		color = get_color(p_end_date)
		percents_ready = 0
		# Adding a new project to the projects table.
		
		add_project(p_name, subject, p_start_date,
					p_end_date, p_duration, p_descrip, owner, color, percents_ready)
		# Print results. ---> DELETE IT
		# print("ADDED")
		# print("***NEW PROJECT INFO:")
		# print("Name: " + p_name + '\n' +
		# "Subject: " + subject + '\n' +
		# "Start Date: " + p_start_date + '\n' +
		# "End Date: " + p_end_date + '\n' +
		# "Duration: " + str(p_duration) + '\n' +
		# "Description: " + p_descrip + '\n' +
		# "Owner: " + owner)
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
				percent = (level_duration / p_duration) * 100
				level_color = get_color(level_end)
				# Adding the project's levels to the levels table.
				add_level(level_name, level_num, level_start,
				level_end, level_duration, percent, level_descrip, from_p, owner, level_color)
				# Print results. ---> DELETE IT
				# print("ADDED LEVEL")
				# print("Name: " + level_name + '\n' +
				# "Num: " + str(level_num) + '\n' +
				# "Start Date: " + level_start + '\n' +
				# "End Date: " + level_end + '\n' +
				# "Duration: " + str(level_duration) + '\n' +
				# "Description: " + level_descrip + '\n' +
				# "Owner: " + owner)
			except:
				# print("PASS...") ---> DELETE IT
				pass
		
		update_active_proj_num(current_user.username)
		# current_user = return_user(current_user.username)
		return render_template("projects.html")
	return render_template("new_project.html", today = today)

@app.route('/current_proj')
def current_proj():
	return render_template("current_proj.html")

@app.route('/project_edit', methods=['GET', 'POST'])
def project_edit():
	if request.method == "POST":
		print(request.form["name"])
		return render_template("projects.html")	
	return render_template("project_edit.html")

@app.route('/edit_level', methods=['GET', 'POST'])
def edit_level():
	if request.method == "POST":
		return redirect("projects.html")	
	return render_template("edit_level.html")

if __name__ == '__main__':
    app.run(debug=True)
