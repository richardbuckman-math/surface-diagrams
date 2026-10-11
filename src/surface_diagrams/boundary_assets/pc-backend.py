"""Pyodide adapter for the puncture-capped lantern lab."""

import json
from urllib.parse import parse_qs, urlsplit

from surface_diagrams.pc_lantern_lab import PCLanternLab


lab = PCLanternLab()


def restore_browser_session(text):
    global lab
    if not text:
        return
    try:
        if len(text) > 16 * 1024 * 1024:
            raise ValueError('Saved workspace exceeds 16 MiB')
        lab.restore(json.loads(text))
    except (ValueError, TypeError, IndexError, KeyError, OverflowError) as error:
        lab = PCLanternLab()
        lab.message = 'Could not reopen saved work: ' + str(error) + '; started a new PC lantern project.'


def dispatch(path, method, body):
    try:
        parsed = urlsplit(path)
        route = parsed.path
        if method == 'GET' and route == '/api/state':
            result = lab.state()
        elif method == 'POST' and route == '/api/action':
            payload = json.loads(body)
            lab.mutate(payload)
            return json.dumps({'status': 200, 'body': json.dumps(lab.state()),
                               'session': lab.session_document(), 'mime': 'application/json'})
        elif method == 'GET' and route == '/api/export.svg':
            query = parse_qs(parsed.query)
            if (query.get('compact',['0'])[0] not in ('0','1') or
                    query.get('mirror',['1'])[0] not in ('0','1')):
                raise ValueError('Invalid display option')
            return json.dumps({'status': 200, 'body': lab.export_svg(
                compact=query.get('compact',['0'])[0]=='1',
                mirror_vertical=query.get('mirror',['1'])[0]=='1'),
                               'mime': 'image/svg+xml'})
        else:
            return json.dumps({'status': 404, 'body': json.dumps({'error': 'Not found'}),
                               'mime': 'application/json'})
        return json.dumps({'status': 200, 'body': json.dumps(result),
                           'mime': 'application/json'})
    except (ValueError, TypeError, IndexError, KeyError, OverflowError) as error:
        return json.dumps({'status': 400, 'body': json.dumps({'error': str(error)}),
                           'mime': 'application/json'})
