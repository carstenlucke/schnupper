// Agent Party – Dashboard
// Ein klassisches Skript im globalen Scope, kein Modul, kein Bundler.

// ---------------------------------------------------------------------------
// Konstanten
// ---------------------------------------------------------------------------
const FARBEN = [
  { wert: "gruen", label: "Grün" },
  { wert: "grau", label: "Grau" },
  { wert: "rot", label: "Rot" },
  { wert: "gelb", label: "Gelb" },
  { wert: "hellblau", label: "Hellblau" },
  { wert: "blau", label: "Blau" },
];

// So viele Plätze hat der Tisch — dieselbe Grenze wie MAX_TEILNEHMER im Server.
const MAX_TEILNEHMER = 8;
// Obergrenze im Formular — MAX_RUNDEN im Server. „Weitere Runde" darf darüber.
const MAX_RUNDEN = 5;

const STATUS_TEXT = {
  neu: "Noch nicht gestartet",
  laeuft: "Läuft",
  pausiert: "Angehalten",
  fertig: "Fertig",
  fehler: "Abgebrochen",
};

// ---------------------------------------------------------------------------
// Zustand
// ---------------------------------------------------------------------------
let ansicht = "profile";        // "profile" | "einrichten" | "party"
let profile = [];               // Serverliste, Quelle der Wahrheit für Name und Farbe
let gruppen = [];               // [{name, profile: [slug]}] wie in profile/gruppen.json
let gruppenKette = Promise.resolve(); // Speichervorgänge der Gruppen, nacheinander
let zugeklappt = new Set();     // eingeklappte Gruppen: Name, "" für „Ohne Gruppe"
let auswahlZugeklappt = new Set(); // dasselbe für „Party vorbereiten", eigener Zustand
let gezogen = null;             // Slug der Kachel, die gerade gezogen wird
let modelle = [];
let editorSlug = null;          // null = neues Profil
let entwurfAbbruch = null;      // AbortController; nicht-null = Entwurf läuft
let besetzung = [];             // Slugs in Sprechreihenfolge, jeder höchstens einmal
let bearbeitung = null;         // {slug, sitzung, status}: Party, die „Party vorbereiten" gerade ändert
let aktuelleParty = null;       // {slug, sitzung, status, erwartet}
let partyQuelle = null;         // EventSource
let aktiveBlase = null;         // {wurzel, textEl, denkEl, roh}
let fertigeBeitraege = 0;
let zwischenrufe = 0;           // Einwürfe der Gesprächsleitung in dieser Sitzung
let letzteRunde = 0;            // für den Rundentrenner im Verlauf
let beitragZaehler = {};        // Slug -> Anzahl Beiträge, für die Teilnehmerkarte
let scrollAngefordert = false;

// ---------------------------------------------------------------------------
// API
// ---------------------------------------------------------------------------
async function api(pfad, opts = {}) {
  try {
    const res = await fetch(pfad, {
      headers: { "Content-Type": "application/json" },
      ...opts,
    });
    if (res.status === 204) return {};
    const daten = await res.json();
    if (!res.ok) return { fehler: daten.fehler || `Fehler ${res.status}`, ...daten };
    return daten;
  } catch (e) {
    return { fehler: "Der Server antwortet nicht." };
  }
}

const ladeProfile = () => api("/api/profile");
const ladeModelle = () => api("/api/modelle");
const ladePartys = () => api("/api/partys");
const ladeParty = (slug) => api(`/api/partys/${slug}`);

const neuesProfil = (daten) =>
  api("/api/profile", { method: "POST", body: JSON.stringify(daten) });
const aendereProfil = (slug, daten) =>
  api(`/api/profile/${slug}`, { method: "PUT", body: JSON.stringify(daten) });
const entferneProfil = (slug, erzwingen) =>
  api(`/api/profile/${slug}${erzwingen ? "?force=1" : ""}`, { method: "DELETE" });
const ladeGruppen = () => api("/api/gruppen");
const setzeGruppen = (liste) =>
  api("/api/gruppen", { method: "PUT", body: JSON.stringify(liste) });

const neueParty = (daten) =>
  api("/api/partys", { method: "POST", body: JSON.stringify(daten) });
const starteParty = (slug) => api(`/api/partys/${slug}/start`, { method: "POST" });
const stoppeParty = (slug) => api(`/api/partys/${slug}/stop`, { method: "POST" });
const wirfEin = (slug, text) =>
  api(`/api/partys/${slug}/zwischenruf`, { method: "POST", body: JSON.stringify({ text }) });
const haengeRundeAn = (slug) => api(`/api/partys/${slug}/runde`, { method: "POST" });
const starteFazit = (slug) => api(`/api/partys/${slug}/fazit`, { method: "POST" });
const entferneParty = (slug) => api(`/api/partys/${slug}`, { method: "DELETE" });
const aendereParty = (slug, daten) =>
  api(`/api/partys/${slug}`, { method: "PUT", body: JSON.stringify(daten) });
const setzePartyZurueck = (slug) =>
  api(`/api/partys/${slug}/zuruecksetzen`, { method: "POST" });

// ---------------------------------------------------------------------------
// DOM-Handles
// ---------------------------------------------------------------------------
const $inhalt = document.querySelector("main");
const $tabProfile = document.getElementById("tab-profile");
const $tabEinrichten = document.getElementById("tab-einrichten");
const $tabParty = document.getElementById("tab-party");
const $ansichtProfile = document.getElementById("ansicht-profile");
const $ansichtEinrichten = document.getElementById("ansicht-einrichten");
const $ansichtParty = document.getElementById("ansicht-party");

const $profilGruppen = document.getElementById("profil-gruppen");
const $profileAnzahl = document.getElementById("profile-anzahl");
const $neueGruppeBtn = document.getElementById("neue-gruppe-btn");
const $alleKlappenBtn = document.getElementById("alle-klappen-btn");
const $alleKlappenIcon = document.getElementById("alle-klappen-icon");
const $alleKlappenText = document.getElementById("alle-klappen-text");
const $gruppenHinweis = document.getElementById("gruppen-hinweis");
const $editorBreiteBtn = document.getElementById("editor-breite-btn");
const $editorBreiteIcon = document.getElementById("editor-breite-icon");
const $editorTitel = document.getElementById("editor-titel");
const $feldName = document.getElementById("feld-name");
const $feldBeschreibung = document.getElementById("feld-beschreibung");
const $feldModel = document.getElementById("feld-model");
const $feldThinking = document.getElementById("feld-thinking");
const $farbwahl = document.getElementById("farbwahl");
const $feldGruppe = document.getElementById("feld-gruppe");
const $feldText = document.getElementById("feld-text");
const $speichernBtn = document.getElementById("speichern-btn");
const $abbrechenBtn = document.getElementById("abbrechen-btn");
const $loeschenBtn = document.getElementById("loeschen-btn");
const $duplizierenBtn = document.getElementById("duplizieren-btn");
const $editorHinweis = document.getElementById("editor-hinweis");

const $entwurfIdee = document.getElementById("entwurf-idee");
const $entwurfBtn = document.getElementById("entwurf-btn");
const $entwurfBtnText = document.getElementById("entwurf-btn-text");
const $entwurfStatus = document.getElementById("entwurf-status");
const $entwurfDenkenBox = document.getElementById("entwurf-denken-box");
const $entwurfDenken = document.getElementById("entwurf-denken");

const $auswahlRaster = document.getElementById("auswahl-raster");
const $besetzung = document.getElementById("besetzung");
const $partyListe = document.getElementById("party-liste");
const $feldTitel = document.getElementById("feld-titel");
const $feldStarter = document.getElementById("feld-starter");
const $feldRunden = document.getElementById("feld-runden");
const $feldPartymodell = document.getElementById("feld-partymodell");
const $partyStartBtn = document.getElementById("party-start-btn");
const $partyStartIcon = document.getElementById("party-start-icon");
const $partyStartText = document.getElementById("party-start-text");
const $bearbeitenAbbrechenBtn = document.getElementById("bearbeiten-abbrechen-btn");
const $rundeTitel = document.getElementById("runde-titel");
const $bearbeitenInfo = document.getElementById("bearbeiten-info");
const $einrichtenHinweis = document.getElementById("einrichten-hinweis");

const $partyTitel = document.getElementById("party-titel");
const $partyStarter = document.getElementById("party-starter");
const $partyMeta = document.getElementById("party-meta");
const $partyStatusBadge = document.getElementById("party-status-badge");
const $partyFortschritt = document.getElementById("party-fortschritt");
const $teilnehmerListe = document.getElementById("teilnehmer-liste");
const $kennzahlRunde = document.getElementById("kennzahl-runde");
const $kennzahlBeitraege = document.getElementById("kennzahl-beitraege");
const $kennzahlZwischenrufe = document.getElementById("kennzahl-zwischenrufe");
const $verlauf = document.getElementById("verlauf");
const $blasenVorlage = document.getElementById("blasen-vorlage");
const $zwischenrufVorlage = document.getElementById("zwischenruf-vorlage");
const $rundenVorlage = document.getElementById("runden-vorlage");

const $steuerleiste = document.getElementById("steuerleiste");
const $zwischenrufFeld = document.getElementById("zwischenruf-feld");
const $einwerfenBtn = document.getElementById("einwerfen-btn");
const $rundeBtn = document.getElementById("runde-btn");
const $fazitBtn = document.getElementById("fazit-btn");
const $partyStopBtn = document.getElementById("party-stop-btn");
const $partyFortBtn = document.getElementById("party-fort-btn");
const $partyFortText = document.getElementById("party-fort-text");
const $partyBearbeitenBtn = document.getElementById("party-bearbeiten-btn");
const $partyZurueckBtn = document.getElementById("party-zurueck-btn");
const $neuePartyBtn = document.getElementById("neue-party-btn");
const $steuerHinweis = document.getElementById("steuer-hinweis");

