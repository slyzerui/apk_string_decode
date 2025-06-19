from core_logic.apk_string_decode_consts import path_extracted_smali_folder
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
import base64
import time
from copy import deepcopy
import io
import shutil
import math
import shutil


def class_to_filepath(class_name):
    """
    Convert a Smali class name (e.g., Lcom/something/encrypt/StringPool;)
    to its corresponding file path in the smali directory.
    """
    class_path = class_name[1:].replace('/', os.sep) + ".smali"
    return os.path.join(path_extracted_smali_folder, class_path)

def find_const_string_in_class(class_file, class_name, field_name):
    """
    Search the specified Smali class file for the sput-object and corresponding const-string.
    """

    #class_name = "Lcom/something/encrypt/StringPool"
    #field_name = "wYzfgיʿˑˉᵔٴᵢʿʾʻٴʿˏˈˏʾˈᴵٴᵢـˋˑʽˆـᵔᵔˈٴBZxee"

    # Correct pattern for matching sput-object followed by const-string
    pattern = rf'sput-object v\d+, {re.escape(class_name)};->{re.escape(field_name)}:Ljava/lang/String;\s*const-string v\d+, "(.*?)"'
    
    with open(class_file, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(pattern, content, re.DOTALL)  # re.DOTALL ensures newlines are handled correctly
        if match:
            return match.group(1)  # Return the captured string value
    return None


def replace_sget_with_const(content):
    """
    Process the given Smali file content to replace sget-object instructions with const-string values where applicable.
    """
    # Find all occurrences of sget-object with a static field
    sget_pattern = r"sget-object (v\d+), (L[^;]+);->([^\s]+):Ljava/lang/String;"
    matches = re.finditer(sget_pattern, content)
    
    for match in matches:
        register = match.group(1)  # v2, etc.
        class_name = match.group(2)  # Lcom/something/encrypt/StringPool
        field_name = match.group(3)  # waJsvʼˆ...

        # Convert class name to a file path
        class_file = class_to_filepath(class_name)

        # Find the const-string value in the class file
        if os.path.exists(class_file):
            const_value = find_const_string_in_class(class_file, class_name, field_name)
            if const_value:
                # Replace sget-object with const-string
                replacement = f'const-string {register}, "{const_value}"'
                content = content.replace(match.group(0), replacement)
    
    return content  # Return the modified content