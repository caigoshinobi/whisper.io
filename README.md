# Whisper.io

Whisper.io is an audiobook library written in Flask that allows you to manage your audiobooks. You can add, edit, and listen to your audiobooks from the web app or download them to your device. You can also add multiple covers to each audiobook, and the web app will randomly choose a cover each time the book is served. Whisper.io is designed to be easy to set up on TrueNAS and FreeBSD systems.

<img src="https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/static/img/screen-2.jpg" alt="img-1" height="325">  <img src="https://raw.githubusercontent.com/caigoshinobi/whisper.io/main/static/img/screen-2_1.jpg" alt="img-2" height="325">

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

**Options:**

```
main.py [-h] [--library LIBRARY] [--port PORT] [-h, --help]

Options:
  --library, -l  The audiobook directory (default: static/audiobooks)
  --port, -p    The port to run the application on (default: 5000)
  -?            Show the help message and exit
```

**Example:**

To start Whisper.io on port 1234 and with the audiobook directory set to `static/mybooks`, run the following command:

```
python main.py --port 1234 --library static/mybooks
```

## Import Audiobooks

To import new audiobooks we have 2 choices:
- The first option is to use the "+ADD" button within the web app. In this case, we need to fill out the form with the necessary information and then upload the audio file along with some cover images.

- The second option, if we need to perform a mass import, is to create a new folder inside the audiobooks folder using the following structure:

```
- AUDIOBOOKS_FOLDER
    - [TITLE] - [AUTHOR] (example: The Jungle Book - R. Kipling)
        - c-1.jpg (It is necessary to maintain this naming format for the covers)
        - c-2.jpg
        - c-3.jpg
        - audiofile.mp3 (Audio files can be in M4A, MP3, OGG, or WAV format)
```

Please note that the cover images should be named following the specified format (c-1.jpg, c-2.jpg, etc.). Additionally, the audio files can be in M4A, MP3, OGG, or WAV format.

After completing the above steps, we need to start the app and click the 'SYNC' button. Whisper.io will automatically populate the audiobook.json file with the information found inside the audiobooks folders.

## License

Whisper.io is licensed under the CC BY-NC-SA 4.0 License.
