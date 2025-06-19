import subprocess
import os
from core_logic.apk_string_decode_consts import smali_type_mapping_with_registers, STRINGS_HANDLING_PROCESS_METHOD_ROOT, STRINGS_HANDLING_PROCESS_METHOD_RECEIVERLOGCAT, STRINGS_HANDLING_PROCESS_METHOD_DEFAULT

def updateStatus(thread, update_message):
    print(update_message)
    if thread:
        thread.updateText.emit(update_message)

def get_smali_type(java_type):
    """Convert Java type to corresponding Smali type, handling arrays."""
    array_depth = java_type.count('[]')
    base_type = java_type.replace('[]', '')

    if base_type in smali_type_mapping_with_registers:
        smali_base_type, _ = smali_type_mapping_with_registers[base_type]
        smali_type = '[' * array_depth + smali_base_type  # Add array brackets if needed
        return smali_type
    
    print(f"Unknown type: {java_type}")
    return None

def resolve_register_count(java_type):
    """Determine the register count for a given Java type, including arrays."""
    array_depth = java_type.count('[]')
    base_type = java_type.replace('[]', '')

    if base_type in smali_type_mapping_with_registers:
        _, base_register_count = smali_type_mapping_with_registers[base_type]
        # Arrays use the same register count as their base type
        return base_register_count
    else:
        raise ValueError(f"Unknown type: {java_type}")


def generate_smali_signature_from_java_signature(java_signature):
    """Generate Smali signature from Java-style method signature."""
    # Strip outer parentheses and split the parameters by comma
    param_types = java_signature.strip("()").split(',')
    
    # Generate Smali type codes for the parameters
    smali_signature = ''.join(
        get_smali_type(param_type.strip()) for param_type in param_types if param_type.strip()
    )
    
    return smali_signature

def is_device_rooted():
    try:
        result = subprocess.run(["adb", "shell", "which su"], capture_output=True, text=True)
        return bool(result.stdout.strip())  # If su path is returned, device is rooted
    except Exception as e:
        print(f"Error: {e}")
        return False
    #to try:
    #    su_check = subprocess.run(["adb", "shell", "which su"], capture_output=True, text=True).stdout.strip()
    #    su_exec = subprocess.run(["adb", "shell", "su -c 'echo rooted'"], capture_output=True, text=True).stdout.strip()
    #    file_check = subprocess.run(["adb", "shell", "[ -f /system/xbin/su ] || [ -f /system/bin/su ] && echo rooted"], capture_output=True, text=True).stdout.strip()
    #    build_check = subprocess.run(["adb", "shell", "getprop ro.build.tags"], capture_output=True, text=True).stdout.strip()

    #    return any([
    #        bool(su_check), 
    #        "rooted" in su_exec, 
    #        "rooted" in file_check, 
    #        "test-keys" in build_check
    #    ])
    #except Exception as e:
    #    print(f"Error: {e}")
    #    return False


def isStringsHandlingProcessMethodRoot(strings_handling_process_method):
    if strings_handling_process_method == STRINGS_HANDLING_PROCESS_METHOD_ROOT:
        return True
    if strings_handling_process_method == STRINGS_HANDLING_PROCESS_METHOD_RECEIVERLOGCAT:
        return False
    
    if strings_handling_process_method == STRINGS_HANDLING_PROCESS_METHOD_DEFAULT and is_device_rooted():
        return True
    else:
        return True
    

def fileExistsCaseSensitive(path):
    if not os.path.exists(path):
        return False

    # Split into components
    parts = os.path.normpath(path).split(os.sep)
    current_path = parts[0] if os.path.isabs(path) else "."

    for part in parts[1:] if os.path.isabs(path) else parts:
        try:
            entries = os.listdir(current_path)
        except FileNotFoundError:
            return False

        if part not in entries:
            return False

        current_path = os.path.join(current_path, part)

    return os.path.isfile(current_path)    