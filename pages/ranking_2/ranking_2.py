import psycopg2
from flask import Blueprint, render_template, request, redirect, session
from dbUtils import interact_db

# events blueprint definition
ranking_2 = Blueprint('ranking_2', __name__, static_folder='static', static_url_path='/ranking_2', template_folder='templates')


# Routes
@ranking_2.route('/ranking_2')
def ranking_22():
    return render_template('ranking_2.html')


@ranking_2.route('/insertRanks2')
def insertRanks2():
    continentOption = request.args.get('rank1')
    typeOption = request.args.get('rank2')
    sleepOption = request.args.get('rank3')
    query = """UPDATE "users" SET "continentOption" = '%s', "typeOption" = '%s', "sleepOption" = '%s'
     WHERE "id" = '%s'""" % (continentOption, typeOption, sleepOption, session['code'])
    interact_db(query=query, query_type='commit')
    return



