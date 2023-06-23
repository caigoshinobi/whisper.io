# Whisper.io

Whisper.io is an audiobook library written in Flask that allows you to manage your audiobooks. 

<img src="https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/static/img/screen-2.jpg" alt="img-1" height="300" width="559">

## Features

- Add & listen to your audiobooks from the web app or download them to your device;
- Manage multiple covers to each audiobook. The web app will randomly choose a cover each time the book is served;
- Automatic bookmarks will also be applied to your audiobook while listening, so you can resume it whenever you want.
- Responsive and mobile-oriented, thanks to Bootstrap.
- Designed to be easy to set up on FreeBSD systems (I didn't find anything simple for my TrueNAS).

## Installation

To install Whisper.io, simply clone the repository and install the requirements.txt file.

```
git clone https://github.com/bard/whisper.io
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
main.py [-h] [--library LIBRARY] [--port PORT] [-h, --help]

Options:
  --library, -l  The audiobook directory (default: static/audiobooks)
  --port, -p    The port to run the application on (default: 5000)
  -?            Show the help message and exit
```

**Example**

To start Whisper.io on port 1234 and with the audiobook directory set to `static/mybooks`, run the following command:

```
python main.py --port 1234 --library static/mybooks
```

## Import Audiobooks

To import new audiobooks we have 2 choices:
- The first option is to use the ➕**ADD** button within the web app. In this case, we need to fill out the form with the necessary information and then upload the audio file along with some cover images.

- The second option, if we need to perform a mass import, is to create a new folder inside the audiobooks folder using the following structure:

```
- AUDIOBOOKS_FOLDER
    - [TITLE] - [AUTHOR] (example: The Jungle Book - R. Kipling)
        - c-1.jpg (It is necessary to maintain this naming format for the covers)
        - c-2.jpg
        - c-3.jpg
        - audiofile.mp3 (Audio files can be in M4A, MP3, OGG, or WAV format)
```

After completing the above steps, we need to start the app and click the ⚙️**SYNC** button. Whisper.io will automatically populate the audiobook.json file with the information found inside the audiobooks folders.

## License

Whisper.io is licensed under the [GPLv3](https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/LICENSE) License.
