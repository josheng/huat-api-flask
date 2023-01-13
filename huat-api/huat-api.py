from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import ipdb

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/huat_api_flask'
db = SQLAlchemy(app)

db.init_app(app)

class Fourds(db.Model):
    __tablename__ = 'fourds'
    id = db.Column(db.Integer, primary_key=True)
    drawnumber = db.Column(db.String)
    drawdate = db.Column(db.Date)
    first = db.Column(db.String)
    second = db.Column(db.String)
    third = db.Column(db.String)
    starter = db.Column(db.String)
    consolation = db.Column(db.String)

# fourds = Fourds.query.all()

# ipdb.set_trace()

@app.route("/")
def hello_world():
    with app.app_context():
        last = Fourds.query.first()
        # ipdb.set_trace()
        result = {'draw_date': last.drawdate, 'draw_number': last.drawnumber, 'first': last.first,
                  'second': last.second, 'third': last.third, 'starter': last.starter, 'consolation': last.consolation}

        return jsonify(result)
