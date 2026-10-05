"""Local interactive six-strand factorization labs. Run with --no-browser."""
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
from .factorization_explorer import initial_factors,move_factor,split_factor,combine_factors,export_factors,simplify_factor,checked,product,parse_global_conjugator,checked_global_frame,global_conjugate_factors
from .fibration_lab_seeds import XIAO_FOUR_THREE
from .braid_actions import free_homotopy_key,reduce_word
from .factorization_geometry import support_svg,braid_svg,row_height,factorization_svg
from .factorization_audit import support_audit
from .factorization_explorer import parse_factors
from .mapping_classes import VerificationLimitError,exact_action
from .sphere_actions import sphere_inner_certificate
from .sphere_cut_system import sphere_chart_drawing


def starting_factors(seed_slug='6-7'):
    """Only executable, verified six-strand seeds are available as labs."""
    if seed_slug=='6-7': return initial_factors()
    if seed_slug=='4-3': return XIAO_FOUR_THREE.factors
    raise ValueError('Unknown factorization lab seed')


def validated_session_document(saved,seed_slug='6-7'):
    """Decode a workspace with the same checks for disk and browser storage."""
    if not isinstance(saved,dict) or saved.get('format')!='surface-diagrams-session-v1':
        raise ValueError('Not a Factorization Lab session file')
    if saved.get('seed','6-7')!=seed_slug:
        raise ValueError('This workspace belongs to a different factorization lab')
    seed_factors=starting_factors(seed_slug)
    entries=saved.get('history'); position=saved.get('position')
    if not isinstance(entries,list) or not 1<=len(entries)<=60 or type(position) is not int or not 0<=position<len(entries):
        raise ValueError('Invalid session history')
    saved_frames=saved.get('frames',[[] for _ in entries])
    if not isinstance(saved_frames,list) or len(saved_frames)!=len(entries):
        raise ValueError('Invalid global conjugation history')
    operations=saved.get('operations',[f'Earlier saved state {i+1}' for i in range(len(entries))])
    if (not isinstance(operations,list) or len(operations)!=len(entries) or
            any(not isinstance(label,str) or not 1<=len(label)<=300 for label in operations)):
        raise ValueError('Invalid operation history')
    history=[];frames=[];limited=[]
    for index,entry in enumerate(entries):
        factors=parse_factors(entry,expected_seed=seed_slug)
        frame=parse_global_conjugator(saved_frames[index])
        try:
            if frame: checked_global_frame(factors,frame,seed_factors)
            else: checked(seed_factors,factors)
        except VerificationLimitError:
            if seed_slug=='4-3': raise
            limited.append(index+1)
        history.append(factors);frames.append(frame)
    return history,frames,operations,position,limited


