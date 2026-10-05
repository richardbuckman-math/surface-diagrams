"""Pyodide adapter for the exact boundary-twist playground."""

import json
from urllib.parse import urlsplit

from surface_diagrams.boundary_playground_app import BoundaryLab


lab = BoundaryLab()


def restore_browser_session(text):
    if not text:
        return
    try:
        if len(text) > 16*1024*1024:
            raise ValueError('Saved workspace exceeds 16 MiB')
        lab.restore(json.loads(text))
    except (ValueError, TypeError, IndexError, KeyError, OverflowError) as error:
        lab.message = 'Could not reopen saved work: '+str(error)+'; started a new project.'


def dispatch(path, method, body):
    try:
        route = urlsplit(path).path
        if method == 'GET' and route == '/api/state':
            result = lab.state()
        elif method == 'POST' and route == '/api/action':
            payload = json.loads(body)
            lab.mutate(payload)
            return json.dumps({'status':200,'body':json.dumps(lab.state()),
                               'session':lab.session_document(),'mime':'application/json'})
        elif method == 'GET' and route == '/api/export.svg':
            return json.dumps({'status':200,'body':lab.export_svg(),
                               'mime':'image/svg+xml'})
        else:
            return json.dumps({'status':404,'body':json.dumps({'error':'Not found'}),
                               'mime':'application/json'})
        return json.dumps({'status':200,'body':json.dumps(result),
                           'mime':'application/json'})
    except (ValueError, TypeError, IndexError, KeyError, OverflowError) as error:
        return json.dumps({'status':400,'body':json.dumps({'error':str(error)}),
                           'mime':'application/json'})
