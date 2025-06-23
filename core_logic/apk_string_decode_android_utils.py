from core_logic.apk_string_decode_consts import triggerCallerToDecodeMethod, APK_STRING_DECODE_ACTIVITY_NAME, ANDROID_LOG_MAX_ENTRIES_ALLOWED, APK_STRING_DECODE_BROADCAST_RECEIVER_NAME, ANDROID_BROADCAST_COMMAND_MAX_LENGTH, APK_STRING_DECODE_SERVICE_NAME
from core_logic.apk_string_decode_common_utils import convert_slash_to_dot, encodeHashMapToBase64WithDelimiter, encodeStringIntoBase64
from core_logic.apk_string_decode_logic_smali_code import receiver_manifest_content
from core_logic.apk_string_decode_logic_utils import updateStatus
from core_logic.apk_string_decode_config import Config

import time
import subprocess
import glob
import os
import re
import xml.etree.ElementTree as ET
import shutil
import math

def compileApkWithRetries(task_thread, retries=15):
    """
    Attempts to compile the APK multiple times, handling errors dynamically with a maximum number of retries.
    Stops if the same error occurs 5 times in a row.
    """

    MAX_IDENTICAL_ERRORS = 3
    last_errors = []
    
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} to compile the APK...")
        errors = runCommandToCompileApk(task_thread)

        if not errors.strip():
            print("APK compiled successfully!")
            return ""

        # Store last 5 errors
        last_errors.append(errors.strip())
        if len(last_errors) > MAX_IDENTICAL_ERRORS:
            last_errors.pop(0)

        # Check if last 5 errors are identical
        if len(last_errors) == MAX_IDENTICAL_ERRORS and len(set(last_errors)) == 1:
            print("The same error has occurred for 5 consecutive builds. Stopping.")
            return "Error Recompiling the Apk"

        handle_problematic_files(errors)
    
    print("APK compilation failed after multiple attempts.")
    return "Error Recompiling the Apk" 

def parse_error_log(error_log):
    """
    Parses the error log to extract file paths and problematic resource names for private and missing resources.

    :param error_log: The error log string.
    :return: A dictionary with file paths as keys and lists of problematic resources as values.
    """
    file_resource_map = {}

    # Regular expressions for private resources and missing resources
    private_resource_pattern = re.compile(r"(/[^:\s]+\.xml):\d+: error: resource (android:[\w/]+) is private")
    missing_resource_with_alias_pattern = re.compile(r"(/[^:\s]+\.xml):\d+: error: resource ([\w/]+) \(aka [^:]+:[\w/]+\) not found")
    missing_symbol_no_definition_pattern = re.compile(r"(/[^:\s]+\.xml):\d+: error: no definition for declared symbol '([\w\.]+:[\w/]+)'")

    # Extract private resource errors
    for match in private_resource_pattern.findall(error_log):
        file_path, resource_name = match
        if file_path not in file_resource_map:
            file_resource_map[file_path] = {"private": [], "missing": []}
        file_resource_map[file_path]["private"].append(resource_name)
        print(f"[DEBUG] Private resource detected: {resource_name} in {file_path}")

    # Extract missing resource errors with alias (aka format)
    for match in missing_resource_with_alias_pattern.findall(error_log):
        file_path, resource_name = match
        if file_path not in file_resource_map:
            file_resource_map[file_path] = {"private": [], "missing": []}
        file_resource_map[file_path]["missing"].append(resource_name)
        print(f"[DEBUG] Missing resource with alias detected: {resource_name} in {file_path}")

    # Extract missing symbol errors with no definition for declared symbol
    for match in missing_symbol_no_definition_pattern.findall(error_log):
        file_path, resource_name = match
        if file_path not in file_resource_map:
            file_resource_map[file_path] = {"private": [], "missing": []}
        file_resource_map[file_path]["missing"].append(resource_name)
        print(f"[DEBUG] Missing symbol (no definition) detected: {resource_name} in {file_path}")

    return file_resource_map

def remove_private_resources_and_add_placeholders(file_path, private_resources):
    """
    Removes lines with private resources and adds placeholders for them if they are colors.

    :param file_path: Path to the XML file.
    :param private_resources: List of private resource names to remove.
    """
    if not os.path.exists(file_path):
        print(f"[DEBUG] File {file_path} not found!")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if any(private_resource in line for private_resource in private_resources):
                # Replace private color resources with a placeholder color if it's in colors.xml
                if 'color' in line:
                    placeholder_color = "#FFFFFF"  # Default placeholder color
                    color_name = re.search(r'name="([^"]+)"', line)
                    if color_name:
                        file.write(f'    <color name="{color_name.group(1)}">{placeholder_color}</color>\n')
                        print(f"[DEBUG] Replaced private color resource with placeholder: {color_name.group(1)}")
                else:
                    print(f"[DEBUG] Removed line with private resource: {line.strip()}")
            else:
                file.write(line)

