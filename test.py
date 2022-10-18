from geon_services_core.runtime_config import RuntimeConfig
from geon_services_core.permissions_reader import PermissionsReader
from flask import json, safe_join

from flask import Flask, Request as RequestBase, request, jsonify, send_file
from flask_restx import Api, Resource, fields, reqparse
import requests
import json
tenant = 'default'
app = Flask(__name__)
logger = app.logger

"""pr = PermissionsReader(tenant, logger)
resource_key = 'data_datasets'
identity = 'burak'
resource_name = "idarisinir"
print(pr.resource_permissions(resource_key, identity, resource_name))
print("************************************")
resource_key = 'wms_services'
identity = 'burak'
print(pr.resource_permissions(resource_key, identity))
print("************************************")
resource_key = 'background_layers'
identity = 'burak'
print(pr.resource_permissions(resource_key, identity))
print("end")"""


"""url = "http://localhost:3000/rpc/gn_get_config"

payload = json.dumps({
  "inp": "mapViewerConfig"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
response = json.loads(response.text)"""
        
config_handler = RuntimeConfig("mapViewer", logger)
config = config_handler.tenant_config(tenant)

permissions_handler = PermissionsReader(tenant, logger)


print("--------------------------------------------")
print(config.get('auth_service_url'))
print("--------------------------------------------")
print(permissions_handler)

