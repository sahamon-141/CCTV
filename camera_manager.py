import json
import os
from collections import defaultdict

class CameraManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.cameras = self._load_cameras()
        
    def _load_cameras(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cameras(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.cameras, f)
    
    def add_camera(self, name, url):
        self.cameras[name] = {'url': url, 'active': True}
        self._save_cameras()
    
    def remove_camera(self, name):
        if name in self.cameras:
            del self.cameras[name]
            self._save_cameras()
    
    def get_cameras(self):
        return self.cameras
    
    def get_camera(self, name):
        return self.cameras.get(name)
    
    def check_stream(self, url):
        # Implement stream checking logic
        # You might use requests or cv2 to check if stream is available
        return True  # Simplified for example