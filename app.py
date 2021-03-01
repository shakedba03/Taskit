from flask import *
from model import *
from databases import *
from handle_dates import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"

current_user = None

@app.route('/', methods=['GET', 'POST'])
def index():
	global current_user
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		users_list = return_all_users()

		for user in users_list:
			if user.username == username and user.password == password:
				# get the user's porjects and levels from the db.
				current_user = return_user(username)
				print(current_user.username)
				return render_template("projects.html")
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
				# if the emails are the same - what happens? can someone have 2 users?
				msg = "שם המשתמש שהוזן כבר קיים במערכת. אנא בחרו שם משתמש אחר!"

		if password != password2:
			msg = "אימות הסיסמה אינו תואם לסיסמה שהוזנה."
		if msg == "":
			add_user(username, password, email)
			return render_template("index.html")
	return render_template("signup.html", msg = msg)

@app.route('/projects')
def projects():
	
	return render_template("projects.html")

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
	global current_user
	today = datetime.today().strftime('%Y-%m-%d')
	if request.method == 'POST':
		p_name = request.form['name']
		subject = request.form['subject']
		p_start_date = request.form['start_date']
		p_end_date = request.form['end_date']
		p_duration = duration_calc(p_start_date, p_end_date)
		p_descrip = request.form['message']
		owner = current_user.username
		add_project(p_name, subject, p_start_date, p_end_date, p_duration, p_descrip, owner)
		print("ADDED")
		# new_project_data = request.form
		# for key in f.keys():
		# 	for value in f.getlist(key):
		# 		print(key,":",value)

		return render_template("projects.html", today = today)
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