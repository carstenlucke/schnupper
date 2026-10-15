<!--
  Das große Bild zu <AgentDurchlauf>: Dort lief ein kleiner Auftrag
  (einen Absatz kürzen) in drei Runden durch den Agenten. Hier ein
  größerer — Fakten im Referat prüfen und Quellen ergänzen — in rund
  dreißig Runden. Jedes Kästchen ist eine Runde: eine Anfrage ans
  Modell, und das Werkzeug, das es sich darin wünscht. Die letzte Runde
  wünscht sich keins mehr, das Modell meldet „fertig“.

  Dazwischen zwei Halte, an denen ihr gefragt seid — der Auftrag
  verlangt sie: Vor dem Korrigieren legt der Agent seinen Plan vor, ihr
  streicht eine Änderung (die gestrichene Korrektur bleibt als leeres
  Kästchenpaar stehen). Am Ende legt er seinen Bericht vor, ihr prüft.
  Halte zählen nicht als Runden; die Schleife wartet dort auf euch.

  Pro Klick kommt ein Abschnitt dazu, die Kästchen laufen nacheinander
  ein, oben zählt die Schleife mit. Im letzten Schritt markiert ein Ring
  zwei Runden beim Korrigieren: Absatz lesen, Absatz schreiben — das,
  was <AgentDurchlauf> Schritt für Schritt gezeigt hat.

  Die Rundenzahlen sind ausgedacht, liegen für so einen Auftrag aber in
  einer realistischen Größenordnung. Werkzeuge und Icons kommen aus
  `harness.ts`, damit sie zu <AgentDurchlauf> und <AgentAnatomie> passen.

  Geblättert wird mit den Klicks der Folie: Die Folie braucht
  `clicks: 8` (fünf Phasen und zwei Halte, dann Ring und Merksatz).
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { werkzeuge } from './harness'

/* 'aus': eine Korrektur, die ihr beim ersten Halt gestrichen habt */
type Runde = (typeof werkzeuge)[number]['id'] | 'fertig' | 'aus'

interface Phase {
  art: 'phase'
  name: string
  text: string
  erklaerung: string
  runden: Runde[]
  /* Kästchen pro Zeile; höchstens zwei Zeilen */
  spalten: number
  /* die beiden Runden, die <AgentDurchlauf> gezeigt hat */
  ausschnitt?: [number, number]
}

/* Ein Halt: Der Agent legt etwas vor, ihr antwortet */
interface Halt {
  art: 'halt'
  name: string
  text: string
  erklaerung: string
  antwort: string
}

type Abschnitt = Phase | Halt

const abschnitte: Abschnitt[] = [
  {
    art: 'phase',
    name: 'Verstehen',
    text: 'Referat und Aufgabe lesen',
    erklaerung: 'Zuerst liest der Agent euer Referat und die Aufgabenstellung.',
    runden: ['lesen', 'lesen'],
    spalten: 2,
  },
  {
    art: 'phase',
    name: 'Recherchieren',
    text: 'jede Zahl im Web nachschlagen',
    erklaerung: 'Dann schlägt er jede Zahl im Web nach und liest die Quellen — eine Runde pro Suche oder Seite.',
    runden: Array(14).fill('web'),
    spalten: 7,
  },
  {
    art: 'halt',
    name: 'Ihr gebt frei',
    text: 'Plan: 4\u00a0Zahlen ändern',
    erklaerung: 'Bevor er etwas ändert, legt er euch seinen Plan vor: vier Zahlen sind veraltet. Ihr streicht eine — die stimmt.',
    antwort: '„Nr. 3 nicht, die stimmt.“',
  },
  {
    art: 'phase',
    name: 'Korrigieren',
    text: 'veraltete Zahlen ersetzen',
    erklaerung: 'Er ersetzt nur, was ihr freigegeben habt: Absatz lesen, Absatz schreiben. Nr. 3 bleibt, wie sie ist.',
    runden: ['lesen', 'schreiben', 'lesen', 'schreiben', 'aus', 'aus', 'lesen', 'schreiben'],
    spalten: 4,
    ausschnitt: [6, 7],
  },
  {
    art: 'phase',
    name: 'Quellen ergänzen',
    text: 'Belege und Verzeichnis',
    erklaerung: 'Zu jeder Zahl kommt ein Beleg, am Ende ein Quellenverzeichnis.',
    runden: ['schreiben', 'schreiben', 'schreiben'],
    spalten: 3,
  },
  {
    art: 'phase',
    name: 'Kontrolle',
    text: 'Links testen, gegenlesen',
    erklaerung: 'Zum Schluss testet er mit einem kleinen Programm die Links, liest alles noch einmal — und meldet sich mit seinem Bericht.',
    runden: ['starten', 'lesen', 'fertig'],
    spalten: 3,
  },
  {
    art: 'halt',
    name: 'Ihr prüft',
    text: 'Bericht: 3\u00a0Zahlen, 9\u00a0Quellen',
    erklaerung: 'Am Ende prüft ihr den Bericht: Was hat er geändert, stimmt das? Erst dann ist der Auftrag erledigt.',
    antwort: '„Passt.“',
  },
]

