<!--
  Ein Agent bei der Arbeit, Klick für Klick: ein Auftrag läuft einmal
  durch den Agenten. Gegenstück zu <CopyPasteSchleife> — dasselbe
  Referat, aber jetzt trägt nicht ihr die Texte hin und her, sondern das
  Harness.

  Links das Modell, in der Mitte das Harness mit den vier Bausteinen der
  Steuerung aus <AgentAnatomie>, rechts die Werkzeuge und das Referat,
  oben ihr. Jeder Klick schickt eine Nachricht über einen Pfeil; der
  aktive Pfeil wird grün, ein Punkt läuft darüber, die Nachricht steht
  daneben. Im Harness leuchtet auf, was gerade gebraucht wird: die
  Schleife zählt die Runden, das Gedächtnis sammelt Einträge, die
  Leitplanken prüfen jeden Werkzeugwunsch. Unten erklärt eine Zeile den
  Schritt; nach dem letzten wird sie zum Merksatz.

  Geblättert wird mit den Klicks der Folie: Die Folie braucht
  `clicks: 10` (Schritte 1 bis 10, Klick 0 ist das Ausgangsbild).
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

type Pfeil = 'auftrag' | 'ergebnis' | 'zumModell' | 'vomModell' | 'zumWerkzeug' | 'vomWerkzeug'

interface Schritt {
  text: string
  pfeile?: Partial<Record<Pfeil, string>>
  werkzeug?: 'lesen' | 'schreiben'
  /* die Anweisungen gehen mit ans Modell und leuchten auf */
  anweisungen?: boolean
}

const schritte: Schritt[] = [
  { text: 'Ein Auftrag, Schritt für Schritt durch den Agenten.' },
  {
    text: 'Ihr gebt den Auftrag — einmal, in ganz normalem Deutsch.',
    pfeile: { auftrag: '„Mach Absatz 3 in meinem Referat besser.“' },
  },
  {
    text: 'Das Harness schickt den Auftrag ans Modell, dazu seine Anweisungen und die Liste der Werkzeuge.',
    pfeile: { zumModell: 'Auftrag + Anweisungen + Werkzeuge' },
    anweisungen: true,
  },
  {
    text: 'Das Modell kann nichts anfassen. Es antwortet mit einem Wunsch: dieses Werkzeug, bitte.',
    pfeile: { vomModell: 'Bitte „Datei lesen“: Referat.docx' },
  },
  {
    text: 'Das Harness prüft, ob das erlaubt ist — und führt das Werkzeug aus.',
    pfeile: { zumWerkzeug: 'Datei lesen' },
    werkzeug: 'lesen',
  },
  {
    text: 'Das Ergebnis geht ans Modell — und alles andere noch einmal mit. Das Modell merkt sich nichts.',
    pfeile: { vomWerkzeug: 'Text des Referats', zumModell: 'Anweisungen + Werkzeuge + Verlauf' },
    anweisungen: true,
  },
  {
    text: 'Jetzt kennt das Modell das Referat und schreibt einen besseren Absatz 3.',
    pfeile: { vomModell: 'Bitte „Datei schreiben“: neuer Absatz 3' },
  },
  {
    text: 'Wieder prüft das Harness — und speichert den neuen Absatz im Referat.',
    pfeile: { zumWerkzeug: 'Datei schreiben' },
    werkzeug: 'schreiben',
  },
  {
    text: 'Dritte Runde: Das Modell erfährt, dass es geklappt hat.',
    pfeile: { vomWerkzeug: 'gespeichert ✓', zumModell: 'Anweisungen + Werkzeuge + Verlauf' },
    anweisungen: true,
  },
  {
    text: 'Kein Werkzeug mehr nötig — das Modell meldet: fertig.',
    pfeile: { vomModell: '„Fertig: Absatz 3 ist überarbeitet.“' },
  },
  {
    text: '',
    pfeile: { ergebnis: '„Absatz 3 ist überarbeitet.“' },
  },
]

