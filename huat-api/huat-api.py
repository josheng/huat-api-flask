from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import ipdb
from datetime import datetime

app = Flask(__name__)
# prevent sorting of json result by alphabetical order
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

@app.route("/api/v1/4d/result", methods=['GET','POST'])
def latest_result():
    with app.app_context():
        if request.method == 'POST':
            data = request.get_json()
            # drawdate is required
            try:
                data['drawdate']
            except KeyError:
                return jsonify({"error": "please provide the drawdate"})
            date_format = "%d/%m/%Y"
            date_object = datetime.strptime(data['drawdate'], date_format).date()
            date_result = Fourds.query.filter(Fourds.drawdate == date_object).first()
            result = {'draw_date': date_result.drawdate, 'draw_number': date_result.drawnumber, 'first': date_result.first,
                      'second': date_result.second, 'third': date_result.third, 'starter': date_result.starter.replace('{', '').replace('}', ''), 'consolation': date_result.consolation.replace('{', '').replace('}', '')}
            # check if got number in json
            try :
                data['number']
            except KeyError:
            # just return dated result
                return jsonify(result)
            else:
            # else return winnings if there is
                fullresult = result | check_result(
                    data['number'], data['bet'], result)
                return jsonify(fullresult)
        else:
            # GET
            last = Fourds.query.first()
            # refactor below
            result = {'draw_date': last.drawdate, 'draw_number': last.drawnumber, 'first': last.first,
                  'second': last.second, 'third': last.third, 'starter': last.starter.replace('{', '').replace('}', ''), 'consolation': last.consolation.replace('{', '').replace('}', '')}
            return jsonify(result)

def check_result(number, bet, result):
    matched = []
    total = 0
    prize = 0
    for index, num in enumerate(number):
        if result['first'] == num:
            prize = calc_winning_bet(bet[index], 'first')
            matched.append(f'first: {num}, prize: {prize}')
        if result['second'] == num:
            prize = calc_winning_bet(bet[index], 'second')
            matched.append(f'second: {num}, prize: {prize}')
        if result['third'] == num:
            prize = calc_winning_bet(bet[index], 'third')
            matched.append(f'third: {num}, prize: {prize}')
        if num in result['starter']:
            prize = calc_winning_bet(bet[index], 'starter')
            matched.append(f'starter: {num}, prize: {prize}')
        if num in result['consolation']:
            prize = calc_winning_bet(bet[index], 'consolation')
            matched.append(f'consolation: {num}, prize: {prize}')
        if prize: total += prize
    if len(matched) == 0: matched = 'no winning numbers'
    return { 'winningnumber': matched, 'totalwinnings': total }

def calc_winning_bet(bet, category):
    # prize structure based on official website
    total = 0
    prize = {'big1': 2000, 'small1': 3000, 'big2': 1000, 'small2': 2000,
             'big3': 490, 'small3': 800, 'bigs': 250, 'bigc': 60}
    match category:
        case 'first':
            total = (bet['b'] * prize['big1']) + (bet['s'] * prize['small1'])
        case 'second':
            total = (bet['b'] * prize['big2']) + (bet['s'] * prize['small2'])
        case 'third':
            total = (bet['b'] * prize['big3']) + (bet['s'] * prize['small3'])
        case 'starter':
            total = bet['b'] * prize['bigs']
        case 'consolation':
            total = bet['b'] * prize['bigc']
    return total

@app.get("/api/v1/4d/dates")
def get_dates():
    with app.app_context():
        dates = Fourds.query.with_entities(Fourds.drawdate).all()
        # convert query rows to list
        date_list = [list(date) for date in dates]
        # flatten the list
        date_list = [item for items in date_list for item in items]
        result = {'dates': date_list}
        return jsonify(result)
