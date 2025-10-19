
/* -------------------------------------------------------------
   Dynamic Quote Generator – Integrated Solution
   Features:
     - Advanced DOM manipulation
     - LocalStorage persistence (quotes, selected category)
     - SessionStorage (last viewed quote index per session)
     - JSON export/import with validation & de-duplication
     - Category filter populated dynamically
     - Mock server sync (fetch + merge + conflict policy)
   Repo: alx_fe_javascript / dom-manipulation
--------------------------------------------------------------*/

// ====== Configuration ======
const LS_QUOTES_KEY = 'dqg.quotes.v1';
const LS_FILTER_KEY = 'dqg.filter.v1';
const SS_LAST_INDEX_KEY = 'dqg.lastIndex.v1';

// Mock server config (uses JSONPlaceholder posts as demo data)
const SERVER = {
  fetchUrl: 'https://jsonplaceholder.typicode.com/posts?_limit=5',
  postUrl: 'https://jsonplaceholder.typicode.com/posts',
  syncIntervalMs: 30000 // 30s
};

// ====== State ======
/** Quote shape: { id, text, category, source: 'local'|'server', updatedAt } */
let quotes = [];

// ====== DOM helpers ======
const el = sel => document.querySelector(sel);
const els = sel => Array.from(document.querySelectorAll(sel));
function setStatus(msg) { const s = el('#status'); if (s) s.textContent = msg || ''; }
function setNotice(msg) { const n = el('#notice'); if (n) n.textContent = msg || ''; }

// ====== Storage ======
function saveQuotes() {
  localStorage.setItem(LS_QUOTES_KEY, JSON.stringify(quotes));
  setStatus(`Saved ${quotes.length} quotes.`);
  refreshListsAndFilters();
}
function createAddQuoteForm() {
  const form = document.createElement("form");
  form.id = "add-quote-form";

  const textInput = document.createElement("input");
  textInput.type = "text";
  textInput.placeholder = "Enter quote...";
  textInput.required = true;

  const categoryInput = document.createElement("input");
  categoryInput.type = "text";
  categoryInput.placeholder = "Enter category...";
  categoryInput.required = true;

  const btn = document.createElement("button");
  btn.type = "submit";
  btn.textContent = "Add Quote";

  form.append(textInput, categoryInput, btn);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    addQuote(textInput.value, categoryInput.value);
    form.reset();
  });

  document.body.appendChild(form);
}

function loadQuotes() {
  try {
    const raw = localStorage.getItem(LS_QUOTES_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        quotes = parsed
          .filter(q => q && typeof q.text === 'string' && typeof q.category === 'string')
          .map(q => ({
            id: q.id ?? crypto.randomUUID(),
            text: q.text.trim(),
            category: q.category.trim(),
            source: q.source === 'server' ? 'server' : 'local',
            updatedAt: q.updatedAt ?? Date.now()
          }))
          .filter(q => q.text && q.category);
        return;
      }
    }
  } catch {}
  // Seed data
  quotes = [
    { id: crypto.randomUUID(), text: 'The only limit to our realization of tomorrow is our doubts of today.', category: 'Motivation', source: 'local', updatedAt: Date.now() },
    { id: crypto.randomUUID(), text: 'In the middle of every difficulty lies opportunity.', category: 'Wisdom', source: 'local', updatedAt: Date.now() },
    { id: crypto.randomUUID(), text: 'Happiness depends upon ourselves.', category: 'Philosophy', source: 'local', updatedAt: Date.now() }
  ];
  saveQuotes();
}

// ====== Rendering ======
function displayQuote(q) {
  const box = el('#quoteDisplay');
  if (!box) return;
  if (!q) { box.textContent = 'No quote to show.'; return; }
  box.textContent = `"${q.text}" — (${q.category})`;
}

function renderList(filtered) {
  const list = el('#quoteList');
  list.innerHTML = '';
  (filtered || []).forEach(q => {
    const li = document.createElement('li');
    const left = document.createElement('div');
    const right = document.createElement('div');
    right.className = 'right';

    left.innerHTML = `
      <div>"${q.text}"</div>
      <div class="meta">Category: <span class="pill">${q.category}</span> • Source: ${q.source} • Updated: ${new Date(q.updatedAt).toLocaleString()}</div>
    `;

    const showBtn = document.createElement('button');
    showBtn.textContent = 'Show';
    showBtn.addEventListener('click', () => displayQuote(q));

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.addEventListener('click', () => {
      quotes = quotes.filter(x => x.id !== q.id);
      saveQuotes();
      setStatus('Quote deleted.');
      applyFilterAndRender();
    });

    right.append(showBtn, delBtn);
    li.append(left, right);
    list.append(li);
  });
}

