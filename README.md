# CCTV Surveillance System with Flask

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-lightgrey)
![OpenCV](https://img.shields.io/badge/opencv-4.5%2B-orange)
![ESP32-CAM](https://img.shields.io/badge/ESP32--CAM-compatible-green)
![Raspberry Pi 4](https://img.shields.io/badge/ESP32--CAM-compatible-green)
A Cheap Wireless Home surveillance system that records and manages video streams from ESP32-CAM modules, with a Flask-based web interface.

## ✨ Features

- **Multi-camera support** - Add unlimited cameras via web interface
- **Smart recording** - Creates new video files every minute in a their respective Hour and Day folder
- **Advanced filtering** - Search recordings by date, hour, minute, and camera
- **Disk management** - Automatic cleanup when storage reaches thresholds
- **Live preview** - View streams while recording
- **Responsive web UI** - Access from any device

## 📦 Hardware Requirements

- Raspberry Pi 4 (With Raspbian 64 bit operating system) (Recommended)
- ESP32-CAM modules (Used Esp32S3 xiao camera and AI Thinker Esp32CAM boards)
- USB storage device(external SSD or HDD recommended) (for recordings)
- A 400-1000 mah battery to power the esp32s3 cam even in power cut 

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/cctv-surveillance-system.git
   cd cctv-surveillance-system
2. **Install dependencies**:
   -sudo apt update && sudo apt upgrade -y 
   -sudo apt-get install python3-pip python3-venv libatlas-base-dev ffmpeg
   -sudo apt install python-opencv
   -sudo apt install python flask
3. **Mount Storage**:
   # Create mount point
   sudo mkdir /media/usb

    # Find your disk
    sudo fdisk -l

    # Mount (add to /etc/fstab for auto-mount)
    sudo mount /dev/sda1 /media/usb (replace dev/sda1 with your disk name)
4.  ** Execute Flask Application **
    -open terminal
    -cd /yourProject/Directory
    -sudo python3 app.py

## 🖥️ Web Interface
**Main Dashboard**
![image](https://github.com/user-attachments/assets/495886c6-dc3b-4841-8cf4-f3163f038b40)

-Real-time camera streams
-Disk usage monitoring
-One-click recording control

**Recordings Manager**
![image](https://github.com/user-attachments/assets/232e9502-824e-438f-a35a-3e141e7e2e0d)

Filter by:
📅 Date (YYYY-MM-DD)

🕒 Hour (00-23)

⏱️ Minute (00-59)

📷 Camera name

Actions:
▶️ Play in browser

⬇️ Download

🗑️ Delete

**Live View**
![image](https://github.com/user-attachments/assets/7503799b-cda1-43ba-b2bc-6f217bb9c0c1)

**Home Setup**
![WhatsApp Image 2025-07-03 at 00 25 55_b6752dc2](https://github.com/user-attachments/assets/28eb499a-a0fd-42e0-bff1-57463f889a2e)

🤝 Contributing
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request
