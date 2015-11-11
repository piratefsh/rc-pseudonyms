from flask import Flask, request, redirect, url_for, jsonify
import requests
import urllib.parse
import os
import json 

app = Flask(__name__)
app.config.from_envvar('RC_OAUTH_CLIENT_SECRETS')
app.config['RC_API_URI'] = 'http://www.recurse.com/api/v1'
app.config['RC_OAUTH_AUTH_URI'] = 'https://www.recurse.com/oauth/authorize'
app.config['RC_OAUTH_TOKEN_URI'] = 'https://www.recurse.com/oauth/token'
app.config['RC_OAUTH_REDIRECT_AUTH_URI'] = 'http://localhost:6060/access_token'

TOKENS = {}

@app.route('/', methods=['GET'])
def index():
    params = {
        "client_id": app.config['RC_OAUTH_CLIENT_ID'],
        "redirect_uri": app.config['RC_OAUTH_REDIRECT_AUTH_URI'],
        "response_type": 'code'
    }

    url_params = urllib.parse.urlencode(params)
    oauth_url = "%s?%s" % (app.config['RC_OAUTH_AUTH_URI'], url_params)
    return redirect(oauth_url)


@app.route('/access_token', methods=['GET', 'POST'])
def access_token():
    code = request.args.get('code')
    params = {
        'client_id': app.config['RC_OAUTH_CLIENT_ID'],
        'client_secret': app.config['RC_OAUTH_CLIENT_SECRET'],
        'redirect_uri': app.config['RC_OAUTH_REDIRECT_AUTH_URI'],
        'grant_type': 'authorization_code',
        'code': code
    }

    req = requests.post(app.config['RC_OAUTH_TOKEN_URI'], data=params)
    data = json.loads(req.text)
    print(data)
    token = data['access_token']
    return str(get_mine(token))

def get_mine(access_token):
    headers = {
        'Authorization': 'Bearer %s' % access_token
    }
    req = requests.get("%s/people/me" % app.config['RC_API_URI'], headers=headers)
    return json.loads(req.text)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=6060)
