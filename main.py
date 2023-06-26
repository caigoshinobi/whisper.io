import argparse
from flask_httpauth import HTTPBasicAuth
from flask import jsonify

# Arguments

parser = argparse.ArgumentParser()
parser.add_argument('--ip', '-i', default='0.0.0.0', help='The IP to run the application on [0.0.0.0]')
parser.add_argument('--port', '-p', default=5000, help='The port to run the application on [5000]')

args = parser.parse_args()
IP = args.ip
PORT = args.port

# Authentication

USER = 'admin' #CHANGEME
PASS = 'whisper' #CHANGEME

auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return jsonify({'message': 'Uh-oh! It seems you forgot the keys...'}), 401, {'Refresh': '3; url=/'}

@auth.verify_password
def verify_password(username, password):
    return username == USER and password == PASS

 # Main

if __name__ == '__main__':
    from routes import app
    app.run(host=IP, port=PORT)
