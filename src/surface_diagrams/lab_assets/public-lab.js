'use strict';
// On GitHub Pages, the same Python lab runs in a browser worker. All requests
// stay on this device; the local HTTP server still uses its ordinary API.
window.surfaceLabPublic = true;
window.surfaceLabStorageAvailable = true;
const labSeed = document.documentElement.dataset.labSeed === '4-3' ? '4-3' : '6-7';
const labStorageKey = labSeed === '4-3' ? 'surface-diagrams-xiao-four-three-workspace-v1' :
 'surface-diagrams-six-seven-workspace-v1';
let savedLabSession = '';
try { savedLabSession = localStorage.getItem(labStorageKey) || ''; }
catch (_) { window.surfaceLabStorageAvailable = false; }
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
  try { localStorage.setItem(labStorageKey, JSON.stringify(session)); }
  catch (_) { window.surfaceLabStorageAvailable = false; }
 }
 pending.resolve(new Response(body, {status, headers: {'Content-Type': mime}}));
};
labWorker.onerror = event => {
 for (const pending of pendingLabRequests.values()) pending.reject(new Error(event.message || 'Could not start the browser calculation engine'));
 pendingLabRequests.clear();
};
const ordinaryFetch = window.fetch.bind(window);
// A small, build-time snapshot can paint a new visitor's seed diagram while
// the Python worker starts. Saved explorations always wait for their own state.
window.surfaceLabSeedPreview = savedLabSession ? null : ordinaryFetch(
 new URL(`seed-preview-${labSeed}.json`, document.currentScript.src)
).then(response => {
 if (!response.ok) throw new Error('Seed preview unavailable');
 return response.json();
});
window.fetch = (input, options = {}) => {
 const path = typeof input === 'string' ? input : input.url;
 if (!path.startsWith('/api/')) return ordinaryFetch(input, options);
 return new Promise((resolve, reject) => {
  const id = ++nextLabRequest;
  pendingLabRequests.set(id, {resolve, reject});
  labWorker.postMessage({id, path, method: options.method || 'GET', body: options.body || '',
   savedSession: savedLabSession, labSeed});
 });
};
