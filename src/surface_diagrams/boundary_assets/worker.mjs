import {loadPyodide} from 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';

const start = (async () => {
  const pyodide = await loadPyodide();
  const [packageResponse,backendResponse] = await Promise.all([
    fetch('../lab/surface_diagrams.zip'),fetch('backend.py')
  ]);
  if (!packageResponse.ok || !backendResponse.ok)
    throw new Error('Could not load the published boundary playground');
  pyodide.FS.writeFile('/tmp/surface_diagrams.zip',
    new Uint8Array(await packageResponse.arrayBuffer()));
  pyodide.runPython("import sys; sys.path.insert(0, '/tmp/surface_diagrams.zip')");
  pyodide.runPython(await backendResponse.text());
  return pyodide;
})();
let restored = false;

self.onmessage = async event => {
  const {id,path,method,body,savedSession} = event.data;
  try {
    const pyodide = await start;
    if (!restored) {
      pyodide.globals.set('saved_session_text',savedSession||'');
      pyodide.runPython('restore_browser_session(saved_session_text)');
      restored = true;
    }
    pyodide.globals.set('request_path',path);
    pyodide.globals.set('request_method',method);
    pyodide.globals.set('request_body',body);
    const response = JSON.parse(pyodide.runPython(
      'dispatch(request_path,request_method,request_body)'));
    self.postMessage({id,...response});
  } catch (error) {
    self.postMessage({id,status:500,
      body:JSON.stringify({error:String(error)}),mime:'application/json'});
  }
};
