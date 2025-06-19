# Apk String Decode

> A semi-static approach to decode obfuscated / encrypted Strings.

## 📦 Features

- Provide an apk path, 
## 🚀 Getting Started

### Prerequisites

- TODO

### Installation

```bash
# Clone the repository
git clone https://github.com/slyzerui/apk_string_decode.git

# Go into the project folder
cd apk_string_decode

# TODO Set up environment / install dependencies


```
---

## 🧪 Usage
python main.py  --path <apk_path> --java_signature <java_signature>

## 📘 Examples
python main.py  --path "/Users/slyzerui/Downloads/my_app.apk" --java_signature "com.my.app.c("RkB9ZkNWQ2BDUUc=")"

python main.py  --path "/Users/slyzerui/Downloads/my_other_app.apk" --java_signature "com.my.app.decodemethod(byte[], byte[])" -m true -c true


### Parameters
'-p', '--path', type=str, required=False, help='The file system path to be processed.'

'-s', '--java_signature', type=str, required=False, help='The Java signature to be processed.'

'-m', '--multi_processing', type=str, choices=['true', 'false'], required=False, help='If the processing should use a multiple cores. Accepts true or false.'

'-r', '--file_rollback', type=str, choices=['true', 'false'], required=False, help='If the app should roll back to the original file in case of a bad compilation'

'--gui', action='store_true', help='Enable GUI mode.' #Not working properly yet

'-c', '--complex_flow', type=str, choices=['true', 'false'], required=False, help='If the app should do a deep complex analyse on every class'

'-v', '--clean_static_variables', type=str, choices=['true', 'false'], required=False, help='If the app should clean the static references variables being used on the decode process'

'-g', '--single_class_analysis', type=str, required=False, help='If provided, will only decode the app with the passed class paths'

'-e', '--strings_handling_process_method', type=int, choices=[0, 1, 2], required=False, help='0 - Will pass Strings using the most optimzed process; 1 - Will pass Strings using local storage (Requires ROOT); 2 - Will Pass Strings using a Broadcast Receiver and logcat'



