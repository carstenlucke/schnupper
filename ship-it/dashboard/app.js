/* Ship It! Dashboard – Frontend-Logik */

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
let currentSlug = null;
let currentAgent = null;
let currentFile = null;  // aktuell ausgewählte Datei
let agents = [];
let terminals = {};      // agent-name → Terminal instance
let eventSources = {};   // agent-name → EventSource
let pollInterval = null;

// Agent-Abhängigkeiten: welche Agenten müssen "done" sein, bevor dieser starten kann
const AGENT_DEPS = {
  "zielgruppe": [],
  "marketing": ["zielgruppe"],
  "social-media": ["marketing"],
  "kalkulation": [],
  "website": ["zielgruppe", "marketing", "kalkulation"],
  "app-prototyp": ["zielgruppe", "marketing", "kalkulation"],
};

// ---------------------------------------------------------------------------
// API-Calls
// ---------------------------------------------------------------------------
async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (opts.raw) return res;
  return res.json();
}

async function fetchProjekte() {
  return api("/api/projekte");
}

async function createProjekt(name, beschreibung) {
  return api("/api/projekte", {
    method: "POST",
    body: JSON.stringify({ name, beschreibung }),
  });
}

async function fetchAgents(slug) {
  return api(`/api/projekte/${slug}/agents`);
}