const icon: Record<Runde, string> = {
  ...Object.fromEntries(werkzeuge.map(w => [w.id, w.icon])),
  fertig: 'check',
  aus: 'x',
} as Record<Runde, string>

const legende = [
  ...werkzeuge.map((w): { id: Runde, text: string } => ({ id: w.id, text: w.text })),
  { id: 'fertig' as Runde, text: 'fertig' },
  { id: 'aus' as Runde, text: 'von euch gestrichen' },
]

const { $clicks } = useSlideContext()
const schritte = abschnitte.length + 1
const n = computed(() => Math.min(Math.max($clicks.value, 0), schritte))
const fertig = computed(() => n.value === schritte)

/* Abschnitt i ist mit Klick i + 1 da */
const zustand = (i: number) => (n.value === i + 1 ? 'jetzt' : n.value > i + 1 ? 'vorbei' : 'kommt')
const da = (i: number) => n.value >= i + 1

/* Runden sind Anfragen ans Modell: Halte und gestrichene Korrekturen zählen nicht */
const zaehle = (liste: Abschnitt[]) =>
  liste.reduce((summe, a) => summe + (a.art === 'phase' ? a.runden.filter(r => r !== 'aus').length : 0), 0)
const runde = computed(() => zaehle(abschnitte.slice(0, n.value)))
const maxRunden = zaehle(abschnitte)
const wartet = computed(() => abschnitte[n.value - 1]?.art === 'halt')

