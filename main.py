import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--library', '-l', default='static/audiobooks', help='The audiobook directory [static/audibooks]')
parser.add_argument('--port', '-p', default=5000, help='The port to run the application on [5000]')
parser.add_argument('-h, --help', action='help', help='Show the help message and exit')

args = parser.parse_args()

LIBRARY = args.library
PORT = args.port

 # Main

if __name__ == '__main__':
    from routes import app
    app.run(host='0.0.0.0', port=PORT)
