import os
from flask import Flask, request, send_file, abort
from util.process_video_utils import save_uploaded_video, process_video, load_json_results, cleanup_files
from util.heatmap import generate_heatmap

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') or os.path.join('static', 'videos')
RESULTS_FILE_PATH = os.getenv('RESULT_FILE_PATH') or os.path.join('static', 'results')
CONFIG_FILE = os.getenv('CONFIG_FILE') or os.path.join('helpers', 'config.json')
HEATMAP_FOLDER = os.getenv('UPLOAD_FOLDER') or os.path.join('static', 'heatmap')

# preprocessing
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULTS_FILE_PATH):
    os.makedirs(RESULTS_FILE_PATH)

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process():
    video_file = save_uploaded_video(request.files, UPLOAD_FOLDER)
    results_file = process_video(video_file, RESULTS_FILE_PATH, CONFIG_FILE)
    results = load_json_results(results_file)
    heatmap_id = generate_heatmap(results, HEATMAP_FOLDER)
    cleanup_files(video_file, results_file)
    return {
        'heatmap_id': heatmap_id
    }


@app.route('/download/<string:heatmap_id>', methods=['GET'])
def get_heatmap(heatmap_id):

    heatmap_fn = os.path.join(HEATMAP_FOLDER, f'{heatmap_id}.png')
    print(heatmap_fn)
    if os.path.exists(heatmap_fn):
        return send_file(heatmap_fn, mimetype='image/png')

    abort(404, description="Heatmap id not found.")

