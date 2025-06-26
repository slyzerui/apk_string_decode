from core_logic.apk_string_decode_consts import APK_STRING_DECODE_BROADCAST_RECEIVER_NAME, APK_STRING_DECODE_ACTIVITY_NAME, APK_STRING_DECODE_SERVICE_NAME, APK_STRING_DECODE_RUNNABLE_NAME, APK_STRING_DECODE_COMMON_NAME, triggerCallerToDecodeMethod, smali_type_mapping_with_registers, METHOD_BEGIN_PUBLIC_PATTERN_REGEX_COMPILED, END_CLASS_PATTERN_REGEX_COMPILED, DEVICE_TMP_DECODE_FILE_PATH, DEVICE_TMP_DECODE_FILE_PATH, INSTANCES_TO_DECODE_FILE, android_log_tag_to_search, STRING_DECODED_ERROR, MOVE_RESULT_OBJECT_PATTERN_REGEX_COMPILED, PARAMETER_TYPE_TAKING_2_REGISTERS
from core_logic.apk_string_decode_logic_clean_static_variables import replace_sget_with_const
from core_logic.apk_string_decode_logic_utils import updateStatus, fileExistsCaseSensitive, generate_smali_signature_from_java_signature, get_smali_type, resolve_register_count
from core_logic.apk_string_decode_logic_smali_code import receiver_smali_code, activity_smali_code, service_smali_code, runnable_smali_code, common_smali_code, trigger_decode_method_smali
from core_logic.apk_string_decode_common_utils import encodeStringIntoBase64, decode_base64_to_hashmap, decodeBase64IntoString, convert_dot_to_slash
from core_logic.apk_string_decode_android_utils import get_application_class, get_launcher_activity, preparaStringForAndroidDecoding, encodeHashMapToBase64WithDelimiter, sendSplitLogToAndroid, prepareStringForSmali
from core_logic.apk_string_decode_config import Config

from abc import ABC, abstractmethod

import multiprocessing
from multiprocessing import Manager, Pool, cpu_count, Lock
from functools import partial
import os
import subprocess
import sys
import re
from datetime import datetime
import xml.etree.ElementTree as ET
import glob
from collections import defaultdict
import json

import time
from copy import deepcopy
import io
import shutil
import shutil
import tempfile
import glob


def isJavaSignatureValid(javaSignature):
    #pattern = re.compile(r'^[\w.]+\.\w+\("[^"\\]*(?:\\.[^"\\]*)*"\)$')
    pattern = re.compile(r'^[\w.]+\.\w+\(([^)]*)\)$')

    
    # Verify the signature also contains a method that takes a single String parameter
    if pattern.match(javaSignature):
        # Further breakdown to ensure it's a method with a single String parameter
        parameter_pattern = re.compile(r'\("[^"]*"\)$')
        if parameter_pattern.search(javaSignature):
            print(f"Valid Java signature: {javaSignature}")
            return True
        else:
            print(f"Valid Java signature but not supported right now")
    print(f"Invalid Java signature: {javaSignature}")
    return False

def getExtractedInfoFromJavaSignatureCall(java_signature_call):
    class_package_name, method_name, method_signature = extractInfoFromJavaCall(java_signature_call)

    if class_package_name is not None and method_name is not None and method_signature is not None:
        print("Package Name: " + class_package_name)
        print("Method Name: " + method_name)
        print("Method signature: " + method_signature)
    else:
        print('Incorrect inputs. Closing the script')
        sys.exit()  # Exit the script 
    
    return class_package_name, method_name, method_signature 

def extractInfoFromJavaCall(java_call):
     # Extracting the method name and parameters from the call
    method_pattern = re.compile(r"(\w+(?:\.\w+)+)\((.*)\)", re.DOTALL)
    match = method_pattern.search(java_call)
    
    if not match:
        print("Invalid method call")
        return None, None, None

    full_method_name = match.group(1)
    params_string = match.group(2).strip()

    # Separate the class package name and the method name
    last_dot_index = full_method_name.rfind('.')
    class_package_name = full_method_name[:last_dot_index]
    method_name = full_method_name[last_dot_index + 1:]

    # Splitting parameters considering possible strings with commas inside
    params = []
    current_param = ''
    in_string = False
    for char in params_string:
        if char == '"' and (len(current_param) == 0 or current_param[-1] != '\\'):
            in_string = not in_string
        if char == ',' and not in_string:
            params.append(current_param.strip())
            current_param = ''
        else:
            current_param += char
    if current_param:
        params.append(current_param.strip())

    # Classifying each parameter and constructing method signature
    param_types = []
    for param in params:
        # Check if parameter is in the format "type name" and ignore the name part
        param_type_match = re.match(r'(\w+(\[\])?)\s+\w+', param)  # Matches "type varName" pattern
        if param_type_match:
            param_types.append(param_type_match.group(1))  # Only take the type part
        elif re.match(r'^\s*-?\d+\s*$', param):  # Integer
            param_types.append('int')
        elif re.match(r'^\s*-?\d+L\s*$', param, re.IGNORECASE):  # Long
            param_types.append('long')
        elif re.match(r'^\s*(true|false)\s*$', param, re.IGNORECASE):  # Boolean
            param_types.append('boolean')
        elif param.startswith('"') and param.endswith('"'):  # String
            param_types.append('String')
        else:
            param_types.append(param)  # Assume it is a type if nothing else matches

    method_signature = '(' + ','.join(param_types) + ')'

    return class_package_name, method_name, method_signature

def backupManifest(task_thread):
    updateStatus(task_thread, " ----- BACKUP MANIFEST ----- ")
    """Backup the original AndroidManifest.xml to a backup file."""
    directory = os.path.dirname(Config.get_manifest_backup())
    if not os.path.exists(directory):
        os.makedirs(directory)

    shutil.copy2(Config.get_manifest_path(), Config.get_manifest_backup())
    print(f"Backup created at {Config.get_manifest_backup()}")

def restoreManifest(task_thread):
    updateStatus(task_thread, " ----- RESTORE MANIFEST ----- ")
    """Restore the AndroidManifest.xml from the backup file."""
    shutil.copy2(Config.get_manifest_backup(), Config.get_manifest_path())
    print(f"Manifest restored from backup at {Config.get_manifest_backup()}")

def find_class_location(decompiled_apk_path, class_name):
    class_path = class_name.replace('.', '/') + ".smali"
    smali_dirs = [
        os.path.join(decompiled_apk_path, d) for d in os.listdir(decompiled_apk_path)
        if d.startswith("smali") or d.startswith("smali_classes")
    ]
    
    for smali_dir in smali_dirs:
        target_path = os.path.join(smali_dir, class_path)
        if os.path.exists(target_path):
            relative_path = os.path.dirname(os.path.relpath(target_path, smali_dir))
            return os.path.dirname(target_path), relative_path

    return None, None

def getDecodeClassRelateClassPath(class_package_name):
    # - get Decode class location
    decodeClassLocationPath, decodeClassRelativeClassPath = getDecodeClassPath(class_package_name)

    # - get Receiver location
    if decodeClassRelativeClassPath == "" or decodeClassRelativeClassPath == None:
        #get Application class / launcher Activity path instead
        decodeClassLocationPath, decodeClassRelativeClassPath = getReceiverPath()
    
    return decodeClassLocationPath, decodeClassRelativeClassPath

def getDecodeClassPath(class_package_name):
    receiverLocationPath, relativeClassPath = find_class_location(Config.get_extracted_folder(), class_package_name)
    return receiverLocationPath, relativeClassPath

def getReceiverPath():
    if not Config.get_manifest_path():
        return
    
    rootManifest = parse_manifest()
    if not rootManifest:
        return


    application_class = get_application_class(rootManifest)
    if application_class:
        print(f"[INFO] Found Application class: {application_class}")
        receiverLocationPath, relativeClassPath = find_class_location(Config.get_extracted_folder(), application_class)
        if application_class:
            print(f"[INFO] Application class location: {application_class}")
        else:
            print("[WARNING] Application class not found in decompiled folders.")
    else:
        launcher_activity = get_launcher_activity(rootManifest)
        if launcher_activity:
            print(f"[INFO] No valid Application class found. Using Launcher Activity: {launcher_activity}")
            receiverLocationPath, relativeClassPath = find_class_location(Config.get_extracted_folder(), launcher_activity)
            if launcher_activity:
                print(f"[INFO] Launcher Activity location: {launcher_activity}")
            else:
                print("[WARNING] Launcher Activity not found in decompiled folders.")
        else:
            print("[ERROR] No Application class or Launcher Activity found.")
    
    return receiverLocationPath, relativeClassPath

def parse_manifest():
    try:
        tree = ET.parse(Config.get_manifest_path())
        root = tree.getroot()
        return root
    except Exception as e:
        print(f"[ERROR] Failed to parse manifest: {e}")
        return None
    


def createSmaliReceiver(task_thread, receiverLocationPath, relativeClassPath):
    updateStatus(task_thread, " ----- CREATE SMALI RECEIVER ----- ")
    file_path = "{}/{}.smali".format(receiverLocationPath, APK_STRING_DECODE_BROADCAST_RECEIVER_NAME)
    formatted_smali = receiver_smali_code.replace('{}', convert_dot_to_slash(relativeClassPath), 12)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as smali_file:
        smali_file.write(formatted_smali)

    updateStatus(task_thread, "Receiver Smali file created: {}".format(file_path))

def createSmaliActivity(task_thread, serviceLocationPath, relativeClassPath):
    updateStatus(task_thread, " ----- CREATE SMALI ACTIVITY ----- ")
    # Write the Smali code to the file
    file_path = "{}/{}.smali".format(serviceLocationPath, APK_STRING_DECODE_ACTIVITY_NAME) 
    formatted_smali = activity_smali_code.replace('{}', convert_dot_to_slash(relativeClassPath), 8)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as smali_file:
        smali_file.write(formatted_smali)

    updateStatus(task_thread, "Activity Smali file created: {}".format(file_path))