/* Beschriftung der Pfeile, solange gerade nichts über sie läuft */
const ruhe: Record<Pfeil, string> = {
  auftrag: 'Auftrag',
  ergebnis: 'Ergebnis',
  zumModell: 'Anfrage',
  vomModell: 'Antwort',
  zumWerkzeug: 'ausführen',
  vomWerkzeug: 'Ergebnis',
}

/* Was im Gedächtnis landet: euer Auftrag, jede Antwort des Modells,
   jedes Ergebnis eines Werkzeugs */
const merkt: Pfeil[] = ['auftrag', 'vomModell', 'vomWerkzeug']

const { $clicks } = useSlideContext()
const n = computed(() => Math.min(Math.max($clicks.value, 0), schritte.length - 1))
const s = computed(() => schritte[n.value])

const aktiv = (p: Pfeil) => s.value.pfeile?.[p] !== undefined
const text = (p: Pfeil) => s.value.pfeile?.[p] ?? ruhe[p]

/* Runden zählen die Anfragen ans Modell, Einträge alles, was im Gedächtnis landet */
const zaehleRunden = (liste: Schritt[]) => liste.filter(x => x.pfeile?.zumModell).length
const zaehleEintraege = (liste: Schritt[]) =>
  liste.reduce((summe, x) => summe + merkt.filter(p => x.pfeile?.[p]).length, 0)

const bisher = computed(() => schritte.slice(0, n.value + 1))
const runde = computed(() => zaehleRunden(bisher.value))
const eintraege = computed(() => zaehleEintraege(bisher.value))
const maxRunden = zaehleRunden(schritte)
const maxEintraege = zaehleEintraege(schritte)

const steuerung = computed(() => [
  {
    icon: 'refresh-cw',
    name: 'Schleife',
    an: aktiv('zumModell'),
    info: runde.value
      ? `Runde ${runde.value}`
      : aktiv('auftrag') ? 'Auftrag ist da' : 'wartet auf einen Auftrag',
  },
  {
    icon: 'file-text',
    name: 'Anweisungen',
    an: !!s.value.anweisungen,
    info: s.value.anweisungen ? 'gehen mit ans Modell' : 'Rolle und Aufgabe',
  },
  {
    icon: 'notebook-pen',
    name: 'Gedächtnis',
    an: merkt.some(aktiv),
    info: '',
  },
  {
    icon: 'shield-check',
    name: 'Leitplanken',
    an: !!s.value.werkzeug,
    info: s.value.werkzeug ? `„Datei ${s.value.werkzeug}“ ist erlaubt ✓` : 'was erlaubt ist',
  },
])

const werkzeuge = [
  { id: 'lesen', icon: 'eye', text: 'Dateien lesen' },
  { id: 'schreiben', icon: 'pen-line', text: 'Dateien schreiben' },
  { id: 'starten', icon: 'square-terminal', text: 'Programme starten' },
  { id: 'web', icon: 'globe', text: 'Im Web suchen' },
]

const modellAktiv = computed(() => aktiv('zumModell') || aktiv('vomModell'))
const liest = computed(() => s.value.werkzeug === 'lesen')
const geschrieben = computed(() => bisher.value.some(x => x.werkzeug === 'schreiben'))
const fertig = computed(() => n.value === schritte.length - 1)
</script>

