from flask import Blueprint, render_template

# events blueprint definition
instructions = Blueprint('instructions', __name__, static_folder='static', static_url_path='/instructions', template_folder='templates')


# Routes
@instructions.route('/instructions')
def instructions2():
    return render_template('instructions.html')
