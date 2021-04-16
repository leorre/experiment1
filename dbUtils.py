import psycopg2

# DB connection
def interact_db(query, query_type: str):
    return_value = False
    #connection = psycopg2.connect(host='localhost', user='postgres', password='root', database='postgres')
    connection = psycopg2.connect(host='ec2-18-206-20-102.compute-1.amazonaws.com',
                                  user='cntypknleqxhhu',
                                  password='5320e3ed5187e37e1979e9a821f6c12cd9787ff041110fad903af85751a0dc46',
                                  database='d3fcoagc68lur7')
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
