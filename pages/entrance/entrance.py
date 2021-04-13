from flask import Blueprint, render_template, session, request, redirect

# events blueprint definition
entrance = Blueprint('entrance', __name__, static_folder='static', static_url_path='/entrance', template_folder='templates')


# Routes
@entrance.route('/entrance', methods=['GET', 'POST'])
def entrance2():
    if request.method == 'POST':
        code = request.form['code_id']
        print("code = ", code)
        if code == "":
            return render_template('entrance.html')
        else:
            session['code'] = code
            return redirect('/consent')
    return render_template('entrance.html')


@entrance.route('/insertCode')
def insertCode():
    session['code'] = request.args.get('code')
    print("in insertCode", session['code'])
    return

