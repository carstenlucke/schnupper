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
let modelle = [];
let editorSlug = null;          // null = neues Profil
let entwurfAbbruch = null;      // AbortController; nicht-null = Entwurf läuft
let besetzung = [];             // Slugs in Sprechreihenfolge, jeder höchstens einmal
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

const neueParty = (daten) =>
  api("/api/partys", { method: "POST", body: JSON.stringify(daten) });
const starteParty = (slug) => api(`/api/partys/${slug}/start`, { method: "POST" });
const stoppeParty = (slug) => api(`/api/partys/${slug}/stop`, { method: "POST" });
const wirfEin = (slug, text) =>
  api(`/api/partys/${slug}/zwischenruf`, { method: "POST", body: JSON.stringify({ text }) });
const haengeRundeAn = (slug) => api(`/api/partys/${slug}/runde`, { method: "POST" });
const starteFazit = (slug) => api(`/api/partys/${slug}/fazit`, { method: "POST" });
const entferneParty = (slug) => api(`/api/partys/${slug}`, { method: "DELETE" });

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

const $profilRaster = document.getElementById("profil-raster");
const $profileAnzahl = document.getElementById("profile-anzahl");
const $editorTitel = document.getElementById("editor-titel");
const $feldName = document.getElementById("feld-name");
const $feldBeschreibung = document.getElementById("feld-beschreibung");
const $feldModel = document.getElementById("feld-model");
const $feldThinking = document.getElementById("feld-thinking");
const $farbwahl = document.getElementById("farbwahl");
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
const $neuePartyBtn = document.getElementById("neue-party-btn");
const $steuerHinweis = document.getElementById("steuer-hinweis");

const $dialogHintergrund = document.getElementById("dialog-hintergrund");
const $dialogTitel = document.getElementById("dialog-titel");
const $dialogText = document.getElementById("dialog-text");
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
function zeigeDialog({ titel, text, okText = "OK", mitAbbrechen = true }) {
  return new Promise((aufloesen) => {
    $dialogTitel.textContent = titel;
    $dialogText.textContent = text;
    $dialogOk.textContent = okText;
    $dialogAbbrechen.classList.toggle("hidden", !mitAbbrechen);
    $dialogHintergrund.classList.remove("hidden");

    const schliessen = (ergebnis) => {
      $dialogHintergrund.classList.add("hidden");
      $dialogOk.removeEventListener("click", aufOk);
      $dialogAbbrechen.removeEventListener("click", aufAbbruch);
      aufloesen(ergebnis);
    };
    const aufOk = () => schliessen(true);
    const aufAbbruch = () => schliessen(false);

    $dialogOk.addEventListener("click", aufOk);
    $dialogAbbrechen.addEventListener("click", aufAbbruch);
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

function rendereProfilRaster() {
  $profilRaster.innerHTML = "";
  $profileAnzahl.textContent = `${profile.length} ${profile.length === 1 ? "Profil" : "Profile"}`;

  if (profile.length === 0) {
    const leer = document.createElement("p");
    leer.className = "text-sm text-on-surface-variant sm:col-span-2";
    leer.textContent = "Noch kein Profil da. Rechts eins anlegen — von Hand oder ausarbeiten lassen.";
    $profilRaster.appendChild(leer);
    return;
  }

  profile.forEach((profil) => {
    const kachel = baueKachel(profil);
    if (editorSlug === profil.slug) kachel.classList.add("kachel-gewaehlt");
    kachel.querySelector(".kachel-bearbeiten").addEventListener("click", () => {
      oeffneEditor(profil.slug);
    });
    $profilRaster.appendChild(kachel);
  });
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
  $loeschenBtn.classList.toggle("hidden", !profil);
  $duplizierenBtn.classList.toggle("hidden", !profil);
  zeigeHinweis($editorHinweis, "");
  rendereProfilRaster();
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
  rendereProfilRaster();
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

  profile = await ladeProfile();
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

  profile = await ladeProfile();
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
  rendereProfilRaster();
}

async function ladeUndRendereProfile() {
  profile = await ladeProfile();
  if (profile.fehler) profile = [];
  rendereProfilRaster();
  if (!$feldModel.options.length) rendereModellauswahl($feldModel, "");
}

// ---------------------------------------------------------------------------
// Ansicht 2: Party einrichten
// ---------------------------------------------------------------------------
function rendereAuswahl() {
  $auswahlRaster.innerHTML = "";
  if (profile.length === 0) {
    const leer = document.createElement("p");
    leer.className = "text-sm text-on-surface-variant sm:col-span-2";
    leer.textContent = "Erst Profile anlegen, dann kann die Party losgehen.";
    $auswahlRaster.appendChild(leer);
    return;
  }
  profile.forEach((profil) => {
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
    $auswahlRaster.appendChild(kachel);
  });
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
      <button class="weg p-1 rounded hover:bg-on-surface/10" aria-label="Party löschen" title="Party löschen">
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant" aria-hidden="true">delete</span>
      </button>`;
    zeile.querySelector(".oeffnen").addEventListener("click", () => {
      zeigeAnsicht("party", eintrag.slug);
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
  profile = await ladeProfile();
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

async function partyAnlegenUndStarten() {
  zeigeHinweis($einrichtenHinweis, "");
  const angelegt = await neueParty({
    titel: $feldTitel.value,
    starter: $feldStarter.value,
    teilnehmer: besetzung,
    runden: parseInt($feldRunden.value, 10) || 2,
    modell: $feldPartymodell.value,
  });
  if (angelegt.fehler) return zeigeHinweis($einrichtenHinweis, angelegt.fehler);

  const gestartet = await starteParty(angelegt.slug);
  if (gestartet.fehler) return zeigeHinweis($einrichtenHinweis, gestartet.fehler);

  zeigeAnsicht("party", angelegt.slug);
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
  rendereKennzahlen();
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

  $feldTitel.addEventListener("input", pruefeStartbereit);
  $feldStarter.addEventListener("input", pruefeStartbereit);
  $partyStartBtn.addEventListener("click", partyAnlegenUndStarten);

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
