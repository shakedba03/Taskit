from flask import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


@app.route('/')
def index():
	return render_template("projects.html")
	
@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/projects')
def projects():
	return render_template("projects.html")

@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
	if request.method == 'POST':
		f = request.form
		for key in f.keys():
			for value in f.getlist(key):
				print(key,":",value)
	return render_template("new_project.html")

@app.route('/current_proj')
def current_proj():
	return render_template("current_proj.html")

if __name__ == '__main__':
    app.run(debug=True)