"""Local interactive (6,7) factorization prototype. Run with --no-browser."""
import argparse
from dataclasses import asdict
from http.server import ThreadingHTTPServer
from importlib import resources
import json
import secrets
import threading
import webbrowser
from .editor import EditorHandler
from .factorization_explorer import initial_factors,move_factor,split_factor,combine_factors,export_factors,import_factors
from .factorization_geometry import support_svg,braid_svg,row_height


class LabServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,port=0):
        super().__init__(('127.0.0.1',port),LabHandler)
        self.token=secrets.token_urlsafe(32)
        self.allowed_hosts={f'127.0.0.1:{self.server_port}',f'localhost:{self.server_port}'}
        self.lock=threading.Lock()
        self.history=[initial_factors()]; self.position=0; self.revision=0
        self.message='Loaded 13 factors / 178 braid letters from the earlier SVG.'
    @property
    def url(self): return f'http://127.0.0.1:{self.server_port}'
    def state(self):
        factors=self.history[self.position]
        rows=[]
        for f in factors:
            try: svg=support_svg(f); warning=''
            except ValueError as error: svg=''; warning=str(error)
            options=[]
            if f.power>1: options.append(['powers',f'Split into {f.power} equal factors'])
            if not f.half and f.points==2: options.append(['halves','Split into half twists'])
            if not f.half and f.points==3: options.append(['lantern','Lantern: three pairwise twists (marked points)'])
            rows.append(dict(asdict(f),word=f.word,label=f.label,svg=svg,warning=warning,
                             height=row_height(f),splits=options))
        return dict(token=self.token,revision=self.revision,factors=rows,braid=braid_svg(factors),
                    undo=self.position>0,redo=self.position<len(self.history)-1,message=self.message,
                    export=export_factors(factors))
    def mutate(self,payload):
        if payload.get('revision')!=self.revision: raise ValueError('State changed; reload before editing')
        op=payload.get('op'); factors=self.history[self.position]
        if op=='undo':
            if self.position==0: raise ValueError('Nothing to undo')
            self.position-=1; self.message='Undid the previous operation.'
        elif op=='redo':
            if self.position==len(self.history)-1: raise ValueError('Nothing to redo')
            self.position+=1; self.message='Redid the operation.'
        else:
            i=payload.get('index')
            if op not in ('reset','import') and (type(i) is not int or not 0<=i<len(factors)):
                raise ValueError('Choose a valid factor')
            if op=='move':
                result=move_factor(factors,i,payload.get('target'))
                message=f'Moved {factors[i].id}; crossed factors conjugated. Every adjacent move passed exact disk-action checks.'
            elif op=='split':
                result=split_factor(factors,i,payload.get('kind'))
                message=f'Split {factors[i].id}; replacement passed exact disk-action verification.'
            elif op=='combine':
                result=combine_factors(factors,i)
                message='Combined adjacent powers; exact disk action verified.'
            elif op=='reset': result=initial_factors(); message='Restored original factorization. Undo is available.'
            elif op=='import': result=import_factors(payload.get('document')); message='Loaded saved exploration; exact product agrees with the starting factorization.'
            else: raise ValueError('Unknown operation')
            self.history=self.history[:self.position+1]+[result]
            if len(self.history)>60: self.history=self.history[-60:]
            self.position=len(self.history)-1; self.message=message
        self.revision+=1


class LabHandler(EditorHandler):
    def do_GET(self):
        if not self._local_request(): return
        if self.path=='/api/state':
            with self.server.lock: data=self.server.state()
            self._reply(200,json.dumps(data)); return
        assets={'/':('index.html','text/html; charset=utf-8'),
                '/lab.js':('lab.js','text/javascript; charset=utf-8'),
                '/lab.css':('lab.css','text/css; charset=utf-8')}
        if self.path not in assets: self._error(404,'Not found'); return
        name,mime=assets[self.path]
        self._reply(200,resources.files('surface_diagrams').joinpath('lab_assets',name).read_bytes(),mime)
    def do_POST(self):
        if not self._local_request(): return
        if not secrets.compare_digest(self.headers.get('X-Surface-Token','').encode('utf-8'),self.server.token.encode('ascii')):
            self._error(403,'Open the lab first'); return
        if self.path!='/api/action': self._error(404,'Not found'); return
        try:
            if self.headers.get('Transfer-Encoding') or self.headers.get('Content-Type','').split(';')[0]!='application/json':
                raise ValueError('Use a bounded JSON request')
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=262144: raise ValueError('Request is too large (maximum 256 KiB)')
            self.connection.settimeout(10)
            payload=json.loads(self.rfile.read(size))
            if not isinstance(payload,dict): raise ValueError('Expected an operation object')
            with self.server.lock:
                self.server.mutate(payload); data=self.server.state()
            self._reply(200,json.dumps(data))
        except (ValueError,TypeError,IndexError,OverflowError) as error:
            self._error(400,str(error))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=0)
    parser.add_argument('--no-browser',action='store_true')
    args=parser.parse_args(argv)
    if not 0<=args.port<=65535: parser.error('port must be between 0 and 65535')
    server=LabServer(args.port)
    print(server.url,flush=True)
    if not args.no_browser: webbrowser.open(server.url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__=='__main__': main()
