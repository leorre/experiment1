import psycopg2
from flask import Blueprint, render_template, redirect, session, request, jsonify
from dbUtils import interact_db

# events blueprint definition
algo_data = Blueprint('algo_data', __name__, static_folder='static', static_url_path='/algo_data', template_folder='templates')


# Routes
@algo_data.route('/algo_data', methods=['GET', 'POST'])
def algo_data1():
    if request.method == 'POST':
        last_vac = request.form['last_vac']
        vacs_in_three = request.form['vacs_in_three']
        advance_book = request.form['book']
        plan = request.form['plan']
        query = """UPDATE "users" SET "last_vac" = '%s', "vacs_in_three" = '%s', "advance_book" = '%s', "plan" = '%s'
                         WHERE "id" = '%s'""" % (last_vac, vacs_in_three, advance_book, plan, session['code'])
        interact_db(query=query, query_type='commit')
        return redirect('/ranking_2')
    return render_template('algo_data.html')