// ====== Category filter ======
function getCategories() {
  const set = new Set(quotes.map(q => q.category).filter(Boolean));
  return Array.from(set).sort((a,b) => a.localeCompare(b));
}

function populateCategories() {
  const sel = el('#categoryFilter');
  const current = localStorage.getItem(LS_FILTER_KEY) || 'all';
  sel.innerHTML = '';

  const optAll = document.createElement('option');
  optAll.value = 'all';
  optAll.textContent = 'All Categories';
  sel.appendChild(optAll);

  getCategories().forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat; opt.textContent = cat;
    sel.appendChild(opt);
  });

  sel.value = current;
}

function filterQuotes() {
  const sel = el('#categoryFilter');
  const value = sel.value;
  localStorage.setItem(LS_FILTER_KEY, value);
  applyFilterAndRender();
}

function applyFilterAndRender() {
  const selected = localStorage.getItem(LS_FILTER_KEY) || 'all';
  const filtered = selected === 'all' ? quotes : quotes.filter(q => q.category === selected);
  renderList(filtered);
}

function refreshListsAndFilters() {
  populateCategories();
  applyFilterAndRender();
}

// ====== Core interactions ======
function showRandomQuote() {
  const selected = localStorage.getItem(LS_FILTER_KEY) || 'all';
  const pool = selected === 'all' ? quotes : quotes.filter(q => q.category === selected);
  if (!pool.length) { displayQuote({ text: 'No quotes match this filter. Add one!', category: selected }); return; }
  const idx = Math.floor(Math.random() * pool.length);
  const q = pool[idx];
  displayQuote(q);
  sessionStorage.setItem(SS_LAST_INDEX_KEY, String(idx));
}

function addQuote() {
  const text = el('#newQuoteText').value.trim();
  const category = el('#newQuoteCategory').value.trim();
  if (!text || !category) { alert('Please enter both a quote and a category.'); return; }

  // de-dup (text+category)
  const key = `${text.toLowerCase()}::${category.toLowerCase()}`;
  const exists = quotes.some(q => `${q.text.toLowerCase()}::${q.category.toLowerCase()}` === key);
  if (exists) { alert('That quote already exists in this category.'); return; }

  quotes.push({ id: crypto.randomUUID(), text, category, source: 'local', updatedAt: Date.now() });
  saveQuotes();

  // Clear inputs and refresh UI
  el('#newQuoteText').value = '';
  el('#newQuoteCategory').value = '';
  displayQuote({ text, category });
  setStatus('Quote added.');
}

