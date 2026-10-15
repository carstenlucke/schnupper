<!--
  Das große Bild zu <AgentDurchlauf>: Dort lief ein kleiner Auftrag
  (einen Absatz kürzen) in drei Runden durch den Agenten. Hier ein
  größerer — Fakten im Referat prüfen und Quellen ergänzen — in rund
  dreißig Runden. Jedes Kästchen ist eine Runde: eine Anfrage ans
  Modell, und das Werkzeug, das es sich darin wünscht. Die letzte Runde
  wünscht sich keins mehr, das Modell meldet „fertig“.

  Pro Klick kommt eine Phase dazu, die Kästchen laufen nacheinander ein,
  oben zählt die Schleife mit. Im letzten Schritt markiert ein Ring
  zwei Runden beim Korrigieren: Absatz lesen, Absatz schreiben — das,
  was <AgentDurchlauf> Schritt für Schritt gezeigt hat.

  Die Rundenzahlen sind ausgedacht, liegen für so einen Auftrag aber in
  einer realistischen Größenordnung. Werkzeuge und Icons kommen aus
  `harness.ts`, damit sie zu <AgentDurchlauf> und <AgentAnatomie> passen.

  Geblättert wird mit den Klicks der Folie: Die Folie braucht
  `clicks: 6` (fünf Phasen, dann Ring und Merksatz).
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { werkzeuge } from './harness'

type Runde = 'lesen' | 'schreiben' | 'starten' | 'web' | 'fertig'

interface Phase {
  name: string
  text: string
  erklaerung: string
  runden: Runde[]
  /* Kästchen pro Zeile; höchstens zwei Zeilen */
  spalten: number
  /* die beiden Runden, die <AgentDurchlauf> gezeigt hat */
  ausschnitt?: [number, number]
}

const phasen: Phase[] = [
  {
    name: 'Verstehen',
    text: 'Referat und Aufgabe lesen',
    erklaerung: 'Zuerst liest der Agent euer Referat und die Aufgabenstellung.',
    runden: ['lesen', 'lesen'],
    spalten: 2,
  },
  {
    name: 'Recherchieren',
    text: 'jede Zahl im Web nachschlagen',
    erklaerung: 'Dann schlägt er jede Zahl im Web nach und liest die Quellen — eine Runde pro Suche oder Seite.',
    runden: Array(14).fill('web'),
    spalten: 7,
  },
  {
    name: 'Korrigieren',
    text: 'veraltete Zahlen ersetzen',
    erklaerung: 'Wo eine Zahl nicht mehr stimmt, ersetzt er sie: Absatz lesen, Absatz schreiben.',
    runden: ['lesen', 'schreiben', 'lesen', 'schreiben', 'lesen', 'schreiben', 'lesen', 'schreiben'],
    spalten: 4,
    ausschnitt: [4, 5],
  },
  {
    name: 'Quellen ergänzen',
    text: 'Belege und Verzeichnis',
    erklaerung: 'Zu jeder Zahl kommt ein Beleg, am Ende ein Quellenverzeichnis.',
    runden: ['schreiben', 'schreiben', 'schreiben'],
    spalten: 3,
  },
  {
    name: 'Kontrolle',
    text: 'Links testen, alles noch mal lesen',
    erklaerung: 'Zum Schluss testet er mit einem kleinen Programm die Links, liest alles noch einmal — und meldet: fertig.',
    runden: ['starten', 'lesen', 'fertig'],
    spalten: 3,
  },
]

const icon: Record<Runde, string> = {
  ...Object.fromEntries(werkzeuge.map(w => [w.id, w.icon])),
  fertig: 'check',
} as Record<Runde, string>

const legende = [
  ...werkzeuge.map(w => ({ id: w.id as Runde, text: w.text })),
  { id: 'fertig' as Runde, text: 'fertig' },
]

const { $clicks } = useSlideContext()
const schritte = phasen.length + 1
const n = computed(() => Math.min(Math.max($clicks.value, 0), schritte))
const fertig = computed(() => n.value === schritte)

/* Phase i ist mit Klick i + 1 da */
const zustand = (i: number) => (n.value === i + 1 ? 'jetzt' : n.value > i + 1 ? 'vorbei' : 'kommt')
const da = (i: number) => n.value >= i + 1

const runde = computed(() =>
  phasen.slice(0, n.value).reduce((summe, p) => summe + p.runden.length, 0),
)
const maxRunden = phasen.reduce((summe, p) => summe + p.runden.length, 0)

const text = computed(() =>
  n.value === 0
    ? 'Ein größerer Auftrag — ihr gebt ihn einmal, wie vorhin.'
    : phasen[n.value - 1]?.erklaerung ?? '',
)

const markiert = (p: Phase, k: number) =>
  fertig.value && !!p.ausschnitt && k >= p.ausschnitt[0] && k <= p.ausschnitt[1]
</script>

