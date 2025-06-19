from datetime import datetime
import base64
import json

def registersCurrentTime():
    return datetime.now().strftime("%m-%d %H:%M:%S")  

def encodeStringIntoBase64(input_string):
    byte_string = input_string.encode('utf-8')
    base64_encoded = base64.b64encode(byte_string)
    base64_string = base64_encoded.decode('utf-8')
    return base64_string   

def decodeBase64IntoString(input_string):
    decoded_bytes = base64.b64decode(input_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def convert_dot_to_slash(input_string):
    return input_string.replace('.', '/')

def convert_slash_to_dot(input_string):
    return input_string.replace('/', '.')

def encodeHashMapToBase64(hash_map):
    json_string = json.dumps(hash_map)
    return base64.b64encode(json_string.encode()).decode()

def encodeHashMapToBase64WithDelimiter(hash_map):
    json_data = json.dumps(hash_map)
    return base64.b64encode(json_data.encode('utf-8')).decode('utf-8')

def decode_base64_to_hashmap(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return json.loads(decoded_string)