const $dialogHintergrund = document.getElementById("dialog-hintergrund");
const $dialogTitel = document.getElementById("dialog-titel");
const $dialogText = document.getElementById("dialog-text");
const $dialogEingabe = document.getElementById("dialog-eingabe");
const $dialogOk = document.getElementById("dialog-ok");
const $dialogAbbrechen = document.getElementById("dialog-abbrechen");

// ---------------------------------------------------------------------------
// Helfer
// ---------------------------------------------------------------------------
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text == null ? "" : String(text);
  return div.innerHTML;
}

// marked soll rohes HTML aus Modellantworten nicht ausführen.
marked.use({
  breaks: true,
  gfm: true,
  renderer: {
    html(token) {
      return escapeHtml(typeof token === "string" ? token : token.raw || "");
    },
  },
});

function profilFinden(slug) {
  return profile.find((p) => p.slug === slug) || null;
}

/** Liest einen POST-SSE-Strom. EventSource kann kein POST — daher fetch. */
async function sseLesen(res, aufEreignis) {
  const leser = res.body.getReader();
  const dekoder = new TextDecoder();
  let puffer = "";
  while (true) {
    const { done, value } = await leser.read();
    if (done) break;
    puffer += dekoder.decode(value, { stream: true });
    let trenner;
    while ((trenner = puffer.indexOf("\n\n")) !== -1) {
      const block = puffer.slice(0, trenner);
      puffer = puffer.slice(trenner + 2);
      if (block.startsWith("event: done")) return;
      for (const zeile of block.split("\n")) {
        if (!zeile.startsWith("data: ")) continue;
        try {
          aufEreignis(JSON.parse(zeile.slice(6)));
        } catch (e) {
          /* unvollständige Zeile – ignorieren */
        }
      }
    }
  }
}

/** Spiegel des Server-Parsers: trennt Frontmatter vom Rollentext. */
function frontmatterTrennen(text) {
  if (!text.startsWith("---")) return null;
  const ende = text.indexOf("---", 3);
  if (ende === -1) return null;
  const meta = {};
  for (const zeile of text.slice(3, ende).trim().split("\n")) {
    if (!zeile.includes(":") || zeile.startsWith(" ")) continue;
    const trenner = zeile.indexOf(":");
    meta[zeile.slice(0, trenner).trim()] = zeile.slice(trenner + 1).trim();
  }
  return { meta, rumpf: text.slice(ende + 3).trim() };
}

function zeigeHinweis(element, text) {
  if (!text) {
    element.classList.add("hidden");
    element.textContent = "";
    return;
  }
  element.textContent = text;
  element.classList.remove("hidden");
}

function scrolleWennAmEnde() {
  const abstand = $inhalt.scrollHeight - $inhalt.scrollTop - $inhalt.clientHeight;
  // Wer nach oben gescrollt hat, um einen früheren Beitrag zu lesen, wird
  // nicht weggerissen.
  if (abstand > 120 || scrollAngefordert) return;
  scrollAngefordert = true;
  requestAnimationFrame(() => {
    $inhalt.scrollTop = $inhalt.scrollHeight;
    scrollAngefordert = false;
  });
}

// ---------------------------------------------------------------------------
// Farbthema (Hell/Dunkel)
// Die Farbwerte stehen in style.css. Hier wird nur die Klasse "dark" am
// <html>-Element geschaltet: gespeicherte Wahl → Systemeinstellung.
// ---------------------------------------------------------------------------
const THEME_KEY = "agent-party-theme";
const systemDunkel = window.matchMedia("(prefers-color-scheme: dark)");

function gespeichertesTheme() {
  try {
    return localStorage.getItem(THEME_KEY);
  } catch (e) {
    return null;
  }
}

function setzeTheme(dunkel) {
  document.documentElement.classList.toggle("dark", dunkel);
  const icon = document.getElementById("theme-toggle-icon");
  const btn = document.getElementById("theme-toggle");
  icon.textContent = dunkel ? "light_mode" : "dark_mode";
  const label = dunkel
    ? "Zum hellen Farbthema wechseln"
    : "Zum dunklen Farbthema wechseln";
  btn.setAttribute("aria-label", label);
  btn.title = label;
}

function initTheme() {
  const wahl = gespeichertesTheme();
  setzeTheme(wahl ? wahl === "dark" : systemDunkel.matches);
  // Solange nichts gespeichert ist, folgt das Dashboard der Systemeinstellung.
  systemDunkel.addEventListener("change", (e) => {
    if (!gespeichertesTheme()) setzeTheme(e.matches);
  });
}

function wechsleTheme() {
  const dunkel = !document.documentElement.classList.contains("dark");
  try {
    localStorage.setItem(THEME_KEY, dunkel ? "dark" : "light");
  } catch (e) {}
  setzeTheme(dunkel);
}

// ---------------------------------------------------------------------------
// Dialog
// ---------------------------------------------------------------------------
/** Mit `eingabe` ({wert, platzhalter}) fragt der Dialog nach einem Text und
    liefert ihn getrimmt zurück — oder null bei Abbruch. Sonst true/false. */
function zeigeDialog({ titel, text, okText = "OK", mitAbbrechen = true, eingabe = null }) {
  return new Promise((aufloesen) => {
    $dialogTitel.textContent = titel;
    $dialogText.textContent = text || "";
    $dialogText.classList.toggle("hidden", !text);
    $dialogEingabe.classList.toggle("hidden", !eingabe);
    $dialogOk.textContent = okText;
    $dialogAbbrechen.classList.toggle("hidden", !mitAbbrechen);
    $dialogHintergrund.classList.remove("hidden");

    const schliessen = (ok) => {
      $dialogHintergrund.classList.add("hidden");
      $dialogOk.removeEventListener("click", aufOk);
      $dialogAbbrechen.removeEventListener("click", aufAbbruch);
      $dialogEingabe.removeEventListener("keydown", aufTaste);
      if (!eingabe) return aufloesen(ok);
      aufloesen(ok ? $dialogEingabe.value.trim() : null);
    };
    const aufOk = () => schliessen(true);
    const aufAbbruch = () => schliessen(false);
    const aufTaste = (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        schliessen(true);
      } else if (e.key === "Escape") {
        schliessen(false);
      }
    };

    $dialogOk.addEventListener("click", aufOk);
    $dialogAbbrechen.addEventListener("click", aufAbbruch);
    if (eingabe) {
      $dialogEingabe.value = eingabe.wert || "";
      $dialogEingabe.placeholder = eingabe.platzhalter || "";
      $dialogEingabe.addEventListener("keydown", aufTaste);
      $dialogEingabe.focus();
      $dialogEingabe.select();
    }
  });
}

// ---------------------------------------------------------------------------
// Ansichtswechsel
// ---------------------------------------------------------------------------
function zeigeAnsicht(name, arg) {
  if (ansicht === "party" && name !== "party") schliesseStrom();
  ansicht = name;

  $ansichtProfile.hidden = name !== "profile";
  $ansichtEinrichten.hidden = name !== "einrichten";
  $ansichtParty.hidden = name !== "party";
  $steuerleiste.hidden = name !== "party";
  $tabProfile.setAttribute("aria-selected", String(name === "profile"));
  $tabEinrichten.setAttribute("aria-selected", String(name === "einrichten"));
  $tabParty.setAttribute("aria-selected", String(name === "party"));
  $inhalt.scrollTop = 0;

  if (name === "profile") {
    setzeHash("#profile");
    ladeUndRendereProfile();
  } else if (name === "einrichten") {
    // Über Navigation, Hash oder „Neue Party" heißt die Ansicht: neue Party.
    // Nur starteBearbeitung() kommt mit "bearbeiten" hierher.
    if (arg !== "bearbeiten" && bearbeitung) beendeBearbeitung();
    setzeHash("#einrichten");
    ladeUndRendereEinrichten();
  } else if (name === "party" && arg) {
    setzeHash(`#party/${arg}`);
    oeffneParty(arg);
  }
}

/** Adresszeile nachziehen, ohne die Ansicht ein zweites Mal zu laden.
    `location.hash = …` würde hashchange auslösen und damit zeigeAnsicht
    erneut aufrufen; pushState tut das nicht, die Zurück-Taste funktioniert
    trotzdem (siehe popstate-Listener). */
function setzeHash(wert) {
  if (location.hash !== wert) history.pushState(null, "", wert);
}

function ausHash() {
  const hash = location.hash.slice(1);
  if (hash.startsWith("party/")) return zeigeAnsicht("party", hash.slice(6));
  if (hash === "einrichten") return zeigeAnsicht("einrichten");
  return zeigeAnsicht("profile");
}

// ---------------------------------------------------------------------------
// Ansicht 1: Profile
// ---------------------------------------------------------------------------
function baueKachel(profil, { auswaehlbar = false } = {}) {
  const kachel = document.createElement("div");
  kachel.className = `kachel profil-${profil.farbe} p-3 ${auswaehlbar ? "cursor-pointer" : ""}`;
  kachel.innerHTML = `
    <div class="flex items-start gap-2">
      <div class="min-w-0 flex-1">
        <div class="profil-schrift font-headline font-semibold text-sm truncate">${escapeHtml(profil.name)}</div>
        <div class="text-xs text-on-surface-variant mt-0.5 line-clamp-2">${escapeHtml(profil.beschreibung)}</div>
        <div class="text-[11px] text-on-surface-variant/80 mt-2 truncate">${escapeHtml(profil.model || "Standardmodell")}</div>
      </div>
      ${auswaehlbar ? "" : `
      <button class="kachel-bearbeiten shrink-0 p-1 rounded hover:bg-on-surface/10 transition-colors"
              aria-label="Profil bearbeiten" title="Profil bearbeiten">
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant" aria-hidden="true">edit</span>
      </button>`}
    </div>`;
  return kachel;
}

