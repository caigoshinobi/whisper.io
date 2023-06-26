import os
import json
from flask import jsonify

def get_json():
    return os.path.join(os.path.dirname(__file__), 'audiobooks.json')
  
def get_audiobook_from_id(audiobook_id):

  audiobooks_file = get_json()

  if os.path.exists(audiobooks_file):
    with open(audiobooks_file, 'r') as f:
      audiobooks_data = json.load(f)

      for audiobook_data in audiobooks_data['audiobooks']:
        if audiobook_data['id'] == audiobook_id:
          return audiobook_data
  else:
    return jsonify({'message': 'Audiobook ID not found. Please wait...'}), 400, {'Refresh': '2; url=/'}