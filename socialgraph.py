import inspect, os, sqlite3

from flask import (
        Flask,
        g,
        request,
        session
)

# Configuration
DATABASE = os.path.join(
        os.path.dirname(
            os.path.abspath(
                inspect.getfile(inspect.currentframe()))), 
        'socialgraph.db')
SECRET_KEY = os.urandom(12)
DEBUG = True

# App construction
app = Flask(__name__)
app.config.from_object(__name__)


# App helpers
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    from contextlib import closing
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()
    if not app.config['TESTING'] and request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if not app.config['TESTING'] and '_csrf_token' not in session:
        session['_csrf_token'] = hashlib.sha1(os.urandom(40)).hexdigest()
    return session.get('_csrf_token', '')

app.jinja_env.globals['csrf_token'] = generate_csrf_token 

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

