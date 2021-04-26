import time
from flask import Blueprint, render_template, session
from dbUtils import interact_db

# events blueprint definition
end = Blueprint('end', __name__, static_folder='static', static_url_path='/end', template_folder='templates')


# Routes
@end.route('/end')
def end2():
    all_time = time.time() - session.get('start_time_experiment', 0)
    query = """UPDATE "users" SET "exp_time" = '%s' WHERE "id" = '%s'""" \
            % (all_time, session['code'])
    interact_db(query=query, query_type='commit')
    code = session.get('code', 0)
    amazon_code = int(code)+3000
    #amazon_code = 1234
    return render_template('end.html', amazon_code=amazon_code)
