from core_logic.apk_string_decode_shell_utils import decompileLastApk, decompileLastApkWithoutResources, generateKeystore, signExtractedApk, changeApkPermission, signDecodedApk
from core_logic.apk_string_decode_logic import getPackageNameFromManifest, backupManifest, getDecodeClassRelateClassPath, createSmaliReceiver, createSmaliActivity, createSmaliService, createSmaliRunnable, createSmaliCommon, injectTriggerOnDecodeClass, check_method_in_smali, backupSmaliCode, collectParametersFromSmaliFiles, writeEncodedStringsIntoFileRoot, collectLargeLogResultsFromFile, collectLargeLogResultsFromLogcat, checkIfHasValidDecodedStrings, replaceWithDecodedStringOnSmaliFiles, restoreManifest, removeInjectedMethod, exportNotReplacedDecodedStrings, compareDictionaries
from core_logic.apk_string_decode_android_utils import removeElementsFromManifest, removeAppplicationNameFromManifest, addReceiverToManifest, compileApkWithRetries, installExtractedApk, triggerBroadcastReceiverSimplePing, validateIfPermissionsIsRequired, triggerActivityMultipleRoot, triggerBroadcastReceiverMultiple, compileDecodedApk
from core_logic.apk_string_decode_common_utils import convert_dot_to_slash
from core_logic.apk_string_decode_adb_utils import clearLogcat, copy_file_from_tmp_to_internal, wait_for_android_status_flag
from core_logic.apk_string_decode_logic_utils import updateStatus, isStringsHandlingProcessMethodRoot

from abc import ABC, abstractmethod

import multiprocessing
from multiprocessing import Manager, Pool, cpu_count, Lock
from functools import partial

import xml.etree.ElementTree as ET

from collections import defaultdict

from copy import deepcopy

import shutil

#Interfaces
class WarningHandlerInterface(ABC):
    @abstractmethod
    def warn(self, message):
        pass


class MainLogicInterface:
    def __init__(self, warning_handler: WarningHandlerInterface):
        self.warning_handler = warning_handler

    def showWarnMessage(self, message):
        # Example condition that triggers a warning
        self.warning_handler.warn(message)


def decodeWholeApp(task_thread, digestApk, class_package_name, method_name, java_signature, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method):
    appPackageName, compiledErrorMessage, relativeReceiverClassPath = fullFlowPart1(task_thread, digestApk, class_package_name, method_name, java_signature, current_time, is_file_rollback, strings_handling_process_method)

    if compiledErrorMessage == "":
        fullFlowPart2(task_thread, appPackageName, class_package_name, method_name, java_signature, relativeReceiverClassPath, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method)
    else:              
        updateStatus(task_thread, compiledErrorMessage)
        return compiledErrorMessage

def decompileAndCompileApk(task_thread, lastApk, class_package_name, method_name, java_signature, is_decompiling_with_resources):
    # - Disassemble APK:
    if is_decompiling_with_resources:
        decompileLastApk(task_thread, lastApk)
    else:
        decompileLastApkWithoutResources(task_thread, lastApk)

    appPackageName = getPackageNameFromManifest()
    
    # - Backup Manifest:
    backupManifest(task_thread)

    decodeClassLocationPath, decodeClassRelativeClassPath = getDecodeClassRelateClassPath(class_package_name) 


    # - Remove all Receivers, Services and Provider from Manifest
    removeElementsFromManifest(task_thread)

    # - Remove Application class from Manifest
    removeAppplicationNameFromManifest()

    # - Modify the AndroidManifest.xml:
    addReceiverToManifest(task_thread, decodeClassRelativeClassPath)  

    # - Create Smali Receiver:
    createSmaliReceiver(task_thread, decodeClassLocationPath, decodeClassRelativeClassPath)

    # - Create Smali Activity:
    createSmaliActivity(task_thread, decodeClassLocationPath, decodeClassRelativeClassPath)

    # - Create Smali Service:
    createSmaliService(task_thread, decodeClassLocationPath, decodeClassRelativeClassPath)

    # - Create Smali Runnable:
    createSmaliRunnable(task_thread, decodeClassLocationPath, decodeClassRelativeClassPath)

    # - Create Smali Common:
    createSmaliCommon(task_thread, decodeClassLocationPath, decodeClassRelativeClassPath)

    # - Create a static method inside Smali that triggers the decode method:
    injectTriggerOnDecodeClass(task_thread, class_package_name, method_name, java_signature)

    # - Reassemble the APK
    #compiledErrorMessage = compileApk(task_thread)
    compiledErrorMessage = compileApkWithRetries(task_thread)
    
    return appPackageName, compiledErrorMessage, decodeClassRelativeClassPath

def decodeWholeAppFromPart2(task_thread, class_package_name, method_name, java_signature, decodeClassRelativeClassPath, current_time, is_multi_processing, is_file_rollback, isComplexFlow, is_clean_static_variables, single_class_analysis, strings_handling_process_method):
    appPackageName = getPackageNameFromManifest()
    
    if decodeClassRelativeClassPath == "":
        decodeClassLocationPath, decodeClassRelativeClassPath = getDecodeClassRelateClassPath(class_package_name) 

    return fullFlowPart2(task_thread, appPackageName, class_package_name, method_name, java_signature, decodeClassRelativeClassPath, current_time, is_multi_processing, is_file_rollback, isComplexFlow, is_clean_static_variables, single_class_analysis, strings_handling_process_method)