def add_missing_color_placeholders(colors_xml_path, missing_colors):
    """
    Adds placeholder definitions for missing colors in colors.xml.

    :param colors_xml_path: Path to the colors.xml file.
    :param missing_colors: List of color names that need placeholder definitions.
    """
    if not os.path.exists(colors_xml_path):
        print(f"[DEBUG] {colors_xml_path} not found! Creating a new colors.xml.")
        with open(colors_xml_path, 'w') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>')

    with open(colors_xml_path, 'r') as file:
        lines = file.readlines()

    with open(colors_xml_path, 'w') as file:
        # Write existing lines except closing </resources> tag
        for line in lines:
            if '</resources>' not in line:
                file.write(line)
        
        # Add placeholders for each missing color
        for color in missing_colors:
            file.write(f'    <color name="{color}">#FFFFFF</color>\n')
            print(f"[DEBUG] Added placeholder for missing color: {color}")

        # Close the resources tag
        file.write('</resources>\n')

def ensure_valid_xml_placeholders(line, resource_type):
    """
    Ensures that the inserted placeholder is valid within the XML structure.

    :param line: The current line in the XML file.
    :param resource_type: The type of resource (color, other) to determine the placeholder.
    :return: The modified line with a valid placeholder.
    """
    if 'color' in resource_type:
        return re.sub(r'>(.*?)<', f'>#FFFFFF<', line)
    else:
        return re.sub(r'>(.*?)<', f'>@null<', line)

def process_xml(file_path, resources_to_remove):
    """
    Processes XML to remove private resources and adds placeholders for missing resources.

    :param file_path: The path to the XML file.
    :param resources_to_remove: Dictionary containing 'private' resources to remove and 'missing' resources to add placeholders for.
    """
    if not os.path.exists(file_path):
        print(f"[DEBUG] File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            # Skip lines with private resources to effectively remove them
            if any(resource in line for resource in resources_to_remove["private"]):
                print(f"[DEBUG] Removed private resource reference from {file_path}: {line.strip()}")
                continue  # Skip this line, so it doesn't get written back to the file

            # Process any missing resources by adding placeholders
            modified_line = line
            for resource in resources_to_remove["missing"]:
                if resource in line:
                    # Ensure valid XML structure when replacing with placeholders
                    modified_line = ensure_valid_xml_placeholders(line, resource)
                    print(f"[DEBUG] Added placeholder for missing resource in {file_path}: {line.strip()}")

            # Write the modified or original line back to the file
            file.write(modified_line)

def remove_unsupported_manifest_attributes(unsupported_attributes):
    """
    Removes specific unsupported attributes from the <manifest> tag in AndroidManifest.xml
    without altering the rest of the tag or line.

    :param manifest_path: Path to AndroidManifest.xml.
    :param unsupported_attributes: List of attribute names to remove.
    """
    if not os.path.exists(Config.get_manifest_path()):
        print(f"[DEBUG] Manifest file {Config.get_manifest_path()} not found!")
        return

    with open(Config.get_manifest_path(), 'r') as file:
        lines = file.readlines()

    with open(Config.get_manifest_path(), 'w') as file:
        for line in lines:
            # Only modify the line if it contains the <manifest> tag
            if '<manifest' in line:
                for attr in unsupported_attributes:
                    # Use regex to remove the specific attribute and its value
                    line = re.sub(rf'\s+{attr}="[^"]*"', '', line)
                print(f"[DEBUG] Processed <manifest> tag with unsupported attributes removed: {line.strip()}")
                file.write(line)  # Write the modified <manifest> line
            else:
                file.write(line)  # Write other lines unchanged


def handle_problematic_files(error_log):
    """
    Handles problematic Smali files, private resources, missing attributes, and manifest issues.

    :param error_log: The error log string.
    """
    print("🔍 Analyzing errors...")

    # Step 1: Fix Smali Enum Issues - This might cause other issues in other apps. If it is the case, it is required a rework on this fix
    fix_enum_issues(error_log)

    # Step 2: Fix Private & Missing Resources
    file_resource_map = parse_error_log(error_log)
    for file_path, resources in file_resource_map.items():
        print(f"[DEBUG] Processing file: {file_path}")

        if "private" in resources and resources["private"]:
            remove_private_resources_and_add_placeholders(file_path, resources["private"])

        if "missing" in resources and resources["missing"]:
            add_missing_color_placeholders(file_path, resources["missing"])

    # Step 3: Fix AndroidManifest.xml Issues
    if "AndroidManifest.xml" in error_log:
        fix_manifest_namespaces()
        unsupported_attributes = ["android:requiredSplitTypes", "android:splitTypes"]
        remove_unsupported_manifest_attributes(unsupported_attributes)

    print("Issues handled. Retrying compilation...")

def fix_manifest_namespaces():
    """
    Replaces incorrectly assigned XML namespaces in AndroidManifest.xml.

    :param manifest_path: Path to AndroidManifest.xml.
    """
    if not os.path.exists(Config.get_manifest_path()):
        print(f"Warning: {Config.get_manifest_path()} not found. Skipping namespace fix.")
        return

    with open(Config.get_manifest_path(), "r", encoding="utf-8") as file:
        manifest_content = file.read()

    # Detects any namespace prefix (e.g., ns0, ns1, etc.)
    match = re.search(r'xmlns:(ns\d+)="http://schemas.android.com/apk/res/android"', manifest_content)
    if match:
        incorrect_prefix = match.group(1)  # Extracts nsX (e.g., ns0)
        print(f"🔄 Replacing '{incorrect_prefix}' with 'android' in {Config.get_manifest_path()}...")

        # Replace all occurrences of nsX: with android:
        manifest_content = manifest_content.replace(f"{incorrect_prefix}:", "android:")

        # Replace namespace declaration
        manifest_content = manifest_content.replace(f'xmlns:{incorrect_prefix}=', 'xmlns:android=')

        with open(Config.get_manifest_path(), "w", encoding="utf-8") as file:
            file.write(manifest_content)

        print("Namespace issue fixed.")
    else:
        print("No incorrect namespace found.")


def fix_enum_issues(error_log):
    """
    Extracts Smali classes from the error log and fixes their `values()` methods.
    """
    problematic_classes = extract_problematic_classes(error_log)

    if not problematic_classes:
        print("No problematic Smali classes found.")
        return

    print(f"🛠 Fixing {len(problematic_classes)} problematic Smali classes...")

    for smali_class in problematic_classes:
        smali_file = find_smali_file(smali_class)
        if "c61" in smali_class:
            print("c61")
        if "com/inmobi/media/h6" in smali_class:
            print("com/inmobi/media/h6")
        if smali_file:
            print(f"Fixing: {smali_file}")
            modify_smali_values(smali_file)
        else:
            print(f"Could not find Smali file for {smali_class}")


def extract_problematic_classes(error_log):
    """
    Extracts Smali class names from the error log efficiently using regex findall().
    """
    matches = re.findall(r"Exception.*method\s+L([\w/$]+);->values", error_log)
    return list(set(matches))  # Remove duplicates and return a list

def find_smali_file(class_name):
    """
    Finds the correct Smali file for a class, ensuring:
    - Exact class name match (no `c61$a.smali` for `c61`)
    - Prefers `c61.smali` over `c61.1.smali` if both exist
    - Skips missing directories gracefully
    """
    class_path = class_name.replace(".", "/") + ".smali"
    smali_folders = glob.glob(os.path.join(Config.get_extracted_folder(), "smali*"))

    exact_match = None
    numbered_match = None

    for smali_folder in smali_folders:
        smali_file = os.path.join(smali_folder, class_path)
        dir_path = os.path.dirname(smali_file)

        if not os.path.isdir(dir_path):
            continue  # Skip if the folder does not exist

        # List files in the directory and find exact matches
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)

            # 🔹 Strict exact match (e.g., `c61` must match `c61.smali`)
            if file == os.path.basename(smali_file):
                exact_match = file_path

            # 🔹 Match `.1.smali` files only if no exact match is found
            elif file.startswith(os.path.basename(smali_file).replace(".smali", "") + ".") and file.endswith(".smali"):
                numbered_match = file_path

    # 🔹 Prefer `c61.smali` if it exists, otherwise use `c61.1.smali`
    return exact_match if exact_match else numbered_match

