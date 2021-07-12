from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 1

app = Flask(__name__)
app.config['SECRET_KEY'] = "xxxxxxxx"    # 2

db = SQLAlchemy(app)

# our database uri
username = "user2"
password = "password"
dbname = "ourdb"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{username}:{password}@localhost:5432/{dbname}"

if __name__ == "__main__":
    app.run()