def createSmaliService(task_thread, serviceLocationPath, relativeClassPath):
    updateStatus(task_thread, " ----- CREATE SMALI RECEIVER ----- ")
    file_path = "{}/{}.smali".format(serviceLocationPath, APK_STRING_DECODE_SERVICE_NAME)
    formatted_smali = service_smali_code.replace('{}', convert_dot_to_slash(relativeClassPath), 8)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as smali_file:
        smali_file.write(formatted_smali)

    updateStatus(task_thread, "Service Smali file created: {}".format(file_path))   

def createSmaliRunnable(task_thread, runnableLocationPath, relativeClassPath):
    updateStatus(task_thread, " ----- CREATE SMALI RUNNABLE ----- ")
    file_path = "{}/{}.smali".format(runnableLocationPath, APK_STRING_DECODE_RUNNABLE_NAME)
    formatted_smali = runnable_smali_code.replace('{}', convert_dot_to_slash(relativeClassPath), 13)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as smali_file:
        smali_file.write(formatted_smali)

    updateStatus(task_thread, "Runnable Smali file created: {}".format(file_path))   

def createSmaliCommon(task_thread, commonLocationPath, relativeClassPath):
    updateStatus(task_thread, " ----- CREATE SMALI COMMON ----- ")
    file_path = "{}/{}.smali".format(commonLocationPath, APK_STRING_DECODE_COMMON_NAME)
    formatted_smali = common_smali_code.replace('{}', convert_dot_to_slash(relativeClassPath), 113)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as smali_file:
        smali_file.write(formatted_smali)

    updateStatus(task_thread, "Common Smali file created: {}".format(file_path))

def getPackageNameFromManifest():
    try:
        # Parse the XML file
        tree = ET.parse(Config.get_manifest_path())
        root = tree.getroot()

        # Find the package attribute in the root element
        package_name = root.get('package')

        if package_name:
            return package_name
        else:
            print("Package name not found in the manifest.")
    except Exception as e:
        print("Error:", str(e))

    return None

def injectTriggerOnDecodeClass(task_thread, triggerDecodeClass, triggerDecodeMethod, javaSignature):
    updateStatus(task_thread, " ----- INJECT TRIGGER ON DECODE CLASS ----- ")

    smali_signature, smali_params, smali_access_flags, smali_names, smali_invoke_static_params, smali_registers = getSmaliInjectTriggerParamters(javaSignature)

    try:
        trigger_method_folder = findTriggeringMethodSmaliClass(triggerDecodeClass)
        
        if not os.path.isfile(trigger_method_folder):
            decode_class_file = findDecodeClassFile(Config.get_extracted_folder(), convert_dot_to_slash(triggerDecodeClass))
            if decode_class_file is not None:
                trigger_method_folder = decode_class_file
        
        # Read the existing smali file content
        with open(trigger_method_folder, 'r') as file:
            smali_content = file.read()

        #Remove missing interfaces
        smali_content = remove_missing_interfaces(smali_content)


        # Format the method signature to find it in the smali file
        method_signature = f".method {smali_access_flags} {triggerDecodeMethod}({smali_params}){smali_signature}"

        # Check if method already exists
        method_start_idx = smali_content.find(method_signature)
        if method_start_idx != -1:
            # Find end of method
            method_end_idx = smali_content.find(".end method", method_start_idx)
            if method_end_idx != -1:
                method_end_idx += len(".end method")
                # Remove the existing method
                smali_content = smali_content[:method_start_idx] + smali_content[method_end_idx:]

        trigger_decode_method_smali_formated = trigger_decode_method_smali.replace('{}', triggerCallerToDecodeMethod, 1).replace('{}', smali_signature, 1).replace('{}', str(smali_registers), 1).replace('{}', smali_params, 1).replace('{}', smali_access_flags, 1).replace('{}', smali_names, 1).replace('{}', smali_invoke_static_params, 1).replace('{}', convert_dot_to_slash(triggerDecodeClass), 1).replace('{}', triggerDecodeMethod, 1).replace('{}', smali_signature, 1)


        # Find the position to insert the new method
        insert_position = smali_content.find('.method')

        # Insert the triggerDecode method at the specified position
        updated_content = smali_content[:insert_position] + trigger_decode_method_smali_formated + smali_content[insert_position:]

        # Save the updated content back to the smali file
        with open(trigger_method_folder, 'w') as file:
            file.write(updated_content)

        updateStatus(task_thread, f"Method 'triggerDecode' added to {trigger_method_folder}")

    except FileNotFoundError:
        updateStatus(task_thread, f"Error: File not found - {trigger_method_folder}")
    except Exception as e:
        updateStatus(task_thread, f"Error: {e}")

def findTriggeringMethodSmaliClass(triggerDecodeClass):
    trigger_method_folder = Config.get_smali_folder() + convert_dot_to_slash(triggerDecodeClass) + ".smali"
    if fileExistsCaseSensitive(trigger_method_folder):
        return trigger_method_folder
    
    # Search in smali folders
    smali_folders = [
        os.path.join(Config.get_extracted_folder(), f)
        for f in os.listdir(Config.get_extracted_folder())
        if f.startswith('smali')
    ]
    escaped_class_name = convert_dot_to_slash(triggerDecodeClass)
    class_declaration_pattern = f"^\\.class.*L{escaped_class_name};$"

    for smali_folder in smali_folders:
        try:
            # Find all candidate files with potential matches
            result = subprocess.run(
                ['grep', '-r', '-l', '-E', class_declaration_pattern, smali_folder],
                capture_output=True, text=True, check=True
            )
            if result.stdout:
                candidate_files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                for file_path in candidate_files:
                    # Open each file and confirm it contains the exact class declaration
                    with open(file_path, 'r') as file:
                        for line in file:
                            if re.match(class_declaration_pattern, line.strip()):
                                return file_path  # Return the correct match
        except subprocess.CalledProcessError:
            # Ignore if grep fails (no matches in folder)
            continue
    return None

def find_smali_directories():
    return [d for d in glob.glob(os.path.join(Config.get_extracted_folder(), "smali*")) if os.path.isdir(d)]

def interface_exists(interface_name):

    interface_relative_path = interface_name.replace("/", os.sep)[1:] + ".smali"  # Remove 'L' prefix
    for smali_dir in find_smali_directories():
        interface_path = os.path.join(smali_dir, interface_relative_path)
        if os.path.exists(interface_path):
            return True  # Found the interface in one of the Smali directories
    return False  # Interface is missing in all Smali folders

def remove_missing_interfaces(smali_content):
    interfaces = re.findall(r"\.implements\s+(L[\w\/]+);", smali_content)

    if not interfaces:
        return smali_content  # No interfaces to check

    updated_content = smali_content

    #Next code will remove specific interfaces, although right now it is based on presence of the interfaces file.
    #missing_interfaces = [iface for iface in interfaces if not interface_exists(iface)]
    #if missing_interfaces:
    #    print(f"Removing missing interfaces: {missing_interfaces}")
    #    for interface in missing_interfaces:
    #        updated_content = re.sub(rf"\.implements\s+{interface};\n?", "", updated_content)
    
    updated_content = re.sub(r"\.implements\s+L[\w\/]+;\n?", "", updated_content)


    return updated_content


def removeInjectedMethod(task_thread, triggerDecodeClass):
    updateStatus(task_thread, "----- REMOVE INJECTED METHOD FROM CLASS -----")

    try:
        trigger_method_file = os.path.join(Config.get_smali_folder(), convert_dot_to_slash(triggerDecodeClass) + ".smali")
        
        if not os.path.isfile(trigger_method_file):
            decode_class_file = findDecodeClassFile(Config.get_extracted_folder(), convert_dot_to_slash(triggerDecodeClass))
            if decode_class_file is not None:
                trigger_method_file = decode_class_file

        if not os.path.isfile(trigger_method_file):
            updateStatus(task_thread, f"Error: File not found - {trigger_method_file}")
            return
        
        # Read the existing smali file content
        with open(trigger_method_file, 'r') as file:
            smali_content = file.read()

        # Format the method signature to find it in the smali file
        method_signature_start = f".method public static {triggerCallerToDecodeMethod}"
        method_start_idx = smali_content.find(method_signature_start)

        if method_start_idx != -1:
            # Find end of method
            method_end_idx = smali_content.find(".end method", method_start_idx)
            if method_end_idx != -1:
                method_end_idx += len(".end method")
                # Remove the existing method
                smali_content = smali_content[:method_start_idx] + smali_content[method_end_idx:]

                # Save the updated content back to the smali file
                with open(trigger_method_file, 'w') as file:
                    file.write(smali_content)

                updateStatus(task_thread, f"Method '{triggerCallerToDecodeMethod}' removed from {trigger_method_file}")
            else:
                updateStatus(task_thread, f"Error: End of method not found for {triggerCallerToDecodeMethod} in {trigger_method_file}")
        else:
            updateStatus(task_thread, f"Method '{triggerCallerToDecodeMethod}' not found in {trigger_method_file}")

    except FileNotFoundError:
        updateStatus(task_thread, f"Error: File not found - {trigger_method_file}")
    except Exception as e:
        updateStatus(task_thread, f"Error: {e}")


def findDecodeClassFile(base_path, file_path):
    for dir in glob.glob(os.path.join(base_path, 'smali_classes*')):
        potential_path = os.path.join(dir, file_path) + ".smali"
        if os.path.isfile(potential_path):
            return potential_path
    return None

