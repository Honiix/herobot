import base64
import json
import pyperclip

raw = pyperclip.paste()
splitter = "Fe12NAfA3R6z4k0z"
save = raw.split(splitter)[0]

save_json_base64 = ''.join([char for char in save[::2]])
save_json = base64.b64decode(save_json_base64).decode('UTF-8')

print(json.dumps(json.loads(save_json), sort_keys=True, indent=4))
