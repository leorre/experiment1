import time

import psycopg2
from dbUtils import interact_db
from flask import Blueprint, render_template, request, session, g
import random

# events blueprint definition
choosing = Blueprint('choosing', __name__, static_folder='static', static_url_path='/choosing',
                     template_folder='templates')

recomm_list = []
vacation_list = []

# Routes
@choosing.route('/choosing')
def choosing2():
    session['start_time'] = time.time()
    print("start_time:", session['start_time'])
    autonomy_lvl = generateAutonomyLvl()
    query_rec = """SELECT "continentRank", "typeRank", "sleepRank", "continentOption", "typeOption", "sleepOption" FROM users WHERE "id" = '%s'""" % (session['code'])
    user_ranking = interact_db(query=query_rec, query_type='fetch')
    user_ranking = user_ranking[0]
    print("user_ranking:", user_ranking, "autonomy level:", autonomy_lvl)
    if autonomy_lvl == 'low':
        recomm_list = recommForLowAutonomy(user_ranking)
        addsIdToVacation
    else:  # autonomy_lvl == 'high'
        recomm_list = recommForHighAutonomy(user_ranking)
    vacation_list = createVacationSet(user_ranking, recomm_list)
    print("vacation list", vacation_list)
    print("recomm", recomm_list)
    session['vacation_list'] = vacation_list
    session['recomm_list'] = recomm_list
    return render_template('choosing.html', vacation_list=vacation_list, recomm_list=recomm_list)


# recieve a vacation without id (as a () and not a list) and returns the vacation with id (as a list)
def addsIdToVacation (vacation):
    query = """SELECT "vac_id", "continent", "type", "sleep" FROM vacations WHERE "continent" = '%s' AND "type" = '%s' AND "sleep" = '%s'""" % (vacation[0], vacation[1], vacation[2])
    vacationWithId = interact_db(query=query, query_type='fetch')
    return vacationWithId


# return true if the vacation differs only in one element (the number element)
def validVacationDifferInOneElement (user_ranking,vacation,number):
    if user_ranking[0] == number:  # the chosen element is continent
        if matchingVacationOption(user_ranking[3]) == vacation[1]: # continent has to be the same
            return False
        if matchingVacationOption(user_ranking[4]) != vacation[2]: # type has to be different
            return False
        if matchingVacationOption(user_ranking[5]) != vacation[3]: # sleep has to be different
            return False
        return True
    elif user_ranking[1] == number:  # the chosen element is type
        if matchingVacationOption(user_ranking[4]) == vacation[2]:  # type has to be the same
            return False
        if matchingVacationOption(user_ranking[3]) != vacation[1]:  # continent has to be different
            return False
        if matchingVacationOption(user_ranking[5]) != vacation[3]:  # sleep has to be different
            return False
        return True
    else: # user_ranking[2] == number:  # the chosen element is sleep
        if matchingVacationOption(user_ranking[5]) == vacation[3]:  # sleep has to be the same
            return False
        if matchingVacationOption(user_ranking[4]) != vacation[2]:  # type has to be different
            return False
        if matchingVacationOption(user_ranking[3]) != vacation[1]:  # continent has to be different
            return False
        return True

# return true if the vacation is the same in only one element (the number element)
def validVacationSameInOneElement (user_ranking,vacation,number):
    if user_ranking[0] == number:  # the chosen element is continent
        if matchingVacationOption(user_ranking[3]) != vacation[1]: # continent has to be the same
            return False
        if matchingVacationOption(user_ranking[4]) == vacation[2]: # type has to be different
            return False
        if matchingVacationOption(user_ranking[5]) == vacation[3]: # sleep has to be different
            return False
        return True
    elif user_ranking[1] == number:  # the chosen element is type
        if matchingVacationOption(user_ranking[4]) != vacation[2]:  # type has to be the same
            return False
        if matchingVacationOption(user_ranking[3]) == vacation[1]:  # continent has to be different
            return False
        if matchingVacationOption(user_ranking[5]) == vacation[3]:  # sleep has to be different
            return False
        return True
    else: # user_ranking[2] == number:  # the chosen element is sleep
        if matchingVacationOption(user_ranking[5]) != vacation[3]:  # sleep has to be the same
            return False
        if matchingVacationOption(user_ranking[4]) == vacation[2]:  # type has to be different
            return False
        if matchingVacationOption(user_ranking[3]) == vacation[1]:  # continent has to be different
            return False
        return True