def modify_smali_values(smali_file):
    """
    Modifies the `values()` method in the given Smali file.
    """
    with open(smali_file, "r") as file:
        lines = file.readlines()

    new_lines = []
    inside_method = False

    for line in lines:
        if ".method public static values()" in line:
            inside_method = True
            new_lines.append(line)  # Keep the method signature
            new_lines.append("    .locals 1\n")
            new_lines.append("    const/4 v0, 0x0\n")
            new_lines.append("    return-object v0\n")
            new_lines.append(".end method\n")
        elif ".end method" in line and inside_method:
            inside_method = False  # End method, do not append original code
        elif not inside_method:
            new_lines.append(line)

    with open(smali_file, "w") as file:
        file.writelines(new_lines)

def runCommandToCompileApk(task_thread):
    # Construct the apktool command
    try:
        result = subprocess.run(['apktool', 'b', '-o', Config.get_modified_apk(), Config.get_extracted_folder()],
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                text=True)

        #command = ["apktool", "b", "-o", Config.get_modified_apk(), Config.get_extracted_folder()]
        # Run the apktool command using subprocess
        #subprocess.run(command)
        print(result)
        if result.returncode != 0:
            updateStatus(task_thread, f"Compilation failed with error")
            errors = result.stderr
            return errors
        else:
            if file_exists(Config.get_modified_apk()):
                return ""
            else:
                updateStatus(task_thread, f"Compilation failed with error")
                return "Error Recompiling the Apk"     
    except subprocess.CalledProcessError as e:
        updateStatus(task_thread, f"Compilation failed with error: {e.stderr}")
        return "Error Recompiling the Apk"


