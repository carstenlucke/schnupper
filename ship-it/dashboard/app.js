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
let isProduktSelected = false;
let isProduktEditing = false;
let produktRawContent = "";  // Zwischenspeicher für Edit-Modus

// Agent-Abhängigkeiten: welche Agenten müssen "done" sein, bevor dieser starten kann
const AGENT_DEPS = {
  "zielgruppe": [],
  "marketing": ["zielgruppe"],
  "social-media": ["marketing"],
  "kalkulation": [],
  "website": ["zielgruppe", "marketing", "kalkulation"],
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
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: res.statusText }));
    console.error(`API ${res.status}: ${path}`, error);
    return error;
  }
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

async function updateProdukt(slug, content) {
  return api(`/api/projekte/${slug}/produkt`, {
    method: "PUT",
    body: JSON.stringify({ content }),
  });
}

async function generateImage(slug, agent) {
  return api(`/api/projekte/${slug}/generate-image/${agent}`, { method: "POST" });
}

async function fetchAgentPrompt(agentName) {
  return api(`/api/agents/${agentName}/prompt`);
}

function escapeHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
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
const $contentResult = document.getElementById("content-result");
const $contentTerminal = document.getElementById("content-terminal");
const $resultMarkdown = document.getElementById("result-markdown");
const $resultPreview = document.getElementById("result-preview");
const $terminalToggle = document.getElementById("terminal-toggle");
const $artifactList = document.getElementById("artifact-list");
const $artifactAgentName = document.getElementById("artifact-agent-name");
const $produktEntry = document.getElementById("produkt-entry");
const $produktEditBtn = document.getElementById("produkt-edit-btn");
const $produktCancelBtn = document.getElementById("produkt-cancel-btn");

