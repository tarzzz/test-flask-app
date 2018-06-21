from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
import os
from requests.auth import HTTPBasicAuth
import requests
import urllib

app = Flask(__name__)

auth = HTTPBasicAuth('tesla', '4x0qb4YcRfDaOv5DqW4Y')
headers = {'Plotly-Client-Platform': 'python'}

base_url = 'https://plotly.charleyferrari.com/v2'
endpoint = '/oauth-apps/lookup?name=test Oauth'

r = requests.get(base_url + endpoint, auth=auth, headers=headers, verify=False)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = r.json()[0]['client_id']
client_secret = r.json()[0]['client_secret']
redirect_uri = r.json()[0]['redirect_uris']

print r.json()
authorization_base_url = 'https://plotly.charleyferrari.com/o/authorize'
authorization_url = ('{}?response_type=token&'
                     'client_id={}&redirect_uri={}'.format(
                         authorization_base_url, client_id, redirect_uri
                      ))


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """

    print authorization_url
    return render_template('index.html', url=authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route('/_oauth-redirect', methods=['GET'])
def callback():
    return render_template('redirect.html')


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    token = request.cookies.get('access_token')
    headers = {
        'content-type': 'application/json',
        'plotly-client-platform': 'python',
        'Authorization':'Bearer {}'.format(token)
    }
    return jsonify(requests.get(base_url + '/users/current', headers=headers, verify=False).json())


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8080)