/** Die Profile nach Gruppen, wie beide Ansichten sie zeigen: erst die Gruppen
    aus `gruppen.json` in ihrer Reihenfolge, zuletzt „Ohne Gruppe" (Index -1)
    mit allen übrigen. */
function profileNachGruppen() {
  const einsortiert = new Set();
  const liste = gruppen.map((gruppe, index) => {
    const mitglieder = gruppe.profile.map(profilFinden).filter(Boolean);
    mitglieder.forEach((p) => einsortiert.add(p.slug));
    return { name: gruppe.name, index, mitglieder };
  });
  const rest = profile.filter((p) => !einsortiert.has(p.slug));
  liste.push({ name: "Ohne Gruppe", index: -1, mitglieder: rest });
  return liste;
}

function rendereProfilGruppen() {
  $profilGruppen.innerHTML = "";
  $profileAnzahl.textContent = `${profile.length} ${profile.length === 1 ? "Profil" : "Profile"}`;

  // „Ohne Gruppe" steht immer da, als Rest und als Ablage zum Herausnehmen.
  profileNachGruppen().forEach(({ name, index, mitglieder }) => {
    $profilGruppen.appendChild(baueGruppe(name, index, mitglieder));
  });
  aktualisiereAlleKlappen();
}

/** Schlüssel aller Gruppen, wie `zugeklappt` sie führt — "" ist „Ohne Gruppe". */
function alleGruppenSchluessel() {
  return [...gruppen.map((g) => g.name), ""];
}

function alleZugeklappt() {
  return alleGruppenSchluessel().every((s) => zugeklappt.has(s));
}

/** Der Knopf klappt zu, solange noch irgendeine Gruppe offen ist; erst wenn
    alle zu sind, klappt er alle auf. */
function aktualisiereAlleKlappen() {
  const zu = alleZugeklappt();
  $alleKlappenIcon.textContent = zu ? "unfold_more" : "unfold_less";
  $alleKlappenText.textContent = zu ? "Alle aufklappen" : "Alle zuklappen";
}

function klappeAlle() {
  if (alleZugeklappt()) zugeklappt.clear();
  else alleGruppenSchluessel().forEach((s) => zugeklappt.add(s));
  rendereProfilGruppen();
}

/** Eine Gruppe mit Kopf und Kachelraster. `index` zeigt in `gruppen`,
    -1 ist „Ohne Gruppe" — die steht in keiner Datei und lässt sich weder
    umbenennen noch löschen. */
function baueGruppe(name, index, mitglieder) {
  const ohne = index < 0;
  const schluessel = ohne ? "" : name;
  const zu = zugeklappt.has(schluessel);

  const sektion = document.createElement("section");
  sektion.className = ohne ? "gruppe gruppe-ohne" : "gruppe";
  sektion.setAttribute("aria-label", ohne ? "Profile ohne Gruppe" : `Gruppe ${name}`);
  sektion.innerHTML = `
    <div class="gruppe-kopf">
      <button type="button" class="gruppe-klappe" aria-expanded="${!zu}">
        <span class="material-symbols-outlined text-[18px] gruppe-pfeil" aria-hidden="true">expand_more</span>
        <span class="gruppe-name">${escapeHtml(name)}</span>
      </button>
      <span class="gruppe-zahl">${mitglieder.length}</span>
      ${ohne ? "" : `
      <button type="button" class="gruppe-umbenennen symbol-knopf ml-auto"
              aria-label="Gruppe umbenennen" title="Gruppe umbenennen">
        <span class="material-symbols-outlined text-[16px]" aria-hidden="true">edit</span>
      </button>
      <button type="button" class="gruppe-loeschen symbol-knopf"
              aria-label="Gruppe löschen" title="Gruppe löschen">
        <span class="material-symbols-outlined text-[16px]" aria-hidden="true">delete</span>
      </button>`}
    </div>
    <div class="gruppe-raster grid gap-3 sm:grid-cols-2 mt-3"></div>`;

  // Klasse statt hidden-Attribut: Tailwinds `grid` schlägt das Attribut.
  const raster = sektion.querySelector(".gruppe-raster");
  raster.classList.toggle("hidden", zu);
  mitglieder.forEach((profil) => {
    const kachel = baueKachel(profil);
    if (editorSlug === profil.slug) kachel.classList.add("kachel-gewaehlt");
    kachel.querySelector(".kachel-bearbeiten").addEventListener("click", () => {
      oeffneEditor(profil.slug);
    });
    macheZiehbar(kachel, profil.slug);
    raster.appendChild(kachel);
  });
  if (mitglieder.length === 0) {
    const leer = document.createElement("p");
    leer.className = "gruppe-leer sm:col-span-2";
    if (!ohne) leer.textContent = "Noch leer. Profile hierher ziehen.";
    else if (profile.length === 0) leer.textContent = "Noch kein Profil da. Rechts eins anlegen — von Hand oder ausarbeiten lassen.";
    else leer.textContent = "Alle Profile sind einsortiert. Hierher ziehen nimmt eins aus seiner Gruppe.";
    raster.appendChild(leer);
  }

  const klappe = sektion.querySelector(".gruppe-klappe");
  klappe.addEventListener("click", () => {
    const jetztZu = raster.classList.toggle("hidden");
    klappe.setAttribute("aria-expanded", String(!jetztZu));
    if (jetztZu) zugeklappt.add(schluessel);
    else zugeklappt.delete(schluessel);
    aktualisiereAlleKlappen();
  });
  if (!ohne) {
    sektion.querySelector(".gruppe-umbenennen").addEventListener("click", () => benenneGruppeUm(index));
    sektion.querySelector(".gruppe-loeschen").addEventListener("click", () => loescheGruppe(index));
  }

  // Die ganze Gruppe nimmt Kacheln an, auch eingeklappt. Innerhalb einer
  // benannten Gruppe zählt die Stelle: abgelegt wird vor der Kachel unter
  // dem Zeiger. „Ohne Gruppe" ist nach Namen sortiert, dort gibt es keine.
  sektion.addEventListener("dragover", (e) => {
    if (!gezogen) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    sektion.classList.add("gruppe-ziel");
    markiereEinfuegestelle(ohne ? null : e.target.closest(".kachel"));
  });
  sektion.addEventListener("dragleave", (e) => {
    if (sektion.contains(e.relatedTarget)) return;
    sektion.classList.remove("gruppe-ziel");
    markiereEinfuegestelle(null);
  });
  sektion.addEventListener("drop", (e) => {
    if (!gezogen) return;
    e.preventDefault();
    // Vor dem Neuzeichnen zurücksetzen: Die gezogene Kachel verschwindet
    // dabei aus dem DOM, und ohne sie feuert kein Browser mehr "dragend".
    const slug = gezogen;
    gezogen = null;
    const vor = ohne ? null : e.target.closest(".kachel");
    verschiebeProfil(slug, index, vor ? vor.dataset.slug : null);
  });
  return sektion;
}

function macheZiehbar(kachel, slug) {
  kachel.draggable = true;
  kachel.dataset.slug = slug;
  kachel.addEventListener("dragstart", (e) => {
    gezogen = slug;
    e.dataTransfer.effectAllowed = "move";
    // Firefox beginnt das Ziehen nur, wenn Daten dranhängen.
    e.dataTransfer.setData("text/plain", slug);
    kachel.classList.add("kachel-zieht");
  });
  kachel.addEventListener("dragend", () => {
    gezogen = null;
    kachel.classList.remove("kachel-zieht");
    document.querySelectorAll(".gruppe-ziel").forEach((el) => el.classList.remove("gruppe-ziel"));
    markiereEinfuegestelle(null);
  });
}

function markiereEinfuegestelle(kachel) {
  document.querySelectorAll(".kachel-davor").forEach((el) => el.classList.remove("kachel-davor"));
  if (kachel && kachel.dataset.slug !== gezogen) kachel.classList.add("kachel-davor");
}

function gruppeVon(slug) {
  const gruppe = gruppen.find((g) => g.profile.includes(slug));
  return gruppe ? gruppe.name : "";
}

/** Profil in die Gruppe `index` legen (-1 = ohne Gruppe), vor `vorSlug`
    oder ans Ende. Jedes Profil steht höchstens in einer Gruppe. */
function verschiebeProfil(slug, index, vorSlug) {
  if (vorSlug === slug) return Promise.resolve();
  const neu = gruppen.map((g) => ({ name: g.name, profile: g.profile.filter((s) => s !== slug) }));
  if (index >= 0) {
    const liste = neu[index].profile;
    const platz = vorSlug ? liste.indexOf(vorSlug) : -1;
    if (platz >= 0) liste.splice(platz, 0, slug);
    else liste.push(slug);
  }
  // Steht das Profil gerade im Editor, zieht die Auswahl dort mit — sonst
  // holte „Speichern" es in die alte Gruppe zurück.
  const wahl = slug === editorSlug ? (index >= 0 ? neu[index].name : "") : $feldGruppe.value;
  return speichereGruppen(neu, wahl);
}

/** Neue Fassung sofort zeigen, dann speichern. Jede Fassung ersetzt die
    ganze Liste; deshalb gehen sie nacheinander raus, damit zwei schnelle
    Züge beim Server nicht vertauscht ankommen. */
function speichereGruppen(neu, wahl = $feldGruppe.value) {
  gruppen = neu;
  rendereProfilGruppen();
  rendereGruppenwahl(wahl);
  gruppenKette = gruppenKette.then(async () => {
    const ergebnis = await setzeGruppen(neu);
    if (ergebnis.fehler) {
      zeigeHinweis($gruppenHinweis, ergebnis.fehler);
      gruppen = await ladeGruppenListe();
    } else {
      zeigeHinweis($gruppenHinweis, "");
      // Kam inzwischen eine neuere Fassung, gilt die; sonst die des Servers,
      // falls er etwas bereinigt hat.
      if (gruppen !== neu || JSON.stringify(ergebnis) === JSON.stringify(neu)) return;
      gruppen = ergebnis;
    }
    rendereProfilGruppen();
    rendereGruppenwahl($feldGruppe.value);
  });
  return gruppenKette;
}

