from core_logic.apk_string_decode_consts import apksigner_installation, BEHAVIOR_STATUS_TASK_TIMEOUT_SECONDS, BEHAVIOR_STATUS_TRUE, BEHAVIOR_STATUS_TASK_FLAG_FILE
from core_logic.apk_string_decode_logic_utils import updateStatus

import time
import subprocess
import sys

def copy_file_from_tmp_to_internal(package_name):
    device_tmp_path = "/data/local/tmp/apk_string_decode_instances.txt"
    app_file_path = f"/data/data/{package_name}/files/apk_string_decode_instances.txt"

    print(f"Copying file from {device_tmp_path} to {app_file_path} using su 0...")

    full_command = f"su 0 cat {device_tmp_path} > {app_file_path}"

    result = subprocess.run(
        ["adb", "shell", full_command],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("File copied successfully.")
    else:
        print("Failed to copy file:")
        print(result.stderr)

def clearLogcat(task_thread):
    updateStatus(task_thread, " ----- CLEAR LOGCAT ----- ")
    try:
        subprocess.run(["adb", "logcat", "-c"], check=True)
        print("Logcat cleared successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to clear logcat:", e)

def wait_for_android_status_flag(package_name):
    print(f"Waiting for Android decoding process to complete...")
    start_time = time.time()
    while time.time() - start_time < BEHAVIOR_STATUS_TASK_TIMEOUT_SECONDS:
        flag = read_behavior_flag(package_name)
        if flag == BEHAVIOR_STATUS_TRUE:
            print("Android decoding completed")
            return True
        time.sleep(1)

    print("Timeout reached. Behavior status falg not updated")
    return False

def read_behavior_flag(package_name):
    cmd = f'adb shell "su 0 cat /data/data/{package_name}/files/{BEHAVIOR_STATUS_TASK_FLAG_FILE}"'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        return result.stdout.decode('utf-8').strip()
    except UnicodeDecodeError:
        print("Could not decode file content. Possibly corrupted or binary.")
        return None
    
def checkPreRequesites(main_logic_interface):
    # Run the adb devices command and capture its output
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Split the output into lines
    lines = result.stdout.splitlines()

    # Filter out empty lines and the first line (which is a header)
    devices = [line for line in lines if line and not line.startswith('List')]

    # Check if any devices are connected
    if not devices:
        main_logic_interface.showWarnMessage("No Android devices found. Please attach a device and start again.")
        sys.exit()  # Exit the script

    if not isApksignerAvailable(main_logic_interface):
        main_logic_interface.showWarnMessage("Apksigner is not available, please install it")
        sys.exit()  # Exit the script

def isApksignerAvailable(main_logic_interface):
    try:
        # Attempt to execute 'apksigner --version' command
        subprocess.run(["apksigner", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("apksigner is available.")
        return True
    except subprocess.CalledProcessError:
        intial_message = "apksigner is not installed correctly or not added to PATH."
        return False
    except FileNotFoundError:
        intial_message = "apksigner command is not available.\n Somethinh Something"

    main_logic_interface.showWarnMessage(intial_message + "\n\n" + apksigner_installation)
    
    return False    
    