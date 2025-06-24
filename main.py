import sys
import argparse
import os

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition

from cli.apk_string_decode_cli import CLIWarningHandler, get_cli_user_inputs, cli_main_menu
from gui.apk_string_decode_gui import GUIWarningHandler, get_gui_user_input, gui_main_menu, LoadingScreen
from core_logic.apk_string_decode_consts import INTERFACE_GUI, INTERFACE_CLI, STRINGS_HANDLING_PROCESS_METHOD_ROOT, STRINGS_HANDLING_PROCESS_METHOD_RECEIVERLOGCAT, STRINGS_HANDLING_PROCESS_METHOD_DEFAULT

from core_logic.apk_string_decode_main_core_logic import decodeWholeApp, decodeWholeAppFromPart2, MainLogicInterface
from core_logic.apk_string_decode_logic import getExtractedInfoFromJavaSignatureCall
from core_logic.apk_string_decode_adb_utils import checkPreRequesites
from core_logic.apk_string_decode_common_utils import registersCurrentTime
from core_logic.apk_string_decode_config import Config



def getUserInterfaceHandler(user_interface):
    if user_interface == INTERFACE_GUI:
        return GUIWarningHandler()
    else:
        return CLIWarningHandler()

def showInputsScreen(user_interface):
    #if user_interface == INTERFACE_GUI:
    if user_interface == INTERFACE_GUI:
        return get_gui_user_input()
    else:
        return get_cli_user_inputs()

def showMainMenuScreen(user_interface):
    if user_interface == INTERFACE_GUI:
        return gui_main_menu()
    else:
        return cli_main_menu()


#python apk_string_decode.py -p /path/to/somefile -s "Lcom/example/MyClass;->myMethod()V"
#python apk_string_decode.py --path /path/to/somefile --java_signature "Lcom/example/MyClass;->myMethod()V"

def runDecodeApp(task_thread, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method):
    # Executing code based on the choice
    if main_menu_choice == '1':
        # Whole App - Download, decompile, inject, compile, install, trigger
        decodeWholeApp(task_thread, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method)
    #elif main_menu_choice == '2':
        # Single String - Download, decompile, inject, compile, install, trigger
        #fullFlowSingleString(digestApk, class_package_name, method_name, parameter_value, current_time)
    elif main_menu_choice == '3':
        print("Comming soon...")  
    elif main_menu_choice == '4':
        decodeWholeAppFromPart2(task_thread, class_package_name, method_name, java_signature, "", current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method)
    elif main_menu_choice == '5':
        print("Exiting the script.")
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


class TaskThread(QThread):
    finished = pyqtSignal()  # Signal to indicate task completion
    pauseRequested = pyqtSignal(str, str)  # Signal to request a pause
    updateText = pyqtSignal(str)  # Signal to send text updates

    def __init__(self, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method, parent=None):
        super(TaskThread, self).__init__()
        self._mutex = QMutex()
        self._pause_condition = QWaitCondition()
        self.main_menu_choice = main_menu_choice
        self.apk_path = apk_path
        self.class_package_name = class_package_name
        self.method_name = method_name
        self.java_signature = java_signature
        self.current_time = current_time
        self.is_multi_processing = is_multi_processing
        self.is_file_rollback = is_file_rollback
        self._isPaused = False
        self.is_complex_flow = is_complex_flow
        self.is_clean_static_variables = is_clean_static_variables
        self.single_class_analysis = single_class_analysis
        self.strings_handling_process_method = strings_handling_process_method

    def run(self):
        print("Task Initiated")
        self.perform_long_running_task()
        print("Task Completed")
        self.finished.emit()

    def perform_long_running_task(self):
        import time
        #time.sleep(5)  # Simulate a long-running task
        runDecodeApp(self, self.main_menu_choice, self.apk_path, self.class_package_name, self.method_name, self.java_signature, self.current_time, self.is_multi_processing, self.is_file_rollback, self.is_complex_flow, self.is_clean_static_variables, self.single_class_analysis, self.strings_handling_process_method)
        
    def pause(self, tile="", message=""):
        self._mutex.lock()
        self._isPaused = True
        self._mutex.unlock()
        self.pauseRequested.emit(tile, message)

    def resume(self):
        self._mutex.lock()
        self._isPaused = False
        self._pause_condition.wakeAll()
        self._mutex.unlock()

    def check_pause(self):
        self._mutex.lock()
        while self._isPaused:
            self._pause_condition.wait(self._mutex)
        self._mutex.unlock()


def showDecodeUi(user_interface, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method):
    if user_interface == INTERFACE_GUI:
        mainApp = MainApplication(sys.argv, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method)
        mainApp.run()
    else:
        runDecodeApp(None, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method)