async function ladeGruppenListe() {
  const geladen = await ladeGruppen();
  return Array.isArray(geladen) ? geladen : [];
}

function gruppenKopie() {
  return gruppen.map((g) => ({ name: g.name, profile: [...g.profile] }));
}

/** Wie `_einzeilig()` im Server: Leerraum zusammenziehen, drei Bindestriche
    zum Gedankenstrich. Sonst speicherte der Server einen anderen Namen, als
    das Dashboard prüft und im Gruppenfeld des Editors vermerkt. */
function saeubereGruppenname(name) {
  return name.split(/\s+/).filter(Boolean).join(" ").replace(/-{3,}/g, "–").slice(0, 60).trim();
}

function pruefeGruppenname(name, bisher) {
  if (!name) return "Die Gruppe braucht einen Namen.";
  const klein = name.toLowerCase();
  if (klein === "ohne gruppe") return `„Ohne Gruppe" gibt es schon — dort landen alle Profile ohne Gruppe.`;
  if (gruppen.some((g) => g.name !== bisher && g.name.toLowerCase() === klein)) {
    return "Eine Gruppe mit diesem Namen gibt es schon.";
  }
  return null;
}

async function legeGruppeAn() {
  let name = await zeigeDialog({
    titel: "Neue Gruppe",
    text: "Wie soll die Gruppe heißen? Die Profile ziehst du danach hinein.",
    okText: "Anlegen",
    eingabe: { platzhalter: "Vorstellungsgespräch" },
  });
  if (name === null) return;
  name = saeubereGruppenname(name);
  const fehler = pruefeGruppenname(name, null);
  if (fehler) return zeigeHinweis($gruppenHinweis, fehler);
  speichereGruppen([...gruppenKopie(), { name, profile: [] }]);
}

async function benenneGruppeUm(index) {
  const bisher = gruppen[index].name;
  let name = await zeigeDialog({
    titel: "Gruppe umbenennen",
    okText: "Umbenennen",
    eingabe: { wert: bisher },
  });
  if (name === null) return;
  name = saeubereGruppenname(name);
  if (name === bisher) return;
  const fehler = pruefeGruppenname(name, bisher);
  if (fehler) return zeigeHinweis($gruppenHinweis, fehler);

  if (zugeklappt.delete(bisher)) zugeklappt.add(name);
  const neu = gruppenKopie();
  neu[index].name = name;
  speichereGruppen(neu, $feldGruppe.value === bisher ? name : $feldGruppe.value);
}

async function loescheGruppe(index) {
  const gruppe = gruppen[index];
  const anzahl = gruppe.profile.length;
  // Eine leere Gruppe geht ohne Rückfrage: Es geht nichts verloren.
  if (anzahl > 0) {
    const bestaetigt = await zeigeDialog({
      titel: "Gruppe löschen?",
      text: anzahl === 1
        ? `„${gruppe.name}" wird aufgelöst. Das Profil darin bleibt erhalten und steht danach unter „Ohne Gruppe".`
        : `„${gruppe.name}" wird aufgelöst. Die ${anzahl} Profile darin bleiben erhalten und stehen danach unter „Ohne Gruppe".`,
      okText: "Gruppe löschen",
    });
    if (!bestaetigt) return;
  }
  zugeklappt.delete(gruppe.name);
  speichereGruppen(gruppenKopie().filter((_, i) => i !== index));
}

function rendereGruppenwahl(wert) {
  $feldGruppe.innerHTML = "";
  $feldGruppe.add(new Option("Ohne Gruppe", ""));
  gruppen.forEach((g) => $feldGruppe.add(new Option(g.name, g.name)));
  // Eine Gruppe, die es nicht mehr gibt, heißt: ohne Gruppe.
  $feldGruppe.value = gruppen.some((g) => g.name === wert) ? wert : "";
}

function setzeEditorBreit(breit) {
  $ansichtProfile.classList.toggle("editor-breit", breit);
  $editorBreiteIcon.textContent = breit ? "close_fullscreen" : "open_in_full";
  const label = breit ? "Profilliste wieder einblenden" : "Editor auf volle Breite";
  $editorBreiteBtn.setAttribute("aria-label", label);
  $editorBreiteBtn.setAttribute("aria-pressed", String(breit));
  $editorBreiteBtn.title = label;
}

function rendereFarbwahl(gewaehlt) {
  $farbwahl.innerHTML = "";
  FARBEN.forEach((farbe) => {
    const label = document.createElement("label");
    label.className = `farbwahl profil-${farbe.wert} relative`;
    label.title = farbe.label;
    label.innerHTML = `
      <input type="radio" name="farbe" value="${farbe.wert}" ${farbe.wert === gewaehlt ? "checked" : ""}/>
      <span aria-hidden="true"></span>
      <span class="sr-only">${farbe.label}</span>`;
    $farbwahl.appendChild(label);
  });
}

function gewaehlteFarbe() {
  const gewaehlt = $farbwahl.querySelector("input:checked");
  return gewaehlt ? gewaehlt.value : "grau";
}

function rendereModellauswahl(select, wert, standardLabel = "Standardmodell des Servers") {
  select.innerHTML = "";
  const standard = document.createElement("option");
  standard.value = "";
  standard.textContent = standardLabel;
  select.appendChild(standard);

  let letzterAnbieter = null;
  let gruppe = null;
  modelle.forEach((m) => {
    if (m.anbieter !== letzterAnbieter) {
      gruppe = document.createElement("optgroup");
      gruppe.label = m.anbieter;
      select.appendChild(gruppe);
      letzterAnbieter = m.anbieter;
    }
    const option = document.createElement("option");
    option.value = m.id;
    option.textContent = m.denken ? m.modell : `${m.modell} (kein Denken)`;
    gruppe.appendChild(option);
  });

  // Ein Modell aus einer Datei, das pi gerade nicht anbietet, darf nicht
  // stillschweigend verschwinden.
  if (wert && !modelle.some((m) => m.id === wert)) {
    const option = document.createElement("option");
    option.value = wert;
    option.textContent = `${wert} (nicht in der Liste)`;
    select.appendChild(option);
  }
  select.value = wert || "";
}

function oeffneEditor(slug) {
  const profil = slug ? profilFinden(slug) : null;
  editorSlug = profil ? profil.slug : null;

  $editorTitel.textContent = profil ? `Profil: ${profil.name}` : "Neues Profil";
  $feldName.value = profil ? profil.name : "";
  $feldBeschreibung.value = profil ? profil.beschreibung : "";
  $feldThinking.value = profil ? profil.thinking : "medium";
  $feldText.value = profil ? profil.text : "";
  rendereFarbwahl(profil ? profil.farbe : "gruen");
  rendereModellauswahl($feldModel, profil ? profil.model : "");
  rendereGruppenwahl(profil ? gruppeVon(profil.slug) : "");
  $loeschenBtn.classList.toggle("hidden", !profil);
  $duplizierenBtn.classList.toggle("hidden", !profil);
  zeigeHinweis($editorHinweis, "");
  rendereProfilGruppen();
}

function dupliziereProfil() {
  if (!editorSlug) return;
  // Die Kopie liegt nur im Editor, noch nichts auf der Platte: Name freilegen,
  // alles andere stehen lassen, gespeichert wird auf Knopfdruck. So bleibt das
  // Anlegen einer zweiten, ähnlichen Stimme ein bewusster Schritt.
  editorSlug = null;
  $feldName.value = freierName($feldName.value);
  $editorTitel.textContent = "Neues Profil";
  $loeschenBtn.classList.add("hidden");
  $duplizierenBtn.classList.add("hidden");
  zeigeHinweis($editorHinweis, "");
  rendereProfilGruppen();
  $feldName.focus();
  $feldName.select();
}

function freierName(name) {
  const vergeben = new Set(profile.map((p) => p.name));
  const basis = name.trim().replace(/ \(Variante( \d+)?\)$/, "");
  let kandidat = `${basis} (Variante)`;
  let nummer = 1;
  while (vergeben.has(kandidat)) {
    nummer += 1;
    kandidat = `${basis} (Variante ${nummer})`;
  }
  return kandidat;
}

async function speichereProfil() {
  const daten = {
    name: $feldName.value,
    beschreibung: $feldBeschreibung.value,
    model: $feldModel.value,
    thinking: $feldThinking.value,
    farbe: gewaehlteFarbe(),
    text: $feldText.value,
  };
  if (!daten.name.trim()) return zeigeHinweis($editorHinweis, "Das Profil braucht einen Namen.");
  if (!daten.text.trim()) return zeigeHinweis($editorHinweis, "Das Profil braucht einen Rollentext.");

  const ergebnis = editorSlug
    ? await aendereProfil(editorSlug, daten)
    : await neuesProfil(daten);
  if (ergebnis.fehler) return zeigeHinweis($editorHinweis, ergebnis.fehler);

  const wunschgruppe = $feldGruppe.value;
  profile = await ladeProfile();
  // Die Gruppe steht nicht in der Profildatei, sondern in gruppen.json —
  // erst jetzt gibt es den Slug, unter dem das Profil dort eingetragen wird.
  if (gruppeVon(ergebnis.slug) !== wunschgruppe) {
    await verschiebeProfil(ergebnis.slug, gruppen.findIndex((g) => g.name === wunschgruppe), null);
  }
  oeffneEditor(ergebnis.slug);
}