def runCommandToCompileApkIgnoringResources(task_thread):
    # Construct the apktool command
    try:
        result = subprocess.run(['apktool', 'b', '--no-res', '-o' ,Config.get_modified_apk(), Config.get_extracted_folder()],
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                text=True)

        #command = ["apktool", "b", "-o", Config.get_modified_apk(), Config.get_extracted_folder()]
        # Run the apktool command using subprocess
        #subprocess.run(command)
        print(result)
        if result.returncode != 0:
            updateStatus(task_thread, f"Compilation failed with error")
            errors = result.stderr
            return errors
        else:
            if file_exists(Config.get_modified_apk()):
                return ""
            else:
                updateStatus(task_thread, f"Compilation failed with error")
                return "Error Recompiling the Apk"     
    except subprocess.CalledProcessError as e:
        updateStatus(task_thread, f"Compilation failed with error: {e.stderr}")
        return "Error Recompiling the Apk"

def findProblematicFiles(errors):
    """
    Extract problematic file paths from the compilation error message.
    
    :param errors: Error message from the APK compilation process.
    :return: List of problematic file paths.
    """
    problematic_files = []
    
    # Extract file paths from error logs using regex
    pattern = r'(\/[^\s]+\.xml)'  # Adjust pattern as needed to capture other files
    problematic_files = re.findall(pattern, errors)
    
    print("Identified problematic files:", problematic_files)
    return problematic_files


def deleteProblematicFiles(problematic_files):
    for file_path in problematic_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

def removeReferencesFromPublicXmlfile1(problematic_files):
    # Extract file names without extension
    file_names = [os.path.splitext(os.path.basename(path))[0] for path in problematic_files]
    
    # Read the XML file
    with open(Config.get_public_xml_path(), 'r') as file:
        lines = file.readlines()
    
    # Open the file again to write the changes
    with open(Config.get_public_xml_path(), 'w') as file:
        for line in lines:
            # Assuming that the XML line format is: <public type="drawable" name="ic_jazz" id=" />
            if any(f'<public type="drawable" name="{file_name}"' in line for file_name in file_names):
                print(f"Removed reference to {line.strip()} from XML")
            else:
                file.write(line)

def removeReferencesFromPublicXmlfile(problematic_files):
    """
    Remove references from the public XML file for the specified types.
    
    :param problematic_files: List of file paths that are problematic.
    :param types_to_remove: List of types (e.g., 'drawable', 'mipmap') to remove.
    """
    types_to_remove = ['drawable', 'mipmap', 'anim', 'color', 'raw']


    # Extract file names without extension
    file_names = [os.path.splitext(os.path.basename(path))[0] for path in problematic_files]
    
    if not os.path.exists(Config.get_public_xml_path()):
        #print(f"Public XML file not found: {public_xml_file_path}. Skipping.")
        return

    # Read the XML file
    with open(Config.get_public_xml_path(), 'r') as file:
        lines = file.readlines()
    
    # Open the file again to write the changes
    with open(Config.get_public_xml_path(), 'w') as file:
        for line in lines:
            # Check if the line contains a reference to any of the problematic files for the specified types
            if any(f'<public type="{type_to_remove}" name="{file_name}"' in line 
                   for type_to_remove in types_to_remove for file_name in file_names):
                print(f"Removed reference to {line.strip()} from XML")
            else:
                file.write(line)

def removeResourceReferences(problematic_files, resource_types=None):
    """
    Remove references to the specified resources from all XML files in the given directory.
    
    :param problematic_files: List of file paths that are problematic.
    :param resource_types: List of resource types to remove (default is all types).
    """
    if resource_types is None:
        resource_types = ['mipmap', 'drawable', 'color', 'raw', 'anim', 'font', 'xml', 'menu', 'layout', 'values', 'transition', 'interpolator']

    # Extract file names without extension
    file_names = [os.path.splitext(os.path.basename(path))[0] for path in problematic_files]

    # Compile regex pattern to match resource references dynamically
    resource_pattern = re.compile(
        r'@\b(?:{})\b/({})'.format('|'.join(resource_types), '|'.join(re.escape(name) for name in file_names))
    )

    xml_files = find_xml_files(Config.get_res_folder())

    for file_path in xml_files:
        with open(file_path, 'r') as file:
            content = file.read()

        # Remove references to the specified resources
        new_content = resource_pattern.sub('@null', content)

        with open(file_path, 'w') as file:
            file.write(new_content)

def find_xml_files(directory):
    """
    Recursively find all XML files in the given directory.
    
    :param directory: Root directory to search for XML files.
    :return: List of XML file paths.
    """
    xml_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    return xml_files




def file_exists(filepath):
    return os.path.exists(filepath)

