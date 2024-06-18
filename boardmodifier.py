import os
import re
import time
import requests
import zipfile
import shutil
import win32com.client
 
from colorama import Fore, init
 
init(autoreset=True)
 
ARDUINO_CLI_ZIP_URL = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
ARDUINO_CLI_FILENAME = "arduino-cli.exe"
SKETCH_FILE = "mouse/mouse.ino"
BOARDS_TXT_LOCATION = os.path.expandvars("%LOCALAPPDATA%/Arduino15/packages/arduino/hardware/avr/1.8.6/boards.txt")
 
def download_arduino_cli():
    print(Fore.CYAN + "Downloading Arduino CLI...")
    response = requests.get(ARDUINO_CLI_ZIP_URL, stream=True)
    with open("arduino-cli.zip", "wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)
 
    with zipfile.ZipFile("arduino-cli.zip", 'r') as zip_ref:
        zip_ref.extractall("./")
 
def replace_and_save_boards_txt(vid, pid):
    with open(BOARDS_TXT_LOCATION, 'r') as file:
        data = file.readlines()
 
    for idx, line in enumerate(data):
        if line.startswith("leonardo.build.vid="):
            data[idx] = f"leonardo.build.vid={vid}\n"
        elif line.startswith("leonardo.build.pid="):
            data[idx] = f"leonardo.build.pid={pid}\n"
        elif "leonardo.upload_port." in line and ".vid=" in line:
            suffix = line.split(".vid=")[0].split("leonardo.upload_port.")[1]
            data[idx] = f"leonardo.upload_port.{suffix}.vid={vid}\n"
        elif "leonardo.upload_port." in line and ".pid=" in line:
            suffix = line.split(".pid=")[0].split("leonardo.upload_port.")[1]
            data[idx] = f"leonardo.upload_port.{suffix}.pid={pid}\n"
        elif line.startswith("leonardo.vid."):
            suffix = line.split("leonardo.vid.")[1].split("=")[0]
            data[idx] = f"leonardo.vid.{suffix}={vid}\n"
        elif line.startswith("leonardo.pid."):
            suffix = line.split("leonardo.pid.")[1].split("=")[0]
            data[idx] = f"leonardo.pid.{suffix}={pid}\n"
 
    with open(BOARDS_TXT_LOCATION, 'w') as file:
        file.writelines(data)
 
def list_mice_devices():
    wmi = win32com.client.GetObject("winmgmts:")
    devices = wmi.InstancesOf("Win32_PointingDevice")
    mice_list = []
 
    for device in devices:
        name = device.Name
        match = re.search(r'VID_(\w+)&PID_(\w+)', device.PNPDeviceID)
        
        vid, pid = match.groups() if match else (None, None)
        mice_list.append((name, vid, pid))
 
    return mice_list
 
def select_mouse_and_configure():
    print(Fore.CYAN + "\nDetecting mice devices...")
    mice = list_mice_devices()
 
    if not mice:
        print(Fore.RED + "No mouse devices found. Exiting...")
        time.sleep(5)
        exit()
 
    for idx, (name, vid, pid) in enumerate(mice, 1):
        print(f"{Fore.CYAN}{idx} →{Fore.RESET} {name}\tVID: {vid or 'Not found'}, PID: {pid or 'Not found'}")
 
    choice = int(input(Fore.CYAN + "Select your mouse number: ")) - 1
    _, vid, pid = mice[choice]
    replace_and_save_boards_txt("0x" + vid, "0x" + pid)
 
def install_avr_core():
    print(Fore.CYAN + "\nInstalling AVR 1.8.6...")
    os.system(f"{ARDUINO_CLI_FILENAME} core install arduino:avr@1.8.6 >NUL 2>&1")
    os.system(f"{ARDUINO_CLI_FILENAME} lib install Mouse >NUL 2>&1")
            
def compile_sketch():
    os.system(f"{ARDUINO_CLI_FILENAME} compile --fqbn arduino:avr:leonardo {SKETCH_FILE} >NUL 2>&1")
 
def upload_sketch():
    if not os.path.exists(SKETCH_FILE):
        print(Fore.RED + f"Error: Sketch file '{SKETCH_FILE}' not found!")
        return
    com_port = input(Fore.CYAN + "\nEnter your Arduino Leonardo COM port: ")
    print(Fore.GREEN + "Uploading sketch to Arduino...")
    os.system(f"{ARDUINO_CLI_FILENAME} upload -p {com_port} --fqbn arduino:avr:leonardo {SKETCH_FILE} >NUL 2>&1")
 
if __name__ == '__main__':
    download_arduino_cli()
    install_avr_core()
    select_mouse_and_configure()
    compile_sketch()
    upload_sketch()