#!/usr/bin/python
# Copyright 2018, Sourcepole AG
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


import json
from flask import Flask, request
import requests
from flask_jwt_extended import (jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies)
from flask import Flask, jsonify, request, render_template, redirect, \
    make_response, url_for, render_template_string



app = Flask(__name__)

class test_service:
    def __init__(self, reqtype):
        reqtype='test'



@app.route('/', methods=['GET'])
def welcome():
    return '<div style="width:800px; border:2px; border-style:solid; border-color:#000000; margin: auto; padding:10px; border-radius: 15px;"><h1 style="color: #5e9ca0; text-align: center;">Welcome to Geon Api Service</h1> <h2 style="color: #2e6c80;">How to use this service:</h2> <p>To use any function in database that your user has access to, use the url and get result as json.</p> <blockquote> <p><span style="color: #00a1ff;">url:5021/&lt;schema&gt;/&lt;function&gt;/&lt;input&gt;</span></p> </blockquote> <p>Doing this you will pass the <span style="color: #00a1ff;">&lt;input&gt;</span> to <span style="color: #00a1ff;">&lt;function&gt;</span> in <span style="color: #00a1ff;">&lt;schema&gt;</span> in database.</p> <p>To pass a JSON as input you should use <em>Curly braces&nbsp;</em>around input like this:</p> <blockquote> <p><span style="color: #00a1ff;">{"feature":{"tableName":"ve_arc_pipe", "id":"2001"}}</span></p> </blockquote> <p><strong>&nbsp;</strong></p> <p><strong><a href="https://github.com/Giswater/giswater_dbmodel/wiki/Use-existing-PLpgSQL-function">These</a> are some giswater functions that you can use, schema names are "ws" and "ud"</strong></p></div>'

# root burada ogc api tarzı birşeyler döndürelim
@app.route('/<schema>/<function>/<input>', methods=['GET'])
def getroot(schema, function, input):
    url = f"http://qwc-postgrest-server:3000/rpc/gn_get_api_yihu"
    payload = json.dumps(
        {
        "schemaname":"{}".format(schema),
        "functionname":"{}".format(function),
        "inputname": "{}".format(input)
        }
        )
    headers = {'Content-Type': 'application/json' }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.text
    
    """userdata= {'role': 'gn_admin' , 'pass':'admin'}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    pgrstresponse = requests.post('http://qwc-postgrest-server:3000/rpc/login', data=userdata, headers=headers)
    json_resp = pgrstresponse.json()
    geon_token = json_resp.get('token')
    # Create the tokens we will be sending back to the user
    access_token = create_access_token('gn_admin')
    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
    set_access_cookies(resp, access_token)
    resp.set_cookie('geon_token_cookie', geon_token)"""
    #result = f'function: {function} input: {input}'
    return result




if __name__ == "__main__":
    from flask_cors import CORS
    CORS(app)
    app.run(host='localhost', port=2324, debug=True)
