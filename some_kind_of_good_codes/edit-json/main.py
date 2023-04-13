import json

with open('/home/inosens/Desktop/prevla_sensors/DCA1000EVM_CLI_ROS/SourceCode-20230305T092254Z-001/SourceCode/last_Release/configFile.json','r') as f:
    json_object = json.loads(f.read())
print(json_object['DCA1000Config']['captureConfig']['filePrefix'])
json_object['DCA1000Config']['captureConfig']['filePrefix'] = "burak"
json_object['DCA1000Config']['captureConfig']['durationToCapture_ms'] = 10
print(json_object['DCA1000Config']['captureConfig']['filePrefix'])
print(json_object['DCA1000Config']['captureConfig']['durationToCapture_ms'])


with open('/home/inosens/Desktop/prevla_sensors/DCA1000EVM_CLI_ROS/SourceCode-20230305T092254Z-001/SourceCode/last_Release/configFile.json','w') as f:
    f.write(json.dumps(json_object, ensure_ascii=False))