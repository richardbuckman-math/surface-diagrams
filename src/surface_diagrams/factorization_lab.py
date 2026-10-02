"""Local interactive (6,7) factorization prototype. Run with --no-browser."""
import argparse
from dataclasses import asdict
from http.server import ThreadingHTTPServer
from importlib import resources
import json
import os
from pathlib import Path
import secrets
import tempfile
import threading
import webbrowser
from urllib.parse import parse_qs,urlsplit
from .editor import EditorHandler
from .factorization_explorer import initial_factors,move_factor,split_factor,combine_factors,export_factors,import_factors,simplify_factor,checked,product
from .braid_actions import free_homotopy_key
from .factorization_geometry import support_svg,braid_svg,row_height,factorization_svg
from .factorization_audit import support_audit
from .factorization_explorer import parse_factors
from .mapping_classes import VerificationLimitError,exact_action
from .sphere_actions import sphere_inner_certificate


class LabServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,port=0,session_path=None):
        self.session_path=Path(session_path).expanduser().resolve() if session_path else None
        history=[initial_factors()]; position=0; limited=[]
        if self.session_path and self.session_path.exists():
            if self.session_path.stat().st_size>16*1024*1024:
                raise ValueError('Session file exceeds 16 MiB')
            saved=json.loads(self.session_path.read_text(encoding='utf-8'))
            if not isinstance(saved,dict) or saved.get('format')!='surface-diagrams-session-v1':
                raise ValueError('Not a Factorization Lab session file')
            entries=saved.get('history'); position=saved.get('position')
            if not isinstance(entries,list) or not 1<=len(entries)<=60 or type(position) is not int or not 0<=position<len(entries):
                raise ValueError('Invalid session history')
            history=[]
            for index,entry in enumerate(entries):
                factors=parse_factors(entry)
                try: checked(initial_factors(),factors)
                except VerificationLimitError: limited.append(index+1)
                history.append(factors)
        super().__init__(('127.0.0.1',port),LabHandler)
        self.token=secrets.token_urlsafe(32)
        self.allowed_hosts={f'127.0.0.1:{self.server_port}',f'localhost:{self.server_port}'}
        self.lock=threading.Lock()
        self.history=history; self.position=position; self.revision=0
        self.message=('Reopened saved exploration and undo history; exact products verified.' if self.session_path and self.session_path.exists()
                      else 'Loaded 13 factors / 178 braid letters from the earlier SVG.')
        self.verification_notice=('Saved history states '+', '.join(map(str,limited))+
            ' reached the exact verification limit on reopening. Their product equality is not reverified; history is preserved.' if limited else '')
        if limited: self.message='Reopened saved exploration and undo history.'
        if self.session_path:
            try: self.save_session()
            except Exception:
                self.server_close(); raise
    @property
    def url(self): return f'http://127.0.0.1:{self.server_port}'
    def save_session(self):
        if self.session_path is None: return
        document=dict(format='surface-diagrams-session-v1',position=self.position,
                      history=[export_factors(factors) for factors in self.history])
        temporary=None
        try:
            with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=self.session_path.parent,
                                             prefix=self.session_path.name+'.',suffix='.tmp',delete=False) as stream:
                temporary=Path(stream.name)
                json.dump(document,stream)
                stream.flush(); os.fsync(stream.fileno())
            os.replace(temporary,self.session_path)
        finally:
            if temporary is not None and temporary.exists(): temporary.unlink()
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
            rows.append(dict(asdict(f),word=f.word,core=f.core,label=f.label,svg=svg,warning=warning,
                             height=row_height(f),splits=options,audit=support_audit(f)))
        return dict(token=self.token,revision=self.revision,factors=rows,braid=braid_svg(factors),
                    persistent=self.session_path is not None,
                    undo=self.position>0,redo=self.position<len(self.history)-1,message=(self.message+' '+self.verification_notice).strip(),
                    export=export_factors(factors))
    def prefix_action(self,index):
        """Exact based meridian images on both sides of a selected factor."""
        from .based_cut_system import based_cut_system_drawing
        factors=self.history[self.position]
        if type(index) is not int or not 0<=index<len(factors):
            raise ValueError('Choose a valid factor position')
        before=exact_action(product(factors[:index]))
        after=exact_action(product(factors[:index+1]))
        def punctures(images):
            keys=tuple(free_homotopy_key(word) for word in images)
            if any(len(key)!=1 for key in keys):
                raise ValueError('Meridian images have no single puncture class')
            return tuple(abs(key[0]) for key in keys)
        def drawing(images):
            try: return based_cut_system_drawing(images),''
            except ValueError as error: return '',str(error)
        before_svg,before_warning=drawing(before)
        after_svg,after_warning=drawing(after)
        return dict(factor=factors[index].id,index=index,revision=self.revision,
                    before=before,after=after,before_punctures=punctures(before),
                    after_punctures=punctures(after),before_svg=before_svg,
                    after_svg=after_svg,before_warning=before_warning,after_warning=after_warning)
    def sphere_action(self):
        return dict(sphere_inner_certificate(product(self.history[self.position])),revision=self.revision)
    def mutate(self,payload):
        previous=(self.history,self.position,self.revision,self.message)
        try:
            self._mutate(payload)
            self.save_session()
        except Exception:
            self.history,self.position,self.revision,self.message=previous
            raise
    def _mutate(self,payload):
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
            if op not in ('reset','import','simplify') and (type(i) is not int or not 0<=i<len(factors)):
                raise ValueError('Choose a valid factor')
            if op=='move':
                result=move_factor(factors,i,payload.get('target'))
                message=f'Moved {factors[i].id}; crossed factors conjugated. Every adjacent move passed exact disk-action checks.'
            elif op=='split':
                result=split_factor(factors,i,payload.get('kind'))
                message=f'Split {factors[i].id}; replacement passed exact disk-action verification.'
            elif op=='combine':
                result=combine_factors(factors,i)
                message='Combined neighboring factors; exact disk action verified.'
            elif op=='reset': result=initial_factors(); message='Restored original factorization. Undo is available.'
            elif op=='simplify':
                result=checked(factors,tuple(simplify_factor(f) for f in factors))
                if result==factors:
                    self.message='No shorter representatives found within the search bounds. Undo and redo history preserved.'
                    self.revision+=1
                    return
                message='Simplified conjugated twists with a bounded search; exact actions verified. Global minimality is not asserted.'
            elif op=='import': result=import_factors(payload.get('document')); message='Loaded saved exploration; exact product agrees with the starting factorization.'
            else: raise ValueError('Unknown operation')
            self.history=self.history[:self.position+1]+[result]
            if len(self.history)>60: self.history=self.history[-60:]
            self.position=len(self.history)-1; self.message=message
        self.revision+=1