def getArguments(arg_list=None):
    parser = argparse.ArgumentParser(description='Process "path" and "java_signature" parameters.')

    # Add arguments with flags
    parser.add_argument('-p', '--path', type=str, required=False, help='The apk file path to be processed.')
    parser.add_argument('-s', '--java_signature', type=str, required=False, help='The Java signature to be processed.')
    parser.add_argument('-m', '--multi_processing', type=str, choices=['true', 'false'], required=False, help='If the processing should use a multiple cores. Accepts true or false.')
    parser.add_argument('-r', '--file_rollback', type=str, choices=['true', 'false'], required=False, help='If the app should roll back to the original file in case of a bad compilation')
    parser.add_argument('--gui', action='store_true', help='Enable GUI mode.')
    parser.add_argument('-c', '--complex_flow', type=str, choices=['true', 'false'], required=False, help='If the app should do a deep complex analyse on every class')
    parser.add_argument('-v', '--clean_static_variables', type=str, choices=['true', 'false'], required=False, help='If the app should clean the static references variables being used on the decode process')
    parser.add_argument('-g', '--single_class_analysis', type=str, required=False, help='If provided, will only decode the app with the passed class paths')

    parser.add_argument('-e', '--strings_handling_process_method', type=int, choices=[0, 1, 2], required=False, help='0 - Will pass Strings using the most optimzed process; 1 - Will pass Strings using local storage (Requires ROOT); 2 - Will Pass Strings using a Broadcast Receiver and logcat')
    parser.add_argument('-f', '--extracted_folder_path', type=str, required=False, help='If provided, will set used as the base extracted folder. Otherwise, it will the same as the provided apk path')

    #Use custom arg list if provided (for test_runner)
    args = parser.parse_args(arg_list)

    # Parse the arguments
    #args = parser.parse_args()

    if args.multi_processing is not None:
        args.multi_processing = True if args.multi_processing.lower() == 'true' else False
    else:
        args.multi_processing = True

    if args.file_rollback is not None:
        args.file_rollback = True if args.file_rollback.lower() == 'true' else False
    else:
        args.file_rollback = False

    if args.gui:
        user_interface = INTERFACE_GUI
    else: 
        user_interface = INTERFACE_CLI

    if args.complex_flow is not None:
        args.complex_flow = True if args.complex_flow.lower() == 'true' else False
    else:
        args.complex_flow = True

    if args.clean_static_variables is not None:
        args.clean_static_variables = True if args.clean_static_variables.lower() == 'true' else False
    else:
        args.clean_static_variables = False
   
    args.strings_handling_process_method = args.strings_handling_process_method if args.strings_handling_process_method is not None else STRINGS_HANDLING_PROCESS_METHOD_DEFAULT

    # Access the arguments using the specified flags
    path = args.path
    java_signature = args.java_signature
    is_multi_processing = args.multi_processing
    is_file_rollback = args.file_rollback
    isComplexFlow  = args.complex_flow
    isCleanStaticVariables = args.clean_static_variables
    single_class_analysis = args.single_class_analysis
    strings_handling_process_method = args.strings_handling_process_method
    extracted_folder_path = args.extracted_folder_path

    return user_interface, path, java_signature, is_multi_processing, is_file_rollback, isComplexFlow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method, extracted_folder_path


class MainApplication(QApplication):
    def __init__(self, argv, main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method):
        super().__init__(argv)
        self.loading_screen = LoadingScreen()
        self.task_thread = TaskThread(main_menu_choice, apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method)

        #self.task_thread.finished.connect(self.loading_screen.close)
        self.task_thread.finished.connect(self.task_thread.deleteLater)
        self.task_thread.pauseRequested.connect(self.onPauseRequested)
        self.task_thread.finished.connect(self.showCompletionDialog) 

        self.task_thread.updateText.connect(self.loading_screen.updateMessage)

    def run(self):
        self.loading_screen.show()
        self.task_thread.start()
        self.exec_()  # Start the event loop

    def updateLoadingMessage(self, message):
        self.loading_screen.updateMessage(message)

    def onPauseRequested(self, title, message):
        # This method is automatically called when the pauseRequested signal is emitted
        result = QMessageBox.information(None, title, message, QMessageBox.Ok)
        if result == QMessageBox.Ok:
            self.task_thread.resume()  # Resume the background task

    def showCompletionDialog(self):
        QMessageBox.information(None, "Task Completed", "Decode Completed.")
        self.loading_screen.close()

def run(arg_list=None):
    #app = QApplication(sys.argv)

    print(" ----- GET ARGUMENTS ----- ")
    user_interface, apk_path, java_signature, is_multi_processing, is_file_rollback, isComplexFlow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method, extracted_folder_path = getArguments(arg_list)

    current_time = registersCurrentTime() 


    handler = getUserInterfaceHandler(user_interface)
    logic = MainLogicInterface(handler)

    #Check device status
    checkPreRequesites(logic)

    if(not apk_path or not java_signature):
        print(" ----- HANDLEING INPUTS ----- ")
        java_signature, apk_path = showInputsScreen(user_interface)
        
    if extracted_folder_path is None:
        extracted_folder_path = os.path.dirname(apk_path)

    Config.set_download_path(extracted_folder_path)


    print(" ----- SHOW MAIN MENU ----- ")
    main_menu_choice = showMainMenuScreen(user_interface)
 
    class_package_name, method_name, java_signature = getExtractedInfoFromJavaSignatureCall(java_signature)

    showDecodeUi(user_interface, main_menu_choice[0], apk_path, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, isComplexFlow, isCleanStaticVariables, single_class_analysis, strings_handling_process_method)


if __name__ == '__main__':
    run()
