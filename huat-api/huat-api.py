from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import ipdb
from datetime import datetime

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

@app.route("/api/v1/4d/result", methods=['GET','POST'])
def latest_result():
    with app.app_context():
        if request.method == 'POST':
            data = request.get_json()
            print(data)
            # date_string = "4/1/2023"
            date_format = "%d/%m/%Y"
            date_object = datetime.strptime(data['date'], date_format).date()
            date_result = Fourds.query.filter(Fourds.drawdate == date_object).first()
            # ipdb.set_trace()
            result = {'draw_date': date_result.drawdate, 'draw_number': date_result.drawnumber, 'first': date_result.first,
                      'second': date_result.second, 'third': date_result.third, 'starter': date_result.starter.replace('{', '').replace('}', ''), 'consolation': date_result.consolation.replace('{', '').replace('}', '')}
            return jsonify(result)
            # print(date_object)
            # post request here
            # return 'post request'
        else:
            last = Fourds.query.first()
        # ipdb.set_trace()
        # refactor below
            result = {'draw_date': last.drawdate, 'draw_number': last.drawnumber, 'first': last.first,
                  'second': last.second, 'third': last.third, 'starter': last.starter.replace('{', '').replace('}', ''), 'consolation': last.consolation.replace('{', '').replace('}', '')}
            return jsonify(result)

@app.get("/api/v1/4d/dates")
def get_dates():
    with app.app_context():
        dates = Fourds.query.with_entities(Fourds.drawdate).all()
        # ipdb.set_trace()
        # convert query rows to list
        date_list = [list(date) for date in dates]
        # flatten the list
        date_list = [item for items in date_list for item in items]
        result = {'dates': date_list}
        return jsonify(result)
