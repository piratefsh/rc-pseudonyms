from flask import Flask, request, redirect, url_for, jsonify
import requests
import urllib.parse
import os

app = Flask(__name__)
app.config.from_envvar('RC_OAUTH_CLIENT_SECRETS')

app.config['RC_OAUTH_REDIRECT_AUTH_URI'] = 'http://localhost:6060/access_token'
app.config['RC_OAUTH_REDIRECT_ACCESS_URI'] = 'http://localhost:6060/access_token/received_token'

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
        'redirect_uri': app.config['RC_OAUTH_REDIRECT_ACCESS_URI'],
        'grant_type': 'authorization_code',
        'code': code
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    req = requests.post(app.config['RC_OAUTH_TOKEN_URI'], data=params)
    return req.text


@app.route('/access_token/received_token', methods=['GET'])
def received_token():
    return 'got token! %s' % request.args.get('access_token')



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=6060)