class LabHandler(EditorHandler):
    def do_GET(self):
        if not self._local_request(): return
        if urlsplit(self.path).path=='/api/sphere':
            try:
                revision=int(parse_qs(urlsplit(self.path).query)['revision'][0])
                with self.server.lock:
                    if revision!=self.server.revision:
                        self._error(409,'State changed; reload before checking'); return
                    data=self.server.sphere_action()
            except (KeyError,ValueError,VerificationLimitError) as error:
                self._error(400,str(error)); return
            self._reply(200,json.dumps(data)); return
        if urlsplit(self.path).path=='/api/prefix':
            try:
                query=parse_qs(urlsplit(self.path).query)
                revision=int(query['revision'][0]); index=int(query['index'][0])
                with self.server.lock:
                    if revision!=self.server.revision:
                        self._error(409,'State changed; reload before inspecting'); return
                    data=self.server.prefix_action(index)
            except (KeyError,ValueError,VerificationLimitError) as error:
                self._error(400,str(error)); return
            self._reply(200,json.dumps(data)); return
        if urlsplit(self.path).path=='/api/export.svg':
            try: revision=int(parse_qs(urlsplit(self.path).query)['revision'][0])
            except (KeyError,ValueError): self._error(400,'Supply the current revision'); return
            with self.server.lock:
                if revision!=self.server.revision:
                    self._error(409,'State changed; reload before exporting'); return
                svg=factorization_svg(self.server.history[self.server.position])
            self._reply(200,svg,'image/svg+xml; charset=utf-8'); return
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
        except OSError:
            self._error(503,'Could not save the session file; operation was not applied. Check available disk space and file permissions.')


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=0)
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('--session',type=Path,help='Save and reopen this workspace file, including undo/redo history')
    args=parser.parse_args(argv)
    if not 0<=args.port<=65535: parser.error('port must be between 0 and 65535')
    try: server=LabServer(args.port,args.session)
    except (ValueError,OSError) as error: parser.error(str(error))
    print(server.url,flush=True)
    if not args.no_browser: webbrowser.open(server.url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__=='__main__': main()
