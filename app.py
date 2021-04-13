from flask import Flask, redirect, url_for, render_template, request, session, jsonify, blueprints, flash, request
from flask_sqlalchemy import *
import psycopg2

###### App setup
app = Flask(__name__)
app.config.from_pyfile('settings.py')
# app.secret_key = '123'



################## Pages ##################
## code
from pages.code.code import code
app.register_blueprint(code)

## entrance
from pages.entrance.entrance import entrance
app.register_blueprint(entrance)

## consent
from pages.consent.consent import consent
app.register_blueprint(consent)

## instructions
from pages.instructions.instructions import instructions
app.register_blueprint(instructions)

## ranking_1
from pages.ranking_1.ranking_1 import ranking_1
app.register_blueprint(ranking_1)

## algo_data
from pages.algo_data.algo_data import algo_data
app.register_blueprint(algo_data)

## ranking_2
from pages.ranking_2.ranking_2 import ranking_2
app.register_blueprint(ranking_2)

## choosing
from pages.choosing.choosing import choosing
app.register_blueprint(choosing)

## questions_1
from pages.questions_1.questions_1 import questions_1
app.register_blueprint(questions_1)

## questions_2
from pages.questions_2.questions_2 import questions_2
app.register_blueprint(questions_2)

## end
from pages.end.end import end
app.register_blueprint(end)


@app.route('/')
def baseFunction():
    session['code'] = 0
    return redirect("/code")


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
