from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import ipdb

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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

@app.get("/api/v1/4d/result")
def latest_result():
    with app.app_context():
        last = Fourds.query.first()
        # ipdb.set_trace()
        # refactor below
        result = {'draw_date': last.drawdate, 'draw_number': last.drawnumber, 'first': last.first,
                  'second': last.second, 'third': last.third, 'starter': last.starter.replace('{', '').replace('}', ''), 'consolation': last.consolation.replace('{', '').replace('}', '')}

        return jsonify(result)