async function runAgent(slug, agent, feedback = null) {
  const body = feedback ? { feedback } : {};
  return api(`/api/projekte/${slug}/agents/${agent}/run`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

async function fetchFiles(slug, agent) {
  return api(`/api/projekte/${slug}/files/${agent}`);
}

async function fetchFileContent(slug, agent, datei) {
  const res = await fetch(`/api/projekte/${slug}/files/${agent}/${datei}`);
  return res.text();
}

async function deleteFile(slug, agent, datei) {
  return api(`/api/projekte/${slug}/files/${agent}/${datei}`, { method: "DELETE" });
}

async function deleteAgentFiles(slug, agent) {
  return api(`/api/projekte/${slug}/files/${agent}`, { method: "DELETE" });
}

// ---------------------------------------------------------------------------
// UI-Elemente
// ---------------------------------------------------------------------------
const $welcomeScreen = document.getElementById("welcome-screen");
const $dashboard = document.getElementById("dashboard");
const $agentList = document.getElementById("agent-list");
const $projektDropdownBtn = document.getElementById("projekt-dropdown-btn");
const $projektDropdown = document.getElementById("projekt-dropdown");
const $projektList = document.getElementById("projekt-list");
const $projektNameDisplay = document.getElementById("projekt-name-display");
const $projektStatusDot = document.getElementById("projekt-status-dot");
const $newProjektBtn = document.getElementById("new-projekt-btn");
const $newProjektModal = document.getElementById("new-projekt-modal");
const $newProjektForm = document.getElementById("new-projekt-form");
const $modalCancel = document.getElementById("modal-cancel");
const $welcomeForm = document.getElementById("welcome-form");
const $terminalContainer = document.getElementById("terminal-container");
const $resultContent = document.getElementById("result-content");
const $previewIframe = document.getElementById("preview-iframe");
const $previewFilename = document.getElementById("preview-filename");
const $previewOpenBtn = document.getElementById("preview-open-btn");
const $activeAgentLabel = document.getElementById("active-agent-label");
const $feedbackInput = document.getElementById("feedback-input");
const $feedbackBtn = document.getElementById("feedback-btn");
const $tabTerminal = document.getElementById("tab-terminal");
const $tabResult = document.getElementById("tab-result");
const $tabPreview = document.getElementById("tab-preview");
const $artifactList = document.getElementById("artifact-list");
const $artifactAgentName = document.getElementById("artifact-agent-name");

// ---------------------------------------------------------------------------
// Initialisierung
// ---------------------------------------------------------------------------
async function init() {
  const projekte = await fetchProjekte();

  // Slug aus URL-Hash lesen
  const hashSlug = location.hash.replace("#", "");
  if (hashSlug && projekte.find(p => p.slug === hashSlug)) {
    currentSlug = hashSlug;
  } else if (projekte.length > 0) {
    currentSlug = projekte[0].slug;
  }

  if (currentSlug) {
    showDashboard();
    await loadProjekt(currentSlug);
  } else {
    showWelcome();
  }

  setupEventListeners();
  startPolling();
}

function showWelcome() {
  $welcomeScreen.classList.remove("hidden");
  $welcomeScreen.classList.add("flex");
  $dashboard.classList.add("hidden");
  $dashboard.classList.remove("flex");
}

function showDashboard() {
  $welcomeScreen.classList.add("hidden");
  $welcomeScreen.classList.remove("flex");
  $dashboard.classList.remove("hidden");
  $dashboard.classList.add("flex");
}

// ---------------------------------------------------------------------------
// Projekt laden
// ---------------------------------------------------------------------------
async function loadProjekt(slug) {
  // Alte Terminals + Streams aufräumen bei Projektwechsel
  for (const [name, es] of Object.entries(eventSources)) {
    es.close();
  }
  eventSources = {};
  for (const entry of Object.values(terminals)) {
    entry.term.dispose();
    entry.div.remove();
  }
  terminals = {};
  currentAgent = null;

  currentSlug = slug;
  location.hash = slug;

  // Dropdown aktualisieren
  const projekte = await fetchProjekte();
  renderProjektDropdown(projekte);

  const projekt = projekte.find(p => p.slug === slug);
  if (projekt) {
    $projektNameDisplay.textContent = projekt.name;
    $projektStatusDot.className = `w-2 h-2 rounded-full projekt-dot-${projekt.status}`;
  }

  // Agenten laden
  agents = await fetchAgents(slug);
  renderAgentList();

  // Ersten sinnvollen Agenten auswählen
  if (!currentAgent || !agents.find(a => a.name === currentAgent)) {
    const running = agents.find(a => a.status === "running");
    currentAgent = running ? running.name : agents[0]?.name;
  }
  selectAgent(currentAgent);
}

// ---------------------------------------------------------------------------
// Projekt-Dropdown
// ---------------------------------------------------------------------------
function renderProjektDropdown(projekte) {
  $projektList.innerHTML = "";
  for (const p of projekte) {
    const div = document.createElement("div");
    div.className = `flex items-center gap-2 px-4 py-2.5 cursor-pointer hover:bg-white/5 transition-colors ${p.slug === currentSlug ? 'bg-white/10' : ''}`;
    div.innerHTML = `
      <div class="w-2 h-2 rounded-full projekt-dot-${p.status}"></div>
      <span class="text-xs text-white/80">${p.slug === currentSlug ? '✓ ' : ''}${p.name}</span>
    `;
    div.addEventListener("click", () => {
      $projektDropdown.classList.add("hidden");
      loadProjekt(p.slug);
    });
    $projektList.appendChild(div);
  }
}

// ---------------------------------------------------------------------------
// Agent-Liste
// ---------------------------------------------------------------------------
function renderAgentList() {
  $agentList.innerHTML = "";
  for (const agent of agents) {
    const canStart = canAgentStart(agent.name);
    const div = document.createElement("div");
    div.className = `agent-item flex flex-col p-3 rounded-sm cursor-pointer ${agent.name === currentAgent ? 'selected' : ''}`;
    div.dataset.agent = agent.name;

    let statusText = "";
    if (agent.status === "running") {
      statusText = `<span class="text-thm-yellow">${agent.file_count} Dateien working...</span>`;
    } else if (agent.status === "done") {
      statusText = `${agent.file_count} ${agent.file_count === 1 ? 'Datei' : 'Dateien'}`;
    } else if (agent.status === "error") {
      statusText = `<span class="text-error">Fehler</span>`;
    } else {
      statusText = canStart ? "bereit" : "wartend";
    }

    div.innerHTML = `
      <div class="flex items-center justify-between mb-1">
        <div class="flex items-center gap-2">
          <div class="status-dot ${agent.status}"></div>
          <span class="text-xs font-medium text-white/80">${agent.label}</span>
        </div>
        ${agent.status === "idle" && canStart ? `
          <button class="start-btn w-6 h-6 flex items-center justify-center rounded bg-thm-green/20 text-thm-green hover:bg-thm-green/30 transition-colors" title="Agent starten">
            <span class="material-symbols-outlined text-[14px]">play_arrow</span>
          </button>
        ` : ""}
      </div>
      <span class="text-[10px] text-white/40 ml-4 ${agent.status === 'running' ? 'italic' : ''}">${statusText}</span>
    `;

    // Click auf Item → Agent auswählen
    div.addEventListener("click", (e) => {
      if (e.target.closest(".start-btn")) return;
      selectAgent(agent.name);
    });

    // Click auf Start-Button
    const startBtn = div.querySelector(".start-btn");
    if (startBtn) {
      startBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        handleStartAgent(agent.name);
      });
    }

    $agentList.appendChild(div);
  }
}