<template>
  <div class="ad">
    <!-- Oben: ihr, mit Auftrag hinein und Ergebnis heraus -->
    <div class="ad-oben">
      <div class="ad-vpfeil runter" :class="{ aktiv: aktiv('auftrag') }">
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('auftrag')" class="ad-nachricht links">{{ text('auftrag') }}</span>
        </Transition>
        <div class="ad-linie"><span class="ad-punkt" /></div>
      </div>
      <div class="ad-ihr">
        <ThmIcon name="user" box :size="2" />
        <span>Ihr</span>
      </div>
      <div class="ad-vpfeil hoch" :class="{ aktiv: aktiv('ergebnis') }">
        <div class="ad-linie"><span class="ad-punkt" /></div>
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('ergebnis')" class="ad-nachricht rechts">{{ text('ergebnis') }}</span>
        </Transition>
      </div>
    </div>

    <!-- Links: das Modell -->
    <div class="ad-modell" :class="{ aktiv: modellAktiv }">
      <ThmIcon name="brain" box :size="2.6" />
      <div class="ad-modell-titel">Modell</div>
      <div class="ad-modell-text">denkt und entscheidet</div>
      <div class="ad-denkt" :class="{ an: aktiv('zumModell') }">denkt nach <i /><i /><i /></div>
    </div>

    <!-- Zwischen Modell und Harness -->
    <div class="ad-spalte">
      <div class="ad-pfeil links oben" :class="{ aktiv: aktiv('zumModell') }">
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('zumModell')" class="ad-nachricht">{{ text('zumModell') }}</span>
        </Transition>
        <div class="ad-linie"><span class="ad-punkt" /></div>
      </div>
      <div class="ad-pfeil rechts unten" :class="{ aktiv: aktiv('vomModell') }">
        <div class="ad-linie"><span class="ad-punkt" /></div>
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('vomModell')" class="ad-nachricht">{{ text('vomModell') }}</span>
        </Transition>
      </div>
    </div>

    <!-- Mitte: das Harness mit seiner Steuerung -->
    <div class="ad-harness">
      <div class="ad-harness-titel"><ThmIcon name="wrench" ton="weiss" :size="0.95" /> Harness</div>
      <div v-for="b in steuerung" :key="b.name" class="ad-baustein" :class="{ an: b.an }">
        <ThmIcon :name="b.icon" box :ton="b.an ? 'gruen' : 'grau'" :size="1.5" />
        <span class="ad-baustein-text">
          <strong>{{ b.name }}</strong>
          <span v-if="b.name === 'Gedächtnis'" class="ad-verlauf">
            <i v-for="k in maxEintraege" :key="k" :class="{ voll: k <= eintraege }" />
          </span>
          <span v-else-if="b.name === 'Schleife' && runde" class="ad-runden">
            {{ b.info }}
            <i v-for="k in maxRunden" :key="k" :class="{ voll: k <= runde }" />
          </span>
          <em v-else>{{ b.info }}</em>
        </span>
      </div>
    </div>

    <!-- Zwischen Harness und Werkzeugen -->
    <div class="ad-spalte">
      <div class="ad-pfeil rechts oben" :class="{ aktiv: aktiv('zumWerkzeug') }">
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('zumWerkzeug')" class="ad-nachricht">{{ text('zumWerkzeug') }}</span>
        </Transition>
        <div class="ad-linie"><span class="ad-punkt" /></div>
      </div>
      <div class="ad-pfeil links unten" :class="{ aktiv: aktiv('vomWerkzeug') }">
        <div class="ad-linie"><span class="ad-punkt" /></div>
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="text('vomWerkzeug')" class="ad-nachricht">{{ text('vomWerkzeug') }}</span>
        </Transition>
      </div>
    </div>

    <!-- Rechts: Werkzeuge und das Referat -->
    <div class="ad-welt">
      <div class="ad-gruppe-titel">Werkzeuge</div>
      <div
        v-for="w in werkzeuge"
        :key="w.id"
        class="ad-werkzeug"
        :class="{ an: s.werkzeug === w.id }"
      >
        <ThmIcon :name="w.icon" :size="0.9" /> {{ w.text }}
      </div>
      <div class="ad-dok" :class="{ liest, geschrieben }">
        <div class="ad-leiste"><span /><span /><span /><b>Referat.docx</b></div>
        <div class="ad-zeilen">
          <div class="ad-zeile titel" />
          <div class="ad-zeile" />
          <div class="ad-zeile kurz" />
          <div class="ad-zeile absatz3" />
          <div class="ad-zeile absatz3 kurz" />
          <div class="ad-zeile" />
        </div>
      </div>
    </div>

    <!-- Unten: was gerade passiert -->
    <div class="ad-text" :class="{ fertig }">
      <template v-if="fertig">
        <ThmIcon name="check" ton="weiss" :size="1.35" />
        <span><strong>Jetzt ist das Harness die Brücke.</strong> Ihr gebt den Auftrag und bekommt das Ergebnis — kein Copy &amp; Paste dazwischen.</span>
      </template>
      <template v-else>
        <span class="ad-nr">{{ n ? `${n} / ${schritte.length - 1}` : 'Start' }}</span>
        <Transition name="ad-wechsel" mode="out-in">
          <span :key="n">{{ s.text }}</span>
        </Transition>
      </template>
    </div>
  </div>