def getSmaliInjectTriggerParamters(java_signature):
    # Extract the parameter types from the signature
    param_types = java_signature.strip("()").split(',')

    # Generate smali type codes for the parameters
    #smali_signature = ''.join(smali_type_mapping_with_registers[type.strip()][0] for type in param_types if type.strip())

    smali_signature = generate_smali_signature_from_java_signature(java_signature)

    # Generate parameter annotations and invoke-static call parameters
    register_index = 0
    param_infos = []
    invoke_static_params = []
    for i, param_type in enumerate(param_types):
        param_type = param_type.strip()
        if param_type:
            smali_type = get_smali_type(param_type)  # Get the Smali type, including array handling
            reg_count = resolve_register_count(param_type)  # Resolve the register count for the type
            param_info = (f"p{register_index}", smali_type, reg_count)
            param_infos.append(param_info)
            if reg_count == 2:
                # If the type is wide, use two consecutive registers
                invoke_static_params.append(f"p{register_index}, p{register_index + 1}")
                register_index += 2
            else:
                invoke_static_params.append(f"p{register_index}")
                register_index += 1

    smali_params = "\n    ".join(f".param {name}, \"value{i+1}\"    # {smali_type}" for i, (name, smali_type, _) in enumerate(param_infos))

    # Calculate the total registers needed (add an extra register for the return type (String))
    smali_registers = sum(reg_count for _, _, reg_count in param_infos) + 1

    # Format 'accessFlags' and 'names' with or without commas depending on the number of parameters
    smali_access_flags = ",\n            ".join("0x0" for _ in param_infos) if len(param_infos) > 1 else "0x0"
    smali_names = ",\n            ".join(f"\"value{i+1}\"" for i in range(len(param_infos))) if len(param_infos) > 1 else f"\"value1\""

    # Generate the invoke-static call parameters
    smali_invoke_static_params = ", ".join(invoke_static_params)

    return smali_signature, smali_params, smali_access_flags, smali_names, smali_invoke_static_params, smali_registers

def collectParametersFromSmaliFiles(task_thread, package_pattern, method_name, java_signature, is_multi_processing, is_complex_analysis, is_clean_static_variables, single_class_analysis):
    updateStatus(task_thread, " ----- COLLECTING PARAMETERS FROM SMALI FILES ----- ")
    hash_map = defaultdict(list)
    hash_map_sanitize = defaultdict(list)

    if is_complex_analysis:
        const_value_regex_patterns_compiled_array, invoke_static_method_call_regex, invoke_general_method_call_regex = generateRegexForCollectingParametersBasedOnSignatureComplexAnalysis(java_signature, package_pattern, method_name)
    else: 
        invoke_static_method_call_regex = generateRegexForCollectingParametersBasedOnSignature(java_signature, package_pattern, method_name)
        const_value_regex_patterns_compiled_array = []
        invoke_general_method_call_regex = ""
    config = {
        'invoke_static_method_call_regex': invoke_static_method_call_regex,
        'invoke_general_method_call_regex': invoke_general_method_call_regex,
        'const_value_regex_patterns_compiled_array': const_value_regex_patterns_compiled_array,
        'java_signature': java_signature,
        'is_complex_analysis': is_complex_analysis,
        'is_clean_static_variables': is_clean_static_variables,
        'single_class_analysis': single_class_analysis
    }

    for item in os.listdir(Config.get_extracted_folder()):
        #hash_map = collectParametersFromSingleSmaliFile(item, regex, hash_map)
        item_path = os.path.join(Config.get_extracted_folder(), item)
        # Check if the item is a directory and starts with 'smali'
        if os.path.isdir(item_path) and item.startswith('smali'):
            print(f"Processing directory: {item}")

            file_paths = [os.path.join(dirpath, filename)
                        for dirpath, _, filenames in os.walk(item_path)
                        for filename in filenames if filename.endswith('.smali')]
            
            if(is_multi_processing):
                with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
                    results = pool.map(collect_wrapper, [(file_path, config) for file_path in file_paths])

                partial_maps, partial_sanitize_maps = zip(*results)
                hash_map = merge_dictionaries([hash_map] + list(partial_maps))
                hash_map_sanitize = merge_dictionaries([hash_map_sanitize] + list(partial_sanitize_maps))
            else:
                partial_map = []
                partial_map_sanitize = []
                for filepath in file_paths:
                    if is_complex_analysis:
                        results_partial_map, results_partial_sanitize_sanitize = collectParametersFromSingleSmaliFile(filepath, invoke_static_method_call_regex, invoke_general_method_call_regex, const_value_regex_patterns_compiled_array, java_signature, is_complex_analysis, is_clean_static_variables, single_class_analysis)
                    
                    partial_map.append(results_partial_map)
                    partial_map_sanitize.append(results_partial_sanitize_sanitize)

                hash_map = merge_dictionaries([hash_map] + list(partial_map))
                hash_map_sanitize = merge_dictionaries([hash_map_sanitize] + list(partial_map_sanitize))

    return hash_map, hash_map_sanitize

def collect_wrapper(args):
    filepath, config = args
    return collectParametersFromSingleSmaliFile(
        filepath,
        config['invoke_static_method_call_regex'],
        config['invoke_general_method_call_regex'],
        config['const_value_regex_patterns_compiled_array'],
        config['java_signature'],
        config['is_complex_analysis'],
        config['is_clean_static_variables'],
        config['single_class_analysis']
    )

def merge_dictionaries(dicts):
    merged = {}
    for d in dicts:
        for key, value in d.items():
            merged.setdefault(key, []).extend(value)
    return merged


def remove_line_directives(input_text):
    lines = input_text.splitlines()  # Split the input into lines
    cleaned_lines = [line for line in lines if not line.strip().startswith('.line')]  # Remove lines starting with .line
    normalized_text = '\n'.join(cleaned_lines)  # Rejoin the cleaned lines
    return normalized_text

def remove_line_and_comments(input_text):
    lines = input_text.splitlines()
    cleaned_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('.line') or stripped_line.startswith('#'):
            continue  # Skip these lines entirely
        cleaned_lines.append(line)  # Keep the original line (preserve indentation)

    return '\n'.join(cleaned_lines)


def generateRegexForCollectingParametersBasedOnSignature(java_signature, package_pattern, method_name):
    # Split the signature to handle multiple parameters
    param_types = java_signature.strip("()").split(',')

    # Start building the regex pattern for loading instructions
    regex_patterns = [
        rf'const-string(?:/jumbo)?\s+(\w+\d+),\s+"([^"]+)"' if param == 'String' else
        #r'const/(4|16|32) (\w\d+), -?\d+' if param == 'int' else
        r'\s*' + r'const/(4|16|32) (\w\d+), (-?0x[\da-fA-F]+|-?\d+)' if param == 'int' else
        r'const/4 (\w\d+), 0x[01]' if param == 'boolean' else
        r'const-wide\s+(\w+\d+),\s+(-?0x[\da-fA-F]+L)' if param == 'long' else
        'UNKNOWN'
        for param in param_types
    ]

    # Join with spacing to allow for separation between instructions
    loading_instructions_regex = r'\s+'.join(regex_patterns)

    # Non-capturing group for optional lines
    #optional_lines_regex = r'(\s*(?:\.\w+\s+.*)?)*?'
    optional_lines_regex = rf'(?:(?:\.\w+\s+.*\s*)*?)\s*'

    # Dynamically build the smali method signature part
    smali_method_signature = ''.join([smali_type_mapping_with_registers[param.strip()][0] for param in param_types])

    # Combine into the final regex pattern
    escaped_package = re.escape(package_pattern)
    escaped_method = re.escape(method_name)

    invoke_static_regex = (
        rf'invoke-static(?:/range)?\s+\{{(?:\w+\d+(?:(?:,\s*)?\w+\d+)*|\w+\d+\s+\.\.\s+\w+\d+)\}},\s*' +
        rf'L{package_pattern};->' + rf'{method_name}' + rf'\({smali_method_signature}\)Ljava/lang/String;'
    )

    final_regex_pattern = loading_instructions_regex + optional_lines_regex + invoke_static_regex + r'\s+move-result-object\s+(\w+\d+)'
    return final_regex_pattern


def generateRegexForCollectingParametersBasedOnSignatureComplexAnalysis(java_signature, package_pattern, method_name):
    # Split the signature to handle multiple parameters
    param_types = java_signature.strip("()").split(',')

    # Build regex patterns for each parameter type
    const_value_patterns_array = [
        r'\s*' + rf'const-string(?:/jumbo)?\s+(\w+\d+),\s+"([^"]+)"' if param == 'String' else
        #r'\s*' + r'const/(4|16|32) (\w\d+), (-?\d+)' if param == 'int' else
        r'\s*' + r'const/(4|16|32) (\w\d+), (-?0x[\da-fA-F]+|-?\d+)' if param == 'int' else
        r'\s*' + r'const/4 (\w\d+), 0x[01]' if param == 'boolean' else
        r'\s*' + r'const-wide\s+(\w+\d+),\s+(-?0x[\da-fA-F]+L)' if param == 'long' else
        r'\s*fill-array-data\s+(\w\d+),\s+(:\w[\w\d_]*)' if param == 'byte[]' else
        'UNKNOWN'
        for param in param_types
    ]

    # Compile regex patterns, skipping 'UNKNOWN'
    const_value_regex_patterns_array = [re.compile(pattern) for pattern in const_value_patterns_array if pattern != 'UNKNOWN']

    # Dynamically build the smali method signature part
    smali_method_signature = ''.join([get_smali_type(param.strip()) for param in param_types])

    invoke_static_method_call_regex = re.compile(
        rf'invoke-static(?:/range)?\s+\{{([\w\s,\.]+)\}},\s*' +  # Adjusted to include ".."
        rf'L{re.escape(package_pattern)};->' + rf'{re.escape(method_name)}' +
        rf'\({re.escape(smali_method_signature)}\)Ljava/lang/String;',
        re.MULTILINE | re.VERBOSE
    )

    # Build a more general regex for invoke-static and invoke-virtual calls
    invoke_general_method_call_regex = re.compile(
        rf'invoke-(static|virtual)(?:/range)?\s+\{{([\w\s,]+)\}},\s*' +
        rf'L[\w/]+;->' + rf'{re.escape(method_name)}' +
        rf'\(([^)]*)\)Ljava/lang/String;',  # Make Group 3 non-mandatory for flexibility
        re.MULTILINE | re.VERBOSE
    )

    return const_value_regex_patterns_array, invoke_static_method_call_regex, invoke_general_method_call_regex


