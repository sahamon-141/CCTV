import os
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from camera_manager import CameraManager
from video_recorder import VideoRecorder
from storage_manager import StorageManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize components
storage_manager = StorageManager('/media/usb')
camera_manager = CameraManager()
recorder = VideoRecorder(camera_manager, storage_manager)

# Global state
is_recording = False
recording_thread = None

@app.route('/')
def index():
    cameras = camera_manager.get_cameras()
    disk_usage = storage_manager.get_disk_usage()
    return render_template('index.html', 
                         cameras=cameras, 
                         is_recording=is_recording,
                         disk_usage=disk_usage)

@app.route('/add_camera', methods=['POST'])
def add_camera():
    name = request.form.get('name')
    url = request.form.get('url')
    if name and url:
        camera_manager.add_camera(name, url)
    return redirect(url_for('index'))

@app.route('/remove_camera/<name>')
def remove_camera(name):
    camera_manager.remove_camera(name)
    return redirect(url_for('index'))

@app.route('/start_recording')
def start_recording():
    global is_recording, recording_thread
    if not is_recording:
        is_recording = True
        recording_thread = threading.Thread(target=recorder.start_recording)
        recording_thread.start()
    return redirect(url_for('index'))

@app.route('/stop_recording')
def stop_recording():
    global is_recording, recording_thread
    if is_recording:
        is_recording = False
        recorder.stop_recording()
        recording_thread.join()
    return redirect(url_for('index'))

@app.route('/fullscreen/<camera_name>')
def fullscreen(camera_name):
    camera = camera_manager.get_camera(camera_name)
    return render_template('fullscreen.html', camera=camera)

@app.route('/recordings')
def recordings():
    recordings = storage_manager.get_recordings()
    cameras = camera_manager.get_cameras()  # Get the cameras list
    return render_template('recordings.html', 
                         recordings=recordings,
                         cameras=cameras)  # Pass cameras to template

@app.route('/download_recording/<path:filename>')
def download_recording(filename):
    return send_from_directory(storage_manager.base_path, filename, as_attachment=True)

@app.route('/delete_recording/<path:filename>')
def delete_recording(filename):
    storage_manager.delete_recording(filename)
    return redirect(url_for('recordings'))

@app.route('/filter_recordings', methods=['POST'])
def filter_recordings():
    date = request.form.get('date')
    camera_name = request.form.get('camera_name')
    recordings = storage_manager.filter_recordings(date, camera_name)
    return render_template('recordings.html', recordings=recordings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)