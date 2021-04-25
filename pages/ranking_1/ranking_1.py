import psycopg2
from flask import Blueprint, render_template, redirect, session, request, jsonify
from dbUtils import interact_db

# events blueprint definition
ranking_1 = Blueprint('ranking_1', __name__, static_folder='static', static_url_path='/ranking_1', template_folder='templates')


# Routes
@ranking_1.route('/ranking_1')
def ranking_11():
    return render_template('ranking_1.html')


@ranking_1.route('/insertRanks1')
def insertRanks1():
    rank1 = request.args.get('rank1')
    rank2 = request.args.get('rank2')
    rank3 = request.args.get('rank3')
    changeRank = request.args.get('changed')
    # transferring rank1, rank2, rank3 to each criteria rank
    # instead of rank2=Sleeping Arrangement, we recieve sleepRank = 2
    continentRank = 3
    typeRank = 3
    sleepRank = 3
    if rank1 == "Continent":
        continentRank=1
    elif rank2 == "Continent":
        continentRank=2
    if rank1 == "Vacation Type":
        typeRank=1
    elif rank2 == "Vacation Type":
        typeRank=2
    if rank1 == "Sleeping Arrangement":
        sleepRank=1
    elif rank2 == "Sleeping Arrangement":
        sleepRank=2
    query = """INSERT INTO users(id, "continent_rank", "type_rank", "sleep_rank", "change_rank") VALUES ('%s', '%s', '%s', '%s', '%s') """ \
            % (session['code'], continentRank, typeRank, sleepRank, changeRank)
    interact_db(query=query, query_type='commit')
    return #no need for render_template or redirect - it doesnt work because of ajax
    #the redirections is from the Javascript