def collectParametersFromSingleSmaliFile(filepath, invoke_regex, invoke_general_regex, const_value_regex_patterns_compiled_array, java_signature, is_complexAnalysis, is_clean_static_variables, single_class_analysis):

    local_hash_map = {}
    local_hash_map_sanitize = {}

    # Determine the number of parameters in the signature
    param_types = java_signature.strip("()").split(',')

    # Process only .smali files
    if filepath.endswith('.smali'):    

        # Read the content of each file
        try:
            #with open(filepath, 'r') as file:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

                if isNotAllowedClass(single_class_analysis, filepath):
                    return local_hash_map, local_hash_map_sanitize

                # Preprocess to remove .line directives
                cleaned_content = remove_line_and_comments(content)

                if is_clean_static_variables:
                    cleaned_content = replace_sget_with_const(cleaned_content)

                cleaned_content = cleanup_sget_instances_from_invoke_calls(cleaned_content, invoke_general_regex)

                # Find all matches of the pattern in the content
                #matches = regex.findall(cleaned_content, re.MULTILINE)
                invoke_regex_matches = invoke_regex.finditer(cleaned_content, re.MULTILINE)


                encoded_values_literal = []
                encoded_values_sanitize = []
                for invoke_match in invoke_regex_matches:

                    if is_complexAnalysis:
                        encoded_value_literal, encoded_value_sanitize = handleMatchedValueAndEncryptionComplexAnalysis(cleaned_content, invoke_match, const_value_regex_patterns_compiled_array, param_types)
                    else:
                       encoded_value_literal, encoded_value_sanitize = handleMatchedValueAndEncryption(invoke_match, param_types)

                    if encoded_value_literal:
                        # Combine encoded values for this match into a single string, separated by commas
                        encoded_values_literal = ",".join(encoded_value_literal)
                        encoded_values_sanitize = ",".join(encoded_value_sanitize)
                        local_hash_map.setdefault(encoded_values_literal, []).append(filepath)
                        local_hash_map_sanitize.setdefault(encoded_values_literal, []).append(encoded_values_sanitize)


        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
    return local_hash_map, local_hash_map_sanitize

def handleMatchedValueAndEncryption(match, param_types):

    encoded_value_literal = []
    encoded_value_sanitize = []
    # Each parameter type leads to two groups in the match due to the regex pattern (register, value)
    #for i in range(1, 2 * num_params, 2):
    for i, param_type in enumerate(param_types):
        #if i < len(match):  
        #match_index = 1 + i * 2
        match_index = 2 + i * 2

        try:
            value_to_encode = match.group(match_index)

            if value_to_encode is not None:
                #value_to_encode = match[match_index]
                value_to_encode = match.group(match_index)
                param_type = param_type.strip()

                encoded_literal, encoded_sanitize = encodeValueBasedOnVariableType(param_type, value_to_encode)
                encoded_value_literal.append(encoded_literal)
                encoded_value_sanitize.append(encoded_sanitize)
                #print(f"Matched value to encode for param type '{param_type}': {value_to_encode}")
                
        except IndexError:
            print(f"No match found for param type '{param_type}' at index {match_index}")

    return encoded_value_literal, encoded_value_sanitize



def handleMatchedValueAndEncryptionComplexAnalysis(smali_code, invoke_match, const_value_regex_patterns_compiled_array, param_types):
    encoded_value_literal = []
    encoded_value_sanitize = []

    try:
        # Parse variables, handling both regular and range-based syntax
        variable_range = invoke_match.group(1).strip()
        variables = []

        if '..' in variable_range:
            # Handle ranges like {v0 .. v3}
            start_var, end_var = variable_range.split(' .. ')
            prefix = start_var[:-1]  # Extract the prefix (e.g., 'v' from 'v0')
            start_index = int(start_var[1:])  # Extract the starting index
            end_index = int(end_var[1:])  # Extract the ending index
            variables = [f"{prefix}{i}" for i in range(start_index, end_index + 1)]
        else:
            # Handle regular syntax like {v0, v1}
            variables = variable_range.split(', ')

        # Extract all lines up to the invoke-static call
        pre_lines = smali_code[:invoke_match.start()].split('\n')

        variable_values = [None] * len(variables)

        byte_array_labels = {}  # Temporarily store labels like :array_1

        # Process each variable individually to avoid mismatched associations
        for idx, (variable, pattern) in enumerate(zip(variables, const_value_regex_patterns_compiled_array)):
            for line in reversed(pre_lines):
                # Stop if the beginning of the method or class is reached
                if METHOD_BEGIN_PUBLIC_PATTERN_REGEX_COMPILED.search(line) or END_CLASS_PATTERN_REGEX_COMPILED.search(line):
                    break

                match = pattern.match(line)
                if match:
                    param_type = param_types[idx].strip()

                    if param_type == "byte[]":
                        #matched_variable = match.group(2) or match.group(3)  # Use group(2) or group(3) for byte[]
                        matched_variable = match.group(1)  # e.g., v2
                        array_label = match.group(2) if len(match.groups()) > 1 else None  # e.g., :array_1
                    elif param_type == "int":
                        matched_variable = match.group(2)  # This should be v0, v1, etc.
                    else:
                        matched_variable = match.group(1)  # Use group(1) for other types like String, int, etc.

                    # Ensure the matched variable corresponds to the current variable
                    if matched_variable == variable:
                        if param_type == "byte[]":
                            #variable_values[idx] = match.group(2) or match.group(3)
                            byte_array_labels[variable] = array_label  # store label like :array_1
                        elif param_type == "int":
                            variable_values[idx] = match.group(3) 
                        else:
                            variable_values[idx] = match.group(2)
                        break

        for idx, param_type in enumerate(param_types):
            param_type = param_type.strip()
            if param_type == "byte[]":
                array_register = variables[idx]

                if array_register in byte_array_labels:
                    array_label = byte_array_labels[array_register]
                    if array_label:
                        array_data = extractFillArrayData(smali_code.split('\n'), array_label)
                        if array_data is not None:
                            variable_values[idx] = array_data


        # Filter out None values from variable_values
        non_none_values = [value for value in variable_values if value is not None]

        # Check if the length of non-None values matches the length of param_types
        if len(param_types) == len(non_none_values):
            for param_type, value_to_encode in zip(param_types, non_none_values):
                param_type = param_type.strip()
                encoded_literal, encoded_sanitize = encodeValueBasedOnVariableType(param_type, value_to_encode)
                encoded_value_literal.append(encoded_literal)
                encoded_value_sanitize.append(encoded_sanitize)

        return encoded_value_literal, encoded_value_sanitize

    except Exception as e:
        print(f"Error: {e}")

    return encoded_value_literal, encoded_value_sanitize


def extractFillArrayData1(lines, array_register):
    """
    Extract array data associated with a given register from the Smali code.
    Handles both inline data and references like :array_X, which can appear
    before or after the invocation.
    """
    label = None

    # First, find the fill-array-data instruction that uses the register
    for line in lines:
        match = re.match(rf'\s*fill-array-data\s+{array_register},\s+(:[\w\d_]+)', line)
        if match:
            label = match.group(1)  # Extract the label (e.g., :array_46)
            break

    if not label:
        return None  # Return None if no fill-array-data instruction is found

    # Next, locate the .array-data block associated with the label
    in_array_data = False
    array_data = []
    for line in lines:
        line = line.strip()
        if line == label:  # Found the label
            in_array_data = True
        elif in_array_data:
            if line.startswith('.array-data'):
                continue  # Skip the .array-data directive
            elif line.startswith('.end array-data'):
                break  # End of the array-data block
            else:
                array_data.append(line)  # Collect array data

    return array_data if array_data else None


def extractFillArrayData(lines, array_label):
    """
    Extract array data associated with a given array label from the Smali code.
    The label (e.g., :array_1) should point to a .array-data block somewhere in the code.
    """
    in_array_data = False
    array_data = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == array_label:
            in_array_data = True
        elif in_array_data:
            if stripped_line.startswith('.array-data'):
                continue  # skip directive
            elif stripped_line.startswith('.end array-data'):
                break
            else:
                array_data.append(stripped_line)

    return array_data if array_data else None


def extractArrayDataFromLabel(smali_code, array_label):
    """
    Extract .array-data block associated with a dynamically detected label.
    """
    array_data = []
    in_array_data = False

    for line in smali_code.splitlines():
        stripped_line = line.strip()

        if in_array_data:
            if stripped_line.startswith(".end array-data"):
                # Successfully parsed the .array-data block
                return array_data if array_data else None
            elif validateArrayDataValue(stripped_line):
                # Collect valid array values
                array_value = stripped_line.split('t')[0]  # Remove the `t` suffix if present
                array_data.append(array_value)

        elif stripped_line == array_label:
            # Found the label, start parsing the .array-data block
            in_array_data = True

    # Return None if no valid .array-data was found
    return None


def validateArrayDataValue(value_line):
    """
    Validate a line from a .array-data block to ensure it contains a valid numeric literal.
    Accepts decimal, hexadecimal, and negative values.
    """
    value = value_line.split('t')[0]  # Remove the `t` suffix if present
    try:
        # Check if it's a valid hexadecimal or decimal value
        if value.startswith("-0x") or value.startswith("0x"):
            int(value, 16)  # Validate hexadecimal
        else:
            int(value, 10)  # Validate decimal
        return True
    except ValueError:
        return False



def encodeValueBasedOnVariableType(param_type, value_to_encode):
    if param_type == "String":
        # Sanitize and encode strings
        encoded_sanitize = encodeStringIntoBase64(preparaStringForAndroidDecoding(value_to_encode))
    elif param_type == "int":
        # Convert hex to int and encode
        encoded_sanitize = encodeStringIntoBase64(str(int(value_to_encode, 16)))
    elif param_type == "boolean":
        # Convert boolean hex values to true/false
        if "0x0" in value_to_encode:
            encoded_sanitize = encodeStringIntoBase64("false")
        elif "0x1" in value_to_encode:
            encoded_sanitize = encodeStringIntoBase64("true")
    elif param_type == "long":
        # Handle long integers; strip the 'L' if present
        if value_to_encode[-1].lower() == 'l':
            value_to_encode_long = value_to_encode[:-1]
        else:
            value_to_encode_long = value_to_encode
        encoded_sanitize = encodeStringIntoBase64(str(int(value_to_encode_long, 16)))
    elif param_type == "byte[]":
        # Join array data into a single string and encode
        if isinstance(value_to_encode, list):
            # Convert byte array values into a hex string, separating values with commas
            value_as_hex = ",".join(value_to_encode)
            encoded_sanitize = encodeStringIntoBase64(value_as_hex)
            value_to_encode = value_as_hex
        else:
            # If value_to_encode is not a list, raise an error
            raise ValueError("Expected a list for byte[] but got: " + str(value_to_encode))
    else:
        raise ValueError(f"Unsupported parameter type: {param_type}")

    # Default literal encoding
    encoded_literal = encodeStringIntoBase64(value_to_encode)

    return encoded_literal, encoded_sanitize




