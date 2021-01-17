from flask import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


@app.route('/')
def index():
	return render_template("projects.html")

@app.route('/signup')
def signup():
	return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)