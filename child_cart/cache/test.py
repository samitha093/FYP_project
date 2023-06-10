import json

data = [['1', '9001', '128.1.23'], ['2', '9001', '128.1.23']]

# Convert the list to a list of dictionaries
result = [{'index': item[0], 'port': item[1], 'ip': item[2]} for item in data]

# Convert the list of dictionaries to a JSON object
json_object = json.dumps(result)

print(json_object)
