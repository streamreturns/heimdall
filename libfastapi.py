import os, json, io, hashlib


def get_stage_identifier(verbose=False):
    if os.path.exists('config/stage_identifier'):
        with open('config/stage_identifier', 'r') as fin:
            if verbose:
                print('[LOAD] `{}`'.format(os.path.abspath('config/stage_identifier')))
            return fin.readline().strip()

    print('[ERROR] No stage identifier found (expected: `{}`)'.format(os.path.join(os.path.abspath('.'), 'config/stage_identifier')))

    return None


def get_stage_configuration(stage_identifier, verbose=True):
    assert stage_identifier is not None
    stage_identifier = str(stage_identifier)

    if verbose:
        print('[INFORMATION] Use stage identifier \'{}\''.format(stage_identifier))

    assert len(stage_identifier) > 0

    if os.path.exists('config/stage_configurations.json'):
        with open('config/stage_configurations.json', 'r', encoding='UTF-8') as fin:
            stage_configurations = json.loads(fin.read())

            for stage_configuration in stage_configurations:
                if stage_configuration['stage'] == stage_identifier:
                    if verbose:
                        print('[INFORMATION] Load stage configuration \'{}\''.format(stage_configuration))

                    return stage_configuration

        print('[ERROR] No \'{}\' stage configuration found'.format(stage_identifier))

    print('[ERROR] No stage configurations found (expected: `{}`)'.format(os.path.join(os.path.abspath('.'), 'config/stage_configurations.json')))

    return None


def get_stage_values(key):
    site_identifier = get_stage_identifier(verbose=False)
    stage_configuration = get_stage_configuration(site_identifier, verbose=False)

    if key in stage_configuration:
        return stage_configuration[key]

    print('[ERROR] `get_stage_values()` | No `key`=\'{}\' found'.format(key))

    return None


def generate_digest(string, method='SHA-256'):
    if method == 'SHA-256':
        with io.StringIO(string) as fin:
            sha256 = hashlib.sha256()
            while True:
                data = fin.read(65536)  # buffer size
                if not data:
                    break
                sha256.update(data.encode('ascii'))
            digest = sha256.hexdigest()

            return digest

    return None
