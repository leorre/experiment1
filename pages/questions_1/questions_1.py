import psycopg2
from flask import Blueprint, render_template, request, session, redirect

# events blueprint definition
questions_1 = Blueprint('questions_1', __name__, static_folder='static', static_url_path='/questions_1', template_folder='templates')


# Routes
@questions_1.route('/questions_1', methods=['GET', 'POST'])
def questions_12():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        exp = request.form['experience']
        device = request.form['device']
        native = request.form['native']
        query = """UPDATE "users" SET "age" = '%s', "gender" = '%s', "experience" = '%s', "device" = '%s', "native" = '%s'
                 WHERE "id" = '%s'""" % (age, gender, exp, device, native, session['code'])
        interact_db(query=query, query_type='commit')
        return redirect('/questions_2')
    return render_template('questions_1.html')


# DB connection
def interact_db(query, query_type: str):
    return_value = False
    connection = psycopg2.connect(host='localhost', user='postgres', password='root', database='postgres')
    cursor = connection.cursor()
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

