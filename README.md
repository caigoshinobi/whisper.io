# Whisper.io

Whisper.io is an audiobook library written in Flask that allows you to manage your audiobooks. 

<img src="https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/static/img/screen-2.jpg" alt="img-1" height="250" width="466">

## Features

- Manage and listen to your audiobooks using the web app or download them to your device.
- Add multiple covers for each audiobook. The web app will randomly select a cover each time it serves the book.
- The audiobook will automatically receive bookmarks as you listen, allowing you to resume playback at any time.
- The web app is responsive and mobile-friendly, thanks to Bootstrap.
- It is designed to be easily set up on FreeBSD systems (since I couldn't find anything simple for my TrueNAS).

## Installation

To install Whisper.io, simply clone the repository and install the `requirements.txt` file.

```
git clone https://github.com/caigoshinobi/whisper.io.git
cd whisper.io
pip install -r requirements.txt
```

## Usage

To start Whisper.io, run the following command:

```
python main.py
```

**Options**

```
usage: main.py [-h] [--ip IP] [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --ip IP, -i IP        The IP to run the application on [0.0.0.0]
  --port PORT, -p PORT  The port to run the application on [5000]
```

**Example**

To initiate Whisper.io on IP `192.168.10.100`, port `1234`, execute the following command:

```
python main.py --port 1234 --ip 192.168.10.100
```

## Authentication

Although whisper.io is publicly accessible for reading, some management features of the web application are protected by basic authentication (e.g., `⚙️SYNC`, `➕ADD`, `✖️DELETE`, ...). The default credentials are `admin:whisper`, but they can be changed by modifying the `main.py` file:

```
# Authentication

USER = 'admin' #CHANGEME
PASS = 'whisper' #CHANGEME

auth = HTTPBasicAuth()
```

## Import Audiobooks

To import new audiobooks we have 2 choices:
- The first option is to use the `➕ADD` button within the web app. In this case, we need to fill out the form with the necessary information and then upload the audio file along with some cover images.

- The second option, if we need to perform a mass import, is to create a new folder inside the audiobooks folder using the following structure:

```
- AUDIOBOOKS_FOLDER
    - [TITLE] - [AUTHOR] (example: The Jungle Book - R. Kipling)
        - c-1.jpg (It is necessary to maintain this naming format for the covers. Max 5.)
        - c-2.jpg
        - c-3.jpg
        - audiofile.mp3 (Audio files can be in M4A, MP3, OGG, or WAV format)
```

After completing the above steps, we need to start the app and click the `⚙️SYNC` button. Whisper.io will automatically populate the `audiobook.json` file with the information found inside the audiobooks folders.

## License

Whisper.io is licensed under the [GPLv3](https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/LICENSE) License.