def isNotAllowedClass(single_class_analysis, filepath):
    if not single_class_analysis:
        return False  # Return False if single_class_analysis is empty

    # Normalize single_class_analysis to handle various formats
    if isinstance(single_class_analysis, str):
        # Remove surrounding brackets if present
        single_class_analysis = single_class_analysis.strip("[]")
        # Split based on common delimiters (',', ';') and strip whitespace
        class_list = [item.strip() for item in single_class_analysis.replace(";", ",").split(",")]
    elif isinstance(single_class_analysis, list):
        class_list = single_class_analysis
    else:
        raise ValueError("Invalid format for single_class_analysis")

    # Normalize each class path in the array and check for exact match
    for class_path in class_list:
        normalized_class = class_path.replace(".", "/").strip()
        # Create the exact filepath by adding ".smali" at the end
        exact_filepath = f"{normalized_class}.smali"
        if exact_filepath in filepath:
            return False  # If an exact match is found, return False (it's allowed)
    
    return True  # If no exact match is found, return True (it's not allowed)

def parse_method_signature(signature):
    """Parse a Smali method signature to calculate the expected parameter count."""
    param_types = re.findall(r'\[?[BCDFIJSZV]|L[^;]+;', signature)
    count = 0
    for param in param_types:
        if param in ['J', 'D']:  # Long and Double take 2 registers
            count += 2
        else:
            count += 1
    return count


def cleanup_sget_instances_from_invoke_calls(smali_code, invoke_general_method_call_regex):
    lines = smali_code.split("\n")
    adjusted_lines = []
    skip_next = False

    for i, line in enumerate(lines):
        # Skip lines that have already been processed
        if skip_next:
            skip_next = False
            continue

        # Use the general regex to match the invoke instruction
        invoke_match = invoke_general_method_call_regex.match(line)
        if invoke_match:
            try:
                # Extract fields and method details
                instruction_type = invoke_match.group(1)  # static or virtual
                fields = [field.strip() for field in invoke_match.group(2).split(",")]
                method_signature = invoke_match.group(3)

                # Calculate expected parameter count
                expected_count = parse_method_signature(method_signature)

                # Handle cases where `this` reference may be redundant
                if instruction_type == "virtual" and len(fields) == expected_count + 1:
                    print(f"Handling potential redundant `this` reference in: {line}")

                    # Identify the `this` reference (first field)
                    this_reference = fields[0]
                    parameters = fields[1:]  # Exclude `this` reference

                    # Look back for sget-object or iget-object for the `this` reference
                    sget_object_line = None
                    field_class = None
                    for j in range(i - 1, -1, -1):
                        sget_match = re.match(
                            rf"\s*sget-object {this_reference}, ([^;]+);->([^:]+):([^;]+);", lines[j]
                        )
                        if sget_match:
                            # Extract the class where the field is defined
                            field_class = sget_match.group(1)
                            sget_object_line = j
                            break

                    # Check if `this` reference is used elsewhere
                    this_used_elsewhere = any(
                        re.search(rf'\b{this_reference}\b', lines[k]) for k in range(i + 1, len(lines))
                    )

                    if sget_object_line is not None:
                        if this_used_elsewhere:
                            print(f"`this` reference is used elsewhere. Keeping `sget-object`.")
                        else:
                            print(f"`this` reference not used elsewhere. Removing `sget-object`.")
                            lines[sget_object_line] = ""  # Remove sget-object line

                        # Extract the actual method name from the invoke-virtual line
                        method_class_match = re.match(r".*?(\w+)/(\w+);->(\w+)", line)
                        if method_class_match:
                            method_name = method_class_match.group(3)

                        # Adjust invoke-virtual to invoke-static
                        adjusted_lines.append(
                            f"    invoke-static {{{', '.join(parameters)}}}, {field_class};->{method_name}({method_signature})Ljava/lang/String;"
                        )
                        skip_next = True  # Skip this invoke-virtual line
                        continue

            except IndexError:
                # If group(3) is missing, log and skip processing this line
                print(f"Skipping line due to missing group(3): {line}")
                adjusted_lines.append(line)
                continue

        # Add line as-is if no match
        adjusted_lines.append(line)

    return "\n".join(adjusted_lines)



