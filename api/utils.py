import configparser
import json
import requests
import os


def read_config():
    config_parser = configparser.RawConfigParser()
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config', 'test.config')
    config_parser.read(config_file_path)
    return config_parser


configParser = read_config()

PIPEDRIVE_API_TOKEN = configParser.get('api-config', 'pipedrive_api_token')
app_path = configParser.get('api-config', 'path')

defaultParams = {
    'restrict_internal_cache': 'true',
    'api_token': PIPEDRIVE_API_TOKEN
}


def do_request(method, endpoint, params={}, data=None, headers={}):
    params = dict(defaultParams.items() | params.items())

    path = app_path + endpoint

    if data:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data)
    r = requests.request(method, path, params=params, data=data, headers=headers)
    r.encoding = 'utf-8'

    try:
        r.json = r.json()
        # print(json.dumps(r.json, indent=4))
    except:
        pass

    return r
