from flask import Blueprint, render_template, session

# events blueprint definition
consent = Blueprint('consent', __name__, static_folder='static', static_url_path='/consent', template_folder='templates')


# Routes
@consent.route('/consent')
def consent2():
    print("in consent", session.get('code'))
    return render_template('consent.html')