async function loescheProfil() {
  if (!editorSlug) return;
  const profil = profilFinden(editorSlug);
  const bestaetigt = await zeigeDialog({
    titel: "Profil löschen?",
    text: `„${profil ? profil.name : editorSlug}" wird von der Platte gelöscht. Das lässt sich nicht rückgängig machen.`,
    okText: "Löschen",
  });
  if (!bestaetigt) return;

  let ergebnis = await entferneProfil(editorSlug, false);
  if (ergebnis.fehler && ergebnis.partys) {
    const trotzdem = await zeigeDialog({
      titel: "Profil wird noch gebraucht",
      text: `Es sitzt noch in: ${ergebnis.partys.join(", ")}. Trotzdem löschen? Diese Partys lassen sich danach nicht fortsetzen.`,
      okText: "Trotzdem löschen",
    });
    if (!trotzdem) return;
    ergebnis = await entferneProfil(editorSlug, true);
  }
  if (ergebnis.fehler) return zeigeHinweis($editorHinweis, ergebnis.fehler);

  // Der Server hat das Profil auch aus seiner Gruppe ausgetragen.
  [profile, gruppen] = await Promise.all([ladeProfile(), ladeGruppenListe()]);
  oeffneEditor(null);
}

// --- Profil ausarbeiten lassen ---------------------------------------------
function entwurfKnopf(laeuft) {
  $entwurfBtnText.textContent = laeuft ? "Abbrechen" : "Ausarbeiten lassen";
  $entwurfStatus.textContent = laeuft ? "Das Modell schreibt …" : "";
}

async function entwurfStarten() {
  if (entwurfAbbruch) {
    entwurfAbbruch.abort();
    return;
  }
  const idee = $entwurfIdee.value.trim();
  if (!idee) return zeigeHinweis($editorHinweis, "Beschreibe die Rolle zuerst in einem Satz.");

  zeigeHinweis($editorHinweis, "");
  entwurfAbbruch = new AbortController();
  entwurfKnopf(true);
  $feldText.value = "";
  $entwurfDenken.textContent = "";
  $entwurfDenkenBox.classList.add("hidden");

  try {
    const res = await fetch("/api/profile/entwurf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idee }),
      signal: entwurfAbbruch.signal,
    });
    if (!res.ok) {
      const fehler = await res.json().catch(() => ({}));
      throw new Error(fehler.fehler || "Der Entwurf hat nicht geklappt.");
    }
    await sseLesen(res, (ev) => {
      if (ev.art === "text") {
        // Kein DOM-Rendern: das Textfeld aktualisiert der Browser selbst,
        // die Zuschauer sehen den Text entstehen.
        $feldText.value += ev.delta;
        $feldText.scrollTop = $feldText.scrollHeight;
      } else if (ev.art === "denken") {
        $entwurfDenkenBox.classList.remove("hidden");
        $entwurfDenken.append(ev.delta);
        $entwurfDenken.scrollTop = $entwurfDenken.scrollHeight;
      } else if (ev.art === "fehler" || ev.art === "meldung") {
        zeigeHinweis($editorHinweis, ev.text);
      }
    });
    entwurfUebernehmen($feldText.value);
  } catch (e) {
    if (e.name !== "AbortError") zeigeHinweis($editorHinweis, e.message);
  } finally {
    entwurfAbbruch = null;
    entwurfKnopf(false);
  }
}

function entwurfUebernehmen(text) {
  const geteilt = frontmatterTrennen(text.trim());
  if (!geteilt) {
    zeigeHinweis($editorHinweis,
      "Frontmatter nicht erkannt — bitte die Felder oben von Hand ausfüllen.");
    return;
  }
  const meta = geteilt.meta;
  if (meta.name) $feldName.value = meta.name;
  if (meta.beschreibung) $feldBeschreibung.value = meta.beschreibung;
  if (meta.thinking) $feldThinking.value = meta.thinking;
  if (meta.model) rendereModellauswahl($feldModel, meta.model);
  rendereFarbwahl(FARBEN.some((f) => f.wert === meta.farbe) ? meta.farbe : "gruen");
  $feldText.value = geteilt.rumpf;
  // Ein Entwurf ist immer ein neues Profil, nie eine Änderung am offenen.
  editorSlug = null;
  $editorTitel.textContent = "Neues Profil";
  $loeschenBtn.classList.add("hidden");
  rendereProfilGruppen();
}

async function ladeUndRendereProfile() {
  [profile, gruppen] = await Promise.all([ladeProfile(), ladeGruppenListe()]);
  if (profile.fehler) profile = [];
  rendereProfilGruppen();
  rendereGruppenwahl($feldGruppe.value);
  if (!$feldModel.options.length) rendereModellauswahl($feldModel, "");
}

// ---------------------------------------------------------------------------
// Ansicht 2: Party einrichten
// ---------------------------------------------------------------------------
function rendereAuswahl() {
  $auswahlRaster.innerHTML = "";
  if (profile.length === 0) {
    const leer = document.createElement("p");
    leer.className = "text-sm text-on-surface-variant";
    leer.textContent = "Erst Profile anlegen, dann kann die Party losgehen.";
    $auswahlRaster.appendChild(leer);
    return;
  }
  // Gruppiert wie unter „Agentenprofile", aber nur zum Auswählen: kein
  // Umbenennen, kein Ziehen, und leere Gruppen bleiben weg.
  profileNachGruppen()
    .filter(({ mitglieder }) => mitglieder.length > 0)
    .forEach(({ name, index, mitglieder }) => {
      $auswahlRaster.appendChild(baueAuswahlGruppe(name, index < 0, mitglieder));
    });
}

function baueAuswahlGruppe(name, ohne, mitglieder) {
  const schluessel = ohne ? "" : name;
  const zu = auswahlZugeklappt.has(schluessel);
  const gewaehlt = mitglieder.filter((p) => besetzung.includes(p.slug)).length;

  const sektion = document.createElement("section");
  sektion.className = ohne ? "gruppe gruppe-ohne" : "gruppe";
  sektion.setAttribute("aria-label", ohne ? "Profile ohne Gruppe" : `Gruppe ${name}`);
  sektion.innerHTML = `
    <div class="gruppe-kopf">
      <button type="button" class="gruppe-klappe" aria-expanded="${!zu}">
        <span class="material-symbols-outlined text-[18px] gruppe-pfeil" aria-hidden="true">expand_more</span>
        <span class="gruppe-name">${escapeHtml(name)}</span>
      </button>
      <span class="gruppe-zahl" title="am Tisch / in der Gruppe">${gewaehlt} / ${mitglieder.length}</span>
    </div>
    <div class="gruppe-raster grid gap-3 sm:grid-cols-2 mt-3"></div>`;

  // Klasse statt hidden-Attribut: Tailwinds `grid` schlägt das Attribut.
  const raster = sektion.querySelector(".gruppe-raster");
  raster.classList.toggle("hidden", zu);
  mitglieder.forEach((profil) => {
    const kachel = baueKachel(profil, { auswaehlbar: true });
    if (besetzung.includes(profil.slug)) kachel.classList.add("kachel-gewaehlt");
    kachel.addEventListener("click", () => {
      // Jedes Profil sitzt höchstens einmal am Tisch, der Klick schaltet also
      // um — und die Markierung auf der Kachel sagt endlich das, wonach sie
      // aussieht. Zwei ähnliche Stimmen? Dafür gibt es "Duplizieren".
      const platz = besetzung.indexOf(profil.slug);
      if (platz >= 0) besetzung.splice(platz, 1);
      else if (besetzung.length < MAX_TEILNEHMER) besetzung.push(profil.slug);
      rendereAuswahl();
      rendereBesetzung();
    });
    raster.appendChild(kachel);
  });

  const klappe = sektion.querySelector(".gruppe-klappe");
  klappe.addEventListener("click", () => {
    const jetztZu = raster.classList.toggle("hidden");
    klappe.setAttribute("aria-expanded", String(!jetztZu));
    if (jetztZu) auswahlZugeklappt.add(schluessel);
    else auswahlZugeklappt.delete(schluessel);
  });
  return sektion;
}

function rendereBesetzung() {
  $besetzung.innerHTML = "";
  if (besetzung.length === 0) {
    const leer = document.createElement("p");
    leer.className = "text-sm text-on-surface-variant";
    leer.textContent = "Noch niemand am Tisch. Links Profile anklicken.";
    $besetzung.appendChild(leer);
  }

  // Durchgehend über den Index arbeiten: dasselbe Profil darf mehrfach in
  // der Runde sitzen, ein Zugriff über den Slug träfe dann den falschen Platz.
  besetzung.forEach((slug, index) => {
    const profil = profilFinden(slug) || { name: slug, farbe: "grau" };
    const zeile = document.createElement("div");
    zeile.className = `profil-${profil.farbe} flex items-center gap-2 py-1.5 px-2 rounded bg-surface-mid`;
    zeile.innerHTML = `
      <span class="text-xs text-on-surface-variant w-4 text-right">${index + 1}.</span>
      <span class="profil-flaeche w-2 h-2 rounded-full shrink-0" aria-hidden="true"></span>
      <span class="text-sm truncate flex-1">${escapeHtml(profil.name)}</span>
      <button class="btn-hoch p-0.5 rounded hover:bg-on-surface/10 disabled:opacity-30" aria-label="Nach oben" title="Nach oben">
        <span class="material-symbols-outlined text-[16px]" aria-hidden="true">arrow_upward</span>
      </button>
      <button class="btn-runter p-0.5 rounded hover:bg-on-surface/10 disabled:opacity-30" aria-label="Nach unten" title="Nach unten">
        <span class="material-symbols-outlined text-[16px]" aria-hidden="true">arrow_downward</span>
      </button>
      <button class="btn-weg p-0.5 rounded hover:bg-on-surface/10" aria-label="Vom Tisch nehmen" title="Vom Tisch nehmen">
        <span class="material-symbols-outlined text-[16px]" aria-hidden="true">close</span>
      </button>`;

    const hoch = zeile.querySelector(".btn-hoch");
    const runter = zeile.querySelector(".btn-runter");
    hoch.disabled = index === 0;
    runter.disabled = index === besetzung.length - 1;
    hoch.addEventListener("click", () => tausche(index, index - 1));
    runter.addEventListener("click", () => tausche(index, index + 1));
    zeile.querySelector(".btn-weg").addEventListener("click", () => {
      besetzung.splice(index, 1);
      rendereAuswahl();
      rendereBesetzung();
    });
    $besetzung.appendChild(zeile);
  });

  pruefeStartbereit();
}

