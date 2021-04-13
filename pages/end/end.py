from flask import Blueprint, render_template

# events blueprint definition
end = Blueprint('end', __name__, static_folder='static', static_url_path='/end', template_folder='templates')


# Routes
@end.route('/end')
def end2():
    amazon_code = 1234
    return render_template('end.html',amazon_code=amazon_code)
