import os
import subprocess

from core_logic.apk_string_decode_main_core_logic import WarningHandlerInterface
from core_logic.apk_string_decode_logic import isJavaSignatureValid

class CLIWarningHandler(WarningHandlerInterface):
    def warn(self, message):
        print(f"WARNING: {message}")


def cli_main_menu():
    while True:
        # Displaying the menu
        print("\nMenu:")
        print("1. Decode the Whole App")
        print("2. Decode 1 String")
        print("3. Add Java method call and Decode the Whole App")
        print("4. Use already decompile App to trigger Decode")
        print("5. Exit")

        # Getting user's choice
        choice = input("Enter your choice (1-5): ")

        # Executing code based on the choice
        if choice == '1':
            print("1. Decode the Whole App")
            return '1'
            # Whole App - Download, decompile, inject, compile, install, trigger
            #fullFlowWholeApp(digestApk, class_package_name, method_name, current_time)
        elif choice == '2':
            print("2. Decode 1 String")
            return '2'
            # Single String - Download, decompile, inject, compile, install, trigger
            #fullFlowSingleString(digestApk, class_package_name, method_name, parameter_value, current_time)
        elif choice == '3':
            print("Comming soon...")
            return '3'  
        elif choice == '4':
            print("4. Use already decompile App to trigger Decode")
            return '4'
            #partFlowWholeApp(class_package_name, method_name, current_time)
        elif choice == '5':
            print("Exiting the script.")
            return '5'
            #break  # This will exit the loop and end the script
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def getApkPath():
    # Get input from the user
    while True:
        print("- Insert app Digest -")     
        user_input = input("Enter the APK path: (or press enter if on Clipboard)")

        if user_input == "":
            insertedApkPath = getClipboardContent()
        else:
            insertedApkPath = user_input

        if isValidApkPath(insertedApkPath):
            return insertedApkPath
        else:
            print("Invalid input. Please enter a valid SHA256 hash.")

def isValidApkPath(path):
    return os.path.isfile(path)

def getClipboardContent():
    while True:
        try:
            clipboard_content = subprocess.check_output(["pbpaste"], universal_newlines=True).strip()
        except subprocess.CalledProcessError as e:
            print("Error reading clipboard:", e)
            clipboard_content = ""

        # Print the raw clipboard content for debugging
        print("Raw Clipboard Content:")
        print(repr(clipboard_content))

        if len(clipboard_content) < 1:
            print('Not a valid clipboard content')
        else:
            return clipboard_content


def getJavaMethodCall():
    while True:
        print('- Insert the Java Method Call (com.example.myapplication.decode("decode_string")) -')     
        user_input = input("Enter a Method call and parameter: (or press enter if on Clipboard)")

        if user_input == "":
            receivedJavaSignature = getClipboardContent()
        else:
            receivedJavaSignature = user_input
        
        if(isJavaSignatureValid(receivedJavaSignature)):
            return receivedJavaSignature
        else:
          print("Invalid input. Please enter a valid Java Method Call.") 

def get_cli_user_inputs():
    # - Handle Inputs: 
    return getJavaMethodCall(), getApkPath() 
