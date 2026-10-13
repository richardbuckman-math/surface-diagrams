'use strict';
// On GitHub Pages, the same Python lab runs in a browser worker. All requests
// stay on this device; the local HTTP server still uses its ordinary API.
window.surfaceLabPublic = true;
window.surfaceLabStorageAvailable = true;
const labSeed = document.documentElement.dataset.labSeed === '4-3' ? '4-3' : '6-7';
const labStorageKey = labSeed === '4-3' ? 'surface-diagrams-xiao-four-three-workspace-v1' :
 'surface-diagrams-six-seven-workspace-v1';
const previewStorageKey = `${labStorageKey}-rendered-preview-v1`;
let savedLabSession = '';
try { savedLabSession = localStorage.getItem(labStorageKey) || ''; }
catch (_) { window.surfaceLabStorageAvailable = false; }
let cachedLabPreview = null;
if (savedLabSession && window.surfaceLabStorageAvailable) {
 try {
  const cached = JSON.parse(localStorage.getItem(previewStorageKey) || 'null');
  const preview = JSON.parse(cached?.state || 'null');
  if (cached?.session === savedLabSession && Array.isArray(preview?.factors) &&
      Array.isArray(preview?.steps) && typeof preview?.braid === 'string')
   cachedLabPreview = preview;
 } catch (_) { /* A corrupt preview never prevents exact session restoration. */ }
}
const labWorker = new Worker(new URL('public-lab-worker.mjs', document.currentScript.src), {type: 'module'});
let nextLabRequest = 0;
const pendingLabRequests = new Map();
labWorker.onmessage = event => {
 if (event.data.kind === 'progress') {
  const message = document.getElementById('lab-loading-message');
  if (message && !document.getElementById('lab-loading').hidden)
   message.textContent = event.data.phase;
  return;
 }
 const {id, status, body, mime, session} = event.data;
 const pending = pendingLabRequests.get(id);
 if (!pending) return;
 pendingLabRequests.delete(id);
 if (session && window.surfaceLabStorageAvailable) {
  try {
   savedLabSession = JSON.stringify(session);
   localStorage.setItem(labStorageKey, savedLabSession);
  }
  catch (_) { window.surfaceLabStorageAvailable = false; }
 }
 if (status === 200 && window.surfaceLabStorageAvailable && savedLabSession &&
     (pending.path === '/api/state' || pending.path === '/api/action')) {
  try { localStorage.setItem(previewStorageKey,
         JSON.stringify({session: savedLabSession, state: body})); }
  catch (_) { /* The rendered preview is optional; the workspace remains saved. */ }
 }
 pending.resolve(new Response(body, {status, headers: {'Content-Type': mime}}));
};
labWorker.onerror = event => {
 for (const pending of pendingLabRequests.values()) pending.reject(new Error(event.message || 'Could not start the browser calculation engine'));
 pendingLabRequests.clear();
};
const ordinaryFetch = window.fetch.bind(window);
// Show a read-only rendering while Python starts. A saved exploration uses
// only a preview tied to its exact session document; the worker remains the
// authority for the restored state and every edit.
window.surfaceLabStartupPreview = cachedLabPreview ? Promise.resolve(cachedLabPreview) : ordinaryFetch(
 new URL(`seed-preview-${labSeed}.json`, document.currentScript.src)
).then(response => {
 if (!response.ok) throw new Error('Seed preview unavailable');
 return response.json();
});
window.surfaceLabPreviewKind = cachedLabPreview ? 'saved' :
 savedLabSession ? 'default-while-restoring' : 'seed';
window.fetch = (input, options = {}) => {
 const path = typeof input === 'string' ? input : input.url;
 if (!path.startsWith('/api/')) return ordinaryFetch(input, options);
 return new Promise((resolve, reject) => {
  const id = ++nextLabRequest;
  pendingLabRequests.set(id, {resolve, reject, path});
  labWorker.postMessage({id, path, method: options.method || 'GET', body: options.body || '',
   savedSession: savedLabSession, labSeed});
 });
};