function canAgentStart(agentName) {
  const deps = AGENT_DEPS[agentName] || [];
  return deps.every(dep => {
    const depAgent = agents.find(a => a.name === dep);
    return depAgent && depAgent.status === "done";
  });
}

// ---------------------------------------------------------------------------
// Agent auswählen
// ---------------------------------------------------------------------------
function selectAgent(agentName) {
  currentAgent = agentName;
  currentFile = null;
  const agent = agents.find(a => a.name === agentName);
  if (!agent) return;

  // Highlight aktualisieren
  document.querySelectorAll(".agent-item").forEach(el => {
    el.classList.toggle("selected", el.dataset.agent === agentName);
  });

  $activeAgentLabel.textContent = agent.label;
  $artifactAgentName.textContent = agent.label;

  // Terminal anzeigen
  showTerminal(agentName);

  // Artefakt-Liste + erste Datei laden
  loadArtifactList(agentName);
}

// ---------------------------------------------------------------------------
// Terminal
// ---------------------------------------------------------------------------
function getOrCreateTerminal(agentName) {
  if (terminals[agentName]) return terminals[agentName];

  const term = new Terminal({
    theme: {
      background: "#0a1929",
      foreground: "#dbe1ff",
      cursor: "#80ba24",
      cursorAccent: "#0a1929",
      selectionBackground: "rgba(128, 186, 36, 0.3)",
    },
    fontSize: 12,
    fontFamily: "'SF Mono', 'Fira Code', 'Cascadia Code', monospace",
    cursorBlink: false,
    disableStdin: true,
    convertEol: true,
    scrollback: 10000,
  });

  const fitAddon = new FitAddon.FitAddon();
  term.loadAddon(fitAddon);

  // Persistentes Div erstellen – xterm.js kann open() nur einmal aufrufen
  const div = document.createElement("div");
  div.style.height = "100%";
  div.style.width = "100%";
  div.style.display = "none";
  div.dataset.termAgent = agentName;
  $terminalContainer.appendChild(div);
  term.open(div);

  terminals[agentName] = { term, fitAddon, div };
  return terminals[agentName];
}

function showTerminal(agentName) {
  // Alle Terminal-Divs verstecken
  for (const entry of Object.values(terminals)) {
    entry.div.style.display = "none";
  }

  const { term, fitAddon, div } = getOrCreateTerminal(agentName);
  div.style.display = "block";

  requestAnimationFrame(() => {
    fitAddon.fit();
  });
}

function streamAgent(slug, agentName) {
  // Bestehenden Stream schließen
  if (eventSources[agentName]) {
    eventSources[agentName].close();
  }

  const { term } = getOrCreateTerminal(agentName);
  const es = new EventSource(`/api/projekte/${slug}/agents/${agentName}/stream`);
  eventSources[agentName] = es;

  es.onmessage = (event) => {
    try {
      const text = JSON.parse(event.data);
      term.write(text);
    } catch {
      term.write(event.data);
    }
  };

  es.addEventListener("done", (event) => {
    const exitCode = parseInt(event.data);
    term.write(`\r\n\x1b[${exitCode === 0 ? '32' : '31'}m--- Agent beendet (exit ${exitCode}) ---\x1b[0m\r\n`);
    es.close();
    delete eventSources[agentName];
    // Status aktualisieren
    refreshAgents();
  });

  es.addEventListener("error", (event) => {
    if (es.readyState === EventSource.CLOSED) return;
    term.write("\r\n\x1b[31m--- Verbindung verloren ---\x1b[0m\r\n");
    es.close();
    delete eventSources[agentName];
  });
}

// ---------------------------------------------------------------------------
// Agent starten
// ---------------------------------------------------------------------------
async function handleStartAgent(agentName, feedback = null) {
  const agent = agents.find(a => a.name === agentName);
  if (!agent) return;

  // Erst sichtbar machen, dann schreiben
  selectAgent(agentName);
  switchTab("terminal");

  const { term } = getOrCreateTerminal(agentName);
  if (feedback) {
    term.write(`\r\n\x1b[33m--- Überarbeitung mit Feedback ---\x1b[0m\r\n`);
  } else {
    term.clear();
    term.write(`\x1b[36m--- ${agent.label} wird gestartet ---\x1b[0m\r\n\r\n`);
  }

  const result = await runAgent(currentSlug, agentName, feedback);
  if (result.error) {
    term.write(`\r\n\x1b[31mFehler: ${result.error}\x1b[0m\r\n`);
    return;
  }

  // SSE-Stream starten
  streamAgent(currentSlug, agentName);

  // Status sofort aktualisieren
  await refreshAgents();
}