// ====== Import/Export ======
function exportToJsonFile() {
  try {
    const data = JSON.stringify(quotes, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const date = new Date().toISOString().slice(0,10);
    a.download = `quotes-${date}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus('Exported quotes to JSON.');
  } catch (e) { alert('Export failed.'); console.error(e); }
}
async function syncQuotes() {
  try {
    const res = await fetch(SERVER.syncUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(quotes),
    });

    if (!res.ok) throw new Error("Failed to sync quotes");

    const serverData = await res.json();
    console.log("Quotes synced with server!");
    alert("Quotes synced with server!"); 
  } catch (err) {
    console.error("Error syncing quotes:", err);
    
  }
}


function importFromJsonFile(event) {
  const file = event?.target?.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const payload = JSON.parse(String(e.target.result || ''));
      const incoming = Array.isArray(payload) ? payload : payload?.quotes;
      if (!Array.isArray(incoming)) throw new Error("Invalid format. Use an array or { quotes: [...] }.");

      const clean = incoming
        .filter(q => q && typeof q.text === 'string' && typeof q.category === 'string')
        .map(q => ({
          id: q.id || crypto.randomUUID(),
          text: q.text.trim(),
          category: q.category.trim(),
          source: q.source === 'server' ? 'server' : 'local',
          updatedAt: Number.isFinite(q.updatedAt) ? q.updatedAt : Date.now()
        }))
        .filter(q => q.text && q.category);

      const seen = new Set(quotes.map(q => `${q.text.toLowerCase()}::${q.category.toLowerCase()}`));
      let added = 0;
      for (const q of clean) {
        const k = `${q.text.toLowerCase()}::${q.category.toLowerCase()}`;
        if (!seen.has(k)) { quotes.push(q); seen.add(k); added++; }
      }
      saveQuotes();
      applyFilterAndRender();
      if (added > 0) showRandomQuote();
      alert('Quotes imported successfully!');
      setStatus(`Imported ${added} new quote(s).`);
    } catch (err) {
      alert('Import failed: ' + err.message);
    } finally {
      event.target.value = '';
    }
  };
  reader.readAsText(file);
}

// ====== Server sync (mock) ======
async function fetchQuotesFromServer() {
  await fetchQuotesFromServer();

  try {
    const res = await fetch(SERVER.fetchUrl);
    const data = await res.json();
    // Map posts -> quotes (body as text, first tag as category)
    const serverQuotes = (Array.isArray(data) ? data : [])
      .map(p => ({
        id: String(p.id),
        text: String(p.body || p.title || '').trim(),
        category: 'Server',
        source: 'server',
        updatedAt: Date.now() // mock timestamp
      }))
      .filter(q => q.text);

    mergeServerData(serverQuotes);
    setNotice('Synced from server.');
  } catch (e) {
    setNotice('Server fetch failed (mock). Working offline.');
    console.warn(e);
  }
}

function mergeServerData(serverQuotes) {
  // Conflict policy: server wins by id/text
  const byKey = q => `${q.id || ''}::${q.text.toLowerCase()}`;
  const localMap = new Map(quotes.map(q => [byKey(q), q]));

  serverQuotes.forEach(sq => {
    const key = byKey(sq);
    const existing = localMap.get(key);
    if (!existing) {
      quotes.push(sq);
    } else {
      // If exists, prefer server (take category/source/updatedAt)
      existing.category = sq.category;
      existing.source = 'server';
      existing.updatedAt = Math.max(existing.updatedAt || 0, sq.updatedAt || 0);
    }
  });
  saveQuotes();
  applyFilterAndRender();
}

async function pushLocalChanges() {
  // Demo-only: POST local quotes to mock server (will not persist)
  const locals = quotes.filter(q => q.source === 'local');
  if (!locals.length) return;
  try {
    await Promise.all(locals.map(q => fetch(SERVER.postUrl, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: q.category, body: q.text })
    })));
    setNotice('Pushed local items to server (mock).');
  } catch (e) { console.warn('Push failed (mock):', e); }
}

async function syncAll() {
  setNotice('Syncing…');
  await fetchFromServer();
  await pushLocalChanges();
  setTimeout(() => setNotice(''), 3000);
}


function startAutoSync() {
  setInterval(syncAll, SERVER.syncIntervalMs);
}

// ====== Init ======
function restoreLastViewedOrRandom() {
  const selected = localStorage.getItem(LS_FILTER_KEY) || 'all';
  const pool = selected === 'all' ? quotes : quotes.filter(q => q.category === selected);
  const idxStr = sessionStorage.getItem(SS_LAST_INDEX_KEY);
  const idx = idxStr != null ? parseInt(idxStr, 10) : NaN;
  if (!Number.isNaN(idx) && idx >= 0 && idx < pool.length) displayQuote(pool[idx]);
  else showRandomQuote();
}

function wireEvents() {
  el('#newQuote').addEventListener('click', showRandomQuote);
  el('#addQuoteBtn').addEventListener('click', addQuote);
  el('#exportBtn').addEventListener('click', exportToJsonFile);

  const importBtn = el('#importBtn');
  const fileInput = el('#importFile');
  importBtn.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', importFromJsonFile);

  el('#categoryFilter').addEventListener('change', filterQuotes);
  el('#syncNow').addEventListener('click', syncAll);
}

function init() {
  createAddQuoteForm();

  const filterSelect = document.getElementById("categoryFilter");
  filterSelect.addEventListener("change", (e) => {
    localStorage.setItem("selectedCategory", e.target.value);
    displayQuote();
  });

  const syncBtn = document.getElementById("syncBtn");
  if (syncBtn) {
    syncBtn.addEventListener("click", () => syncQuotes()
      
    );
  }

  // initial load
  loadQuotes();
  displayQuote();
 
  if (!localStorage.getItem(LS_FILTER_KEY)) localStorage.setItem(LS_FILTER_KEY, 'all');
  refreshListsAndFilters();
  restoreLastViewedOrRandom();
  wireEvents();
  // Kick off a first sync, then periodic
  syncAll();
  startAutoSync();
}

document.addEventListener('DOMContentLoaded', init);