# return a list of vacations (the vacations presented to the user - not recomended by the system)
# 1 = optimal. 2 = differ in the first. 8 = same in the first. 9 = same in the third. 9 = same in the second
def createVacationSet (user_ranking, recomm_list):
    set = []
    optimal = OptimalVacation (user_ranking) #with id num
    optimal = optimal[0]
    set.append(optimal)
    session['optimal_id'] = optimal[0]


    query = """SELECT * FROM vacations"""
    all_vacations = interact_db(query=query, query_type='fetch')
    #random.shuffle(all_vacations)

    recomm_1 = 1
    recomm_2 = 1
    recomm_3 = 1
    recomm_4 = 1

    for vacation in all_vacations:
        if vacation in recomm_list:
            all_vacations.remove(vacation)

    all_vacations_temp = all_vacations.copy()
    for vacation in all_vacations_temp:
        if recomm_3 > 9:  # 9 recomm that differ in the first and second criterion = same in the third
            break
        if validVacationSameInOneElement(user_ranking,vacation,3):
            set.append(vacation)
            all_vacations.remove(vacation)
            print(" differ in the first and second:",vacation)
            recomm_3 = recomm_3 + 1;

    all_vacations_temp = all_vacations.copy()
    for vacation in all_vacations_temp:
        if recomm_4 > 9: # 9 recomm that differ in the first and third criterion = same in the second
            break
        if validVacationSameInOneElement(user_ranking,vacation,2):
            recomm_4 = recomm_4+1;
            set.append(vacation)
            all_vacations.remove(vacation)
            print(" differ in the first and third:",vacation)

    all_vacations_temp = all_vacations.copy()
    for vacation in all_vacations_temp:
        if recomm_2 > 8: # 8 recomm that differ in the second and third criterion
            break
        if validVacationSameInOneElement(user_ranking,vacation,1):
            recomm_2 = recomm_2+1;
            set.append(vacation)
            all_vacations.remove(vacation)
            print(" differ in the second and third:",vacation)

    all_vacations_temp = all_vacations.copy()
    for vacation in all_vacations_temp:
        if recomm_1 > 2: # need two recomm that differ in the first criteria
            break
        if validVacationDifferInOneElement(user_ranking,vacation,1):
            recomm_1 = recomm_1+1;
            set.append(vacation)
            all_vacations.remove(vacation)
            print(" differ in the first:",vacation)

    #random.shuffle(set)
    return set


# return the optimal vacation for a user according to his preferences
def OptimalVacation (user_ranking):
    continent = matchingVacationOption(user_ranking[3])
    type = matchingVacationOption(user_ranking[4])
    sleep = matchingVacationOption(user_ranking[5])
    optimal = (continent, type, sleep)
    optimal = addsIdToVacation(optimal)
    return optimal


# returns a list of all the system's recommendations for a low-autonomy user
# low autonomy = only 1 recommendation, defers in the third rank
def recommForLowAutonomy(user_ranking):
    recomm = recommendationsDeferInAnElement (user_ranking,3)  # different in the second element only
    return recomm #list


# returns a list of all the system's recommendations for a high-autonomy user
# high autonomy = 3 recommendations: one defers in the second rank, two in the first
def recommForHighAutonomy(user_ranking):
    recomm1 = recommendationsDeferInAnElement(user_ranking,2) # different in the second element only
    recomm2 = recommendationsDeferInAnElement(user_ranking,1) # different in the first element only
    recomm3 = recommendationsSameOnlyInOneElement(user_ranking,1) # different in 2 AND 3 (same in the first)
    list = recomm1 + recomm2 + recomm3
    random.shuffle(list)
    return list


# returns a recommendation that DEFERS only in the number element, with id
# (example: number = 2 - same as 1 and 3 and different in 2)
def recommendationsDeferInAnElement(user_ranking, number):
    if user_ranking[0] == number:  # the chosen element is continent
        type = matchingVacationOption(user_ranking[4])  # vacation type
        sleep = matchingVacationOption(user_ranking[5])  # sleep
        continent = getRandContinent(user_ranking)
    elif user_ranking[1] == number:  # the chosen element is type
        continent = matchingVacationOption(user_ranking[3])  # continent
        sleep = matchingVacationOption(user_ranking[5])  # sleep
        type = getRandType(user_ranking)
    else:  # user_ranking[2] == number:  # the chosen element is sleep
        continent = matchingVacationOption(user_ranking[3])  # continent
        type = matchingVacationOption(user_ranking[4])  # vacation type
        sleep = getRandSleep(user_ranking)
    recomm = (continent, type, sleep)
    recomm = addsIdToVacation(recomm)
    return recomm # return 1 recommendation


def getRandContinent (user_ranking):
    continents = ['Africa', 'America', 'Asia', 'Europe']
    temp_continent = user_ranking[3]  # the user chose but we want to change to a different one because it's the second ranked
    continents.remove(temp_continent)  # clears continents list from the original continent choice
    continents = matchingVacationOptionForList(continents)
    continent = random.choice(continents)
    return continent