function tausche(a, b) {
  [besetzung[a], besetzung[b]] = [besetzung[b], besetzung[a]];
  rendereBesetzung();
}

function pruefeStartbereit() {
  const bereit =
    besetzung.length >= 2 &&
    $feldTitel.value.trim() !== "" &&
    $feldStarter.value.trim() !== "";
  $partyStartBtn.disabled = !bereit;
}

function rendereParties(partys) {
  $partyListe.innerHTML = "";
  if (!partys.length) {
    const leer = document.createElement("p");
    leer.className = "text-sm text-on-surface-variant";
    leer.textContent = "Noch keine Party gelaufen.";
    $partyListe.appendChild(leer);
    return;
  }
  partys.forEach((eintrag) => {
    const zeile = document.createElement("div");
    zeile.className = "flex items-center gap-3 p-3 bg-surface border border-on-surface/10 rounded-md";
    zeile.innerHTML = `
      <span class="status-punkt status-${eintrag.status} shrink-0" aria-hidden="true"></span>
      <button class="oeffnen text-left min-w-0 flex-1">
        <div class="text-sm font-medium truncate">${escapeHtml(eintrag.sitzung.titel)}</div>
        <div class="text-xs text-on-surface-variant">
          ${STATUS_TEXT[eintrag.status] || eintrag.status} · ${eintrag.beitraege} von ${eintrag.erwartet} Beiträgen
        </div>
      </button>
      <button class="bearbeiten p-1 rounded hover:bg-on-surface/10 disabled:opacity-30" aria-label="Party bearbeiten" title="Party bearbeiten">
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant" aria-hidden="true">edit</span>
      </button>
      <button class="zurueck p-1 rounded hover:bg-on-surface/10 disabled:opacity-30" aria-label="Auf den Start zurücksetzen" title="Auf den Start zurücksetzen">
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant" aria-hidden="true">restart_alt</span>
      </button>
      <button class="weg p-1 rounded hover:bg-on-surface/10" aria-label="Party löschen" title="Party löschen">
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant" aria-hidden="true">delete</span>
      </button>`;
    zeile.querySelector(".oeffnen").addEventListener("click", () => {
      zeigeAnsicht("party", eintrag.slug);
    });
    // Eine laufende Party ändert niemand unter der Hand; Zurücksetzen hält
    // sie dagegen selbst an und darf deshalb immer.
    const bearbeiten = zeile.querySelector(".bearbeiten");
    bearbeiten.disabled = eintrag.status === "laeuft";
    bearbeiten.addEventListener("click", () => starteBearbeitung(eintrag.slug));
    const zurueck = zeile.querySelector(".zurueck");
    zurueck.disabled = eintrag.status === "neu" && eintrag.zwischenrufe === 0;
    zurueck.addEventListener("click", async () => {
      if (await partyZuruecksetzen(eintrag.slug, eintrag.sitzung.titel, eintrag.beitraege)) {
        ladeUndRendereEinrichten();
      }
    });
    zeile.querySelector(".weg").addEventListener("click", async () => {
      const bestaetigt = await zeigeDialog({
        titel: "Party löschen?",
        text: `„${eintrag.sitzung.titel}" und der gesamte Gesprächsverlauf werden gelöscht.`,
        okText: "Löschen",
      });
      if (!bestaetigt) return;
      await entferneParty(eintrag.slug);
      ladeUndRendereEinrichten();
    });
    $partyListe.appendChild(zeile);
  });
}

async function ladeUndRendereEinrichten() {
  [profile, gruppen] = await Promise.all([ladeProfile(), ladeGruppenListe()]);
  if (profile.fehler) profile = [];
  // Profile, die inzwischen gelöscht wurden, fliegen vom Tisch.
  besetzung = besetzung.filter((slug) => profilFinden(slug));
  rendereAuswahl();
  rendereBesetzung();
  // Leer heißt hier: jedes Profil spricht mit dem Modell aus seiner Datei.
  rendereModellauswahl($feldPartymodell, $feldPartymodell.value,
    "Modell aus dem jeweiligen Profil");
  const partys = await ladePartys();
  rendereParties(Array.isArray(partys) ? partys : []);
}

function formularDaten() {
  return {
    titel: $feldTitel.value,
    starter: $feldStarter.value,
    teilnehmer: besetzung,
    runden: parseInt($feldRunden.value, 10) || 2,
    modell: $feldPartymodell.value,
  };
}

async function partyAnlegenUndStarten() {
  zeigeHinweis($einrichtenHinweis, "");
  const angelegt = await neueParty(formularDaten());
  if (angelegt.fehler) return zeigeHinweis($einrichtenHinweis, angelegt.fehler);

  const gestartet = await starteParty(angelegt.slug);
  if (gestartet.fehler) return zeigeHinweis($einrichtenHinweis, gestartet.fehler);

  zeigeAnsicht("party", angelegt.slug);
}

// ---------------------------------------------------------------------------
// Bestehende Party bearbeiten oder zurücksetzen
// ---------------------------------------------------------------------------

/** Die Party ins Formular von „Party vorbereiten" laden. Gespeichert wird
    erst auf Knopfdruck, gestartet gar nicht — das geht danach in der Sitzung. */
async function starteBearbeitung(slug) {
  const daten = await ladeParty(slug);
  if (daten.fehler) {
    await zeigeDialog({ titel: "Party nicht gefunden", text: daten.fehler, mitAbbrechen: false });
    return;
  }
  bearbeitung = { slug, sitzung: daten.sitzung, status: daten.status };
  besetzung = [...daten.sitzung.teilnehmer];
  $feldTitel.value = daten.sitzung.titel;
  $feldStarter.value = daten.sitzung.starter;
  // Über „Weitere Runde" kann eine Sitzung länger sein als das Formular erlaubt.
  $feldRunden.max = String(Math.max(MAX_RUNDEN, daten.sitzung.runden));
  $feldRunden.value = String(daten.sitzung.runden);
  rendereModellauswahl($feldPartymodell, daten.sitzung.modell || "",
    "Modell aus dem jeweiligen Profil");
  rendereBearbeitungsmodus();
  zeigeAnsicht("einrichten", "bearbeiten");
}

/** Zurück zum Formular für eine neue Party, leer. */
function beendeBearbeitung() {
  bearbeitung = null;
  besetzung = [];
  $feldTitel.value = "";
  $feldStarter.value = "";
  $feldRunden.max = String(MAX_RUNDEN);
  $feldRunden.value = "2";
  $feldPartymodell.value = "";
  zeigeHinweis($einrichtenHinweis, "");
  rendereBearbeitungsmodus();
}

function rendereBearbeitungsmodus() {
  const aktiv = Boolean(bearbeitung);
  $rundeTitel.textContent = aktiv ? "Party bearbeiten" : "Die Runde";
  $partyStartIcon.textContent = aktiv ? "save" : "play_arrow";
  $partyStartText.textContent = aktiv ? "Änderungen speichern" : "Party starten";
  $bearbeitenAbbrechenBtn.classList.toggle("hidden", !aktiv);
  $bearbeitenInfo.classList.toggle("hidden", !aktiv);
  if (aktiv) {
    $bearbeitenInfo.textContent = bearbeitung.status === "neu"
      ? "Die Party hat noch nicht angefangen — alles lässt sich ändern."
      : "Die Party hat schon Beiträge. Runden und Modell lassen sich einfach " +
        "ändern; wer Thema, Einstiegsfrage oder Besetzung ändert, setzt sie " +
        "dabei auf den Start zurück.";
  }
}

async function speichereParty() {
  zeigeHinweis($einrichtenHinweis, "");
  const daten = formularDaten();
  const alt = bearbeitung.sitzung;
  // Dieselbe Säuberung wie im Server, sonst gälte ein Leerzeichen am Ende
  // schon als geändertes Thema.
  const kernGeaendert =
    daten.titel.split(/\s+/).filter(Boolean).join(" ") !== alt.titel ||
    daten.starter.trim() !== alt.starter ||
    daten.teilnehmer.join("|") !== alt.teilnehmer.join("|");

  if (kernGeaendert && bearbeitung.status !== "neu") {
    const bestaetigt = await zeigeDialog({
      titel: "Party zurücksetzen?",
      text: "Thema, Einstiegsfrage oder Besetzung haben sich geändert. Dazu passt " +
            "der bisherige Verlauf nicht mehr: Alle Beiträge, Zwischenrufe und " +
            "das Fazit werden gelöscht.",
      okText: "Speichern und zurücksetzen",
    });
    if (!bestaetigt) return;
  }
  // Auch ohne Beiträge: Zwischenrufe vor dem ersten Beitrag galten der alten Runde.
  daten.zuruecksetzen = kernGeaendert;

  const ergebnis = await aendereParty(bearbeitung.slug, daten);
  if (ergebnis.fehler) return zeigeHinweis($einrichtenHinweis, ergebnis.fehler);

  const slug = bearbeitung.slug;
  beendeBearbeitung();
  zeigeAnsicht("party", slug);
}