class LabServer(ThreadingHTTPServer):
    daemon_threads=True
    def __init__(self,port=0,session_path=None,seed_slug='6-7'):
        self.seed_slug=seed_slug
        self.seed_factors=starting_factors(seed_slug)
        self.session_path=Path(session_path).expanduser().resolve() if session_path else None
        history=[self.seed_factors]; frames=[()]; operations=['Original factorization']; position=0; limited=[]
        if self.session_path and self.session_path.exists():
            if self.session_path.stat().st_size>16*1024*1024:
                raise ValueError('Session file exceeds 16 MiB')
            saved=json.loads(self.session_path.read_text(encoding='utf-8'))
            history,frames,operations,position,limited=validated_session_document(saved,seed_slug)
        super().__init__(('127.0.0.1',port),LabHandler)
        self.token=secrets.token_urlsafe(32)
        self.allowed_hosts={f'127.0.0.1:{self.server_port}',f'localhost:{self.server_port}'}
        self.lock=threading.Lock()
        self.history=history; self.frames=frames; self.operations=operations
        self.position=position; self.revision=0
        self.message=('Reopened saved exploration and undo history; exact products verified.' if self.session_path and self.session_path.exists()
                      else ("Loaded Xiao's seven normalized factors; exact disk product fixed to this seed."
                            if seed_slug=='4-3' else 'Loaded 13 factors / 178 braid letters from the earlier SVG.'))
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
        document=self.session_document()
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
    def session_document(self):
        document=dict(format='surface-diagrams-session-v1',position=self.position,
                      history=[export_factors(factors,self.seed_slug) for factors in self.history],
                      frames=[list(frame) for frame in self.frames],operations=self.operations)
        if self.seed_slug=='4-3': document['seed']='4-3'
        return document
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
        return dict(token=self.token,revision=self.revision,seed_slug=self.seed_slug,
                    factors=rows,braid=braid_svg(factors),
                    persistent=self.session_path is not None,
                    undo=self.position>0,redo=self.position<len(self.history)-1,message=(self.message+' '+self.verification_notice).strip(),
                    frame=self.frames[self.position],steps=self.operations,position=self.position,
                    export=dict(export_factors(factors,self.seed_slug),global_conjugator=self.frames[self.position]))
    def prefix_action(self,index,system='fan'):
        """Exact images of either the boundary fan or adjacent-point chain."""
        from .based_cut_system import based_cut_system_drawing
        from .chain_cut_system import chain_cut_system_drawing,chain_words
        factors=self.history[self.position]
        if type(index) is not int or not 0<=index<len(factors):
            raise ValueError('Choose a valid factor position')
        if system not in ('fan','chain'):
            raise ValueError('Choose the boundary fan or adjacent-point chain')
        before_meridians=exact_action(product(factors[:index]))
        after_meridians=exact_action(product(factors[:index+1]))
        def punctures(images):
            keys=tuple(free_homotopy_key(word) for word in images)
            if any(len(key)!=1 for key in keys):
                raise ValueError('Meridian images have no single puncture class')
            return tuple(abs(key[0]) for key in keys)
        def drawing(images):
            try: return (chain_cut_system_drawing(images) if system=='chain' else
                         based_cut_system_drawing(images)),''
            except ValueError as error: return '',str(error)
        before_svg,before_warning=drawing(before_meridians)
        after_svg,after_warning=drawing(after_meridians)
        if system=='chain':
            before,before_endpoints=chain_words(before_meridians)
            after,after_endpoints=chain_words(after_meridians)
        else:
            before,after=before_meridians,after_meridians
            before_endpoints=tuple((0,p) for p in punctures(before))
            after_endpoints=tuple((0,p) for p in punctures(after))
        return dict(factor=factors[index].id,index=index,revision=self.revision,system=system,
                    before=before,after=after,
                    before_meridians=before_meridians,after_meridians=after_meridians,
                    before_punctures=tuple(end for _,end in before_endpoints),
                    after_punctures=tuple(end for _,end in after_endpoints),
                    before_endpoints=before_endpoints,after_endpoints=after_endpoints,
                    word_kind='adjacent-pair neighborhood boundary' if system=='chain' else 'based meridian',
                    before_svg=before_svg,
                    after_svg=after_svg,before_warning=before_warning,after_warning=after_warning)
    def prefix_arc(self,index,side,arc_index,system='fan'):
        """Inspect one exact arc when joint routing is too large to draw."""
        from .based_cut_system import based_arc_drawing
        from .chain_cut_system import chain_arc_drawing,chain_words
        factors=self.history[self.position]
        if type(index) is not int or not 0<=index<len(factors):
            raise ValueError('Choose a valid factor position')
        if side not in ('before','after') or type(arc_index) is not int or not 0<=arc_index<6:
            raise ValueError('Choose a valid arc and side')
        if system not in ('fan','chain'):
            raise ValueError('Choose the boundary fan or adjacent-point chain')
        images=exact_action(product(factors[:index+(side=='after')]))
        image=(chain_words(images)[0][arc_index] if system=='chain' else images[arc_index])
        try:
            svg=(chain_arc_drawing(images,index=arc_index) if system=='chain' else
                 based_arc_drawing(image,index=arc_index));warning=''
        except ValueError as error: svg='';warning=str(error)
        return dict(factor=factors[index].id,index=index,side=side,arc=arc_index+1,
                    system=system,image=image,svg=svg,warning=warning,revision=self.revision)
    def sphere_action(self):
        word=product(self.history[self.position])
        try: chart_svg,_=sphere_chart_drawing(word);chart_warning=''
        except ValueError as error: chart_svg='';chart_warning=str(error)
        return dict(sphere_inner_certificate(word),revision=self.revision,
                    chart_svg=chart_svg,chart_warning=chart_warning)
    def mutate(self,payload):
        previous=(self.history,self.frames,self.operations,self.position,self.revision,self.message)
        try:
            self._mutate(payload)
            self.save_session()
        except Exception:
            self.history,self.frames,self.operations,self.position,self.revision,self.message=previous
            raise
    def _mutate(self,payload):
        if payload.get('revision')!=self.revision: raise ValueError('State changed; reload before editing')
        op=payload.get('op'); factors=self.history[self.position];frame=self.frames[self.position]
        if op=='undo':
            if self.position==0: raise ValueError('Nothing to undo')
            self.position-=1; self.message='Undid the previous operation.'
        elif op=='redo':
            if self.position==len(self.history)-1: raise ValueError('Nothing to redo')
            self.position+=1; self.message='Redid the operation.'
        elif op=='seek':
            destination=payload.get('position')
            if type(destination) is not int or not 0<=destination<len(self.history):
                raise ValueError('Choose a saved history step')
            self.position=destination;self.message=f'Opened saved history step {destination+1}.'
        else:
            i=payload.get('index')
            if op not in ('reset','import','simplify','conjugate') and (type(i) is not int or not 0<=i<len(factors)):
                raise ValueError('Choose a valid factor')
            next_frame=frame
            if op=='move':
                result=move_factor(factors,i,payload.get('target'))
                message=f'Moved {factors[i].id}; crossed factors conjugated. Every adjacent move passed exact disk-action checks.'
                label=f'Hurwitz: {factors[i].id} from {i+1} to {payload["target"]+1}'
            elif op=='split':
                result=split_factor(factors,i,payload.get('kind'))
                message=f'Split {factors[i].id}; replacement passed exact disk-action verification.'
                label=f'Split {factors[i].id} ({payload["kind"]})'
            elif op=='combine':
                result=combine_factors(factors,i)
                message='Combined neighboring factors; exact disk action verified.'
                label=f'Combine from position {i+1}'
            elif op=='reset':
                result=self.seed_factors;next_frame=();message='Restored original factorization. Undo is available.';label='Reset to original factorization'
            elif op=='conjugate':
                word=parse_global_conjugator(payload.get('word'))
                if not word:
                    self.message='The entered global conjugator reduces to the identity; history preserved.'
                    self.revision+=1;return
                result=global_conjugate_factors(factors,word)
                next_frame=parse_global_conjugator(reduce_word(word+frame))
                checked_global_frame(result,next_frame,self.seed_factors)
                message='Globally conjugated every factor; the complete conjugated disk action was verified.'
                label=('Global conjugation: '+' '.join(map(str,word)))[:300]
            elif op=='simplify':
                result=checked(factors,tuple(simplify_factor(f) for f in factors))
                if result==factors:
                    self.message='No shorter representatives found within the search bounds. Undo and redo history preserved.'
                    self.revision+=1
                    return
                message='Simplified conjugated twists with a bounded search; exact actions verified. Global minimality is not asserted.'
                label='Simplify factor representatives'
            elif op=='import':
                document=payload.get('document')
                result=parse_factors(document,expected_seed=self.seed_slug)
                next_frame=parse_global_conjugator(document.get('global_conjugator',[]))
                if next_frame: checked_global_frame(result,next_frame,self.seed_factors)
                else: result=checked(self.seed_factors,result)
                message='Loaded saved exploration; exact product and global frame verified.'
                label='Import verified factorization'
            else: raise ValueError('Unknown operation')
            if self.seed_slug=='4-3':
                checked_global_frame(result,next_frame,self.seed_factors)
            self.history=self.history[:self.position+1]+[result]
            self.frames=self.frames[:self.position+1]+[next_frame]
            self.operations=self.operations[:self.position+1]+[label]
            if len(self.history)>60:
                self.history=self.history[-60:];self.frames=self.frames[-60:]
                self.operations=self.operations[-60:]
            self.position=len(self.history)-1; self.message=message
        self.revision+=1


