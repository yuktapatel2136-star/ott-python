from flask import Flask, render_template
app = Flask(__name__)
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

with app.app_context():
    db.create_all()

@app.route("/")
def index():
   return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        user = User.query.filter_by(username=username).first()

        # Check username & password
        if user and check_password_hash(user.password, password):
            flash("Login successful ✅")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")

    return render_template('login.html')


@app.route("/registration")
def registration():
   return render_template("registration.html")

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/pricing")
def pricing():
   return render_template("pricing.html")

@app.route("/movielist")
def movielist():
   return render_template("movielist.html")

@app.route("/faq")
def faq():
   return render_template("faq.html")

if __name__ == '__main__':
   app.run(debug = True)