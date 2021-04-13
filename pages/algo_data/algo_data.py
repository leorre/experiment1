import psycopg2
from flask import Blueprint, render_template, redirect, session, request, jsonify

# events blueprint definition
algo_data = Blueprint('algo_data', __name__, static_folder='static', static_url_path='/algo_data', template_folder='templates')


# Routes
@algo_data.route('/algo_data', methods=['GET', 'POST'])
def algo_data1():
    if request.method == 'POST':
        return redirect('/ranking_2')
    return render_template('algo_data.html')
