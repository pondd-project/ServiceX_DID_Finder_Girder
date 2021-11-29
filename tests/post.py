import requests
import json
import sys

servicex_port = sys.argv[1]
json_file = sys.argv[2]
payload = json.load(open(json_file))

r = requests.post('http://localhost:{port}/servicex/transformation'.format(port=port), data = payload)

print(r.json())
