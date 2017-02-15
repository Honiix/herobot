import base64
import json

splitter = "Fe12NAfA3R6z4k0z"

with open('savegame.txt', 'r') as sg:
    raw = sg.read()

save = raw.split(splitter)[0]

save_json_base64 = ''.join([char for char in save[::2]])
save_json = base64.b64decode(save_json_base64)

print(json.dumps(json.loads(save_json), sort_keys=True, indent=4))