/** Fragt nach und setzt zurück. Liefert, ob zurückgesetzt wurde. */
async function partyZuruecksetzen(slug, titel, beitraege) {
  const bestaetigt = await zeigeDialog({
    titel: "Party zurücksetzen?",
    text: `„${titel}" beginnt wieder von vorn. ${beitraege} ` +
          `${beitraege === 1 ? "Beitrag" : "Beiträge"}, alle Zwischenrufe und ` +
          "das Fazit werden gelöscht. Thema, Besetzung und Runden bleiben.",
    okText: "Zurücksetzen",
  });
  if (!bestaetigt) return false;
  const ergebnis = await setzePartyZurueck(slug);
  if (ergebnis.fehler) {
    await zeigeDialog({ titel: "Zurücksetzen klappt nicht", text: ergebnis.fehler, mitAbbrechen: false });
    return false;
  }
  return true;
}

// ---------------------------------------------------------------------------
// Ansicht 3: Party läuft
// ---------------------------------------------------------------------------
async function oeffneParty(slug) {
  const daten = await ladeParty(slug);
  if (daten.fehler) {
    zeigeAnsicht("einrichten");
    return;
  }
  if (!profile.length) profile = await ladeProfile();

  aktuelleParty = daten;
  $tabParty.disabled = false;
  rendereKopfblock(daten);

  $verlauf.innerHTML = "";
  aktiveBlase = null;
  fertigeBeitraege = 0;
  zwischenrufe = 0;
  letzteRunde = 0;
  beitragZaehler = {};
  zeigeHinweis($steuerHinweis, "");
  rendereTeilnehmer(null);
  rendereFortschritt(daten.status);
  oeffneStrom(slug);
}

/** Zwei Buchstaben als Zeichen des Profils — mehr trägt das Quadrat nicht. */
function initialen(name) {
  const woerter = String(name || "").trim().split(/\s+/).filter(Boolean);
  if (!woerter.length) return "??";
  if (woerter.length === 1) return woerter[0].slice(0, 2).toUpperCase();
  return (woerter[0][0] + woerter[1][0]).toUpperCase();
}

function rendereKopfblock(daten) {
  $partyTitel.textContent = daten.sitzung.titel;
  $partyStarter.textContent = daten.sitzung.starter;

  const anzahl = daten.sitzung.teilnehmer.length;
  const runden = daten.sitzung.runden;
  const modell = daten.sitzung.modell;
  $partyMeta.textContent = [
    `${anzahl} ${anzahl === 1 ? "Agent" : "Agenten"}`,
    `${runden} ${runden === 1 ? "Runde" : "Runden"}`,
    // Der Anbieter steht schon in der Einrichtung; hier reicht das Modell.
    modell ? modell.split("/").pop() : "Modell je Profil",
  ].join(" · ");
}

/** Die Teilnehmerkarte rechts. `aktiv` ist der Slug, der gerade formuliert. */
function rendereTeilnehmer(aktiv) {
  if (!aktuelleParty) return;
  $teilnehmerListe.innerHTML = "";

  aktuelleParty.sitzung.teilnehmer.forEach((slug) => {
    const profil = profilFinden(slug) || { name: slug, beschreibung: "", farbe: "grau" };
    const zeile = document.createElement("li");
    zeile.className = `teilnehmer-zeile profil-${profil.farbe}`;
    const zweite = slug === aktiv
      ? `<span class="teilnehmer-spricht puls">formuliert …</span>`
      : `<span class="teilnehmer-rolle">${escapeHtml(profil.beschreibung)}</span>`;
    zeile.innerHTML = `
      <span class="beitrag-zeichen zeichen-klein profil-flaeche" aria-hidden="true">${escapeHtml(initialen(profil.name))}</span>
      <span class="min-w-0">
        <span class="teilnehmer-name block">${escapeHtml(profil.name)}</span>
        ${zweite}
      </span>
      <span class="teilnehmer-zahl">${beitragZaehler[slug] || 0}</span>`;
    $teilnehmerListe.appendChild(zeile);
  });
}

function rendereKennzahlen() {
  if (!aktuelleParty) return;
  $kennzahlRunde.textContent =
    `${letzteRunde || 1} von ${aktuelleParty.sitzung.runden}`;
  $kennzahlBeitraege.textContent = `${fertigeBeitraege} von ${aktuelleParty.erwartet}`;
  $kennzahlZwischenrufe.textContent = String(zwischenrufe);
}

function rendereFortschritt(status) {
  if (!aktuelleParty) return;
  aktuelleParty.status = status;
  const laeuft = status === "laeuft";

  $partyStatusBadge.textContent = STATUS_TEXT[status] || status;
  if (laeuft) {
    const punkt = document.createElement("span");
    punkt.className = "badge-punkt puls";
    $partyStatusBadge.prepend(punkt);
  }
  $partyFortschritt.textContent =
    `${fertigeBeitraege} von ${aktuelleParty.erwartet} Beiträgen`;
  rendereKennzahlen();

  // Anhalten greift nur in einen laufenden Beitrag; eine weitere Runde gibt
  // es erst, wenn die geplanten durch sind. Einwerfen geht immer: der
  // Impuls wartet notfalls auf die nächste Runde.
  $partyStopBtn.disabled = !laeuft;
  $rundeBtn.disabled = status !== "fertig";
  $fazitBtn.disabled = laeuft || fertigeBeitraege === 0;
  // Auch "neu": wer vor dem ersten Beitrag abbricht, landet wieder dort —
  // ohne diesen Knopf ließe sich die Party danach nur noch löschen.
  $partyFortBtn.classList.toggle("hidden", laeuft || status === "fertig");
  $partyFortText.textContent = status === "neu" ? "Starten" : "Fortsetzen";
  $partyBearbeitenBtn.disabled = laeuft;
  $partyZurueckBtn.disabled = status === "neu" && fertigeBeitraege === 0 && zwischenrufe === 0;
}

function oeffneStrom(slug) {
  schliesseStrom();
  partyQuelle = new EventSource(`/api/partys/${slug}/stream`);

  partyQuelle.onmessage = (nachricht) => {
    let ereignis;
    try {
      ereignis = JSON.parse(nachricht.data);
    } catch (e) {
      return;
    }
    switch (ereignis.art) {
      case "beitrag_start": beitragStart(ereignis); break;
      case "text": textDelta(ereignis); break;
      case "denken": denkDelta(ereignis); break;
      case "beitrag_ende": beitragEnde(ereignis); break;
      case "zwischenruf": zwischenrufAnzeigen(ereignis); break;
      case "verworfen": beitragVerworfen(ereignis.text); break;
      case "fehler":
      case "meldung":
        // pi fängt den Beitrag neu an — was bisher in der Blase steht, kommt
        // gleich noch einmal und müsste sonst doppelt dastehen.
        if (ereignis.neustart) blaseZuruecksetzen();
        systemBlase(ereignis.text);
        break;
    }
  };

  partyQuelle.addEventListener("done", (nachricht) => {
    schliesseStrom();
    if (aktiveBlase) {
      aktiveBlase.wurzel.classList.remove("blase-tippt");
      aktiveBlase = null;
    }
    rendereTeilnehmer(null);
    rendereFortschritt(nachricht.data || "fertig");
  });

  partyQuelle.addEventListener("error", () => {
    // Kein Auto-Reconnect: der Server beendet den Strom bewusst mit "done".
    if (partyQuelle && partyQuelle.readyState === EventSource.CLOSED) return;
    schliesseStrom();
  });
}

function schliesseStrom() {
  if (partyQuelle) {
    partyQuelle.close();
    partyQuelle = null;
  }
}

/** Vor dem ersten Beitrag einer Runde eine Trennlinie mit Rundennummer. */
function rundenTrenner(runde) {
  if (!runde || runde === letzteRunde) return;
  letzteRunde = runde;
  const trenner = $rundenVorlage.content.firstElementChild.cloneNode(true);
  trenner.querySelector(".runden-marke").textContent = `Runde ${runde}`;
  $verlauf.appendChild(trenner);
}

function beitragStart(ereignis) {
  const fazit = ereignis.sorte === "fazit";
  if (!fazit) rundenTrenner(ereignis.runde);

  const profil = profilFinden(ereignis.profil) || {
    name: ereignis.name || ereignis.profil,
    beschreibung: "",
    farbe: ereignis.farbe || "grau",
  };
  const wurzel = $blasenVorlage.content.firstElementChild.cloneNode(true);
  wurzel.classList.add(`profil-${profil.farbe}`);
  if (fazit) wurzel.classList.add("beitrag-fazit");

  const zeichen = wurzel.querySelector(".beitrag-zeichen");
  if (fazit) {
    zeichen.classList.remove("profil-flaeche");
    zeichen.innerHTML =
      '<span class="material-symbols-outlined text-[22px]">summarize</span>';
  } else {
    zeichen.textContent = initialen(profil.name);
  }

  wurzel.querySelector(".blase-name").textContent = fazit ? "Fazit" : profil.name;
  wurzel.querySelector(".blase-rolle").textContent =
    fazit ? "Gesprächsleitung" : profil.beschreibung;
  wurzel.querySelector(".blase-runde").textContent =
    fazit ? "" : `Runde ${ereignis.runde}`;
  wurzel.classList.toggle("blase-tippt", !ereignis.nachgeliefert);

  $verlauf.appendChild(wurzel);
  aktiveBlase = {
    wurzel,
    textEl: wurzel.querySelector(".blase-text"),
    denkEl: wurzel.querySelector(".blase-denken-text"),
    denkBox: wurzel.querySelector(".blase-denken"),
    roh: "",
  };
  if (!ereignis.nachgeliefert && !fazit) rendereTeilnehmer(ereignis.profil);
  scrolleWennAmEnde();
}

function textDelta(ereignis) {
  if (!aktiveBlase) return;
  aktiveBlase.roh += ereignis.delta;
  // Nur einen Textknoten anhängen: kein Auslesen des bisherigen Inhalts,
  // kein Neuparsen. Das Markdown kommt genau einmal am Ende — wer das hier
  // durch innerHTML ersetzt, lässt die Ansicht bei jedem Zeichen flackern.
  aktiveBlase.textEl.append(ereignis.delta);
  scrolleWennAmEnde();
}

