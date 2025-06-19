from pathlib import Path
import re

INTERFACE_CLI = 0
INTERFACE_GUI = 1

STRINGS_HANDLING_PROCESS_METHOD_DEFAULT = 0
STRINGS_HANDLING_PROCESS_METHOD_ROOT = 1
STRINGS_HANDLING_PROCESS_METHOD_RECEIVERLOGCAT = 2

#Static variables
path_to_download_folder_path = Path.home() / "Downloads"
path_to_download_folder = str(path_to_download_folder_path) + "/"

path_to_extracted_folder = path_to_download_folder + "apk_extracted/"
manifest_path = path_to_extracted_folder + "AndroidManifest.xml"
path_extracted_smali_folder = path_to_extracted_folder + "smali/"
extracted_apk = path_to_download_folder + "modified_extract_app.apk"
decoded_apk = path_to_download_folder + "decoded_app.apk"

missing_strings_path = path_to_download_folder + "missing_strings.json"

path_to_backup = path_to_download_folder + "apk_extracted_backup/"

manifest_backup_path = path_to_backup + "AndroidManifest.xml"

res_directory_path = path_to_extracted_folder + "res/"
public_xml_file_path = res_directory_path + "values/public.xml"

triggerCallerToDecodeMethod = "getTriggerDecodedValue"

android_log_tag_to_search = "DecodeClassLargeLog"

APK_STRING_DECODE_BROADCAST_RECEIVER_NAME = "ApkStringDecodeBroadcastReceiver"
APK_STRING_DECODE_ACTIVITY_NAME = "ApkStringDecodeActivity"
APK_STRING_DECODE_SERVICE_NAME = "ApkStringDecodeService"
APK_STRING_DECODE_RUNNABLE_NAME = "ApkStringDecodeRunnable"
APK_STRING_DECODE_COMMON_NAME = "ApkStringDecodeCommon"

STRING_DECODED_ERROR = "DecodeClass_DecodingError_1"

JAVA_SIGNATURE_STRING = '(String)'
JAVA_SIGNATURE_STRING_STRING = '(String,String)'

DECODED_FOLDER_ESSENCIAL_FILES = ['AndroidManifest.xml', 'public.xml']

INSTANCES_TO_DECODE_FILE = "apk_string_decode_instances.txt"
RESULTS_DECODED_RESULTS_FILE = "apk_string_decode_results.txt"


BEHAVIOR_STATUS_TASK_FLAG_FILE = "apk_string_behavior_status.txt"
BEHAVIOR_STATUS_TRUE = "True"
BEHAVIOR_STATUS_FALSE = "False"
BEHAVIOR_STATUS_TASK_TIMEOUT_SECONDS=30


DEVICE_TMP_DECODE_FILE_PATH = "/data/local/tmp/" + INSTANCES_TO_DECODE_FILE


# Dictonary mapping Java types to smali representations and registers weight
smali_type_mapping_with_registers = {
    'void': ('V', 0),
    'boolean': ('Z', 1),
    'byte': ('B', 1),
    'char': ('C', 1),
    'short': ('S', 1),
    'int': ('I', 1),
    'long': ('J', 2),
    'float': ('F', 1),
    'double': ('D', 2),
    'Boolean': ('Ljava/lang/Boolean;', 1),
    'Byte': ('Ljava/lang/Byte;', 1),
    'Character': ('Ljava/lang/Character;', 1),
    'Short': ('Ljava/lang/Short;', 1),
    'Integer': ('Ljava/lang/Integer;', 1),
    'Long': ('Ljava/lang/Long;', 1),
    'Float': ('Ljava/lang/Float;', 1),
    'Double': ('Ljava/lang/Double;', 1),
    'String': ('Ljava/lang/String;', 1),
    'Object': ('Ljava/lang/Object;', 1),
    'Class': ('Ljava/lang/Class;', 1),
    'Throwable': ('Ljava/lang/Throwable;', 1),
    'Exception': ('Ljava/lang/Exception;', 1),
    'List': ('Ljava/util/List;', 1),
    'ArrayList': ('Ljava/util/ArrayList;', 1),
    'LinkedList': ('Ljava/util/LinkedList;', 1),
    'Map': ('Ljava/util/Map;', 1),
    'HashMap': ('Ljava/util/HashMap;', 1),
    'Set': ('Ljava/util/Set;', 1),
    'HashSet': ('Ljava/util/HashSet;', 1),
    'LinkedHashSet': ('Ljava/util/LinkedHashSet;', 1),
    'Date': ('Ljava/util/Date;', 1),
    'File': ('Ljava/io/File;', 1),
    'InputStream': ('Ljava/io/InputStream;', 1),
    'OutputStream': ('Ljava/io/OutputStream;', 1),
    'Runnable': ('Ljava/lang/Runnable;', 1)
}

PARAMETER_TYPE_TAKING_2_REGISTERS = ['long', 'double']

METHOD_BEGIN_PUBLIC_PATTERN_REGEX_COMPILED = re.compile(r'\.method\s+public')
END_CLASS_PATTERN_REGEX_COMPILED = re.compile(r'\.class\s+')
METHOD_END_PATTERN_REGEX_COMPILED = re.compile(r'\.method|\.end')
MOVE_RESULT_OBJECT_PATTERN_REGEX_COMPILED = re.compile(r'\s*move-result-object\s+(\w+\d+)')
NON_EXECUTABLE_PATTERN_COMPILED = re.compile(r'\s*\.line|\s*\.prologue|\s*\.local|\s*\.end local|\s*\.restart local|\s*#')





#ANDROID_LOG_MAX_ENTRIES_ALLOWED = 100
ANDROID_LOG_MAX_ENTRIES_ALLOWED = 50
#ANDROID_LOG_MAX_ENTRIES_ALLOWED = 30

ANDROID_BROADCAST_COMMAND_MAX_LENGTH = 50000  # or 60000 for a slightly larger limit as 65500 was bellow the testes limit



apksigner_installation = """

                                             
 - How to make apksigner work - 

Installs Android SDK Tools.

> open -e ~/.zshrc

Copy / Paste path from android built tools and save (adjust your user name and version):
export PATH="$PATH:/Users/<yourusername>/Library/Android/sdk/build-tools/<version>/"

> source ~/.zshrc

------------------------------------------------------------------------------------------------                                             

> open -e ~/.bash_profile

Copy / Paste path from android build tools and save (adjust your user name and version):
export PATH="$PATH:/Users/<yourusername>/Library/Android/sdk/build-tools/<version>/"

> source ~/.bash_profile
"""


#Keystore credentials
keystore_credentials_name_base = "apkstringdecode_"
keystore_name = keystore_credentials_name_base + 'keystore.keystore'
key_alias = keystore_credentials_name_base + 'key_alias'
keystore_password = keystore_credentials_name_base + 'keystore_password'
first_name = keystore_credentials_name_base + 'firstname'
last_name = keystore_credentials_name_base + 'lastname'