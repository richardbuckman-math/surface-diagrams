"""Browser-only adapter for the same exact lab engine used by the local app."""
import json
from urllib.parse import parse_qs, urlsplit

from surface_diagrams.factorization_lab import LabServer, starting_factors, validated_session_document
from surface_diagrams.factorization_geometry import factorization_svg


lab = LabServer.__new__(LabServer)
lab.session_path = None
lab.token = 'browser-only'


def select_lab_seed(seed_slug='6-7'):
    """Bind this worker to one exact starting product before restoring storage."""
    lab.seed_factors = starting_factors(seed_slug)
    lab.seed_slug = seed_slug
    lab.history = [lab.seed_factors]
    lab.frames = [()]
    lab.operations = ['Original factorization']
    lab.position = 0
    lab.revision = 0
    lab.message = 'Loaded the original factorization in this browser.'
    lab.verification_notice = ''


select_lab_seed()


def restore_browser_session(text):
    """Reopen only a valid saved workspace; never overwrite a fresh lab on error."""
    if not text:
        return
    try:
        if len(text) > 16*1024*1024:
            raise ValueError('Saved browser workspace exceeds 16 MiB')
        history,frames,operations,position,limited=validated_session_document(json.loads(text),lab.seed_slug)
    except (ValueError,TypeError,IndexError,KeyError,OverflowError) as error:
        lab.message='Could not reopen the browser workspace: '+str(error)+'; loaded the original factorization.'
        return
    lab.history=history
    lab.frames=frames
    lab.operations=operations
    lab.position=position
    lab.message='Reopened saved browser exploration and undo history.'
    if limited:
        lab.verification_notice=('Saved history states '+', '.join(map(str,limited))+
            ' reached the exact verification limit on reopening. Their product equality is not reverified; history is preserved.')


def dispatch(path, method, body):
    """Return an HTTP-shaped response without any network or server writes."""
    try:
        route = urlsplit(path)
        query = parse_qs(route.query)
        if method == 'GET' and route.path == '/api/state':
            result = lab.state()
        elif method == 'POST' and route.path == '/api/action':
            payload = json.loads(body)
            if not isinstance(payload, dict):
                raise ValueError('Expected an operation object')
            lab.mutate(payload)
            result = lab.state()
            return json.dumps(dict(status=200, body=json.dumps(result),
                                   session=lab.session_document(), mime='application/json'))
        elif method == 'GET' and route.path == '/api/prefix':
            if int(query['revision'][0]) != lab.revision:
                raise ValueError('State changed; reopen this inspector')
            result = lab.prefix_action(int(query['index'][0]),query.get('system',['fan'])[0])
        elif method == 'GET' and route.path == '/api/prefix-arc':
            if int(query['revision'][0]) != lab.revision:
                raise ValueError('State changed; reopen this inspector')
            result = lab.prefix_arc(int(query['index'][0]),query['side'][0],int(query['arc'][0]),
                                    query.get('system',['fan'])[0])
        elif method == 'GET' and route.path == '/api/sphere':
            if int(query['revision'][0]) != lab.revision:
                raise ValueError('State changed; reopen this check')
            result = lab.sphere_action()
        elif method == 'GET' and route.path == '/api/export.svg':
            if int(query['revision'][0]) != lab.revision:
                raise ValueError('State changed; reload before exporting')
            return json.dumps(dict(status=200, body=factorization_svg(lab.history[lab.position]),
                                   mime='image/svg+xml'))
        else:
            return json.dumps(dict(status=404, body=json.dumps({'error': 'Not found'}),
                                   mime='application/json'))
        return json.dumps(dict(status=200, body=json.dumps(result), mime='application/json'))
    except (ValueError, TypeError, IndexError, KeyError, OverflowError) as error:
        return json.dumps(dict(status=400, body=json.dumps({'error': str(error)}),
                               mime='application/json'))
