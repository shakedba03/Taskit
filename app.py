from flask import *

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


@app.route('/')
def index():
	return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)