// ---------------------------------------------------------------------------
// Artefakt-Liste (mittlere Spalte)
// ---------------------------------------------------------------------------
async function loadArtifactList(agentName) {
  if (!currentSlug) return;

  const files = await fetchFiles(currentSlug, agentName);
  const existingFiles = files.filter(f => f.exists);

  $artifactList.innerHTML = "";

  if (existingFiles.length === 0) {
    $artifactList.innerHTML = `
      <div class="p-6 text-center mt-8">
        <div class="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-3 opacity-20">
          <span class="material-symbols-outlined text-[24px]">hourglass_empty</span>
        </div>
        <p class="text-[10px] text-white/30 font-medium">Noch keine Artefakte vorhanden.</p>
      </div>
    `;
    $resultContent.innerHTML = "";
    $previewIframe.srcdoc = "";
    $previewFilename.textContent = "";
    return;
  }

  // "Alle löschen"-Button
  const deleteAllDiv = document.createElement("div");
  deleteAllDiv.className = "px-2 pb-2 border-b border-white/5 mb-1";
  deleteAllDiv.innerHTML = `
    <button class="delete-all-btn w-full flex items-center justify-center gap-1 px-2 py-1.5 text-[10px] text-error/70 hover:text-error hover:bg-error/10 rounded transition-colors">
      <span class="material-symbols-outlined text-[14px]">delete_sweep</span>Alle Artefakte löschen
    </button>
  `;
  deleteAllDiv.querySelector(".delete-all-btn").addEventListener("click", async () => {
    await deleteAgentFiles(currentSlug, agentName);
    await refreshAgents();
    loadArtifactList(agentName);
  });
  $artifactList.appendChild(deleteAllDiv);

  for (const file of existingFiles) {
    const icon = file.name.endsWith(".html") ? "code" : "description";
    const div = document.createElement("div");
    div.className = `artifact-item flex items-center gap-3 p-3 rounded-sm cursor-pointer hover:bg-white/5 transition-colors group`;
    div.dataset.file = file.name;
    div.innerHTML = `
      <span class="material-symbols-outlined text-white/60 text-[20px]">${icon}</span>
      <div class="flex flex-col overflow-hidden flex-1">
        <span class="text-sm text-white font-medium truncate">${file.name}</span>
        <span class="text-[10px] text-white/40">${formatSize(file.size)}</span>
      </div>
      <button class="delete-btn opacity-0 group-hover:opacity-100 w-6 h-6 flex items-center justify-center rounded hover:bg-error/20 text-white/30 hover:text-error transition-all" title="Datei löschen">
        <span class="material-symbols-outlined text-[14px]">close</span>
      </button>
    `;
    div.addEventListener("click", (e) => {
      if (e.target.closest(".delete-btn")) return;
      selectFile(agentName, file.name);
    });
    div.querySelector(".delete-btn").addEventListener("click", async (e) => {
      e.stopPropagation();
      await deleteFile(currentSlug, agentName, file.name);
      await refreshAgents();
      currentFile = null;
      loadArtifactList(agentName);
    });
    $artifactList.appendChild(div);
  }

  // Erste Datei automatisch auswählen
  if (!currentFile || !existingFiles.find(f => f.name === currentFile)) {
    selectFile(agentName, existingFiles[0].name);
  } else {
    selectFile(agentName, currentFile);
  }
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ---------------------------------------------------------------------------
// Einzelne Datei anzeigen
// ---------------------------------------------------------------------------
async function selectFile(agentName, fileName) {
  currentFile = fileName;

  // Highlight in Artefakt-Liste
  document.querySelectorAll(".artifact-item").forEach(el => {
    const selected = el.dataset.file === fileName;
    el.classList.toggle("bg-white/10", selected);
    el.classList.toggle("border-l-2", selected);
    el.classList.toggle("border-thm-light-blue", selected);
  });

  if (!currentSlug) return;

  const content = await fetchFileContent(currentSlug, agentName, fileName);

  if (fileName.endsWith(".html")) {
    // HTML → Ergebnis-Tab zeigt Hinweis, Vorschau-Tab zeigt iframe
    $resultContent.innerHTML = `
      <div class="flex flex-col items-center justify-center h-full text-center py-16">
        <span class="material-symbols-outlined text-thm-green text-4xl mb-4">preview</span>
        <p class="text-white/60 text-sm">HTML-Datei – wechsle zum <strong>Vorschau</strong>-Tab.</p>
      </div>
    `;
    $previewIframe.srcdoc = content;
    $previewFilename.textContent = fileName;
    $previewOpenBtn.onclick = () => {
      const blob = new Blob([content], { type: "text/html" });
      window.open(URL.createObjectURL(blob), "_blank");
    };
  } else {
    // Markdown → rendern im Ergebnis-Tab
    $resultContent.innerHTML = marked.parse(content);
    $previewIframe.srcdoc = "";
    $previewFilename.textContent = "";
  }
}

// ---------------------------------------------------------------------------
// Tabs
// ---------------------------------------------------------------------------
function switchTab(tabName) {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabName);
  });
  $tabTerminal.classList.toggle("hidden", tabName !== "terminal");
  $tabResult.classList.toggle("hidden", tabName !== "result");
  $tabPreview.classList.toggle("hidden", tabName !== "preview");

  // Terminal resize nach Tab-Wechsel
  if (tabName === "terminal" && currentAgent && terminals[currentAgent]) {
    requestAnimationFrame(() => {
      terminals[currentAgent].fitAddon.fit();
    });
  }
}

