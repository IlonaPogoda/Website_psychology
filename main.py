from flask import Flask, render_template
from flask import redirect, url_for, make_response, request
from dbtest import DataBase
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print('Get method')
    elif request.method == 'POST':
        form = request.form

        user_data = {
            'name': form['name'],
            'surname': form['surname'],
            'email': form['email'],
            'password': form['password']
        }

        db = DataBase()
        db.addUser(user_data)

    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('registration.html')


@app.route('/appointment')
def appoint():
    user_data_str = request.cookies.get('user_data')
    if user_data_str != None and user_data_str != '':
        return render_template('appointment.html', time_list=[f"{i}:00" for i in range(9, 23)])
    else:
        return make_response(redirect(url_for('join')))


@app.route('/signout')
def signout():
    resp = make_response(redirect('/'))
    resp.set_cookie('user_data', '')
    return resp

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        user_data_str = request.cookies.get('user_data')
        if user_data_str != None and user_data_str != '':
            return make_response(redirect(url_for('profile')))
        else:
            return render_template('join.html')
    elif request.method == 'POST':
        form = request.form
        user_data = {
            'email': form['email'],
            'password': form['password']
        }

        db = DataBase()
        res = db.checkUser(user_data)

        if res == 1:
            user_data_str = json.dumps(user_data)
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('user_data', user_data_str)
            return resp
        else:
            return render_template('join.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_data_str = request.cookies.get('user_data')
    if user_data_str != None and user_data_str != '':
        user_data = json.loads(user_data_str)
        db = DataBase()
        all_data = db.getFullUserData(user_data)
        all_notes = db.getUserNotes(all_data[0])
        return render_template('profile.html',
            user_name=all_data[1] + " " + all_data[2],
            notes_list=all_notes
        )
    else:
        return redirect(url_for('join'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/noteprocess', methods=['POST']) #обработка записи
def noteProcess():
    doctor_desc={
        'gender': request.form['gender'],
        'direction': request.form['type']
    }

    db = DataBase()
    doctor_data = db.getDoctor(doctor_desc) #Подбор врача

    user_data_str = request.cookies.get('user_data')
    user_data = json.loads(user_data_str)

    full_user_data = db.getFullUserData(user_data)

    note_data={
        'user_id': full_user_data[0],
        'doctor_id': doctor_data[0],
        'reason': 'Консультация',
        'date': request.form['date'] + ' ' + request.form['time']
    }

    db.addNote(note_data)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False)