def runcompileDecodedApk(task_thread):
    try:
        result = subprocess.run(['apktool', 'b', '-o' , Config.get_decoded_apk(), Config.get_extracted_folder()],
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                text=True, check=True)
                                #text=True, check=True)
        
        if result.returncode != 0:
            updateStatus(task_thread, f"Compilation failed with error")
            errors = result.stderr
            return errors, result.returncode
        else:
            if file_exists(Config.get_modified_apk()):
                return "", result.returncode
            else:
                updateStatus(task_thread, f"Compilation failed with error")
                return "Error Recompiling the Apk", result.returncode     
    except subprocess.CalledProcessError as e:
        updateStatus(task_thread, f"Compilation failed with error: {e.stderr}")
        return e.stderr, e.returncode if e.returncode else "Error Recompiling the Apk"



def compileDecodedApk(task_thread, is_file_rollback, retries=6):
    updateStatus(task_thread, " ----- REASSEMBLE APP ----- ")
    if Config.get_extracted_folder():
        # Construct the apktool command

        for attempt in range(retries):
            print(f"Attempt {attempt + 1} to compile the APK...")
            errors, returncode = runcompileDecodedApk(task_thread)
            #errors = runCommandToCompileApkIgnoringResources(task_thread)
            
            if not errors.strip():
                print("APK compiled successfully!")
                return True
            
            handle_problematic_files(errors)


        # Check the result for success or failure
        if returncode and returncode == 0:
            if file_exists(Config.get_decoded_apk()):
                return True
            else:
                updateStatus(task_thread, "APK was not created with an unkown reason")
                return False
        else:
            if is_file_rollback:
                print(f"Compilation failed with error: {errors.stderr}. ")
                handleCompilationError(task_thread, errors.stderr)
                errors, returncode = runcompileDecodedApk(task_thread)
                if returncode == 0:
                    if file_exists(Config.get_decoded_apk()):
                        return True
                    else:
                        updateStatus(task_thread, "APK was not created with an unkown reason")
                        return False
                else:
                    updateStatus(task_thread, f"Compilation failed with error: {errors.stderr}")
                    return False
            else:
                updateStatus(task_thread, f"Compilation failed with error: {errors.stderr}")
                return False


    else:
        updateStatus(task_thread, "No apk extracted folder detected.")
        return False

def handleCompilationError(task_thread, error_message):
    updateStatus(task_thread, " ----- ROLLING BACK FAULTY FILES ----- ")
    if "Cannot get the location of a label that hasn't been placed yet" in error_message:
        # Attempt to parse the problematic file path from the error message
        match = re.search(r'(?P<path>.+/smali/.+\.smali)\[\d+,\d+\]', error_message)
        if match:
            faulty_file_path = match.group('path')
            # Construct the path to the backup file assuming a known structure
            backup_file_path = faulty_file_path.replace('apk_extracted', 'apk_extracted_backup', 1)
            if os.path.exists(backup_file_path):
                # Replace the faulty file with the backup
                shutil.copy2(backup_file_path, faulty_file_path)
                print(f"Replaced faulty file with backup: {faulty_file_path}")
            else:
                print(f"Backup file not found: {backup_file_path}")
        else:
            print("Failed to parse the faulty file path.")
    else:
        # Log a general failure message if the specific error is not detected
        print(f"Compilation failed: {error_message}")
    return False

def removeElementsFromManifest(task_thread):
    """Remove specified tags from the AndroidManifest.xml."""
    tree = ET.parse(Config.get_manifest_path())
    root = tree.getroot()

    tags_to_remove = [
        'receiver', 'service', 'provider', 'activity', 'uses-permission', 
        'meta-data', 'uses-library', 'queries', 'property', 'activity-alias'
    ]

    # Recursive removal function
    def remove_tag(parent):
        for tag in tags_to_remove:
            for element in list(parent.findall(tag)):
                parent.remove(element)
            for child in list(parent):
                remove_tag(child)

    remove_tag(root)
    tree.write(Config.get_manifest_path(), encoding='utf-8', xml_declaration=True)
    print(f"All {', '.join(tags_to_remove)} tags removed from the manifest, including nested ones.")


def removeAppplicationNameFromManifest():
    """Remove the android:name attribute from the application tag in the AndroidManifest.xml."""
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')  # Register namespace
    
    tree = ET.parse(Config.get_manifest_path())
    root = tree.getroot()
    
    application_node = root.find('application')
    if application_node is not None:
        app_name_attr = '{http://schemas.android.com/apk/res/android}name'
        if app_name_attr in application_node.attrib:
            del application_node.attrib[app_name_attr]  # Remove the attribute
            tree.write(Config.get_manifest_path(), encoding='utf-8', xml_declaration=True)
            print("android:name attribute removed from the manifest.")
        else:
            print("No android:name attribute found.")
    else:
        print("No application tag found in the manifest.")


def get_application_class(root):
    namespace = {'android': 'http://schemas.android.com/apk/res/android'}
    application_element = root.find("./application")

    if application_element is not None:
        # Print all attributes for debugging
        print(f"[DEBUG] Application element attributes: {application_element.attrib}")

        # Extract the application class name correctly
        app_class = application_element.get("{http://schemas.android.com/apk/res/android}name")

        # Handle case where namespace might not be present
        if app_class is None:
            app_class = application_element.get("name")  # Try without namespace
        
        # Validate and return the application class
        if app_class and not is_common_application_class(app_class):
            return app_class

    return None