class LabHandler(EditorHandler):
    def do_GET(self):
        if not self._local_request(): return
        if urlsplit(self.path).path=='/api/prefix-arc':
            try:
                query=parse_qs(urlsplit(self.path).query)
                revision=int(query['revision'][0]);index=int(query['index'][0])
                arc_index=int(query['arc'][0]);side=query['side'][0]
                with self.server.lock:
                    if revision!=self.server.revision:
                        self._error(409,'State changed; reload before inspecting'); return
                    data=self.server.prefix_arc(index,side,arc_index,query.get('system',['fan'])[0])
            except (KeyError,ValueError,VerificationLimitError) as error:
                self._error(400,str(error));return
            self._reply(200,json.dumps(data));return
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
                    data=self.server.prefix_action(index,query.get('system',['fan'])[0])
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
        assets={'/':('xiao-4-3.html' if self.server.seed_slug=='4-3' else 'index.html','text/html; charset=utf-8'),
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
    parser.add_argument('--seed',choices=('6-7','4-3'),default='6-7',help='Choose the factorization lab seed')
    args=parser.parse_args(argv)
    if not 0<=args.port<=65535: parser.error('port must be between 0 and 65535')
    try: server=LabServer(args.port,args.session,args.seed)
    except (ValueError,OSError) as error: parser.error(str(error))
    print(server.url,flush=True)
    if not args.no_browser: webbrowser.open(server.url)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__=='__main__': main()
