from flask import Blueprint, render_template, session
import psycopg2

# events blueprint definition
code = Blueprint('code', __name__, static_folder='static', static_url_path='/code', template_folder='templates')


# Routes
@code.route('/code')
def code2():
    query = "SELECT * FROM curr_codes"  # choose the device for current user - mobile/pc
    query_result = interact_db(query=query, query_type='fetch')
    curr_pc_code = query_result[0][0]
    curr_mobile_code = query_result[0][1]
    if curr_pc_code - 1000 > curr_mobile_code - 2000:  # chosen device: mobile #1000 and 2000 - for start points...
        curr_code = curr_mobile_code + 1
        query = """UPDATE "curr_codes" SET "currMobileCode" = '%s' WHERE "currMobileCode" = '%s'""" % (
        curr_mobile_code + 1, curr_mobile_code)
        interact_db(query=query, query_type='commit')
    else:  # chosen device: pc
        curr_code = curr_pc_code + 1
        query = """UPDATE "curr_codes" SET "currPcCode" = '%s' WHERE "currMobileCode" = '%s'""" % (
        curr_pc_code + 1, curr_mobile_code)
        interact_db(query=query, query_type='commit')
    curr_code = 1060  ######################## DELEEEEEEEEEEEEETEEEEEEEEEEEEEEEEEEEEE
    print(curr_code)
    device = "Smartphone"
    if curr_code < 2000: #1000-1999 it's pc user
        device = "Computer"
    return render_template('code.html', device=device, code=curr_code)


def baseFunction():
    query = "SELECT * FROM curr_codes"  # choose the device for current user - mobile/pc
    query_result = interact_db(query=query, query_type='fetch')
    curr_pc_code = query_result[0][0]
    curr_mobile_code = query_result[0][1]
    if curr_pc_code-1000 > curr_mobile_code-2000:  # chosen device: mobile #1000 and 2000 - for start points...
        curr_code = curr_mobile_code+1
        query = """UPDATE "curr_codes" SET "currMobileCode" = '%s' WHERE "currMobileCode" = '%s'""" % (curr_mobile_code+1, curr_mobile_code)
        interact_db(query=query, query_type='commit')
    else:  # chosen device: pc
        curr_code = curr_pc_code+1
        query = """UPDATE "curr_codes" SET "currPcCode" = '%s' WHERE "currMobileCode" = '%s'""" % (curr_pc_code+1, curr_mobile_code)
        interact_db(query=query, query_type='commit')
    curr_code = 1063 ######################## DELEEEEEEEEEEEEETEEEEEEEEEEEEEEEEEEEEE
    print(curr_code)
    return render_template("/code", code=curr_code)


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
