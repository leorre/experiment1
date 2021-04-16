import psycopg2
from flask import Blueprint, render_template, request, session, redirect
from dbUtils import interact_db

# events blueprint definition
questions_2 = Blueprint('questions_2', __name__, static_folder='static', static_url_path='/questions_2', template_folder='templates')


# Routes
@questions_2.route('/questions_2', methods=['GET', 'POST'])
def questions_22():
    if request.method == 'POST':
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        query = """UPDATE "users" SET "q1" = '%s', "q2" = '%s', "q3" = '%s', "q4" = '%s', "q5" = '%s'
                 WHERE "id" = '%s'""" % (q1, q2, q3, q4, q5, session['code'])
        interact_db(query=query, query_type='commit')
        return redirect('/end')
    return render_template('questions_2.html')



