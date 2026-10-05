'use strict';
// The Python engine runs in this page's worker; the workspace stays in this browser.
window.boundaryStorageAvailable = true;
const boundaryStorageKey = 'surface-diagrams-boundary-playground-workspace-v1';
let savedBoundarySession = '';
try { savedBoundarySession = localStorage.getItem(boundaryStorageKey) || ''; }
catch (_) { window.boundaryStorageAvailable = false; }
const boundaryWorker = new Worker(new URL('worker.mjs', document.currentScript.src), {type:'module'});
let nextBoundaryRequest = 0;
const pendingBoundaryRequests = new Map();
boundaryWorker.onmessage = event => {
  const {id,status,body,mime,session} = event.data;
  const pending = pendingBoundaryRequests.get(id);
  if (!pending) return;
  pendingBoundaryRequests.delete(id);
  if (session && window.boundaryStorageAvailable) {
    try { localStorage.setItem(boundaryStorageKey, JSON.stringify(session)); }
    catch (_) { window.boundaryStorageAvailable = false; }
  }
  pending.resolve(new Response(body, {status,headers:{'Content-Type':mime}}));
};
boundaryWorker.onerror = event => {
  for (const pending of pendingBoundaryRequests.values())
    pending.reject(new Error(event.message || 'Could not start the calculation engine'));
  pendingBoundaryRequests.clear();
};
const nativeBoundaryFetch = window.fetch.bind(window);
window.fetch = (input, options={}) => {
  const path = typeof input === 'string' ? input : input.url;
  if (!path.startsWith('/api/')) return nativeBoundaryFetch(input, options);
  return new Promise((resolve,reject) => {
    const id = ++nextBoundaryRequest;
    pendingBoundaryRequests.set(id,{resolve,reject});
    boundaryWorker.postMessage({id,path,method:options.method||'GET',
      body:options.body||'',savedSession:savedBoundarySession});
  });
};
