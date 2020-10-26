import os, requests, libfastapi
from flask import Flask, json, request
from flask_cors import CORS

heimdall = Flask(__name__)

# set CORS origins
heimdall.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(heimdall, resources={r'/*': {'origins': '*'}})

# set max content length
heimdall.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024


def get_api_scheme_host_port_path_by_api_name(api_name):
    if os.path.exists('config/api_definitions.json'):
        with open('config/api_definitions.json', 'r', encoding='UTF-8') as fin:
            api_definitions = json.loads(fin.read())

            for api_definition in api_definitions:
                if 'api_name' in api_definition:
                    if api_name == api_definition['api_name']:
                        # retrieve `api_scheme`
                        if 'api_scheme' in api_definition:
                            api_scheme = api_definition['api_scheme']
                        else:
                            api_scheme = ''

                        # retrieve `api_host`
                        if 'api_host' in api_definition:
                            api_host = api_definition['api_host']
                        else:
                            api_host = ''

                        # retrieve `api_port`
                        if 'api_port' in api_definition:
                            api_port = api_definition['api_port']
                        else:
                            api_port = ''

                        # retrieve `api_path`
                        if 'api_path' in api_definition:
                            api_path = api_definition['api_path']
                        else:
                            api_path = ''

                        return {
                            'api_scheme': api_scheme,
                            'api_host': api_host,
                            'api_port': api_port,
                            'api_path': api_path
                        }

            print('[ERROR] `get_api_scheme_host_port_path_by_api_name()` | No `api_name`=\'{}\' found'.format(api_name))

    return None


@heimdall.route('/bifrost', methods=['POST'])
def bifrost():
    print('POST `sentiment()`')
    if request.method == 'POST':
        # print('[POST]', request.values)

        if 'api_name' in request.values:
            api_name = request.values['api_name']
        else:
            api_name = None

        api_scheme_host_port_path = get_api_scheme_host_port_path_by_api_name(api_name)
        if api_scheme_host_port_path:
            api_scheme = api_scheme_host_port_path['api_scheme']
            api_host = api_scheme_host_port_path['api_host']
            api_port = api_scheme_host_port_path['api_port']
            api_path = api_scheme_host_port_path['api_path']

            api_data = dict()
            for key in request.values:
                if key not in ['api_name', 'token']:
                    api_data[key] = request.values[key]

            r = requests.post('{api_scheme}://{api_host}:{api_port}/{api_path}'.format(api_scheme=api_scheme, api_host=api_host, api_port=api_port, api_path=api_path),
                              data=api_data
                              )

            response = heimdall.response_class(
                response=json.dumps(r.json()),
                status=200,
                mimetype='application/json'
            )
        else:
            response = heimdall.response_class(
                status=418
            )

        response.headers['Access-Control-Allow-Origin'] = '*'

        return response


if __name__ == '__main__':
    heimdall_port = libfastapi.get_stage_values('api')['port']
    heimdall.run(host='0.0.0.0', port=int(heimdall_port), debug=False)