def getRandType (user_ranking):
    vacation_types = ['Backpacking', 'Leisure', 'Package tour', 'Cultural']
    temp_type = user_ranking[4]  # the user chose but we want to change to a different one because it's the second ranked
    vacation_types.remove(temp_type)  # clears vacation types list from the original type choice
    vacation_types = matchingVacationOptionForList(vacation_types)
    type = random.choice(vacation_types)
    return type

def getRandSleep (user_ranking):
    sleeps = ['Hotel', 'Rental Apartment', 'Guesthouse', 'Cabin']
    temp_sleep = user_ranking[5]  # the user chose but we want to change to a different one because it's the second ranked
    sleeps.remove(temp_sleep)  # clears vacation types list from the original type choice
    sleeps = matchingVacationOptionForList(sleeps)
    sleep = random.choice(sleeps)
    return sleep

# returns a recommendation that the SAME only in one element
def recommendationsSameOnlyInOneElement(user_ranking, number): #number=critiria number
    if user_ranking[0] == number:
        continent = matchingVacationOption(user_ranking[3])  # continent
        type = getRandType(user_ranking)
        sleep = getRandSleep(user_ranking)
    elif user_ranking[1] == number:  # the chosen element is type
        type = matchingVacationOption(user_ranking[4])  # vacation type
        sleep = getRandSleep(user_ranking)
        continent = getRandContinent(user_ranking)
    else:  # user_ranking[2] == number:  # the chosen element is sleep
        sleep = matchingVacationOption(user_ranking[5])
        type = getRandType(user_ranking)
        continent = getRandContinent(user_ranking)
    recomm = (continent, type, sleep)
    recomm = addsIdToVacation(recomm)
    return recomm  # return 1 recommendation


# generates the user autonomy level (high/low), insert to DB and returns the level
def generateAutonomyLvl():
    currAutonomy = random.choice(['high', 'low'])
    query = """UPDATE "users" SET "autonomyLvl" = '%s'
         WHERE "id" = '%s'""" % (currAutonomy, session['code'])
    interact_db(query=query, query_type='commit')
    return currAutonomy


# recieve a list of options and match the options to the set-options (and  return a new list)
def matchingVacationOptionForList(vacation_types):
    list = []
    for vacation in vacation_types:
        new_vacation = matchingVacationOption(vacation)
        list.append(new_vacation)
    return list


# return the matching vacation to the user preferences.
# if user chose "africa" - the vacation set option is "south africa" instead
def matchingVacationOption(option):
    if option == "Africa":
        return "South Africa"
    if option == "America":
        return "California"
    if option == "Asia":
        return "Japan"
    if option == "Europe":
        return "France"
    if option == "Backpacking":
        return "Trekking"
    if option == "Leisure":
        return "Relaxation"
    if option == "Package tour":
        return "Package tour"
    if option == "Cultural":
        return "Landmarks & museums"
    if option == "Hotel":
        return "hotel"
    if option == "Rental Apartment":
        return "rental apartment"
    if option == "Guesthouse":
        return "guesthouse"
    if option == "Cabin":
        return "cabin"


# return the full vacation details from the DB according to vacation id
def getVacationAccordingID(id):
    query = """SELECT * FROM vacations WHERE "vac_id" = '%s'""" % (id)
    vacation = interact_db(query=query, query_type='fetch')
    return vacation[0]


# inserts user's choices to DB - wether he chose the recommendation and the number of clicks on the rec window
@choosing.route('/insertUserChoices')
def insertUserChoices():
    time_diff = time.time() - session.get('start_time', 0)  # user time in the page (including time in other websites)
    chosen_vacation_id = request.args.get('id')  # the chosen vacation id number
    chosen_vacation = getVacationAccordingID(chosen_vacation_id)

    print("chosenVacID:", chosen_vacation_id)
    print("chosen_vacation: ", chosen_vacation)
    recomm_list = session['recomm_list']
    vacation_list = session['vacation_list']

    choseOptimal = False
    if (session['optimal_id'] == chosen_vacation_id):
        choseOptimal = True  # the user chose the optimal vacation

    vacIndex = -2  # the place of the chosen vacation in the set
    is_recomm = False  # did the user choose one of the recommendations?
    if chosen_vacation in recomm_list:
        vacIndex = recomm_list.index(chosen_vacation)
        is_recomm = True
    elif chosen_vacation in vacation_list:
        vacIndex = vacation_list.index(chosen_vacation)
    vacIndex = vacIndex + 1  # because it starts in 0
    print("index: ", vacIndex)
    print("recomm: ", is_recomm)

    query = """UPDATE "users" SET "chosenVacId" = '%s', "vacIndex" = '%s', "choseOptimal" = '%s', 
    "isRecomm" = '%s', "time" = '%s' WHERE "id" = '%s'""" \
            % (chosen_vacation_id, vacIndex, choseOptimal, is_recomm, time_diff, session['code'])
    interact_db(query=query, query_type='commit')
    return