// ---------------------------------------------------------------------------
// Markdown-Konfiguration (HTML in Markdown escapen)
// ---------------------------------------------------------------------------
marked.use({
  renderer: {
    html(token) {
      const text = typeof token === "string" ? token : token.text || "";
      return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
  }
});

// ---------------------------------------------------------------------------
// Farbthema (Hell/Dunkel)
// ---------------------------------------------------------------------------
function initTheme() {
  const saved = localStorage.getItem("ship-it-theme");
  if (saved === "light") {
    document.documentElement.classList.remove("dark");
  }
  updateThemeIcon();
}

function toggleTheme() {
  document.documentElement.classList.toggle("dark");
  const isDark = document.documentElement.classList.contains("dark");
  localStorage.setItem("ship-it-theme", isDark ? "dark" : "light");
  updateThemeIcon();
}

function updateThemeIcon() {
  const isDark = document.documentElement.classList.contains("dark");
  const icon = document.getElementById("theme-toggle-icon");
  if (icon) icon.textContent = isDark ? "light_mode" : "dark_mode";
}

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
  renderProduktEntry();

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
    div.className = `flex items-center gap-2 px-4 py-2.5 cursor-pointer hover:bg-on-surface/5 transition-colors ${p.slug === currentSlug ? 'bg-on-surface/10' : ''}`;
    const statusDot = document.createElement("div");
    statusDot.className = `w-2 h-2 rounded-full projekt-dot-${p.status}`;
    const nameSpan = document.createElement("span");
    nameSpan.className = "text-xs text-on-surface/80";
    nameSpan.textContent = (p.slug === currentSlug ? "✓ " : "") + p.name;
    div.appendChild(statusDot);
    div.appendChild(nameSpan);
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
      statusText = `<span class="text-warning">${agent.file_count} Dateien working...</span>`;
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
          <span class="text-xs font-medium text-on-surface/80">${agent.label}</span>
        </div>
        ${agent.status === "idle" && canStart ? `
          <button class="start-btn w-6 h-6 flex items-center justify-center rounded bg-accent/20 text-accent hover:bg-accent/30 transition-colors" title="Agent starten">
            <span class="material-symbols-outlined text-[14px]">play_arrow</span>
          </button>
        ` : ""}
      </div>
      <div class="flex items-center justify-between ml-4">
        <span class="text-[10px] text-on-surface/40 ${agent.status === 'running' ? 'italic' : ''}">${statusText}</span>
        <div class="flex items-center gap-0.5">
          <button class="prompt-btn prompt-formatted w-5 h-5 flex items-center justify-center rounded hover:bg-on-surface/10 text-on-surface/30 hover:text-accent transition-colors" title="Systemprompt formatiert" aria-label="Systemprompt formatiert anzeigen">
            <span class="material-symbols-outlined text-[14px]">article</span>
          </button>
          <button class="prompt-btn prompt-raw w-5 h-5 flex items-center justify-center rounded hover:bg-on-surface/10 text-on-surface/30 hover:text-accent transition-colors" title="Systemprompt Quelltext" aria-label="Systemprompt als Quelltext anzeigen">
            <span class="material-symbols-outlined text-[14px]">code</span>
          </button>
        </div>
      </div>
    `;

    // Click auf Item → Agent auswählen
    div.addEventListener("click", (e) => {
      if (e.target.closest(".start-btn") || e.target.closest(".prompt-btn")) return;
      selectAgent(agent.name);
    });

    // Click auf Prompt-Buttons
    div.querySelector(".prompt-formatted").addEventListener("click", (e) => {
      e.stopPropagation();
      showAgentPrompt(agent.name, false);
    });
    div.querySelector(".prompt-raw").addEventListener("click", (e) => {
      e.stopPropagation();
      showAgentPrompt(agent.name, true);
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
// Produkt-Eintrag (Sidebar)
// ---------------------------------------------------------------------------
function renderProduktEntry() {
  $produktEntry.innerHTML = "";
  const div = document.createElement("div");
  div.className = `agent-item flex items-center gap-2 p-3 rounded-sm cursor-pointer ${isProduktSelected ? 'selected' : ''}`;
  div.innerHTML = `
    <span class="material-symbols-outlined text-accent text-[18px]">description</span>
    <span class="text-xs font-medium text-on-surface/80">Produkt</span>
  `;
  div.addEventListener("click", () => selectProdukt());
  $produktEntry.appendChild(div);
}

function selectProdukt() {
  // Edit-Modus ggf. verwerfen
  if (isProduktEditing) exitProduktEdit(false);

  isProduktSelected = true;
  currentAgent = null;
  currentFile = "produkt.md";

  // Agent-Highlight entfernen
  document.querySelectorAll(".agent-item").forEach(el => {
    el.classList.remove("selected");
  });
  renderProduktEntry();

  $activeAgentLabel.textContent = "Produkt";
  $artifactAgentName.textContent = "Produkt";

  // Artefakt-Liste: nur produkt.md
  loadProduktArtifact();
  // Inhalt laden
  loadProduktContent();
  // Terminal verstecken, Ergebnis anzeigen
  showResultView();
  // Feedback-Bar verstecken
  $feedbackInput.parentElement.classList.add("hidden");
  // Terminal-Toggle verstecken
  $terminalToggle.classList.add("hidden");
}

function loadProduktArtifact() {
  $artifactList.innerHTML = "";
  const div = document.createElement("div");
  div.className = "artifact-item flex items-center gap-3 p-3 rounded-sm bg-on-surface/10 border-l-2 border-accent";
  div.innerHTML = `
    <span class="material-symbols-outlined text-on-surface/60 text-[20px]">description</span>
    <div class="flex flex-col overflow-hidden flex-1">
      <span class="text-sm text-on-surface font-medium truncate">produkt.md</span>
      <span class="text-[10px] text-on-surface/40">Produktbeschreibung</span>
    </div>
  `;
  $artifactList.appendChild(div);
}

function fetchProduktContent(slug) {
  return fetchFileContent(slug, "zielgruppe", "produkt.md");
}

async function loadProduktContent() {
  if (!currentSlug) return;
  const content = await fetchProduktContent(currentSlug);
  produktRawContent = content;

  $resultMarkdown.classList.remove("hidden");
  $resultPreview.classList.add("hidden");
  $resultContent.innerHTML = marked.parse(content, { breaks: true, gfm: true });
  $previewFilename.textContent = "produkt.md";
  $previewOpenBtn.classList.add("hidden");
  $previewOpenBtn.classList.remove("flex");

  // Bearbeiten-Button anzeigen
  $produktEditBtn.classList.remove("hidden");
  $produktEditBtn.classList.add("flex");
  $produktEditBtn.innerHTML = `<span class="material-symbols-outlined text-[14px]">edit</span>Bearbeiten`;
  $produktCancelBtn.classList.add("hidden");
  $produktCancelBtn.classList.remove("flex");
}

function enterProduktEdit() {
  isProduktEditing = true;
  $resultContent.textContent = "";
  const textarea = document.createElement("textarea");
  textarea.id = "produkt-editor";
  textarea.className = "w-full h-full min-h-[300px] px-6 py-6 bg-on-surface/5 border border-on-surface/10 rounded-lg text-on-surface text-sm focus:border-accent focus:ring-1 focus:ring-accent outline-none resize-none";
  textarea.value = produktRawContent;
  $resultContent.appendChild(textarea);
  // Button auf "Speichern" umschalten
  $produktEditBtn.innerHTML = `<span class="material-symbols-outlined text-[14px]">save</span>Speichern`;
  $produktCancelBtn.classList.remove("hidden");
  $produktCancelBtn.classList.add("flex");
}

async function exitProduktEdit(save) {
  if (save) {
    const editor = document.getElementById("produkt-editor");
    if (!editor) return;
    const content = editor.value;
    if (!content.trim()) {
      editor.classList.add("border-error");
      editor.placeholder = "Produktbeschreibung darf nicht leer sein";
      return;
    }
    // Buttons während Speichern deaktivieren
    $produktEditBtn.disabled = true;
    $produktCancelBtn.disabled = true;
    const result = await updateProdukt(currentSlug, content);
    $produktEditBtn.disabled = false;
    $produktCancelBtn.disabled = false;
    if (result.error) {
      editor.classList.add("border-error");
      return;
    }
    produktRawContent = content;
    // Projektname im Dropdown aktualisieren
    const projekte = await fetchProjekte();
    renderProjektDropdown(projekte);
    const projekt = projekte.find(p => p.slug === currentSlug);
    if (projekt) {
      $projektNameDisplay.textContent = projekt.name;
    }
  }
  isProduktEditing = false;
  // Markdown neu rendern
  $resultContent.innerHTML = marked.parse(produktRawContent, { breaks: true, gfm: true });
  $produktEditBtn.innerHTML = `<span class="material-symbols-outlined text-[14px]">edit</span>Bearbeiten`;
  $produktCancelBtn.classList.add("hidden");
  $produktCancelBtn.classList.remove("flex");
}

// ---------------------------------------------------------------------------
// Agent auswählen
// ---------------------------------------------------------------------------
function selectAgent(agentName) {
  // Produkt-Modus verlassen
  if (isProduktEditing) exitProduktEdit(false);
  isProduktSelected = false;
  renderProduktEntry();
  $produktEditBtn.classList.add("hidden");
  $produktEditBtn.classList.remove("flex");
  $produktCancelBtn.classList.add("hidden");
  $produktCancelBtn.classList.remove("flex");
  $feedbackInput.parentElement.classList.remove("hidden");
  $terminalToggle.classList.remove("hidden");

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
// Terminal (immer dunkel/Anthrazit, unabhängig vom Farbthema)
// ---------------------------------------------------------------------------
function getOrCreateTerminal(agentName) {
  if (terminals[agentName]) return terminals[agentName];

  const term = new Terminal({
    theme: {
      background: "#181f23",
      foreground: "#e0e3e5",
      cursor: "#80ba24",
      cursorAccent: "#181f23",
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

  es.addEventListener("not_started", (event) => {
    term.write(`\r\n\x1b[33m--- ${event.data} ---\x1b[0m\r\n`);
    es.close();
    delete eventSources[agentName];
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
  showTerminalView();

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
        <div class="w-12 h-12 rounded-full bg-on-surface/5 flex items-center justify-center mx-auto mb-3 opacity-20">
          <span class="material-symbols-outlined text-[24px]">hourglass_empty</span>
        </div>
        <p class="text-[10px] text-on-surface/30 font-medium">Noch keine Artefakte vorhanden.</p>
      </div>
    `;
    $resultContent.innerHTML = "";
    $previewIframe.srcdoc = "";
    $previewFilename.textContent = "";
    $previewOpenBtn.classList.add("hidden");
    $previewOpenBtn.classList.remove("flex");
    $resultMarkdown.classList.remove("hidden");
    $resultPreview.classList.add("hidden");
    return;
  }

  // "Alle löschen"-Button
  const deleteAllDiv = document.createElement("div");
  deleteAllDiv.className = "px-2 pb-2 border-b border-on-surface/5 mb-1";
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
    const icon = file.name.endsWith(".html") ? "code" : file.name.endsWith(".png") ? "image" : "description";
    const div = document.createElement("div");
    div.className = `artifact-item flex items-center gap-3 p-3 rounded-sm cursor-pointer hover:bg-on-surface/5 transition-colors group`;
    div.dataset.file = file.name;
    div.innerHTML = `
      <span class="material-symbols-outlined text-on-surface/60 text-[20px]">${icon}</span>
      <div class="flex flex-col overflow-hidden flex-1">
        <span class="text-sm text-on-surface font-medium truncate">${file.name}</span>
        <span class="text-[10px] text-on-surface/40">${formatSize(file.size)}</span>
      </div>
      <button class="delete-btn opacity-0 group-hover:opacity-100 w-6 h-6 flex items-center justify-center rounded hover:bg-error/20 text-on-surface/30 hover:text-error transition-all" title="Datei löschen">
        <span class="material-symbols-outlined text-[14px]">close</span>
      </button>
    `;
    div.addEventListener("click", (e) => {
      if (e.target.closest(".delete-btn")) return;
      selectFile(agentName, file.name, { switchToResult: true });
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

  // Bildgenerierungs-Buttons (pro Agent konfiguriert)
  const IMAGE_GEN = {
    "marketing":    { trigger: "konzept.md",   image: "logo.png",           label: "Logo generieren",  labelRegen: "Logo neu generieren" },
    "social-media": { trigger: "instagram.md", image: "instagram-bild.png", label: "Bild generieren",  labelRegen: "Bild neu generieren" },
  };
  const genCfg = IMAGE_GEN[agentName];
  if (genCfg) {
    const triggerExists = existingFiles.some(f => f.name === genCfg.trigger);
    const imageExists = existingFiles.some(f => f.name === genCfg.image);

    if (triggerExists) {
      const btnLabel = imageExists ? genCfg.labelRegen : genCfg.label;
      const btnIcon = imageExists ? "refresh" : "auto_awesome";
      const btnDiv = document.createElement("div");
      btnDiv.className = "px-2 pt-2 mt-1 border-t border-on-surface/5";
      btnDiv.innerHTML = `
        <button id="generate-image-btn"
                class="w-full flex items-center justify-center gap-2 px-3 py-2.5 text-xs font-bold bg-accent/20 text-accent hover:bg-accent/30 rounded transition-colors"
                aria-label="${btnLabel}"
                data-agent="${agentName}" data-image="${genCfg.image}">
          <span class="material-symbols-outlined text-[16px]">${btnIcon}</span>
          ${btnLabel}
        </button>
      `;
      btnDiv.querySelector("#generate-image-btn").addEventListener("click", () => {
        handleGenerateImage(agentName, genCfg.image);
      });
      $artifactList.appendChild(btnDiv);
    }
  }

  // Erste Datei automatisch auswählen
  if (!currentFile || !existingFiles.find(f => f.name === currentFile)) {
    selectFile(agentName, existingFiles[0].name);
  } else {
    selectFile(agentName, currentFile);
  }
}

async function handleGenerateImage(agentName, imageFileName) {
  const btn = document.getElementById("generate-image-btn");
  if (!btn || !currentSlug) return;

  const originalHTML = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `
    <span class="material-symbols-outlined text-[16px] spin-slow">progress_activity</span>
    Bild wird generiert\u2026
  `;

  try {
    const result = await generateImage(currentSlug, agentName);

    if (result.error) {
      const errorSpan = document.createElement("span");
      errorSpan.className = "text-red-400";
      errorSpan.textContent = result.error;
      btn.innerHTML = `<span class="material-symbols-outlined text-[16px] text-red-400">error</span>`;
      btn.appendChild(errorSpan);
      setTimeout(() => {
        btn.innerHTML = originalHTML;
      }, 3000);
      return;
    }

    await loadArtifactList(agentName);
    selectFile(agentName, imageFileName, { switchToResult: true });
  } catch (error) {
    console.error("Fehler bei der Bildgenerierung:", error);
    btn.innerHTML = `
      <span class="material-symbols-outlined text-[16px] text-red-400">error</span>
      <span class="text-red-400">Unerwarteter Fehler bei der Bildgenerierung.</span>
    `;
    setTimeout(() => {
      btn.innerHTML = originalHTML;
    }, 3000);
  } finally {
    btn.disabled = false;
  }
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ---------------------------------------------------------------------------
// Agenten-Systemprompt anzeigen
// ---------------------------------------------------------------------------
async function showAgentPrompt(agentName, raw) {
  // Agent auswählen, falls noch nicht selektiert
  if (currentAgent !== agentName) {
    selectAgent(agentName);
  }

  const data = await fetchAgentPrompt(agentName);
  if (data.error) {
    $resultContent.innerHTML = `<p class="text-error">${escapeHtml(data.error)}</p>`;
    showResultView();
    return;
  }

  // Meta-Badges
  const metaHtml = `<div class="mb-4 flex flex-wrap gap-2">${
    data.meta.model
      ? `<span class="inline-flex items-center gap-1 px-2 py-1 text-[10px] font-medium bg-accent/10 text-accent rounded-full">
          <span class="material-symbols-outlined text-[12px]">smart_toy</span>${escapeHtml(data.meta.model)}</span>`
      : ''
  }${
    data.meta.description
      ? `<span class="inline-flex items-center gap-1 px-2 py-1 text-[10px] font-medium bg-on-surface/5 text-on-surface/60 rounded-full">${escapeHtml(data.meta.description)}</span>`
      : ''
  }</div>`;

  $resultMarkdown.classList.remove("hidden");
  $resultPreview.classList.add("hidden");

  if (raw) {
    $resultContent.innerHTML = metaHtml + `<pre class="prompt-source">${escapeHtml(data.raw)}</pre>`;
  } else {
    $resultContent.innerHTML = metaHtml + marked.parse(data.body, { breaks: true, gfm: true });
  }

  $previewFilename.textContent = "Systemprompt";
  $previewOpenBtn.classList.add("hidden");
  $previewOpenBtn.classList.remove("flex");
  $produktEditBtn.classList.add("hidden");
  $produktEditBtn.classList.remove("flex");
  $produktCancelBtn.classList.add("hidden");

  showResultView();
}

// ---------------------------------------------------------------------------
// Einzelne Datei anzeigen
// ---------------------------------------------------------------------------
async function selectFile(agentName, fileName, { switchToResult = false } = {}) {
  currentFile = fileName;

  // Highlight in Artefakt-Liste
  document.querySelectorAll(".artifact-item").forEach(el => {
    const selected = el.dataset.file === fileName;
    el.classList.toggle("bg-on-surface/10", selected);
    el.classList.toggle("border-l-2", selected);
    el.classList.toggle("border-accent", selected);
  });

  if (!currentSlug) return;

  // Bilder direkt als <img> anzeigen
  if (fileName.endsWith(".png")) {
    $resultMarkdown.classList.remove("hidden");
    $resultPreview.classList.add("hidden");
    const imageUrl = `/api/projekte/${currentSlug}/files/${agentName}/${fileName}`;
    $resultContent.innerHTML = `
      <div class="flex flex-col items-center gap-4 py-4">
        <img src="${imageUrl}" alt="Generiertes Bild"
             class="max-w-full rounded-lg shadow-lg max-h-[70vh]" />
        <p class="text-xs text-on-surface/40">KI-generiertes Bild (Vorschau)</p>
      </div>
    `;
    $previewFilename.textContent = fileName;
    $previewOpenBtn.classList.add("hidden");
    $previewOpenBtn.classList.remove("flex");
    if (switchToResult) showResultView();
    return;
  }

  const content = await fetchFileContent(currentSlug, agentName, fileName);

  if (fileName.endsWith(".html")) {
    // HTML → iframe-Vorschau
    $resultMarkdown.classList.add("hidden");
    $resultPreview.classList.remove("hidden");
    $previewIframe.srcdoc = content;
    $previewFilename.textContent = fileName;
    $previewOpenBtn.classList.remove("hidden");
    $previewOpenBtn.classList.add("flex");
    $previewOpenBtn.onclick = () => {
      const blob = new Blob([content], { type: "text/html" });
      window.open(URL.createObjectURL(blob), "_blank");
    };
  } else {
    // Markdown → rendern
    $resultMarkdown.classList.remove("hidden");
    $resultPreview.classList.add("hidden");
    $resultContent.innerHTML = marked.parse(content, { breaks: true, gfm: true });
    $previewFilename.textContent = "";
    $previewOpenBtn.classList.add("hidden");
    $previewOpenBtn.classList.remove("flex");
  }

  // Zur Ergebnis-Ansicht wechseln bei explizitem User-Klick,
  // aber nicht bei Auto-Selektion (z.B. wenn ein Agent läuft)
  if (switchToResult) {
    showResultView();
  }
}

// ---------------------------------------------------------------------------
// Content-Ansicht umschalten (Ergebnis ↔ Terminal)
// ---------------------------------------------------------------------------
let terminalVisible = false;

function showTerminalView() {
  terminalVisible = true;
  $contentTerminal.classList.remove("hidden");
  $contentResult.classList.add("hidden");
  $terminalToggle.classList.add("text-accent");
  $terminalToggle.classList.remove("text-on-surface/40");
  if (currentAgent && terminals[currentAgent]) {
    requestAnimationFrame(() => terminals[currentAgent].fitAddon.fit());
  }
}

function showResultView() {
  terminalVisible = false;
  $contentResult.classList.remove("hidden");
  $contentTerminal.classList.add("hidden");
  $terminalToggle.classList.remove("text-accent");
  $terminalToggle.classList.add("text-on-surface/40");
}

function toggleTerminalView() {
  terminalVisible ? showResultView() : showTerminalView();
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

  // Terminal-Toggle
  $terminalToggle.addEventListener("click", toggleTerminalView);

  // Theme Toggle
  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

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

  // Produkt bearbeiten / speichern
  $produktEditBtn.addEventListener("click", async () => {
    if (isProduktEditing) {
      await exitProduktEdit(true);
    } else {
      enterProduktEdit();
    }
  });

  $produktCancelBtn.addEventListener("click", async () => {
    await exitProduktEdit(false);
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
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  init();
});
