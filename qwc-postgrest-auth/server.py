import os
import logging

from urllib.parse import urlparse
from flask import Flask, jsonify, request, render_template, redirect, \
    make_response, url_for, render_template_string
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
from flask_jwt_extended import (jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies)

import i18n
from geon_services_core.jwt import jwt_manager
from geon_services_core.tenant_handler import (
    TenantHandler, TenantPrefixMiddleware, TenantSessionInterface)
from geon_services_core.runtime_config import RuntimeConfig
from forms import LoginForm
import requests

app = Flask(__name__)

app.config['JWT_COOKIE_SECURE'] = bool(os.environ.get(
    'JWT_COOKIE_SECURE', False))
app.config['JWT_COOKIE_SAMESITE'] = os.environ.get(
    'JWT_COOKIE_SAMESITE', 'Lax')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get(
    'JWT_ACCESS_TOKEN_EXPIRES', 12*3600))

jwt = jwt_manager(app)
app.secret_key = app.config['JWT_SECRET_KEY']

i18n.set('load_path', [
    os.path.join(os.path.dirname(__file__), 'translations')])
SUPPORTED_LANGUAGES = ['en', 'de']
# *Enable* WTForms built-in messages translation
# https://wtforms.readthedocs.io/en/2.3.x/i18n/
app.config['WTF_I18N_ENABLED'] = False


app.config['DEBUG'] = os.environ.get('FLASK_ENV', '') == 'development'
if app.config['DEBUG']:
    logging.getLogger('flask_ldap3_login').setLevel(logging.DEBUG)


login_manager = LoginManager(app)              # Setup a Flask-Login Manager

# config_handler = RuntimeConfig("dbAuth", app.logger)
# config = config_handler.tenant_config('default')
# db_url = config.get('db_url')
db_url = 'http://qwc-postgrest-server:3000'

if os.environ.get('TENANT_HEADER'):
    app.wsgi_app = TenantPrefixMiddleware(
        app.wsgi_app, os.environ.get('TENANT_HEADER'))

if os.environ.get('TENANT_HEADER') or os.environ.get('TENANT_URL_RE'):
    app.session_interface = TenantSessionInterface(os.environ)


# Create a dictionary to store the users in when they authenticate.
users = {}


# Declare an Object Model for the user, and make it comply with the
# flask-login UserMixin mixin.
class User(UserMixin):
    def __init__(self, username):

        self.username = username

        app.logger.debug("Login username: %s" % username)

    def is_active(self):
        return self.is_enabled

    def __repr__(self):
        return self.username

    def get_id(self):
        return self.username


# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise
# returns None.
@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None




# Declare some routes for usage to show the authentication process.
@app.route('/')
def home():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('login'))

    # User is logged in, so show them a page with their username and dn.
    template = """
    <h1>Welcome: {{ current_user.username }}</h1>
    <h2>{{ current_user.dn }}</h2>
    """

    return render_template_string(template)


@app.route('/login', methods=['GET', 'POST'])
def login():
    target_url = url_path(request.args.get('url', '/'))
    if current_user.is_authenticated:
        return redirect(target_url)
    form = LoginForm(meta=wft_locales())
    if form.validate_on_submit():
        # for geon authentication
        user= User(form.username.data)
        userdata= {'role': '{}'.format(form.username.data) , 'pass':'{}'.format(form.password.data)}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        pgrstresponse = requests.post(db_url + '/rpc/login', data=userdata, headers=headers)
        json_resp = pgrstresponse.json()
        geon_token = json_resp.get('token')
        if geon_token:
            identity = user.username
            login_user(user)
            # Create the tokens we will be sending back to the user
            access_token = create_access_token(identity)
            resp = make_response(redirect(target_url))
            # Set the JWTs and the CSRF double submit protection cookies
            # in this response
            set_access_cookies(resp, access_token)
            resp.set_cookie('geon_token_cookie', geon_token)
            return resp
        else:
            form.username.errors.append(i18n.t('auth.auth_failed'))
            form.password.errors.append(i18n.t('auth.auth_failed'))
    
    return render_template('login.html', form=form, i18n=i18n,
                           title=i18n.t("auth.login_page_title"))


@app.route('/logout', methods=['GET', 'POST'])
@jwt_required(optional=True)
def logout():
    target_url = url_path(request.args.get('url', '/'))
    resp = make_response(redirect(target_url))
    unset_jwt_cookies(resp)
    resp.set_cookie('geon_token_cookie','', expires=-1)
    logout_user()
    return resp


""" readyness probe endpoint """
@app.route("/ready", methods=['GET'])
def ready():
    return jsonify({"status": "OK"})


""" liveness probe endpoint """
@app.route("/healthz", methods=['GET'])
def healthz():
    return jsonify({"status": "OK"})


@app.before_request
def set_lang():
    i18n.set('locale',
             request.accept_languages.best_match(SUPPORTED_LANGUAGES) or 'en')


def wft_locales():
    return {'locales': [i18n.get('locale')]}


def url_path(url):
    """ Extract path and query parameters from URL """
    o = urlparse(url)
    parts = list(filter(None, [o.path, o.query]))
    return '?'.join(parts)


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.run(host='localhost', port=5017, debug=True)