// ---------------------------------------------------------------------------
// Polling für Status-Updates
// ---------------------------------------------------------------------------
function startPolling() {
  pollInterval = setInterval(async () => {
    if (!currentSlug) return;
    await refreshAgents();
  }, 3000);
}

async function refreshAgents() {
  if (!currentSlug) return;
  const newAgents = await fetchAgents(currentSlug);

  // Prüfe ob sich Status geändert hat
  let changed = false;
  for (let i = 0; i < newAgents.length; i++) {
    if (!agents[i] || agents[i].status !== newAgents[i].status || agents[i].file_count !== newAgents[i].file_count) {
      changed = true;
      break;
    }
  }

  if (changed) {
    agents = newAgents;
    renderAgentList();

    // Artefakt-Liste des aktuellen Agenten neu laden wenn er fertig ist
    const current = agents.find(a => a.name === currentAgent);
    if (current && (current.status === "done" || current.status === "error")) {
      loadArtifactList(currentAgent);
    }
  }
}

// ---------------------------------------------------------------------------
// Event-Listeners
// ---------------------------------------------------------------------------
function setupEventListeners() {
  // Projekt-Dropdown
  $projektDropdownBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    $projektDropdown.classList.toggle("hidden");
  });

  document.addEventListener("click", () => {
    $projektDropdown.classList.add("hidden");
  });

  // Neues Projekt (Dropdown)
  $newProjektBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    $projektDropdown.classList.add("hidden");
    $newProjektModal.classList.remove("hidden");
    document.getElementById("modal-name").focus();
  });

  // Modal schließen
  $modalCancel.addEventListener("click", () => {
    $newProjektModal.classList.add("hidden");
  });

  $newProjektModal.addEventListener("click", (e) => {
    if (e.target === $newProjektModal) {
      $newProjektModal.classList.add("hidden");
    }
  });

  // Modal-Formular
  $newProjektForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("modal-name").value;
    const desc = document.getElementById("modal-desc").value;
    const result = await createProjekt(name, desc);
    $newProjektModal.classList.add("hidden");
    document.getElementById("modal-name").value = "";
    document.getElementById("modal-desc").value = "";
    showDashboard();
    await loadProjekt(result.slug);
  });

  // Welcome-Formular
  $welcomeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("welcome-name").value;
    const desc = document.getElementById("welcome-desc").value;
    const result = await createProjekt(name, desc);
    showDashboard();
    await loadProjekt(result.slug);
  });

  // Tabs
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  // Feedback
  $feedbackBtn.addEventListener("click", () => {
    const feedback = $feedbackInput.value.trim();
    if (!feedback || !currentAgent || !currentSlug) return;
    handleStartAgent(currentAgent, feedback);
    $feedbackInput.value = "";
  });

  $feedbackInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      $feedbackBtn.click();
    }
  });

  // Fenster-Resize → Terminal resize
  window.addEventListener("resize", () => {
    if (currentAgent && terminals[currentAgent]) {
      terminals[currentAgent].fitAddon.fit();
    }
  });

  // Hash-Change
  window.addEventListener("hashchange", () => {
    const slug = location.hash.replace("#", "");
    if (slug && slug !== currentSlug) {
      loadProjekt(slug);
    }
  });
}

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", init);