def is_common_application_class(app_class):
    common_classes = ["android.app.Application", "Multiplex", "androidx.multidex.MultiDexApplication"]
    return any(app_class.endswith(cls) for cls in common_classes)

def get_launcher_activity(root):
    namespace = {'android': 'http://schemas.android.com/apk/res/android'}
    for activity in root.findall("application/activity"):
        intent_filters = activity.findall("intent-filter")
        for intent_filter in intent_filters:
            actions = intent_filter.findall("action")
            categories = intent_filter.findall("category")
            
            has_launcher_action = any(
                action.get('{http://schemas.android.com/apk/res/android}name') == "android.intent.action.MAIN"
                for action in actions
            )
            has_launcher_category = any(
                category.get('{http://schemas.android.com/apk/res/android}name') == "android.intent.category.LAUNCHER"
                for category in categories
            )
            
            if has_launcher_action and has_launcher_category:
                return activity.get('{http://schemas.android.com/apk/res/android}name')
    return None


def addReceiverToManifest(task_thread, relativeClassPath):
    updateStatus(task_thread, " ----- ADD RECEIVER / ACTIVITY TO MANIFEST ----- ")
    # Read the original manifest content
    with open(Config.get_manifest_path(), 'r', encoding='utf-8') as file:
        manifest_content = file.read()

    # Add targetSdkVersion if missing
    if '<uses-sdk' not in manifest_content:
        # Insert full <uses-sdk> tag before <application>
        sdk_tag = '<uses-sdk android:minSdkVersion="16" android:targetSdkVersion="29" />\n'
        application_index = manifest_content.find('<application')
        manifest_content = (
            manifest_content[:application_index]
            + sdk_tag
            + manifest_content[application_index:]
        )
    elif 'targetSdkVersion' not in manifest_content:
        # Inject targetSdkVersion into existing <uses-sdk> tag
        import re
        manifest_content = re.sub(
            r'(<uses-sdk[^>]*?)\s*(/?>)',
            r'\1 android:targetSdkVersion="29"\2',
            manifest_content
        )

    # Add <uses-permission> before <application> if not already present
    permission_tag = '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />\n<uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />\n'
    if permission_tag.strip() not in manifest_content:
        application_index = manifest_content.find('<application')
        manifest_content = (
            manifest_content[:application_index]
            + permission_tag
            + manifest_content[application_index:]
        )

    # Find the position to insert the <receiver> element before </application>
    insert_position = manifest_content.find('</application>')

    receiver_manifest_content_adjusted = receiver_manifest_content.replace('{}', convert_slash_to_dot(relativeClassPath), 1).replace('{}', APK_STRING_DECODE_BROADCAST_RECEIVER_NAME, 1).replace('{}', convert_slash_to_dot(relativeClassPath), 1).replace('{}', APK_STRING_DECODE_SERVICE_NAME, 1).replace('{}', convert_slash_to_dot(relativeClassPath), 1).replace('{}', APK_STRING_DECODE_ACTIVITY_NAME, 1)

    new_manifest_content = (
        manifest_content[:insert_position]
        + (receiver_manifest_content_adjusted)
        + manifest_content[insert_position:]
    )

    # Write the modified content back to the manifest file
    with open(Config.get_manifest_path(), 'w', encoding='utf-8') as file:
        file.write(new_manifest_content)

    updateStatus(task_thread, "Receiver added to AndroidManifest.xml.")

def installExtractedApk(task_thread, appPackageName):
    updateStatus(task_thread, " ----- INSTALL EXTRACTED APK ----- ")
    if Config.get_modified_apk():
        # Uninstall app if already installed on the device
        if isPackageInstalled(appPackageName):
            uninstallPackage(appPackageName)

        # Construct the adb install command
        command = ["adb", "install", Config.get_modified_apk()]

        # Run the adb install command using subprocess
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the installation was successful
        if result.returncode == 0:
            updateStatus(task_thread, "Modified Apk installed with Success")
            return ""
        else:
            error_message = f"Failed to install app. Error: {result.stderr}"
            updateStatus(task_thread, error_message)
            return error_message
    else:
        no_apk_message = "No apk extracted file detected."
        updateStatus(task_thread, no_apk_message)
        return no_apk_message