<template>
  <div class="ga">
    <!-- Oben: euer Auftrag und der Rundenzähler -->
    <div class="ga-oben">
      <div class="ga-auftrag">
        <ThmIcon name="user" box :size="2" />
        <span class="ga-blase">„Prüf die Fakten in meinem Referat, bring die Zahlen auf den neuesten Stand und ergänze die Quellen.“</span>
      </div>
      <div class="ga-zaehler">
        <span class="ga-zaehler-titel"><ThmIcon name="refresh-cw" :size="0.9" /> Runde</span>
        <span class="ga-zaehler-zahl">{{ runde }}<small> / {{ maxRunden }}</small></span>
      </div>
    </div>

    <!-- Mitte: die Phasen mit ihren Runden -->
    <div class="ga-phasen">
      <div v-for="(p, i) in phasen" :key="p.name" class="ga-phase" :class="zustand(i)">
        <div class="ga-phase-kopf">{{ p.name }}</div>
        <div class="ga-phase-text">{{ p.text }}</div>
        <div class="ga-runden" :style="{ '--spalten': p.spalten }">
          <span
            v-for="(r, k) in p.runden"
            :key="k"
            class="ga-runde"
            :class="[r, { da: da(i), markiert: markiert(p, k) }]"
            :style="{ transitionDelay: da(i) ? `${k * 60}ms` : '0ms' }"
          >
            <ThmIcon :name="icon[r]" ton="weiss" :size="0.85" />
          </span>
          <span
            v-if="p.ausschnitt"
            class="ga-ausschnitt"
            :class="{ da: fertig }"
            :style="{ gridColumn: `${p.ausschnitt[0] % p.spalten + 1} / span 2` }"
          >eben Schritt für Schritt</span>
        </div>
      </div>
    </div>

    <!-- Welches Kästchen welches Werkzeug ist -->
    <div class="ga-legende">
      <span v-for="l in legende" :key="l.id" class="ga-legende-eintrag">
        <span class="ga-runde da klein" :class="l.id"><ThmIcon :name="icon[l.id]" ton="weiss" :size="0.7" /></span>
        {{ l.text }}
      </span>
    </div>

    <SchrittZeile :schritt="n" :schritte="schritte" :text="text" :fertig="fertig" icon="refresh-cw">
      <strong>Dasselbe Prinzip, nur viel mehr Runden.</strong> Ihr gebt einmal den Auftrag — {{ maxRunden }} Runden später ist das Referat geprüft.
    </SchrittZeile>
  </div>
</template>

<style scoped>
.ga {
  --kaestchen: 1.6rem;
  --luecke: 0.25rem;
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
}

/* ---- Oben: Auftrag und Zähler ---- */

.ga-oben {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 1.4rem;
}

.ga-auftrag {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.ga-blase {
  padding: 0.5rem 0.8rem;
  background: var(--thm-grey-100);
  font-size: 1.05em;
  font-weight: var(--fw-semibold);
  line-height: 1.3;
  color: var(--text-strong);
}

.ga-zaehler {
  flex: none;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.ga-zaehler-titel {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.ga-zaehler-zahl {
  font-size: 2.2em;
  font-weight: var(--fw-bold);
  line-height: 1;
  color: var(--text-strong);
  font-variant-numeric: tabular-nums;
}

.ga-zaehler-zahl small {
  font-size: 0.45em;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-400);
}

/* ---- Phasen ---- */

.ga-phasen {
  display: flex;
  justify-content: space-between;
  gap: 1.4rem;
}

.ga-phase {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.ga-phase-kopf {
  padding-bottom: 0.25rem;
  border-bottom: 2px solid var(--thm-grey-200);
  font-weight: var(--fw-bold);
  white-space: nowrap;
  color: var(--thm-grey-400);
  transition: color 0.3s ease, border-color 0.3s ease;
}

.ga-phase.vorbei .ga-phase-kopf { color: var(--text-strong); border-color: var(--thm-green-300); }
.ga-phase.jetzt .ga-phase-kopf { color: var(--thm-green-700); border-color: var(--thm-green-500); }

/* Platz für zwei Zeilen, damit die Kästchen aller Phasen auf einer Höhe beginnen */
.ga-phase-text {
  max-width: 9.5rem;
  min-height: 2.5em;
  font-size: 0.85em;
  line-height: 1.25;
  color: var(--thm-grey-400);
  transition: color 0.3s ease;
}

.ga-phase.vorbei .ga-phase-text { color: var(--thm-grey-500); }
.ga-phase.jetzt .ga-phase-text { color: var(--text-strong); }

/* Zwei Zeilen Kästchen, darunter Platz für den Strich */
.ga-runden {
  display: grid;
  grid-template-columns: repeat(var(--spalten), var(--kaestchen));
  grid-template-rows: var(--kaestchen) var(--kaestchen) 1.5rem;
  gap: var(--luecke);
}

.ga-runde {
  display: grid;
  place-items: center;
  width: var(--kaestchen);
  height: var(--kaestchen);
  border: 1px dashed var(--thm-grey-200);
  border-radius: var(--radius-icon);
  transition: background 0.25s ease, border-color 0.25s ease, outline-color 0.3s ease;
}

.ga-runde :deep(.thm-icon) {
  opacity: 0;
  transition: opacity 0.25s ease;
  transition-delay: inherit;
}

.ga-runde.da { border: 1px solid transparent; }
.ga-runde.da :deep(.thm-icon) { opacity: 1; }

/* Farbe je Werkzeug */
.ga-runde.da.lesen { background: var(--thm-grey-400); }
.ga-runde.da.schreiben { background: var(--thm-green-500); }
.ga-runde.da.web { background: var(--role-source); }
.ga-runde.da.starten { background: var(--thm-grey-700); }
.ga-runde.da.fertig { background: var(--thm-green-800); }

.ga-runde.markiert {
  outline: 2px solid var(--thm-green-700);
  outline-offset: 2px;
}

/* Strich unter den beiden Runden von eben */
.ga-ausschnitt {
  grid-row: 3;
  margin-top: 0.35rem;
  padding-top: 0.25rem;
  border-top: 2px solid var(--thm-green-700);
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  line-height: 1.1;
  white-space: nowrap;
  color: var(--thm-green-700);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ga-ausschnitt.da { opacity: 1; }

/* ---- Legende ---- */

.ga-legende {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.4rem 1.4rem;
  margin-top: 0.6rem;
  font-size: 0.85em;
  color: var(--thm-grey-500);
}

.ga-legende-eintrag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.ga-runde.klein {
  --kaestchen: 1.15rem;
}
</style>
