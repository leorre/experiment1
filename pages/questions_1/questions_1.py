import psycopg2
from flask import Blueprint, render_template, request, session, redirect
from dbUtils import interact_db
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
        query = """UPDATE "users" SET "age" = '%s', "gender" = '%s', "experience" = '%s', "device" = '%s'
                 WHERE "id" = '%s'""" % (age, gender, exp, device, session['code'])
        interact_db(query=query, query_type='commit')
        return redirect('/questions_2')
    return render_template('questions_1.html')


