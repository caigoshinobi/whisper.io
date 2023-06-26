from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
import os
import random
import json
import secrets
import glob
from utils import get_json, get_audiobook_from_id
from main import auth
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

audiobooks = []
audiobook_path = 'static/audiobooks'

# Renders the index.html template and displays a list of audiobooks retrieved from the JSON file. 
# It also reads the bookmark information for each audiobook if available.

@app.route('/')
def index():
    audiobooks.clear()
    audiobooks_file = get_json()

    if os.path.exists(audiobooks_file):
        with open(audiobooks_file, 'r') as f:
            audiobooks_data = json.load(f)

            for audiobook_data in audiobooks_data['audiobooks']:
                bookmark_file = os.path.join(audiobook_data['folder']['path'], 'bookmark.txt')
                bookmark = 0

                if os.path.exists(bookmark_file):
                    with open(bookmark_file, 'r') as f:
                        bookmark = f.read()

                audiobook = {
                    'id': audiobook_data['id'],
                    'title': audiobook_data['title'],
                    'author': audiobook_data['author'],
                    'bookmark': bookmark
                }

                if 'cover_paths' in audiobook_data['folder']:
                    cover_paths = audiobook_data['folder']['cover_paths']
                    if len(cover_paths) > 0:
                        audiobook['cover'] = random.choice(cover_paths)
                else:
                    audiobook['cover'] = ""

                audiobooks.append(audiobook)

    return render_template('index.html', audiobooks=audiobooks)


# Receives a POST request with keywords and filters the audiobooks based on the keywords.
# Returns the filtered audiobooks as JSON.

@app.route('/api/search', methods=['POST'])
def search_audiobooks():
    keywords = request.form.get('keywords')
    
    filtered_audiobooks = filter(
        lambda audiobook: all(
            keyword.lower() in audiobook['title'].lower() or keyword.lower() in audiobook['author'].lower()
            for keyword in keywords.split()
        ),
        audiobooks
    )

    result_audiobooks = list(filtered_audiobooks)

    return jsonify(result_audiobooks)


# Retrieves the audiobooks from the JSON file and returns them as a downloadable JSON file.

@app.route('/json', methods=['GET'])
@auth.login_required
def list_audiobooks():
    audiobooks_file = get_json()

    if os.path.exists(audiobooks_file):
        with open(audiobooks_file, 'r') as f:
            audiobooks_data = json.load(f)
            audiobooks_text = json.dumps(audiobooks_data, indent=4)
            response = make_response(audiobooks_text)
            response.headers.set('Content-Disposition', 'attachment', filename='audiobooks.json')
            response.headers.set('Content-Type', 'application/json')
            return response

    return jsonify({'message': 'audiobooks.json not found. Please wait...'}), 400, {'Refresh': '3; url=/'}


# Renders the import.html template, which is a page for importing new audiobooks.

@app.route('/import')
@auth.login_required
def import_page():    
    return render_template('import.html')


# Handles the POST request for importing a new audiobook. 
# Saves the audio file, cover images, and updates the audiobooks JSON file with the new audiobook information.

