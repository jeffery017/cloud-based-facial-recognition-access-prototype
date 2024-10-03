import threading
import subprocess

def run_ipCam():
    subprocess.Popen(['python3', 'main.py'], cwd='ipcam')

def run_gateway():
    subprocess.Popen(['python3', 'main.py'], cwd='gateway')

def run_cloud():
    subprocess.Popen(['python3', 'main.py'], cwd='cloud')

if __name__ == "__main__":
    # Create threads for each server
    ipCam_thread = threading.Thread(target=run_ipCam)
    gateway_thread = threading.Thread(target=run_gateway)
    cloud_thread = threading.Thread(target=run_cloud)

    # Start each thread
    ipCam_thread.start()
    gateway_thread.start()
    cloud_thread.start()

    # Join threads to main thread to keep them alive
    ipCam_thread.join()
    gateway_thread.join()
    cloud_thread.join()

    