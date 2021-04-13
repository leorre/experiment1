import psycopg2
from flask import Blueprint, render_template, request, redirect, session

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