@app.route('/api/import', methods=['POST'])
@auth.login_required
def import_audiobook():
    title = request.form.get('title')
    author = request.form.get('author')
    audio_file = request.files.get('audio')
    cover_files = request.files.getlist('cover')

    # Some basic input hardening
    audio_file.filename = secure_filename(audio_file.filename)
    audio_extensions = ['.mp3', '.m4a', '.wav', '.ogg']
    if not audio_file.filename.endswith(tuple(audio_extensions)):
        return jsonify({'message': 'Hey! This is not a valid file extension. Please wait...'}), 400, {'Refresh': '3; url=/import'}

    if len(cover_files) > 5:
        return jsonify({'message': 'Hey! too many covers. 5 or less. Please wait...'}), 400, {'Refresh': '3; url=/import'}

    audiobooks_path = audiobook_path
    folder_name = f"{title} - {author}"
    folder_path = os.path.join(audiobooks_path, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    audio_path = os.path.join(folder_path, audio_file.filename)
    audio_file.save(audio_path)

    for i, cover_file in enumerate(cover_files):
        cover_path = os.path.join(folder_path, f'c-{i}.jpg')
        cover_file.save(cover_path)

    return jsonify({'message': 'Audiobook successfully imported. Please wait...'}), 200, {'Refresh': '2; url=/sync'}


# Handles the GET request for syncing the audiobook folders. 
# Reads the audio files, cover images, and bookmark information from each folder and updates the audiobooks JSON file.

@app.route('/sync', methods=['GET'])
@auth.login_required
def sync_books():
    json_file = 'audiobooks.json'

    if os.path.exists(json_file):
        os.remove(json_file)

    audiobooks_path = audiobook_path
    audiobooks = []

    for folder_name in os.listdir(audiobooks_path):
        folder_path = os.path.join(audiobooks_path, folder_name)

        if os.path.isdir(folder_path):

            # Audio
            audio_extensions = ['.mp3', '.m4a', '.wav', '.ogg']
            audio_paths = []
            for ext in audio_extensions:
                audio_paths.extend(glob.glob(os.path.join(folder_path, '*' + ext)))

            # Covers
            cover_paths = glob.glob(os.path.join(folder_path, 'c-*'))

            # Bookmark
            bookmark_file = os.path.join(folder_path, 'bookmark.txt')

            if audio_paths and os.path.exists(audio_paths[0]) and len(cover_paths) > 0:
                audio_path = audio_paths[0]
                title, author = folder_name.split(' - ')
                audiobook_id = secrets.token_hex(6)

                if not os.path.exists(bookmark_file):
                    with open(bookmark_file, 'w') as f:
                        f.write('0')

                folder = {
                    'path': folder_path,
                    'audio_path': audio_path,
                    'cover_paths': cover_paths,
                }

                audiobook = {
                    'id': audiobook_id,
                    'title': title.strip(),
                    'author': author.strip(),
                    'folder': folder,
                }

                audiobooks.append(audiobook)

    data = {'audiobooks': audiobooks}

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

    return jsonify({'message': 'Sync completed. Please wait...'}), 200, {'Refresh': '2; url=/'}


# Renders the player.html template and displays the audiobook player for the specified audiobook ID. 
# Retrieves the audiobook information from the JSON file.

@app.route('/player/<audiobook_id>', methods=['GET'])
def player(audiobook_id):
    audiobook = get_audiobook_from_id(audiobook_id)

    cover_paths = audiobook['folder']['cover_paths']
    random_cover = random.choice(cover_paths)
    random_cover_path = os.path.join('/', random_cover)

    audio_path = audiobook['folder']['audio_path']
    audio_path_full = os.path.join('/static', os.path.relpath(audio_path, 'static'))

    bookmark_file = os.path.join(audiobook['folder']['path'], 'bookmark.txt')
    bookmark = 0

    if os.path.exists(bookmark_file):
        with open(bookmark_file, 'r') as f:
            bookmark = float(f.read())

    return render_template('player.html',
                            bookmark=bookmark,
                            book_id=audiobook['id'],
                            random_cover=random_cover_path,
                            title=audiobook['title'],
                            author=audiobook['author'],
                            audio_path=audio_path_full)

# Receives a POST request with the audiobook ID and current playback time. 
# Updates the bookmark file for the specified audiobook with the current playback time.

@app.route('/api/bookmark', methods=['POST'])
def save_playback_position():
    audiobook_id = request.form.get('audiobookId')
    current_time = float(request.form.get('currentTime'))

    audiobook = get_audiobook_from_id(audiobook_id)
    path = audiobook['folder']['path']
    bookmark_file = os.path.join(path, 'bookmark.txt')

    with open(bookmark_file, 'w') as f:
        f.write(str(current_time))
    return jsonify({'success': True})
    

# Receive a GET request with the audiobook ID.
# Delete the audiobook folder. 
    
@app.route('/delete/<audiobook_id>', methods=['GET'])
@auth.login_required
def delete(audiobook_id):
    audiobook = get_audiobook_from_id(audiobook_id)

    if audiobook:
        shutil.rmtree(audiobook['folder']['path'], ignore_errors=True)
        return jsonify({'message': 'Audiobook deleted. Please wait...'}), 200, {'Refresh': '2; url=/sync'}
    else:
        return jsonify({'message': 'Audiobook ID not found. Please wait...'}), 400, {'Refresh': '3; url=/'}
    
# favicon.ico

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
