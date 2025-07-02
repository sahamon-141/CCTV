import os
import shutil
import time
from datetime import datetime
import psutil

class StorageManager:
    def __init__(self, base_path):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def get_disk_usage(self):
        usage = psutil.disk_usage(self.base_path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }
    
    def get_video_path(self, camera_name, date, hour, minute):
        path = os.path.join(self.base_path, camera_name, date, hour)
        os.makedirs(path, exist_ok=True)
        return os.path.join(path, f'{minute}.mp4')
    
    def get_recordings(self):
        recordings = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.mp4'):
                    rel_path = os.path.relpath(os.path.join(root, file), self.base_path)
                    stats = os.stat(os.path.join(root, file))
                    recordings.append({
                        'path': rel_path,
                        'size': stats.st_size,
                        'modified': time.ctime(stats.st_mtime),
                        'camera': rel_path.split(os.sep)[0],
                        'date': rel_path.split(os.sep)[1],
                        'hour': rel_path.split(os.sep)[2],
                        'minute': file.replace('.mp4', '')
                    })
        return recordings
    
    def filter_recordings(self, date=None, camera_name=None):
        all_recordings = self.get_recordings()
        filtered = []
        
        for rec in all_recordings:
            if date and date not in rec['path']:
                continue
            if camera_name and camera_name != rec['camera']:
                continue
            filtered.append(rec)
        
        return filtered
    
    def delete_recording(self, rel_path):
        full_path = os.path.join(self.base_path, rel_path)
        if os.path.exists(full_path):
            os.remove(full_path)
    
    def manage_disk_space(self):
        usage = self.get_disk_usage()
        
        if usage['percent'] >= 95:
            # Delete oldest recordings until we reach 85%
            recordings = sorted(self.get_recordings(), key=lambda x: x['modified'])
            
            while usage['percent'] > 85 and recordings:
                oldest = recordings.pop(0)
                self.delete_recording(oldest['path'])
                usage = self.get_disk_usage()