def deleteTempFileFromDevice():

    print(f"Deleting temp file: {DEVICE_TMP_DECODE_FILE_PATH}")

    result = subprocess.run(
        ["adb", "shell", "rm", "-f", DEVICE_TMP_DECODE_FILE_PATH],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Temp file deleted successfully.")
    else:
        print("Failed to delete temp file:")
        print(result.stderr.strip())

def writeEncodedStringsIntoFileRoot(task_thread, hash_map_original_sanitize):
    updateStatus(task_thread, " ----- TRIGGER APP DECODE (ROOT) ----- ")
    
    deleteTempFileFromDevice()
    

    # Encode content
    encoded_part = encodeHashMapToBase64WithDelimiter(hash_map_original_sanitize)
    expected_size = len(encoded_part.encode("utf-8"))

    print(f"Writing to: {DEVICE_TMP_DECODE_FILE_PATH}")
    print(f"Local data size: {expected_size} bytes")

    # --- WRITE PHASE ---
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(encoded_part)
        local_temp_path = temp_file.name

    try:
        result_push = subprocess.run(
            ["adb", "push", local_temp_path, DEVICE_TMP_DECODE_FILE_PATH],
            capture_output=True, text=True
        )

        if result_push.returncode != 0:
            print("Failed to push file to device:")
            print(result_push.stderr)
            return

        print("File pushed to /data/local/tmp")

    finally:
        os.remove(local_temp_path)

    # --- VERIFY PHASE ---
    print("🔍 Verifying file size on device...")

    proc_check = subprocess.Popen(
        ["adb", "shell", f"stat -c %s {DEVICE_TMP_DECODE_FILE_PATH}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout_check, stderr_check = proc_check.communicate()
    return_code_check = proc_check.returncode

    if return_code_check == 0:
        try:
            actual_size = int(stdout_check.strip())
            if actual_size == expected_size:
                print("File verified: size matches.")
            else:
                print(f"Size mismatch! Expected {expected_size}, got {actual_size}")
        except ValueError:
            print(f"Unexpected output from stat: '{stdout_check.strip()}'")
    else:
        print("Failed to check file size:")
        print(stderr_check.strip())



def createEncodedStringsFileRoot(task_thread, package_name, hash_map_original_sanitize, class_name, java_signature):
    updateStatus(task_thread, " ----- TRIGGER APP DECODE (ROOT) ----- ")

    # File paths
    SDCARD_PATH = f"/sdcard/{INSTANCES_TO_DECODE_FILE}"
    APP_FILES_DIR = f"/data/data/{package_name}/files"
    APP_FILES_PATH = f"{APP_FILES_DIR}/{INSTANCES_TO_DECODE_FILE}"

    # Step 2: Create local temp file
    with open(INSTANCES_TO_DECODE_FILE, "w") as file:
        encoded_part = encodeHashMapToBase64WithDelimiter(hash_map_original_sanitize)
        file.write(encoded_part)

    print(f"File created: {INSTANCES_TO_DECODE_FILE}")

    # Step 3: Push file to /sdcard/
    if subprocess.run(f"adb push {INSTANCES_TO_DECODE_FILE} {SDCARD_PATH}", shell=True, check=True).returncode == 0:
        print(f"File pushed to {SDCARD_PATH}")
    else:
        print("Failed to push file.")
        exit(1)

    # Step 4: Create app's files directory (if not exists)
    if subprocess.run(f'adb shell "echo \'mkdir -p {APP_FILES_DIR}\' | su"', shell=True, check=True).returncode == 0:
        print(f"Directory ensured: {APP_FILES_DIR}")
    else:
        print("Failed to create directory.")
        exit(1)

    # Step 5: Move the file to app's private storage
    if subprocess.run(f'adb shell "echo \'mv {SDCARD_PATH} {APP_FILES_PATH}\' | su"', shell=True, check=True).returncode == 0:
        print(f"File moved to {APP_FILES_PATH}")
    else:
        print("Failed to move file.")
        exit(1)

    # Step 6: Get the correct app user using ls -ld
    get_app_user_command = f'adb shell "echo \'ls -ld {APP_FILES_DIR}\' | su"'
    result = subprocess.run(get_app_user_command, shell=True, capture_output=True, text=True)

    if result.returncode == 0 and result.stdout:
        parts = result.stdout.split()
        if len(parts) >= 3:
            app_user = parts[2]
            print(f"Retrieved App User: {app_user}")
        else:
            print(f"Failed to extract user from output: {result.stdout}")
            exit(1)
    else:
        print(f"Failed to retrieve app user. Error: {result.stderr}")
        exit(1)

    # Step 7: Fix file ownership
    if subprocess.run(f'adb shell "echo \'chown {app_user}:{app_user} {APP_FILES_PATH}\' | su"', shell=True, check=True).returncode == 0:
        print(f"Ownership set to {app_user}")
    else:
        print("Failed to set file ownership.")
        exit(1)

    # Step 8: Fix file permissions
    if subprocess.run(f'adb shell "echo \'chmod 600 {APP_FILES_PATH}\' | su"', shell=True, check=True).returncode == 0:
        print("File permissions set to 600")
    else:
        print("Failed to set permissions.")
        exit(1)

    # Step 9: Verify the file exists
    if subprocess.run(f'adb shell "echo \'ls {APP_FILES_PATH}\' | su"', shell=True, check=True).returncode == 0:
        print(f"File verified at {APP_FILES_PATH}")
    else:
        print("File verification failed.")
        exit(1)

    # Step 10: Clean up local temp file
    os.remove(INSTANCES_TO_DECODE_FILE)
    print("Local temp file removed.")

    print("Success! File is ready in the app's private storage.")


def collectLargeLogResultsFromFile(task_thread, package_name):
    updateStatus(task_thread, " ----- COLLECTING DECODED STRINGS (ROOT, exec-out) ----- ")

    DEVICE_FILE = f"/data/data/{package_name}/files/apk_string_decode_results.txt"
    LOCAL_FILE = "apk_string_decode_results.txt"

    try:
        with open(LOCAL_FILE, "wb") as outfile:
            proc = subprocess.run(
                ["adb", "exec-out", "su", "0", "cat", DEVICE_FILE],
                stdout=outfile,
                stderr=subprocess.PIPE
            )

        if proc.returncode != 0:
            print("Failed to pull file:")
            print(proc.stderr.decode().strip())
            return None

        print(f"File pulled successfully using exec-out: {LOCAL_FILE}")

    except Exception as e:
        print(f"Exception while pulling file: {e}")
        return None

    # Parse the JSON
    try:
        with open(LOCAL_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        print("Decoded results successfully loaded (UTF-8)!")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"UTF-8 failed: {e} — trying with Latin-1 fallback...")
        try:
            with open(LOCAL_FILE, "r", encoding="latin-1") as file:
                data = json.load(file)
            print("Decoded results successfully loaded (Latin-1)!")
        except Exception as e:
            print(f"Final failure: {e}")
            return None

    try:
        os.remove(LOCAL_FILE)
    except Exception:
        pass

    return data

def collectLargeLogResultsFromLogcat(task_thread, package_name, current_time):
    updateStatus(task_thread, " ----- COLLECT RESULTS FROM LOGCAT ----- ")
    #large_log = ""
    large_log = io.StringIO()

    #TO DELETE:
    counter = 0
    
    adb_command = f'adb logcat -d -v time {package_name}:V'

    logcat_output_bytes = subprocess.check_output(adb_command, shell=True)

    # Decode the bytes using a specific encoding (e.g., 'utf-8', 'latin-1', etc.)
    try:
        logcat_output = logcat_output_bytes.decode('utf-8')
    except UnicodeDecodeError:
        updateStatus(task_thread, "Error decoding logcat output as UTF-8.")
        try:
            logcat_output = logcat_output_bytes.decode('latin-1')
        except UnicodeDecodeError:
            updateStatus(task_thread, "Error decoding logcat output as latin-1")
            return None 

    pattern1 = re.compile(rf"{android_log_tag_to_search}\(\d+\): (.+)$")
    pattern2 = re.compile(rf"\d+-\d+ \d+:\d+:\d+\.\d+ [A-Z]/" + re.escape(android_log_tag_to_search) + r"\(\s*(\d+)\)\(\s*(\d+)\):\s*(.+)")

    log_entries = logcat_output.splitlines()

    logs_accumulator = {}

    for log_entry in log_entries:
        if android_log_tag_to_search in log_entry:
            matchTime = re.search(r'^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*', log_entry)
            
            if matchTime:
                log_time = matchTime.group(1)
                # Compare with the stored time
                if log_time > current_time:
                    match1 = pattern1.search(log_entry)
                    if match1:
                        decoded_part = decode_base64_to_hashmap(match2.group(1))
                        #combined_data.append(decoded_part)
                        #large_log += match1.group(1)
                        #arge_log.write(match2.group(1))
                        #print(log_entry)
                    else:
                        match2 = pattern2.search(log_entry)
                        
                        if match2:
                            log_id, part_id, base64_part = match2.groups()
                            if log_id not in logs_accumulator:
                                logs_accumulator[log_id] = ""
                            # Append this part's content to the accumulator for its log ID
                            logs_accumulator[log_id] += base64_part

                            #counter = counter + 1

                            #decoded_part = decode_base64_to_hashmap(match2.group(1))
                            #combined_data.append(decoded_part)

                            #large_log.write(match2.group(1))

                            #large_log += match2.group(1)
                            #print(log_entry)

                            #file.write(match2.group(1))  # Write the match followed by a newline character


        #large_log_content = large_log.getvalue()                            

    if logs_accumulator:
            first_logcat_id = None
            final_merged_json = {}
            # Now decode and process each accumulated log entry
            for log_id, encoded_log in logs_accumulator.items():
                try:
                    decoded_json = decode_base64_to_hashmap(encoded_log)
                    final_merged_json.update(decoded_json)
                    if(first_logcat_id == None):
                        first_logcat_id = log_id
                except json.JSONDecodeError:
                    print("Error decoding logcat output as a JSON content")
                    #updateStatus(task_thread, "Error decoding logcat output as a JSON content")
                    #pass  # Handle JSON decode error

            # Check if the first position is empty
            if first_logcat_id != None and first_logcat_id != "0":
                print("Error: Not all elements print on adb were collected by the app. Consider increase the logcat buffer Size: 'adb logcat -G 16M'")
                return final_merged_json, True

            return final_merged_json, False

    return None, False    

def deep_merge(dict1, dict2):
    """Merge two dictionaries, deeply."""
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                deep_merge(dict1[key], dict2[key])
            elif dict1[key] != dict2[key]:
                # Handle conflict or append/extend if it's a list
                if isinstance(dict1[key], list) and isinstance(dict2[key], list):
                    dict1[key].extend(dict2[key])
                else:
                    # Replace or handle differently as needed
                    dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1




def replaceWithDecodedStringOnSmaliFiles(task_thread, decode_method_package, decode_method_name, hash_map_original, hash_map_decoded, java_signature, is_multi_processing, is_complex_flow):
    updateStatus(task_thread, " ----- REPLACE DECODED STRINGS ON SMALI FILES----- ")
    #replacedFilesCounter = 0

    #hash_map_missing = deepcopy(hash_map_original)
    manager = Manager()
    shared_dict = manager.dict(deepcopy(hash_map_original)) 

    #print(f"shared_dict: {dict(shared_dict)}")

    if is_complex_flow:
        # Generate a list of (filepath, keys) tuples from hash_map_original
        hashMapDecodedFilteredByPathsComplexFlow = build_file_to_keys_map(hash_map_original)
        keyFilePathsTupleSimpleFlow = None
    else:
        # Generate a list of (key, filepath) tuples from hash_map_original
        hashMapDecodedFilteredByPathsComplexFlow = None
        keyFilePathsTupleSimpleFlow = [(key, filepath) for key, filepaths in hash_map_original.items() for filepath in filepaths]

    replacement_plan_by_hash = generateReplacementPlan(hash_map_decoded, java_signature, decode_method_package, decode_method_name)

    #Generate generic regex for the replacing process
    invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types = generateGenericRegexForReplacingParametersBasedOnSignatureComplex(java_signature, decode_method_package, decode_method_name)

    #Simple flow + Singleprocessing -> Fine
    #Simple flow + Multiprocessing -> Corrupt data files
    #Complex flow + Singleprocessing -> Fine
    #Complex flow + Multiprocessing -> Fine

    if is_multi_processing and is_complex_flow:
        return replaceWithMultiprocessing(hashMapDecodedFilteredByPathsComplexFlow, shared_dict, decode_method_package, decode_method_name, hash_map_decoded, java_signature, invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types, replacement_plan_by_hash, is_complex_flow)
    else:
        if is_multi_processing and not is_complex_flow:
            print("Simple flow feature is not allowed with multi processing on the replacement process. Continuing using single processing...")
        return replaceWithSingleprocessing(keyFilePathsTupleSimpleFlow, hashMapDecodedFilteredByPathsComplexFlow, shared_dict, decode_method_package, decode_method_name, hash_map_decoded, java_signature, invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types, replacement_plan_by_hash, is_complex_flow)


def generateReplacementPlan(hash_map_decoded, java_signature, decode_method_package, decode_method_name):
    replacement_plan_by_hash = {}

    for smali_key, decoded_value in hash_map_decoded.items():
        try:
            # Generate all the regex & param parsing logic
            const_compiled_regex_patterns_array = generateSpecificRegexForReplacingParametersBasedOnSignatureComplex(java_signature, smali_key)

            if not const_compiled_regex_patterns_array:
                print(f"Skipping {smali_key}: Could not generate regex")
                continue

            # Escape decoded string properly
            prepared_decoded_string = prepareStringForSmali(decoded_value)

            # Store in plan
            replacement_plan_by_hash[smali_key] = {
                #"invoke_pattern": invoke_static_compiled_pattern,
                "const_patterns": const_compiled_regex_patterns_array,
                #"expected_var_count": expected_vars_count,
                "prepared_decoded_string": prepared_decoded_string,
                "decoded_value": decoded_value#,
                #"original_encoded_strings": original_encoded_strings  # Optional
            }

        except Exception as e:
            print(f"Error processing smali_key: {smali_key}: {e}")

    return replacement_plan_by_hash


def build_file_to_keys_map(hash_map_original):
    file_to_keys = defaultdict(list)
    for key, filepaths in hash_map_original.items():
        for filepath in filepaths:
            file_to_keys[filepath].append(key)
    return dict(file_to_keys)

def replaceWithMultiprocessing(file_keys_hashmap, hash_map_missing, decode_method_package, decode_method_name, hash_map_decoded, java_signature, invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types, replacement_plan_by_hash, is_complex_flow):
    from multiprocessing import Pool
    from functools import partial

    task_list = [
        (file_path, keys)
        for file_path, keys in file_keys_hashmap.items()
    ]


    func = partial(
        replaceDecodedStringsOnFileComplexFlow,
        invoke_static_compiled_pattern=invoke_static_compiled_pattern,
        const_value_regex_patterns_array=const_value_regex_patterns_array,
        param_types=param_types,
        replacement_plan_by_hash=replacement_plan_by_hash
     
    )

    with Pool() as pool:
        results = pool.map(func, task_list)

    # Post-process results: flatten and update missing map
    for result_list in results:
        if not result_list:
            continue
        for smali_key, filepath in result_list:
            if smali_key in hash_map_missing and filepath in hash_map_missing[smali_key]:
                hash_map_missing[smali_key].remove(filepath)

    return hash_map_missing



def replaceWithSingleprocessing(keyFilePathsTupleSimpleFlow, file_keys_hashmap, hash_map_missing, decode_method_package, decode_method_name, hash_map_decoded, java_signature, invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types, replacement_plan_by_hash, is_complex_flow):
    if is_complex_flow:
        for file_path, keys in file_keys_hashmap.items():
            key_filepath = (file_path, keys)

            result_list = replaceDecodedStringsOnFileComplexFlow(
                key_filepath,
                invoke_static_compiled_pattern=invoke_static_compiled_pattern,
                const_value_regex_patterns_array=const_value_regex_patterns_array,
                param_types=param_types,
                replacement_plan_by_hash=replacement_plan_by_hash
            )

            if not result_list:
                continue

            for smali_key, filepath in result_list:
                if smali_key in hash_map_missing and filepath in hash_map_missing[smali_key]:
                    hash_map_missing[smali_key].remove(filepath)
    else:
        for key_filepath in keyFilePathsTupleSimpleFlow:
            result = replaceDecodedStringsOnFileSimpleFlow(key_filepath, decode_method_package=decode_method_package, decode_method_name=decode_method_name, hash_map_decoded=hash_map_decoded, java_signature=java_signature
            )

            if result is None:
                continue
            smali_key, filepath = result
            if smali_key in hash_map_missing:
                if filepath in hash_map_missing[smali_key]:
                    hash_map_missing[smali_key].remove(filepath)




    return hash_map_missing

def replaceDecodedStringsOnFileComplexFlow(filepath_keys, invoke_static_compiled_pattern, const_value_regex_patterns_array, param_types, replacement_plan_by_hash):
    results = []

    filepath, smali_keys = filepath_keys

    if not smali_keys or not filepath:
        return results

    try:
        with open(filepath, 'r') as file:
            content = file.read()

            if 'com/example/ActivtityName' in filepath:
                print ("Debug - Find path")

            modified_content = remove_line_and_comments(content)

            modified_content, num_replacements = replaceDecodedStringIntoFileComplexFlow(modified_content, invoke_static_compiled_pattern, const_value_regex_patterns_array, replacement_plan_by_hash, param_types)

            if num_replacements > 0:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(modified_content)
                print(f"File: {filepath} had {num_replacements} instance(s) replaced")
            else:
                print(f"No Strings replaced in file: {filepath}")

    except Exception as e:
        print(f"Error processing file {filepath}: {e}")

    return results

def replaceDecodedStringsOnFileSimpleFlow(filepath_keys, decode_method_package, decode_method_name, hash_map_decoded, java_signature):

    smali_key, filepath = filepath_keys

    if not smali_key or not filepath:
        return

    if smali_key not in hash_map_decoded:
        print(f"Key '{smali_key}' not found in the Decoded Array Strings")
        return

    try:
        with open(filepath, 'r') as file:
            content = file.read()

        prepared_decoded_string = prepareStringForSmali(hash_map_decoded[smali_key])

        if prepared_decoded_string == STRING_DECODED_ERROR:
            return

        cleaned_content = remove_line_and_comments(content)

        regex_pattern = generateRegexForReplacingParametersBasedOnSignature(java_signature, decode_method_package, decode_method_name, smali_key)

        regex = re.compile(regex_pattern, re.DOTALL)
        modified_content, num_replacements = regex.subn(
            lambda m: f'const-string {m.groups()[-1]}, "{prepared_decoded_string}"', cleaned_content)

        if num_replacements > 0:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(modified_content)

            print(f"Modified {num_replacements} instance(s) in file: {filepath} with key: {smali_key}")
            return (smali_key, filepath)  # Let the caller remove this from hash_map

        else:
            print(f"No Strings replaced in file: {filepath}, key: {smali_key}")

    except Exception as e:
        print(f"Error processing file {filepath}: {e}")


def replaceDecodedStringIntoFileSimpleFlow(cleaned_content, regex_pattern, prepared_decoded_string):
    regex = re.compile(regex_pattern, re.DOTALL)
    modified_content, num_replacements = regex.subn(
        lambda m: f'const-string {m.groups()[-1]}, "{prepared_decoded_string}"', cleaned_content)
    return modified_content, num_replacements


def replaceDecodedStringIntoFileComplexFlow(smali_code, generic_invoke_pattern, const_value_regex_patterns_compiled_array, replacement_plan_by_hash, param_types):
    num_replacements = 0
    new_code = smali_code
    offset = 0

    invoke_matches = list(generic_invoke_pattern.finditer(smali_code))

    for invoke_match in invoke_matches:
        orig_start = invoke_match.start()
        orig_end = invoke_match.end()
        adjusted_start = orig_start + offset
        adjusted_end = orig_end + offset

        # 🧠 Step 1: Extract encoded variable values using your existing logic
        encoded_values, _ = handleMatchedValueAndEncryptionComplexAnalysis(
            smali_code,
            invoke_match,
            const_value_regex_patterns_compiled_array,
            param_types
        )

        if not encoded_values or len(encoded_values) != len(param_types):
            continue

        # Step 2: Build base64 smali_key
        smali_key = ",".join(encoded_values)

        if smali_key not in replacement_plan_by_hash:
            continue

        plan = replacement_plan_by_hash[smali_key]

        if plan["prepared_decoded_string"] == STRING_DECODED_ERROR:
            continue

        # Step 3: Find move-result-object on the next actual instruction line
        result = find_immediate_move_result_line(adjusted_end, new_code)
        if result is None:
            continue  # Skip: no valid move-result-* line found immediately after invoke

        move_result_start, move_result_end, result_var = result

        # Step 4: Replace move-result-* line
        replacement_line = f'    const-string {result_var}, "{plan["prepared_decoded_string"]}"'
        new_code = new_code[:move_result_start] + replacement_line + new_code[move_result_end:]
        offset += len(replacement_line) - (move_result_end - move_result_start)

        # Step 5: Remove invoke-static line
        new_code = new_code[:adjusted_start] + '' + new_code[adjusted_end:]
        offset -= (adjusted_end - adjusted_start)

        num_replacements += 1

    return new_code, num_replacements

def find_immediate_move_result_line(invoke_end_index, smali_code):
    post_code = smali_code[invoke_end_index:]
    lines = post_code.splitlines(keepends=True)

    offset = 0
    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            offset += len(line)
            continue

        match = MOVE_RESULT_OBJECT_PATTERN_REGEX_COMPILED.match(stripped)
        if match:
            result_var = match.group(1)
            start = invoke_end_index + offset
            end = start + len(line)
            return start, end, result_var
        else:
            # First real instruction is not move-result → invalid
            return None

    return None


def replace_fill_array_data(lines, array_label, new_array_values):
    in_array_data = False
    for i, line in enumerate(lines):
        if array_label in line:  # Found the label
            in_array_data = True
        elif in_array_data:
            if line.startswith(".array-data"):
                continue  # Skip the `.array-data` directive
            elif line.startswith(".end array-data"):
                break  # Stop at the end of the block
            else:
                # Replace the content with the new array values
                lines[i] = f"    {new_array_values}"
                in_array_data = False

def expected_variable_count(param_types):
    count = 0
    for param_type in param_types:
        param_type = param_type.strip()
        if param_type in PARAMETER_TYPE_TAKING_2_REGISTERS:
            count += 2  # long and double take two registers
        else:
            count += 1
    return count


def generateRegexForReplacingParametersBasedOnSignature(java_signature, package_pattern, method_name, smali_key):
    # Splitting the signature and the smali_key
    stringParts = smali_key.split(',')
    param_types = java_signature.strip("()").split(',')

    # Initialize a list for the regex patterns
    regex_patterns = []

    # Iterate through each parameter type and corresponding value in stringParts
    for i, param_type in enumerate(param_types):
        param_type = param_type.strip()
        value = stringParts[i] if i < len(stringParts) else None

        if param_type == 'String':
            # Decode the string for String type
            originalString = decodeBase64IntoString(value)
            pattern = rf'const-string(?:/jumbo)?\s+(\w+\d+), "{re.escape(originalString)}"'
            #pattern = rf'const-string(?:/jumbo)?\s+(\w+\d+), "{re.escape(originalString)}"'
        elif param_type == 'int':
            # Directly use the value for int, assuming it's provided in decimal
            pattern = rf'const/16 \w+, {value}'            
        elif param_type == 'boolean':
            # Convert 'true'/'false' to '0x1'/'0x0' for boolean
            bool_value = "0x1" if value.lower() == 'true' else "0x0"
            pattern = rf'const/4 \w+, {bool_value}'
            
        elif param_type == 'long':
            originalString = decodeBase64IntoString(value)
            #pattern = rf'const-wide\s+(\w+\d+), {originalString}'
            #pattern = rf'const-wide\s+({re.escape(firstElement)}\w+\d+), "{re.escape(originalString)}"'
            pattern = rf'const-wide\s+(\w+\d+), "{re.escape(originalString)}"'

        else:
            continue  # Skip if the type is not recognized or value is missing
        
        regex_patterns.append(pattern)

    loading_instructions_regex = r'\s+'.join(regex_patterns)    

    #optional_lines_regex = r'.+?'
    optional_lines_regex = rf'(?:(?:\.\w+\s+.*\s*)*?)\s*'

    # Dynamically build the smali method signature part
    smali_method_signature = ''.join([smali_type_mapping_with_registers[param.strip()][0] for param in param_types])


    # Adjusted regex pattern for invoke-static to capture the first variable
    invoke_static_regex = (
        rf'invoke-static(?:/range)?\s+\{{\s*(?P<invoked_var>\w+\d+)(?:\s*,\s*\w+\d+)*\s*\}},\s*' +
        rf'L{package_pattern};->' + rf'{method_name}' + rf'\({smali_method_signature}\)Ljava/lang/String;'
    )

    final_regex_pattern = loading_instructions_regex + optional_lines_regex + invoke_static_regex + rf'\s+move-result-object\s+(?P=invoked_var)\b'

    return final_regex_pattern

def generateGenericRegexForReplacingParametersBasedOnSignatureComplex(java_signature, package_pattern, method_name):
    # Split the signature to handle multiple parameters
    param_types = java_signature.strip("()").split(',')

    # Build regex patterns for each parameter type
    const_value_patterns_array = [
        r'\s*' + rf'const-string(?:/jumbo)?\s+(\w+\d+),\s+"([^"]+)"' if param == 'String' else
        #r'\s*' + r'const/(4|16|32) (\w\d+), -?\d+' if param == 'int' else
        #r'\s*' + r'const/(4|16|32) (\w\d+), (-?\d+)' if param == 'int' else
        r'\s*' + r'const/(4|16|32) (\w\d+), (-?0x[\da-fA-F]+|-?\d+)' if param == 'int' else
        r'\s*' + r'const/4 (\w\d+), 0x[01]' if param == 'boolean' else
        r'\s*' + r'const-wide\s+(\w+\d+),\s+(-?0x[\da-fA-F]+L)' if param == 'long' else
        r'\s*fill-array-data\s+(\w\d+),\s+(:\w[\w\d_]*)' if param == 'byte[]' else
        'UNKNOWN'
        for param in param_types
    ]

    # Compile regex patterns, skipping 'UNKNOWN'
    const_value_regex_patterns_array = [re.compile(pattern) for pattern in const_value_patterns_array if pattern != 'UNKNOWN']

    # Generate Smali method signature
    smali_method_signature = ''.join([get_smali_type(param.strip()) for param in param_types])

    # Escape `[` and `]` in the Smali method signature
    escaped_smali_method_signature = smali_method_signature.replace('[', r'\[').replace(']', r'\]')

    invoke_static_compiled_pattern = re.compile(
        rf'invoke-static(?:/range)?\s+\{{([\w\s,.]+(?:\.\.\s*\w+)?)}},\s*' +
        rf'L{re.escape(package_pattern)};->' + rf'{re.escape(method_name)}' +
        rf'\({escaped_smali_method_signature}\)Ljava/lang/String;'
    )

    #expected_vars_count = len(param_types)
    expected_vars_count = expected_variable_count(param_types)

    return invoke_static_compiled_pattern, const_value_regex_patterns_array, expected_vars_count, param_types

def generateSpecificRegexForReplacingParametersBasedOnSignatureComplex(java_signature, smali_key):
    # Split the Java method signature and the encoded Smali key
    stringParts = smali_key.split(',')
    param_types = java_signature.strip("()").split(',')
    decoded_strings = [decodeBase64IntoString(s) for s in stringParts]

    const_compiled_regex_patterns_array = []

    for i, param_type in enumerate(param_types):
        param_type = param_type.strip()
        value = decoded_strings[i] if i < len(decoded_strings) else None

        if param_type == 'String':
            pattern = rf'const-string(?:/jumbo)?\s+(\w+\d+),\s+"{re.escape(value)}"'
        elif param_type == 'int':
            pattern = rf'const/16\s+(\w+\d+),\s+{value}'
        elif param_type == 'boolean':
            bool_value = "0x1" if value.lower() == 'true' else "0x0"
            pattern = rf'const/4\s+(\w+\d+),\s+{bool_value}'
        elif param_type == 'long':
            pattern = rf'const-wide\s+(\w+\d+),\s+{value}'
        elif param_type == 'byte[]':
            if isinstance(value, str):
                byte_values = value.split(';')
                pattern = (
                    rf'fill-array-data\s+(\w\d+),\s+(:[\w\d_]+)' +
                    rf'|\.array-data\s+\d+\n.*?' +
                    rf'\n'.join([rf'\s+{re.escape(byte)}' for byte in byte_values]) +
                    rf'\s+\.end array-data'
                )
            else:
                raise ValueError(f"Invalid value for byte[]: {value}")
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")

        const_compiled_regex_patterns_array.append(re.compile(pattern, re.DOTALL))

    return const_compiled_regex_patterns_array

def generateRegexForReplacingParametersBasedOnSignatureComplex1(java_signature, package_pattern, method_name, smali_key):
    # Split the Java method signature and the encoded Smali key
    stringParts = smali_key.split(',')
    param_types = java_signature.strip("()").split(',')
    decoded_strings = [decodeBase64IntoString(s) for s in stringParts]

    const_compiled_regex_patterns_array = []

    for i, param_type in enumerate(param_types):
        param_type = param_type.strip()
        value = decoded_strings[i] if i < len(decoded_strings) else None

        if param_type == 'String':
            pattern = rf'const-string(?:/jumbo)?\s+(\w+\d+),\s+"{re.escape(value)}"'
        elif param_type == 'int':
            pattern = rf'const/16\s+(\w+\d+),\s+{value}'
        elif param_type == 'boolean':
            bool_value = "0x1" if value.lower() == 'true' else "0x0"
            pattern = rf'const/4\s+(\w+\d+),\s+{bool_value}'
        elif param_type == 'long':
            pattern = rf'const-wide\s+(\w+\d+),\s+{value}'
        elif param_type == 'byte[]':
            if isinstance(value, str):
                byte_values = value.split(';')
                pattern = (
                    rf'fill-array-data\s+(\w\d+),\s+(:[\w\d_]+)' +
                    rf'|\.array-data\s+\d+\n.*?' +
                    rf'\n'.join([rf'\s+{re.escape(byte)}' for byte in byte_values]) +
                    rf'\s+\.end array-data'
                )
            else:
                raise ValueError(f"Invalid value for byte[]: {value}")
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")

        const_compiled_regex_patterns_array.append(re.compile(pattern, re.DOTALL))

    # Generate Smali method signature
    smali_method_signature = ''.join([get_smali_type(param.strip()) for param in param_types])

    # Escape `[` and `]` in the Smali method signature
    escaped_smali_method_signature = smali_method_signature.replace('[', r'\[').replace(']', r'\]')

    invoke_static_compiled_pattern = re.compile(
        rf'invoke-static(?:/range)?\s+\{{([\w\s,.]+(?:\.\.\s*\w+)?)}},\s*' +
        rf'L{re.escape(package_pattern)};->' + rf'{re.escape(method_name)}' +
        rf'\({escaped_smali_method_signature}\)Ljava/lang/String;'
    )

    #expected_vars_count = len(param_types)
    expected_vars_count = expected_variable_count(param_types)

    return invoke_static_compiled_pattern, const_compiled_regex_patterns_array, decoded_strings, expected_vars_count, param_types


def nonEmptyItems(dd):
    return {key: value for key, value in dd.items() if value}

def exportNotReplacedDecodedStrings(task_thread, hash_map_decoded, hash_map_missing):
    hash_map_missing_clean = nonEmptyItems(hash_map_missing)
    if hash_map_missing_clean:
        updateStatus(task_thread, " ----- STORE DECODED STRINGS NOT REPLACED ON THE SMALIE FILES ----- ")

        data_to_save = {}

        for key, values in hash_map_missing_clean.items():
            if key in hash_map_decoded:  # Check if the key exists in hash_map_decoded
                data_to_save[key] = hash_map_decoded[key]
                #print (key + ":" + hash_map_decoded[key])

        # Write the data to a JSON file
        with open(Config.get_missing_strings_path(), 'w') as file:
            json.dump(data_to_save, file, indent=4)

        print(f"JSON file has been created at {Config.get_missing_strings_path()}")


def compareDictionaries(hash_map_original, hash_map_missing):
    # Check for keys in hash_map_original not in hash_map or vice versa
    if set(hash_map_original.keys()) != set(hash_map_missing.keys()):
        return True

    # For each key in hash_map_original, check if the values differ from those in shared_dict
    for key, original_values in hash_map_original.items():
        hash_map_values = hash_map_missing.get(key)
        # If the values list for the key differs in any way, return True
        if sorted(original_values) != sorted(hash_map_values):
            return True

    # If no differences were found, return False
    return False


def checkIfHasValidDecodedStrings(hash_map_decoded):
    match_count = sum(value == STRING_DECODED_ERROR for value in hash_map_decoded.values())
    if match_count == 0:
        # None of the values match the target string
        return 0
    elif match_count == len(hash_map_decoded):
        # All values match the target string
        return 1
    else:
        # Some (but not all) values match the target string
        return 2    

def backupSmaliCode():
    # Define the full path for the backup directory
    backup_root = os.path.join(Config.get_extracted_folder(), Config.get_backup_path())
    
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_root):
        os.makedirs(backup_root)
    else:
        # Optional: Clear previous backup contents
        for item in os.listdir(backup_root):
            item_path = os.path.join(backup_root, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    
    # Walk through the source directory to find directories starting with "smali"
    for root, dirs, _ in os.walk(Config.get_extracted_folder(), topdown=True):
        # Use slicing to iterate through directories as we may modify 'dirs'
        for dir in dirs[:]:
            if dir.startswith("smali"):
                smali_folder_path = os.path.join(root, dir)
                backup_folder_path = os.path.join(backup_root, os.path.relpath(smali_folder_path, Config.get_extracted_folder()))
                
                # Copy entire smali folder to backup directory
                shutil.copytree(smali_folder_path, backup_folder_path)
                
                # To prevent further recursion into this directory
                dirs.remove(dir)   


def check_method_in_smali(class_package_name: str, method_name: str) -> str:
    # Convert the package name to a relative file path
    relative_file_path = class_package_name.replace(".", os.sep) + ".smali"

    # Collect all smali folders under ROOT_PATH
    smali_folders = [os.path.join(Config.get_extracted_folder(), d) for d in os.listdir(Config.get_extracted_folder()) if os.path.isdir(os.path.join(Config.get_extracted_folder(), d)) and "smali" in d]

    for smali_folder in smali_folders:
        file_path = os.path.join(smali_folder, relative_file_path)

        # Check if the file exists in this smali folder
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as smali_file:
                    for line in smali_file:
                        # Check if the method is defined in the file
                        if line.strip().startswith(".method") and method_name in line:
                            return ""  # Method found
            except Exception as e:
                print(f"Error: Could not read the file '{file_path}'. Details: {e}")

    return f"Error: The method '{method_name}' was not found in any '{class_package_name}' smali files under '{Config.get_extracted_folder()}'."