def fullFlowPart1(task_thread, lastApk, class_package_name, method_name, java_signature, current_time, is_file_rollback, strings_handling_process_method): 

    updateStatus(task_thread, "lastApk: " + lastApk)   

    apkFileErrorMessage = changeApkPermission(lastApk)
    if apkFileErrorMessage != "":
        return None, apkFileErrorMessage, "" 


    appPackageName, compiledErrorMessage, relativeClassPath = decompileAndCompileApk(task_thread, lastApk, class_package_name, method_name, java_signature, True)

    #if compiledErrorMessage != "":
    #    #try recompiling the app without resources
    #    appPackageName, compiledErrorMessage = decompileAndCompileApk(task_thread, lastApk, class_package_name, method_name, java_signature, False)

    isMethodAvailableErrorMessage = check_method_in_smali(class_package_name, method_name)

    if compiledErrorMessage == "":
        if isMethodAvailableErrorMessage == "":
            # Generate keystore
            generateKeystore(task_thread)

            # Sign the modified APK
            signExtractedApk(task_thread)

            # - Install APK:
            installExtractedApkErrorMessage = installExtractedApk(task_thread, appPackageName)
            if installExtractedApkErrorMessage != "":
                return None, installExtractedApkErrorMessage, ""

            if is_file_rollback:
                backupSmaliCode()

            # - Gives permissions
            #givePermissionstoApp(appPackageName, current_time)
            return appPackageName, "", relativeClassPath
        else:
            return None, compiledErrorMessage, ""
    else:
        return None, compiledErrorMessage, ""


def fullFlowPart2(task_thread, appPackageName, class_package_name, method_name, java_signature, relativeReceiverClassPath, current_time, is_multi_processing, is_file_rollback, is_complex_flow, is_clean_static_variables, single_class_analysis, strings_handling_process_method):

    # Find the pattern in files and store in hash_map
    hash_map_original, hash_map_original_sanitize = collectParametersFromSmaliFiles(task_thread, convert_dot_to_slash(class_package_name), method_name, java_signature, is_multi_processing, is_complex_flow, is_clean_static_variables, single_class_analysis)

    if(hash_map_original != None and hash_map_original):
        # Display the hash map
        #for key, value in hash_map_original.items():
        #    print(f"Found '{key}' in files: {value}")

        #Clear logcat buffer
        clearLogcat(task_thread)

        #Ping to trigger the app 
        triggerBroadcastReceiverSimplePing(task_thread, appPackageName, relativeReceiverClassPath)

        validateIfPermissionsIsRequired(task_thread, appPackageName, current_time)

        if isStringsHandlingProcessMethodRoot(strings_handling_process_method):
            #createEncodedStringsFileRoot(task_thread, appPackageName, hash_map_original_sanitize, class_package_name, java_signature)
            writeEncodedStringsIntoFileRoot(task_thread, hash_map_original_sanitize)
            
            copy_file_from_tmp_to_internal(appPackageName)

            triggerActivityMultipleRoot(task_thread, appPackageName, class_package_name, java_signature, relativeReceiverClassPath)
            success = wait_for_android_status_flag(appPackageName)

            hash_map_decoded = collectLargeLogResultsFromFile(task_thread, appPackageName)
            errorAdbLogcatBuffer = False
        else:
            triggerBroadcastReceiverMultiple(task_thread, appPackageName, hash_map_original_sanitize, class_package_name, java_signature, relativeReceiverClassPath)

            hash_map_decoded, errorAdbLogcatBuffer = collectLargeLogResultsFromLogcat(task_thread, appPackageName, current_time)

        # Display the hash map
        if(hash_map_decoded != None):
            failled_decoded_string = checkIfHasValidDecodedStrings(hash_map_decoded)
            if(failled_decoded_string != 1):

                #for key, value in hash_map_decoded.items():
                #    print(f"Found '{key}' with decode: '{value}'")

                # Modify the Smali files

                hash_map_missing = replaceWithDecodedStringOnSmaliFiles(task_thread, convert_dot_to_slash(class_package_name), method_name, hash_map_original, hash_map_decoded, java_signature, is_multi_processing, is_complex_flow)

                # - Restore original Manifest
                restoreManifest(task_thread)

                # - Remove Injected code
                removeInjectedMethod(task_thread, class_package_name)

                # - Reassemble Decoded APK
                #compile_decode_apk_ok = compileApkWithRetries(task_thread)
                compile_decode_apk_ok = compileDecodedApk(task_thread, is_file_rollback)

                # Sign the modified APK
                sign_decode_apk_ok = signDecodedApk(task_thread)

                # Export not replaced decoded Strings
                exportNotReplacedDecodedStrings(task_thread, hash_map_decoded, hash_map_missing)

                if(compile_decode_apk_ok == True and sign_decode_apk_ok == True):
                    if(compareDictionaries(hash_map_decoded, hash_map_missing)):
                        if(failled_decoded_string == 2):
                            updateStatus(task_thread, "App Decoded with Success, but some Strings were not able to be decoded")
                        elif(errorAdbLogcatBuffer == True):
                            updateStatus(task_thread, "App Decoded with Success, but not all elements print on adb were collected by the app. Consider increase the logcat buffer Size. E.g. 'adb logcat -G 16M'")
                        else:
                            updateStatus(task_thread, "App Decoded with Success")
                        return "App Decoded with Success"
                    else:
                        updateStatus(task_thread, "App Decoded but not all Strings were replaced. Please check the missing_strings.json file")
                        return "App Decoded but not all Strings were replaced"
                else:
                    updateStatus(task_thread, "Error: App Could not Decoded")
                    return "Error: App Could not Decoded"
            else:
                updateStatus(task_thread, 'Error: All Strings failled on the decoded process')
                return 'No new Strings to replace'       
        else:
            updateStatus(task_thread, 'No new Strings to replace')
            return 'No new Strings to replace'           
    else:
        updateStatus(task_thread, 'No instances found on the smali files to replace')
        return 'No instances found on the smali files to replace'