</template>

<style scoped>
.ad {
  --punkt: 0.55rem;
  display: grid;
  grid-template-columns: 8rem 8.6rem minmax(0, 1fr) 8.6rem 9.6rem;
  grid-template-rows: auto auto auto;
  column-gap: 0.6rem;
  align-items: center;
  font-size: 0.85rem;
}

/* ---- Pfeile ---- */

.ad-linie {
  position: relative;
  background: var(--thm-grey-300);
  transition: background 0.3s ease;
}

.aktiv > .ad-linie { background: var(--thm-green-500); }

/* Pfeilspitze */
.ad-linie::after {
  content: '';
  position: absolute;
  border: 0.38rem solid transparent;
  transition: border-color 0.3s ease;
}

/* Laufender Punkt: die Nachricht unterwegs */
.ad-punkt {
  position: absolute;
  width: var(--punkt);
  height: var(--punkt);
  border-radius: 50%;
  background: var(--thm-green-700);
  opacity: 0;
}

.aktiv .ad-punkt { opacity: 1; }

.ad-pfeil {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.ad-pfeil .ad-linie { height: 2px; margin: 0 0.4rem; }
.ad-pfeil .ad-punkt { top: 50%; margin-top: calc(var(--punkt) / -2); }

.ad-pfeil.rechts .ad-linie::after { right: -0.4rem; top: -0.38rem; border-right: 0; border-left-width: 0.55rem; border-left-color: var(--thm-grey-300); }
.ad-pfeil.links .ad-linie::after { left: -0.4rem; top: -0.38rem; border-left: 0; border-right-width: 0.55rem; border-right-color: var(--thm-grey-300); }
.ad-pfeil.rechts.aktiv .ad-linie::after { border-left-color: var(--thm-green-500); }
.ad-pfeil.links.aktiv .ad-linie::after { border-right-color: var(--thm-green-500); }

.ad-pfeil.rechts.aktiv .ad-punkt { animation: ad-rechts 1.4s ease-in-out infinite; }
.ad-pfeil.links.aktiv .ad-punkt { animation: ad-links 1.4s ease-in-out infinite; }

@keyframes ad-rechts {
  from { left: 0; }
  to { left: calc(100% - var(--punkt)); }
}

@keyframes ad-links {
  from { left: calc(100% - var(--punkt)); }
  to { left: 0; }
}

/* Platz für bis zu drei Zeilen, damit beim Wechsel nichts springt */
.ad-pfeil .ad-nachricht {
  min-height: 3.3em;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  text-align: center;
}

.ad-pfeil.unten .ad-nachricht { align-items: flex-start; }

.ad-spalte {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ad-nachricht {
  font-size: 0.82em;
  font-weight: var(--fw-semibold);
  line-height: 1.25;
  color: var(--thm-grey-400);
  transition: color 0.3s ease;
}

.aktiv > .ad-nachricht,
.aktiv > .ad-wechsel-enter-active {
  color: var(--text-strong);
}

/* ---- Oben: ihr ---- */

.ad-oben {
  grid-column: 3;
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 2.4rem;
}

.ad-ihr {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.4rem;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.ad-vpfeil {
  position: relative;
  display: flex;
  justify-content: center;
  width: 1rem;
  height: 3rem;
}

.ad-vpfeil .ad-linie { width: 2px; height: calc(100% - 0.45rem); }
.ad-vpfeil.runter .ad-linie { margin-bottom: auto; }
.ad-vpfeil.hoch .ad-linie { margin-top: auto; }
.ad-vpfeil .ad-punkt { left: 50%; margin-left: calc(var(--punkt) / -2); }

.ad-vpfeil.runter .ad-linie::after { bottom: -0.45rem; left: -0.38rem; border-bottom: 0; border-top-width: 0.55rem; border-top-color: var(--thm-grey-300); }
.ad-vpfeil.hoch .ad-linie::after { top: -0.45rem; left: -0.38rem; border-top: 0; border-bottom-width: 0.55rem; border-bottom-color: var(--thm-grey-300); }
.ad-vpfeil.runter.aktiv .ad-linie::after { border-top-color: var(--thm-green-500); }
.ad-vpfeil.hoch.aktiv .ad-linie::after { border-bottom-color: var(--thm-green-500); }

.ad-vpfeil.runter.aktiv .ad-punkt { animation: ad-runter 1.4s ease-in-out infinite; }
.ad-vpfeil.hoch.aktiv .ad-punkt { animation: ad-hoch 1.4s ease-in-out infinite; }

@keyframes ad-runter {
  from { top: 0; }
  to { top: calc(100% - var(--punkt)); }
}

@keyframes ad-hoch {
  from { top: calc(100% - var(--punkt)); }
  to { top: 0; }
}

/* Die Nachricht steht neben dem Pfeil, nach außen weg vom Ihr-Block */
.ad-vpfeil .ad-nachricht {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: max-content;
  max-width: 13rem;
}

.ad-nachricht.links { right: 1.4rem; text-align: right; }
.ad-nachricht.rechts { left: 1.4rem; text-align: left; }

/* ---- Modell ---- */

.ad-modell {
  grid-column: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.9rem 0.5rem 0.7rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
  text-align: center;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.ad-modell.aktiv {
  border-color: var(--thm-green-500);
  box-shadow: 0 0 0 2px var(--thm-green-200), 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
}

.ad-modell-titel {
  font-size: 1.1em;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.ad-modell-text {
  font-size: 0.82em;
  line-height: 1.3;
  color: var(--thm-grey-500);
}

.ad-denkt {
  display: flex;
  align-items: center;
  gap: 0.18rem;
  margin-top: 0.2rem;
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--thm-green-700);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ad-denkt.an { opacity: 1; }

.ad-denkt i {
  width: 0.25rem;
  height: 0.25rem;
  border-radius: 50%;
  background: currentColor;
  animation: ad-puls 1.2s ease-in-out infinite;
}

.ad-denkt i:nth-child(2) { animation-delay: 0.2s; }
.ad-denkt i:nth-child(3) { animation-delay: 0.4s; }

@keyframes ad-puls {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 1; }
}

/* ---- Harness ---- */

.ad-harness {
  grid-column: 3;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem 0.9rem 0.8rem;
  background: var(--thm-green-50);
  border: 2px solid var(--thm-green-500);
}

.ad-harness-titel {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.12rem 0.6rem;
  background: var(--thm-green-500);
  color: var(--white);
  font-size: 0.78em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.ad-baustein {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.25rem 0.4rem;
  border: 1px solid transparent;
  transition: background 0.3s ease, border-color 0.3s ease;
}

.ad-baustein.an {
  background: var(--white);
  border-color: var(--thm-green-300);
}

.ad-baustein-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
  color: var(--text-strong);
}

.ad-baustein-text strong { font-weight: var(--fw-bold); }

.ad-baustein-text em {
  font-style: normal;
  font-size: 0.85em;
  color: var(--thm-grey-500);
}

.ad-baustein.an .ad-baustein-text em { color: var(--thm-green-800); }

.ad-verlauf,
.ad-runden {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  min-height: 1.02em;
  font-size: 0.85em;
  color: var(--thm-grey-500);
}

.ad-runden { gap: 0.25rem; }
.ad-baustein.an .ad-runden { color: var(--thm-green-800); }

.ad-verlauf i {
  width: 0.7rem;
  height: 0.5rem;
  background: var(--thm-grey-200);
  transition: background 0.3s ease;
}

.ad-runden i {
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 50%;
  background: var(--thm-grey-200);
}

.ad-runden i:first-of-type { margin-left: 0.2rem; }

.ad-verlauf i.voll,
.ad-runden i.voll { background: var(--thm-green-500); }

/* ---- Werkzeuge und Referat ---- */

.ad-welt {
  grid-column: 5;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.ad-gruppe-titel {
  font-size: 0.75em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.ad-werkzeug {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.25rem 0.55rem;
  background: var(--white);
  border: 1px dashed var(--thm-grey-300);
  font-size: 0.85em;
  font-weight: var(--fw-semibold);
  color: var(--text-strong);
  transition: background 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.ad-werkzeug.an {
  background: var(--thm-green-500);
  border: 1px solid var(--thm-green-500);
  color: var(--white);
}

.ad-werkzeug.an :deep(.thm-icon) { color: var(--white); }

.ad-dok {
  margin-top: 0.35rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
}

.ad-leiste {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.3rem 0.5rem;
  background: var(--thm-grey-50);
  border-bottom: 1px solid var(--thm-grey-200);
  font-size: 0.72em;
}

.ad-leiste span {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background: var(--thm-grey-200);
}

.ad-leiste b {
  margin-left: 0.35rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-600);
}

.ad-zeilen {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.55rem 0.65rem;
}

.ad-zeile {
  height: 0.32rem;
  background: var(--thm-grey-200);
  transition: background 0.4s ease;
}

.ad-zeile.kurz { width: 65%; }
.ad-zeile.titel { width: 45%; height: 0.5rem; background: var(--thm-grey-400); }

/* Beim Lesen läuft eine Markierung über die Zeilen */
.ad-dok.liest .ad-zeile:not(.titel) { animation: ad-lesen 1.6s ease-in-out infinite; }
.ad-dok.liest .ad-zeile:nth-child(3) { animation-delay: 0.15s; }
.ad-dok.liest .ad-zeile:nth-child(4) { animation-delay: 0.3s; }
.ad-dok.liest .ad-zeile:nth-child(5) { animation-delay: 0.45s; }
.ad-dok.liest .ad-zeile:nth-child(6) { animation-delay: 0.6s; }

@keyframes ad-lesen {
  0%, 100% { background: var(--thm-grey-200); }
  50% { background: var(--thm-green-200); }
}

/* Nach dem Schreiben: Absatz 3 ist neu */
.ad-dok.geschrieben .ad-zeile.absatz3 { background: var(--thm-green-400); }

/* ---- Erklärzeile, am Ende Merksatz ---- */

.ad-text {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  min-height: 3.1rem;
  margin-top: 1.1rem;
  padding: 0.55rem 1.1rem;
  background: var(--thm-grey-50);
  border-left: 0.25rem solid var(--thm-green-500);
  font-size: 1.05em;
  line-height: var(--lh-snug);
  color: var(--text-strong);
  transition: background 0.3s ease, color 0.3s ease;
}

.ad-text.fertig {
  background: var(--thm-green-500);
  color: var(--white);
}

.ad-text.fertig strong { color: inherit; }

.ad-nr {
  flex: none;
  min-width: 3.2rem;
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

/* ---- Wechsel einer Nachricht ---- */

.ad-wechsel-enter-active,
.ad-wechsel-leave-active { transition: opacity 0.2s ease; }

.ad-wechsel-enter-from,
.ad-wechsel-leave-to { opacity: 0; }
</style>
