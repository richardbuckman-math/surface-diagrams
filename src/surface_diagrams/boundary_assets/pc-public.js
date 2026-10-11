'use strict';
// The exact Python engine runs in this page's worker; saves stay in this browser.
window.boundaryStorageAvailable = true;
const pcStorageKey = 'surface-diagrams-pc-lantern-workspace-v1';
let savedPcSession = '';
try { savedPcSession = localStorage.getItem(pcStorageKey) || ''; }
catch (_) { window.boundaryStorageAvailable = false; }
const pcWorker = new Worker(new URL('pc-worker.mjs', document.currentScript.src), {type:'module'});
let nextPcRequest = 0;
const pendingPcRequests = new Map();
pcWorker.onmessage = event => {
  const {id, status, body, mime, session} = event.data;
  const pending = pendingPcRequests.get(id);
  if (!pending) return;
  pendingPcRequests.delete(id);
  if (session && window.boundaryStorageAvailable) {
    try { localStorage.setItem(pcStorageKey, JSON.stringify(session)); }
    catch (_) { window.boundaryStorageAvailable = false; }
  }
  pending.resolve(new Response(body, {status, headers:{'Content-Type':mime}}));
};
pcWorker.onerror = event => {
  for (const pending of pendingPcRequests.values())
    pending.reject(new Error(event.message || 'Could not start the PC lantern engine'));
  pendingPcRequests.clear();
};
const nativePcFetch = window.fetch.bind(window);
window.fetch = (input, options={}) => {
  const path = typeof input === 'string' ? input : input.url;
  if (!path.startsWith('/api/')) return nativePcFetch(input, options);
  return new Promise((resolve, reject) => {
    const id = ++nextPcRequest;
    pendingPcRequests.set(id, {resolve, reject});
    pcWorker.postMessage({id, path, method:options.method || 'GET',
      body:options.body || '', savedSession:savedPcSession});
  });
};
