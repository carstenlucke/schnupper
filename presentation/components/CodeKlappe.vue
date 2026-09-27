<!--
  Knopf unter dem SQL-Beispiel auf „Vom Code zur Sprache“: öffnet über der
  Folie echten Programmcode für eine Aufgabe, die später ein Agent mit zwei
  Sätzen erledigt — Primzahlen aus einem Zahlenstrom sammeln, Zahl für Zahl,
  und sich merken, wie weit man gekommen ist.

  Der Code ist lauffähiges TypeScript (Node), aber nicht zum Lesen gedacht:
  Er soll zeigen, wie viel Handwerk hinter einem Satz steckt. Der Satz
  rechts folgt dem Rollentext des Primzahl-Agenten in
  the-counting-agents/agents/prime.md — ohne die Demo auf der Folie zu
  nennen, denn die Folie gehört zum gemeinsamen Strang.

  Die Einfärbung macht ein kleiner Tokenizer hier, damit die Farben im CD
  bleiben. Das Overlay ist `position: fixed` und liegt damit über der
  ganzen Folie (die Folie ist transformiert und fängt es ein).
-->
<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from 'vue'

const code = `// Primzahlen aus dem Zahlenstrom sammeln — Zahl für Zahl
import { readFileSync, writeFileSync } from "node:fs";

type Stand = { erledigt: number; primzahlen: number[] };

function istPrimzahl(n: number): boolean {
  if (n < 2) return false;
  for (let teiler = 2; teiler * teiler <= n; teiler++) {
    if (n % teiler === 0) return false;
  }
  return true;
}

const stand: Stand = JSON.parse(readFileSync("stand.json", "utf8"));
const zahlen = readFileSync("zahlen.log", "utf8")
  .split("\\n")
  .filter((zeile) => zeile.trim() !== "")
  .map(Number);

const n = zahlen[stand.erledigt];
if (n !== undefined) {
  if (istPrimzahl(n)) stand.primzahlen.push(n);
  stand.erledigt += 1;
  writeFileSync("stand.json", JSON.stringify(stand));
}`

const zeilen = code.split('\n')

const muster = /(\/\/.*$)|("(?:[^"\\]|\\.)*")|\b(import|from|type|function|if|return|for|let|const|false|true|undefined)\b|\b(number|boolean)\b|\b(\d+)\b/g

function escape(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

function faerben(zeile: string) {
  let html = ''
  let pos = 0
  for (const m of zeile.matchAll(muster)) {
    html += escape(zeile.slice(pos, m.index))
    const klasse = m[1] ? 'kommentar' : m[2] ? 'text' : m[3] ? 'wort' : m[4] ? 'typ' : 'zahl'
    html += `<span class="${klasse}">${escape(m[0])}</span>`
    pos = m.index! + m[0].length
  }
  return html + escape(zeile.slice(pos))
}

const gefaerbt = zeilen.map(faerben)

const offen = ref(false)

function oeffnen(e: MouseEvent) {
  offen.value = true;
  /* Sonst löst die Leertaste zum Weiterblättern den Knopf erneut aus */
  (e.currentTarget as HTMLElement).blur()
}

function taste(e: KeyboardEvent) {
  if (e.key === 'Escape') offen.value = false
}

watch(offen, o => o
  ? window.addEventListener('keydown', taste)
  : window.removeEventListener('keydown', taste))
onBeforeUnmount(() => window.removeEventListener('keydown', taste))
</script>

<template>
  <button class="ck-knopf" @click="oeffnen">
    <ThmIcon name="code" :size="0.9" />
    Und wenn es komplizierter wird?
  </button>

  <div v-if="offen" class="ck-overlay" @click.self="offen = false">
    <div class="ck-panel">
      <button class="ck-zu" aria-label="Schließen" @click="offen = false">
        <ThmIcon name="x" :size="1.1" />
      </button>

      <div class="ck-spalte">
        <div class="thm-eyebrow">Früher · Primzahlen sammeln in TypeScript</div>
        <pre class="ck-code"><code><span v-for="(z, i) in gefaerbt" :key="i" class="ck-zeile"><span class="ck-nr">{{ i + 1 }}</span><span v-html="z" /></span></code></pre>
      </div>

      <div class="ck-spalte ck-heute">
        <div class="thm-eyebrow">Heute · als Auftrag an einen Agenten</div>
        <div class="ck-satz">
          „Prüf jede Zahl, ob sie eine Primzahl ist, und sammle die, die es
          sind. Merk dir, wie weit du gekommen bist.“
        </div>
        <div class="ck-bilanz">
          <span><strong>{{ zeilen.length }}</strong> Zeilen Code</span>
          <span class="ck-gegen">gegen</span>
          <span><strong>2</strong> Sätze</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ck-knopf {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.7rem;
  padding: 0.3rem 0.7rem;
  font: inherit;
  font-size: 0.72rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-600);
  background: var(--white);
  border: 1px solid var(--thm-grey-300);
  cursor: pointer;
}

.ck-knopf:hover {
  border-color: var(--thm-green-500);
  color: var(--thm-green-700);
}

.ck-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 44, 49, 0.55);
}

.ck-panel {
  position: relative;
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  gap: 1.6rem;
  width: calc(100% - 3rem);
  max-height: calc(100% - 2.4rem);
  padding: 1.3rem 1.5rem;
  background: var(--white);
  border-top: 0.3rem solid var(--thm-green-500);
  font-size: 1rem;
}

.ck-zu {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  padding: 0.2rem;
  background: none;
  border: none;
  color: var(--thm-grey-500);
  cursor: pointer;
}

.ck-spalte {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  min-width: 0;
}

.ck-code {
  margin: 0;
  padding: 0.7rem 0.9rem;
  background: var(--thm-grey-800);
  color: var(--thm-grey-100);
  font-family: var(--font-mono);
  font-size: 0.66rem;
  line-height: 1.5;
  /* Keine Ligaturen: `===` soll aussehen wie getippt, nicht wie ≡ */
  font-variant-ligatures: none;
  font-feature-settings: 'calt' 0, 'liga' 0;
  overflow: hidden;
}

/* Die globale Formatierung für Inline-Code nicht übernehmen */
.ck-code code {
  display: block;
  padding: 0;
  background: none;
  border: none;
  color: inherit;
  font: inherit;
}

.ck-zeile { display: block; white-space: pre; }

.ck-nr {
  display: inline-block;
  width: 1.6rem;
  margin-right: 0.6rem;
  text-align: right;
  color: var(--thm-grey-500);
  user-select: none;
}

.ck-code :deep(.kommentar) { color: var(--thm-grey-400); font-style: italic; }
.ck-code :deep(.text) { color: var(--thm-green-300); }
.ck-code :deep(.wort) { color: var(--thm-cyan); }
.ck-code :deep(.typ) { color: var(--thm-green-400); }
.ck-code :deep(.zahl) { color: var(--thm-green-200); }

.ck-heute { justify-content: center; }

.ck-satz {
  padding: 0.8rem 1rem;
  background: var(--thm-green-50);
  border-left: 0.25rem solid var(--thm-green-500);
  font-size: 1.05rem;
  font-style: italic;
  line-height: var(--lh-snug);
  color: var(--text-strong);
}

.ck-bilanz {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--thm-grey-600);
}

.ck-bilanz strong {
  font-size: 1.6rem;
  color: var(--thm-green-600);
}

.ck-gegen { color: var(--thm-grey-400); }
</style>
