import os
import cv2
import threading
import time
from datetime import datetime
from collections import defaultdict, deque

class VideoRecorder:
    def __init__(self, camera_manager, storage_manager):
        self.camera_manager = camera_manager
        self.storage_manager = storage_manager
        self.is_recording = False
        self.recording_threads = {}
        self.frame_buffers = {}
        self.fps_values = defaultdict(deque)
        self.current_minute = None
        self.show_windows = True  # Control whether to show preview windows
    
    def start_recording(self):
        self.is_recording = True
        for name, camera in self.camera_manager.get_cameras().items():
            if camera['active']:
                thread = threading.Thread(
                    target=self._record_camera,
                    args=(name, camera['url'])
                )
                self.recording_threads[name] = thread
                self.frame_buffers[name] = deque(maxlen=100)
                thread.start()
    
    def stop_recording(self):
        self.is_recording = False
        for thread in self.recording_threads.values():
            thread.join()
        cv2.destroyAllWindows()  # Close all preview windows when stopping
        self.recording_threads = {}
        self.frame_buffers = {}
    
    def _record_camera(self, name, url):
        cap = cv2.VideoCapture(url)
        fps = self._calculate_fps(cap, name)
        
        if fps <= 0:
            fps = 15  # Default FPS if calculation fails
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_hour = datetime.now().strftime('%H')
        self.current_minute = datetime.now().strftime('%M')
        
        # Create initial video file
        file_path = self.storage_manager.get_video_path(name, current_date, current_hour, self.current_minute)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(file_path, fourcc, fps, (800, 600))
        
        last_check_time = time.time()
        window_name = f"Live Feed: {name}"
        
        while self.is_recording and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Write frame to video file
            out.write(frame)
            
            # Show live feed in window if enabled
            if self.show_windows:
                display_frame = frame.copy()
                cv2.putText(display_frame, f"Recording: {current_date} {current_hour}:{self.current_minute}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow(window_name, display_frame)
                cv2.waitKey(1)  # Needed to update the window
            
            self.frame_buffers[name].append(time.time())
            
            # Check if we've reached a new minute
            current_time = time.time()
            if current_time - last_check_time >= 1:  # Check every second
                now = datetime.now()
                current_minute = now.strftime('%M')
                
                if current_minute != self.current_minute:
                    # Minute changed, create new file
                    out.release()
                    current_hour = now.strftime('%H')
                    self.current_minute = current_minute
                    file_path = self.storage_manager.get_video_path(
                        name, current_date, current_hour, self.current_minute)
                    out = cv2.VideoWriter(file_path, fourcc, fps, (800, 600))
                
                last_check_time = current_time
            
            # Check disk space every 5 minutes
            if int(current_time) % 300 == 0:
                self.storage_manager.manage_disk_space()
        
        cap.release()
        if out:
            out.release()
        cv2.destroyWindow(window_name)
    
    def _calculate_fps(self, cap, name, sample_duration=5):
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < sample_duration and cap.isOpened():
            ret, _ = cap.read()
            if ret:
                frame_count += 1
        
        fps = frame_count / sample_duration
        self.fps_values[name].append(fps)
        
        return sum(self.fps_values[name]) / len(self.fps_values[name])