function denkDelta(ereignis) {
  if (!aktiveBlase) return;
  aktiveBlase.denkBox.classList.remove("hidden");
  aktiveBlase.denkEl.append(ereignis.delta);
}

function beitragEnde(ereignis) {
  // Das Fazit ist kein Redebeitrag: es zählt weder gegen die Rundenzahl noch
  // in der Teilnehmerkarte.
  if (ereignis.sorte !== "fazit") {
    fertigeBeitraege += 1;
    if (ereignis.profil) {
      beitragZaehler[ereignis.profil] = (beitragZaehler[ereignis.profil] || 0) + 1;
    }
  }
  if (aktiveBlase) {
    aktiveBlase.wurzel.classList.remove("blase-tippt");
    aktiveBlase.textEl.innerHTML = marked.parse(aktiveBlase.roh);
    aktiveBlase.textEl.classList.add("md");
    aktiveBlase.textEl.classList.remove("blase-text");
    if (ereignis.dauer_s) {
      aktiveBlase.wurzel.querySelector(".blase-dauer").textContent = `${ereignis.dauer_s} s`;
    }
    aktiveBlase = null;
  }
  rendereTeilnehmer(null);
  rendereFortschritt(aktuelleParty ? aktuelleParty.status : "laeuft");
  scrolleWennAmEnde();
}

function zwischenrufAnzeigen(ereignis) {
  const wurzel = $zwischenrufVorlage.content.firstElementChild.cloneNode(true);
  wurzel.querySelector(".zwischenruf-text").textContent = ereignis.text;
  wurzel.querySelector(".blase-runde").textContent =
    ereignis.runde ? `Runde ${ereignis.runde}` : "";
  $verlauf.appendChild(wurzel);
  zwischenrufe += 1;
  // Fortschritt statt nur Kennzahlen: „Zurücksetzen" hängt an den Zwischenrufen.
  if (aktuelleParty) rendereFortschritt(aktuelleParty.status);
  scrolleWennAmEnde();
}

function blaseZuruecksetzen() {
  if (!aktiveBlase) return;
  aktiveBlase.roh = "";
  aktiveBlase.textEl.textContent = "";
  aktiveBlase.denkEl.textContent = "";
  aktiveBlase.denkBox.classList.add("hidden");
}

function beitragVerworfen(text) {
  // Der Server hat den angefangenen Beitrag weggeworfen. Die Blase stehen zu
  // lassen und durchzustreichen ist ehrlicher, als sie verschwinden zu
  // lassen: man sieht, wie weit das Modell gekommen ist, und dass es nicht
  // zählt.
  if (aktiveBlase) {
    aktiveBlase.wurzel.classList.remove("blase-tippt");
    aktiveBlase.wurzel.classList.add("blase-verworfen");
    aktiveBlase = null;
  }
  systemBlase(text, "text-on-surface-variant border-on-surface/10 bg-surface-mid");
}

function systemBlase(text, klassen = "text-error border-error/40 bg-error-container/40") {
  const kasten = document.createElement("div");
  kasten.className = `text-sm border rounded-md p-3 ${klassen}`;
  kasten.textContent = text;
  $verlauf.appendChild(kasten);
  scrolleWennAmEnde();
}

// ---------------------------------------------------------------------------
// Steuerleiste: eingreifen, verlängern, abschließen
// ---------------------------------------------------------------------------
// Solange eine Anfrage unterwegs ist, ist der Griff belegt. Der gesperrte
// Knopf allein genügt nicht: die Enter-Taste kommt daran vorbei, und das Feld
// wird erst nach der Antwort geleert — zweimal Enter schickte sonst denselben
// Satz zweimal los.
let einwurfLaeuft = false;

async function zwischenrufEinwerfen() {
  if (!aktuelleParty || einwurfLaeuft) return true;
  const text = $zwischenrufFeld.value.trim();
  if (!text) return true;

  zeigeHinweis($steuerHinweis, "");
  einwurfLaeuft = true;
  $einwerfenBtn.disabled = true;
  const ergebnis = await wirfEin(aktuelleParty.slug, text);
  einwurfLaeuft = false;
  $einwerfenBtn.disabled = false;
  if (ergebnis.fehler) {
    zeigeHinweis($steuerHinweis, ergebnis.fehler);
    return false;
  }

  $zwischenrufFeld.value = "";
  // Läuft gerade nichts, gibt es auch keinen Strom, der den Einwurf zurück
  // ins Dashboard trägt — dann hängt ihn die Ansicht selbst an.
  if (!ergebnis.live) zwischenrufAnzeigen(ergebnis.eintrag);
  return true;
}

async function rundeAnhaengen() {
  if (!aktuelleParty) return;
  // Sofort sperren: zwei Anfragen hintereinander sind unterwegs, und ein
  // zweiter Klick hängt eine Runde an, die der Server gleich wieder
  // zurücknimmt. Auf dem Erfolgsweg setzt oeffneParty() den Knopf neu.
  $rundeBtn.disabled = true;

  // Steht noch ein Impuls im Feld, geht er der Runde voraus: ein Griff für
  // „so, und jetzt redet bitte darüber".
  if (!(await zwischenrufEinwerfen())) {
    $rundeBtn.disabled = false;
    return;
  }

  const ergebnis = await haengeRundeAn(aktuelleParty.slug);
  if (ergebnis.fehler) {
    $rundeBtn.disabled = false;
    await zeigeDialog({
      titel: "Die Runde startet nicht",
      text: ergebnis.fehler,
      mitAbbrechen: false,
    });
    return;
  }
  oeffneParty(aktuelleParty.slug);
}

async function fazitAnfordern() {
  if (!aktuelleParty) return;
  $fazitBtn.disabled = true;
  const ergebnis = await starteFazit(aktuelleParty.slug);
  if (ergebnis.fehler) {
    $fazitBtn.disabled = false;
    await zeigeDialog({
      titel: "Kein Fazit",
      text: ergebnis.fehler,
      mitAbbrechen: false,
    });
    return;
  }
  // Neu aufbauen: der Strom zeigt das Fazit dann live, wie einen Beitrag.
  oeffneParty(aktuelleParty.slug);
}

async function partyFortsetzen() {
  if (!aktuelleParty) return;
  const ergebnis = await starteParty(aktuelleParty.slug);
  if (ergebnis.fehler) {
    await zeigeDialog({
      titel: "Fortsetzen klappt nicht",
      text: ergebnis.fehler,
      mitAbbrechen: false,
    });
    return;
  }
  oeffneParty(aktuelleParty.slug);
}

async function partyAbbrechen() {
  if (!aktuelleParty) return;
  await stoppeParty(aktuelleParty.slug);
}

// ---------------------------------------------------------------------------
// Verdrahtung
// ---------------------------------------------------------------------------
function setzeListener() {
  document.getElementById("theme-toggle").addEventListener("click", wechsleTheme);

  $tabProfile.addEventListener("click", () => zeigeAnsicht("profile"));
  $tabEinrichten.addEventListener("click", () => zeigeAnsicht("einrichten"));
  $tabParty.addEventListener("click", () => {
    if (aktuelleParty) zeigeAnsicht("party", aktuelleParty.slug);
  });

  $speichernBtn.addEventListener("click", speichereProfil);
  $abbrechenBtn.addEventListener("click", () => oeffneEditor(null));
  $loeschenBtn.addEventListener("click", loescheProfil);
  $duplizierenBtn.addEventListener("click", dupliziereProfil);
  $entwurfBtn.addEventListener("click", entwurfStarten);
  $neueGruppeBtn.addEventListener("click", legeGruppeAn);
  $alleKlappenBtn.addEventListener("click", klappeAlle);
  $editorBreiteBtn.addEventListener("click", () => {
    setzeEditorBreit(!$ansichtProfile.classList.contains("editor-breit"));
  });

  $feldTitel.addEventListener("input", pruefeStartbereit);
  $feldStarter.addEventListener("input", pruefeStartbereit);
  $partyStartBtn.addEventListener("click", () => {
    if (bearbeitung) speichereParty();
    else partyAnlegenUndStarten();
  });
  $bearbeitenAbbrechenBtn.addEventListener("click", () => {
    const slug = bearbeitung && bearbeitung.slug;
    beendeBearbeitung();
    if (slug) zeigeAnsicht("party", slug);
  });

  $partyStopBtn.addEventListener("click", partyAbbrechen);
  $partyFortBtn.addEventListener("click", partyFortsetzen);
  $einwerfenBtn.addEventListener("click", zwischenrufEinwerfen);
  $zwischenrufFeld.addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    e.preventDefault();
    zwischenrufEinwerfen();
  });
  $rundeBtn.addEventListener("click", rundeAnhaengen);
  $fazitBtn.addEventListener("click", fazitAnfordern);
  $neuePartyBtn.addEventListener("click", () => zeigeAnsicht("einrichten"));
  $partyBearbeitenBtn.addEventListener("click", () => {
    if (aktuelleParty) starteBearbeitung(aktuelleParty.slug);
  });
  $partyZurueckBtn.addEventListener("click", async () => {
    if (!aktuelleParty) return;
    const { slug, sitzung } = aktuelleParty;
    if (await partyZuruecksetzen(slug, sitzung.titel, fertigeBeitraege)) oeffneParty(slug);
  });

  window.addEventListener("popstate", ausHash);
  window.addEventListener("beforeunload", schliesseStrom);
}

async function init() {
  setzeListener();
  const geladen = await ladeModelle();
  modelle = Array.isArray(geladen) ? geladen : [];
  oeffneEditor(null);
  ausHash();
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  init();
});