def isPackageInstalled(package_name):
    try:
        subprocess.check_output(['adb', 'shell', 'pm', 'path', package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def uninstallPackage(package_name):
    try:
        subprocess.check_output(['adb', 'uninstall', package_name])
        print(f'Successfully uninstalled: {package_name}')
    except subprocess.CalledProcessError as e:
        print(f'Error uninstalling {package_name}: {e}')

def triggerBroadcastReceiverSimplePing(task_thread, package_name, relativeReceiverClassPath):
    updateStatus(task_thread, " ----- PING RECEIVER ----- ")
    command = [
        "adb",
        "shell",
        "am",
        "broadcast",
        "-n",
        "{}/{}.{}".format(package_name, convert_slash_to_dot(relativeReceiverClassPath), APK_STRING_DECODE_BROADCAST_RECEIVER_NAME),
        "--es",
        "ping",
        "ApkStringDecodeBroadcastPing"
    ]

    # Print the actual command to see what's being executed
    #print("Running command:", " ".join(command))

    # Run the command using subprocess
    result = subprocess.run(command, capture_output=True, text=True)

    # Output the result of the command
    #print("Output:", result.stdout)
    #print("Errors:", result.stderr)


def validateIfPermissionsIsRequired(task_thread, package_name, current_time):
    updateStatus(task_thread, " ----- VALDIATE PERMISSIONS ----- ")
    # Signal to pause (if needed based on some condition)
    if isPermissionRequired(package_name, current_time):
        if task_thread:
            task_thread.pause("Pause Required", "Permission is required from the app. Click Ok once the permission is given")  # Request to pause the execution
            task_thread.check_pause()  # Wait until the resume() is called
        else:
            user_input = input("Press enter once the permission is given:")
            
def isPermissionRequired(package_name, current_time):
    try:
        logcat_command = f'adb logcat -d -v time | grep "{package_name}"/.{APK_STRING_DECODE_BROADCAST_RECEIVER_NAME}'
        logcat_output = subprocess.check_output(logcat_command, shell=True, text=True)

        # Split the output into lines for processing
        logcat_lines = logcat_output.strip().split('\n')

        # Filter the logcat lines based on the timestamp
        filtered_log_lines = []
        for line in logcat_lines:
            # Extract the timestamp from the log line (assuming it starts with the timestamp in the format 'MM-DD HH:MM:SS.sss')
            try:
                matchTime = re.search(r'^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*', line)
                if matchTime:
                    log_time = matchTime.group(1)
                    # Compare with the stored time
                    if log_time > current_time:
                        if "Skipping delivery: permission review required" in line:
                            filtered_log_lines.append(line)

            except (ValueError, IndexError):
                continue  # If parsing fails, skip the line

    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            # grep did not find any matches, handle it as needed
            print("No logs matching the filter were found.")
            return False
        else:
            # An actual error occurred, re-raise the exception
            raise

    if filtered_log_lines:
        return True
    else:
        return False

def hasAllPermissionsGiven(package_name):
    #WARN: 'dumpsys' cal doesn't seem to give an accurate state of the permissions, so this method might be unreliable 
    app_permissions = extractPermissionsFromManifest()

    granted_permissions = set()
    all_permissions_granted = True

    try:
        # Getting the list of granted permissions
        result = subprocess.check_output(
            f'adb shell dumpsys package {package_name} | grep permission', 
            shell=True, text=True
        )

        # Parsing the output
        for line in result.split('\n'):
            if 'granted=true' in line:
                parts = line.split(':')
                if parts and len(parts) > 0:
                    granted_permission = parts[0].strip()
                    granted_permissions.add(granted_permission)

        # Checking if each permission is granted
        for permission in app_permissions:
            if permission not in granted_permissions:
                print(f'Permission {permission} is not granted for package {package_name}')
                all_permissions_granted = False

    except subprocess.CalledProcessError as e:
        print(f'Error occurred: {e}')
        all_permissions_granted = False

    return all_permissions_granted

def extractPermissionsFromManifest():
    permissions = []
    try:
        tree = ET.parse(Config.get_manifest_path())
        root = tree.getroot()
        for elem in root.iter():
            if elem.tag.endswith("uses-permission"):
                permission = elem.get("{http://schemas.android.com/apk/res/android}name")
                if permission:
                    permissions.append(permission)
    except Exception as e:
        print(f"Error extracting permissions from manifest: {e}")
    return permissions

def sendSplitLogToAndroid(package_name, log_data, part_number, total_parts, class_name, java_signature, relativeReceiverClassPath, subpart_number, subtotal_parts):
    command = (
        f"adb shell am broadcast -n {package_name}/{convert_slash_to_dot(relativeReceiverClassPath)}.{APK_STRING_DECODE_BROADCAST_RECEIVER_NAME} "
        f"--es hashmap '{log_data}' "
        f"--ei part_number {part_number} "
        f"--ei total_parts {total_parts} "
        f"--ei subpart_number {subpart_number} "
        f"--ei subtotal_parts {subtotal_parts} "
        f"--es class_name {encodeStringIntoBase64(class_name)} "
        #f"--es class_name {encodeStringIntoBase64(convert_dot_to_slash(class_name))} "
        f"--es method_name {encodeStringIntoBase64(triggerCallerToDecodeMethod)} "
        f"--es java_signature {encodeStringIntoBase64(java_signature)} "
        f"--ei max_entries_allowed {ANDROID_LOG_MAX_ENTRIES_ALLOWED}"
    )
    subprocess.run(command, shell=True)

    log_data_size = sys.getsizeof(log_data)  # Size in bytes
    #print(f"Size of hashmap parameter: {log_data_size} bytes")

    command_length = len(command)
    #print(f"Command length: {command_length} characters")

    time.sleep(1)  # Delay to simulate time gap between logs

def triggerBroadcastReceiverMultiple(task_thread, package_name, hash_map_original_sanitize, class_name, java_signature, relativeReceiverClassPath):
    updateStatus(task_thread, " ----- TRIGGER APP DECODE ----- ")

    #TODO: relativeReceiverClassPath NEEDS TO GET THE CORRECT VALUE
    if relativeReceiverClassPath == "":
        relativeReceiverClassPath = package_name

    total_entries = len(hash_map_original_sanitize)
    total_parts = math.ceil(total_entries / ANDROID_LOG_MAX_ENTRIES_ALLOWED)
    part_counter = 1
    part_map = {}

    for key, value in hash_map_original_sanitize.items():
        part_map[key] = value

        # Check if we reached the max entries allowed or are at the end of the original map
        if len(part_map) == ANDROID_LOG_MAX_ENTRIES_ALLOWED or key == list(hash_map_original_sanitize.keys())[-1]:
            encoded_part = encodeHashMapToBase64WithDelimiter(part_map)
            handleLargePartAndSend(package_name, encoded_part, part_counter, total_parts, class_name, java_signature, relativeReceiverClassPath)
            part_counter += 1
            part_map.clear()  # Reset for next segment

def handleLargePartAndSend(package_name, encoded_part, part_number, total_parts, class_name, java_signature, relativeReceiverClassPath):
    max_size_limit = ANDROID_BROADCAST_COMMAND_MAX_LENGTH - 500  # Buffer for other parameters
    if len(encoded_part) > max_size_limit:
        subparts = splitIntoSubparts(encoded_part, max_size_limit)
        subtotal_parts = len(subparts)
        for subpart_number, subpart in enumerate(subparts, start=1):
            sendSplitLogToAndroid(package_name, subpart, part_number, total_parts, class_name, java_signature, relativeReceiverClassPath, subpart_number, subtotal_parts)
    else:
        # If no splitting is needed, send it as a single subpart
        #sendSplitLogToAndroid(package_name, encoded_part, part_number, total_parts, class_name, java_signature, 0, 1)
        sendSplitLogToAndroid(package_name, encoded_part, part_number, total_parts, class_name, java_signature, relativeReceiverClassPath, 1, 1)


def splitIntoSubparts(data, max_size):
    return [data[i:i + max_size] for i in range(0, len(data), max_size)]

def triggerActivityMultipleRoot(task_thread, package_name, class_name, java_signature, relativeReceiverClassPath):
    updateStatus(task_thread, " ----- TRIGGER APP DECODE ACTIVITY (ROOT) ----- ")

    command = (
        f"adb shell am start -n {package_name}/{convert_slash_to_dot(relativeReceiverClassPath)}.{APK_STRING_DECODE_ACTIVITY_NAME} "
        f"--es class_name {encodeStringIntoBase64(class_name)} "
        #f"--es class_name {encodeStringIntoBase64(convert_dot_to_slash(class_name))} "
        f"--es method_name {encodeStringIntoBase64(triggerCallerToDecodeMethod)} "
        f"--es java_signature {encodeStringIntoBase64(java_signature)} "
        f"--es hashmap_read_file RANDOM_STRING "
    )
    subprocess.run(command, shell=True)

    time.sleep(1)  # Delay to simulate time gap between logs
    #time.sleep(0.1)  # A 100ms delay is negligible but provides some buffer

def prepareStringForSmali(original_str):
    """
    Prepares a given string for insertion into a Smali file by analyzing and escaping each character as needed.
    """
    result = []

    special_characters = {
        '\\': '\\\\',
        '"': '\\"',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        #'\0': '\\u0000',  # Handle null character
        '…': '\\u2026',
        '#': '\\u0023',
        '%': '\\u0025',
        '/': '\\u002F',
        ':': '\\u003A',
        '?': '\\u003F',
        '@': '\\u0040',
        '[': '\\u005B',
        ']': '\\u005D'
    }

    for char in original_str:
        if char in special_characters:
            result.append(special_characters[char])
        else:
            # Escape all non-ASCII characters and control characters using Unicode escape
            if ord(char) < 32 or ord(char) == 127 or ord(char) > 126:
                # Escape non-printable and control characters using Unicode escape
                result.append(f'\\u{ord(char):04X}')
            else:
                result.append(char)

    return ''.join(result)

def preparaStringForAndroidDecoding(smali_string):
    #adjusted_string = handleNewStringFromSmali(smali_string)

    # Unescape double quotes
    adjusted_string = smali_string.replace('\\"', '"')

    # Unescape newline and tab characters
    adjusted_string = adjusted_string.replace("\\n", "\n").replace("\\t", "\t")

    # Unescape backslashes (this should be done last to avoid double unescaping)
    adjusted_string = adjusted_string.replace("\\\\", "\\")

    # Optionally, handle any other special cases specific to your context

    return adjusted_string