import json
import os
from collections import defaultdict
import requests
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
    def set_night_vision(self, camera_name, enable):
        camera = self.get_camera(camera_name)
        if not camera:
            return False
    
        base_url = camera['url'].replace(':81/stream', '')
        params = {
            'night': [
            ('var=framesize&val=8'),
            ('var=quality&val=30'),
            ('var=brightness&val=2'),
            ('var=contrast&val=2'),
            ('var=saturation&val=-2'),
            ('var=special_effect&val=2'),
            ('var=awb&val=0'),
            ('var=awb_gain&val=0'),
            ('var=wb_mode&val=1'),
            ('var=ae_level&val=-2'),
            ('var=aec_value&val=1023'),
            ('var=gainceiling&val=2')
        ],
        'day': [
            # Reset to daytime defaults
            ('var=framesize&val=8'),
            ('var=quality&val=10'),
            ('var=brightness&val=0'),
            ('var=contrast&val=0'),
            ('var=saturation&val=0'),
            ('var=special_effect&val=0'),
            ('var=awb&val=1'),
            ('var=awb_gain&val=1'),
            ('var=wb_mode&val=0'),
            ('var=ae_level&val=0'),
            ('var=aec_value&val=300'),
            ('var=gainceiling&val=0')
            ]
        }
    
    
        settings = params['night'] if enable else params['day']
    
        for setting in settings:
            try:
                control_url = f"{base_url}/control?{setting}"
                response = requests.get(control_url, timeout=2)
                if response.status_code != 200:
                    print(f"Failed to set {setting} for {camera_name}")
            except Exception as e:
                print(f"Error setting night vision: {str(e)}")
    
        camera['night_vision'] = enable
        self._save_cameras()
        return True