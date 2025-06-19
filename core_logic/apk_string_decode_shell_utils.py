from core_logic.apk_string_decode_consts import path_to_extracted_folder, keystore_name, keystore_password, key_alias, first_name, last_name, extracted_apk, decoded_apk
from core_logic.apk_string_decode_logic_utils import updateStatus
import os
import subprocess


def changeApkPermission(last_apk):

    if last_apk and os.path.exists(last_apk):
        # Construct the apktool command
        command = ["chmod", "777", last_apk]

        # Run the apktool command using subprocess
        subprocess.run(command)
        return ""
    else:
        return "No valid APK found to decompile."    
    

def decompileLastApk(task_thread, last_apk):
    updateStatus(task_thread, " ----- DECOMPILE APK ----- ")
    if last_apk:
        # Construct the apktool command
        command = ["apktool", "d", "-o", path_to_extracted_folder, last_apk, "-f"]
        
        # Run the apktool command using subprocess
        subprocess.run(command)
    else:
        updateStatus(task_thread, "No valid APK found to decompile.")

def decompileLastApkWithoutResources(task_thread, last_apk):
    updateStatus(task_thread, " ----- DECOMPILE APK WITHOUT RESOURCES ----- ")
    if last_apk:
        # Construct the apktool command
        #command = ["apktool", "d", last_apk, "-r", "-o", path_to_extracted_folder]
        command = ["apktool", "d", last_apk, "-o", path_to_extracted_folder, "-f", "-resm", "dummy"]
        #-resm <mode>
        
        # Run the apktool command using subprocess
        subprocess.run(command)
    else:
        updateStatus(task_thread, "No valid APK found to decompile.")


def generateKeystore(task_thread):
    updateStatus(task_thread, " ----- GENERATE KEYSTORE ----- ")
    # Generate a keystore
    command = [
        'keytool',
        '-genkeypair',
        '-v',
        '-keystore', keystore_name,
        '-keyalg', 'RSA',
        '-keysize', '2048',
        '-validity', '10000',
        '-storepass', keystore_password,  # Include the keystore password
        '-alias', key_alias,
        '-keypass', keystore_password,  # Include the key password (optional)
        '-dname', f'CN={first_name} {last_name}, OU=YourOrganization, O=YourCompany, L=YourCity, ST=YourState, C=YourCountry'
    ]
    subprocess.run(command)


def signExtractedApk(task_thread):
    updateStatus(task_thread, " ----- SIGN EXTRACTED APK ----- ")
    try:
        signApk(extracted_apk)
    except subprocess.CalledProcessError as e:
        updateStatus(task_thread, f'Error signning {extracted_apk}: {e}')
        return False
    return True
    
def signDecodedApk(task_thread):
    updateStatus(task_thread, " ----- SIGN DECODED APK ----- ")
    try:
        signApk(decoded_apk)
    except subprocess.CalledProcessError as e:
        updateStatus(task_thread, f'Error signning {extracted_apk}: {e}')
        return False
    return True
        
def signApk(apk_path):
    if os.path.isfile(apk_path):
        # Sign the APK
        command = [
            'apksigner', 'sign',
            '--ks', keystore_name,
            '--ks-key-alias', key_alias,
            '--ks-pass', f'pass:{keystore_password}',
            '--key-pass', f'pass:{keystore_password}',
            apk_path
        ]
        subprocess.run(command)