const text = computed(() =>
  n.value === 0
    ? 'Ein größerer Auftrag — mit zwei Stellen, an denen ihr gefragt seid.'
    : abschnitte[n.value - 1]?.erklaerung ?? '',
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
        <span class="ga-blase">
          „Prüf die Fakten in meinem Referat, bring die Zahlen auf den neuesten Stand und ergänze die Quellen.
          <span class="ga-bericht">Zeig mir vorher, was du ändern willst, und berichte am Ende, was du geändert hast.“</span>
        </span>
      </div>
      <div class="ga-zaehler">
        <span class="ga-zaehler-titel"><ThmIcon name="refresh-cw" :size="0.9" /> Runde</span>
        <span class="ga-zaehler-zahl">{{ runde }}<small> / {{ maxRunden }}</small></span>
        <span class="ga-wartet" :class="{ an: wartet }">wartet auf euch</span>
      </div>
    </div>

    <!-- Mitte: Phasen mit ihren Runden, dazwischen eure Halte -->
    <div class="ga-phasen">
      <template v-for="(a, i) in abschnitte" :key="a.name">
        <div v-if="a.art === 'halt'" class="ga-halt" :class="zustand(i)">
          <div class="ga-phase-kopf">{{ a.name }}</div>
          <div class="ga-phase-text">{{ a.text }}</div>
          <div class="ga-halt-ihr" :class="{ da: da(i) }">
            <ThmIcon name="user" box :ton="zustand(i) === 'jetzt' ? 'gruen' : 'grau'" :size="1.6" />
            <span class="ga-antwort">{{ a.antwort }}</span>
          </div>
        </div>
        <div v-else class="ga-phase" :class="zustand(i)">
          <div class="ga-phase-kopf">{{ a.name }}</div>
          <div class="ga-phase-text">{{ a.text }}</div>
          <div class="ga-runden" :style="{ '--spalten': a.spalten }">
            <span
              v-for="(r, k) in a.runden"
              :key="k"
              class="ga-runde"
              :class="[r, { da: da(i), markiert: markiert(a, k) }]"
              :style="{ transitionDelay: da(i) ? `${k * 60}ms` : '0ms' }"
            >
              <ThmIcon :name="icon[r]" :ton="r === 'aus' ? 'grau' : 'weiss'" :size="0.85" />
            </span>
            <span
              v-if="a.ausschnitt"
              class="ga-ausschnitt"
              :class="{ da: fertig }"
              :style="{ gridColumn: `${a.ausschnitt[0] % a.spalten + 1} / span 2` }"
            >eben Schritt für Schritt</span>
          </div>
        </div>
      </template>
    </div>

    <!-- Welches Kästchen welches Werkzeug ist -->
    <div class="ga-legende">
      <span v-for="l in legende" :key="l.id" class="ga-legende-eintrag">
        <span class="ga-runde da klein" :class="l.id">
          <ThmIcon :name="icon[l.id]" :ton="l.id === 'aus' ? 'grau' : 'weiss'" :size="0.7" />
        </span>
        {{ l.text }}
      </span>
    </div>

    <SchrittZeile :schritt="n" :schritte="schritte" :text="text" :fertig="fertig" icon="refresh-cw">
      <strong>Dasselbe Prinzip, nur viel mehr Runden.</strong> Den Auftrag gebt ihr, prüfen müsst ihr selbst — vorher den Plan, am Ende den Bericht.
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

.ga-bericht { color: var(--thm-green-800); }

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

.ga-wartet {
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--thm-green-700);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ga-wartet.an { opacity: 1; }

.ga-zaehler-zahl small {
  font-size: 0.45em;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-400);
}

/* ---- Phasen ---- */

.ga-phasen {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.ga-phase,
.ga-halt {
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

.vorbei > .ga-phase-kopf { color: var(--text-strong); border-color: var(--thm-green-300); }
.jetzt > .ga-phase-kopf { color: var(--thm-green-700); border-color: var(--thm-green-500); }

/* Platz für zwei Zeilen, damit die Kästchen aller Phasen auf einer Höhe beginnen */
.ga-phase-text {
  max-width: 7.5rem;
  min-height: 2.5em;
  font-size: 0.85em;
  line-height: 1.25;
  color: var(--thm-grey-400);
  transition: color 0.3s ease;
}

.vorbei > .ga-phase-text { color: var(--thm-grey-500); }
.jetzt > .ga-phase-text { color: var(--text-strong); }

/* ---- Halt: ihr seid gefragt ---- */

.ga-phase { padding-top: 0.4rem; }

/* Eigene Fläche, Kopf auf derselben Höhe wie bei den Phasen */
.ga-halt {
  padding: 0.4rem 0.6rem 0.5rem;
  background: var(--thm-grey-50);
}

.ga-halt .ga-phase-kopf { margin: 0 -0.6rem; padding-left: 0.6rem; }

.ga-halt-ihr {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.35rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ga-halt-ihr.da { opacity: 1; }

.ga-antwort {
  max-width: 7.5rem;
  padding: 0.3rem 0.5rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  font-size: 0.85em;
  font-weight: var(--fw-semibold);
  line-height: 1.25;
  color: var(--text-strong);
}

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
.ga-runde.da.aus { border: 1px dashed var(--thm-grey-300); }

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
