<!--
  Ein Agent bei der Arbeit, Klick für Klick: ein Auftrag läuft einmal
  durch den Agenten. Gegenstück zu <CopyPasteSchleife> — dasselbe
  Referat, aber jetzt trägt nicht ihr die Texte hin und her, sondern das
  Harness.

  Links das Modell, in der Mitte das Harness mit den vier Bausteinen der
  Steuerung aus <AgentAnatomie>, rechts die Werkzeuge und das Referat,
  oben ihr. Jeder Klick schickt eine Nachricht über einen <LaufPfeil>; der
  aktive Pfeil wird grün, ein Punkt läuft darüber, die Nachricht steht
  daneben. Im Harness leuchtet auf, was gerade gebraucht wird: die
  Schleife zählt die Runden, der Verlauf sammelt Einträge, die
  Leitplanken prüfen jeden Werkzeugwunsch. Unten erklärt eine Zeile den
  Schritt; nach dem letzten wird sie zum Merksatz.

  Geblättert wird mit den Klicks der Folie: Die Folie braucht
  `clicks: 10` (Schritte 1 bis 10, Klick 0 ist das Ausgangsbild).
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { werkzeuge, steuerung as baustein } from './harness'

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
    pfeile: { auftrag: '„Kürze Absatz 3 in meinem Referat auf unter 1000 Zeichen.“' },
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
    text: 'Jetzt kennt das Modell das Referat und schreibt Absatz 3 kürzer.',
    pfeile: { vomModell: 'Bitte „Datei schreiben“: kürzerer Absatz 3' },
  },
  {
    text: 'Wieder prüft das Harness — und speichert den gekürzten Absatz im Referat.',
    pfeile: { zumWerkzeug: 'Datei schreiben' },
    werkzeug: 'schreiben',
  },
  {
    text: 'Dritte Runde: Das Modell erfährt, dass gespeichert ist — und wie lang der Absatz jetzt ist.',
    pfeile: { vomWerkzeug: 'gespeichert ✓ 870 Zeichen', zumModell: 'Anweisungen + Werkzeuge + Verlauf' },
    anweisungen: true,
  },
  {
    text: 'Das Modell prüft: unter 1000 Zeichen, Ziel erreicht. Kein Werkzeug mehr nötig — es meldet: fertig.',
    pfeile: { vomModell: '„Fertig: Absatz 3 hat jetzt 870 Zeichen.“' },
  },
  {
    text: '',
    pfeile: { ergebnis: '„Gekürzt: 870 statt 1400\u00a0Zeichen.“' },
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

/* Was im Verlauf landet: euer Auftrag, jede Antwort des Modells,
   jedes Ergebnis eines Werkzeugs */
const merkt: Pfeil[] = ['auftrag', 'vomModell', 'vomWerkzeug']

const { $clicks } = useSlideContext()
const n = computed(() => Math.min(Math.max($clicks.value, 0), schritte.length - 1))
const s = computed(() => schritte[n.value])

const aktiv = (p: Pfeil) => s.value.pfeile?.[p] !== undefined
const text = (p: Pfeil) => s.value.pfeile?.[p] ?? ruhe[p]

/* Runden zählen die Anfragen ans Modell, Einträge alles, was im Verlauf landet */
const zaehleRunden = (liste: Schritt[]) => liste.filter(x => x.pfeile?.zumModell).length
const zaehleEintraege = (liste: Schritt[]) =>
  liste.reduce((summe, x) => summe + merkt.filter(p => x.pfeile?.[p]).length, 0)

const bisher = computed(() => schritte.slice(0, n.value + 1))
const runde = computed(() => zaehleRunden(bisher.value))
const eintraege = computed(() => zaehleEintraege(bisher.value))
const maxRunden = zaehleRunden(schritte)
const maxEintraege = zaehleEintraege(schritte)

/* Wie ein Baustein seinen Stand zeigt: als Text, als Rundenzähler oder
   als Leiste der Einträge im Verlauf */
interface Baustein {
  icon: string
  name: string
  an: boolean
  art: 'text' | 'runden' | 'verlauf'
  info?: string
}

const steuerung = computed((): Baustein[] => [
  {
    ...baustein.schleife,
    an: aktiv('zumModell'),
    art: runde.value ? 'runden' : 'text',
    info: runde.value
      ? `Runde ${runde.value}`
      : aktiv('auftrag') ? 'Auftrag ist da' : 'wartet auf einen Auftrag',
  },
  {
    ...baustein.anweisungen,
    an: !!s.value.anweisungen,
    art: 'text',
    info: s.value.anweisungen ? 'gehen mit ans Modell' : 'Rolle und Aufgabe',
  },
  {
    ...baustein.verlauf,
    an: merkt.some(aktiv),
    art: 'verlauf',
  },
  {
    ...baustein.leitplanken,
    an: !!s.value.werkzeug,
    art: 'text',
    info: s.value.werkzeug ? `„Datei ${s.value.werkzeug}“ ist erlaubt ✓` : 'was erlaubt ist',
  },
])

const modellAktiv = computed(() => aktiv('zumModell') || aktiv('vomModell'))
const liest = computed(() => s.value.werkzeug === 'lesen')
const geschrieben = computed(() => bisher.value.some(x => x.werkzeug === 'schreiben'))
const fertig = computed(() => n.value === schritte.length - 1)
</script>

<template>
  <div class="ad">
    <!-- Oben: ihr, mit Auftrag hinein und Ergebnis heraus -->
    <div class="ad-oben">
      <LaufPfeil richtung="runter" seite="links" :aktiv="aktiv('auftrag')" :text="text('auftrag')" />
      <div class="ad-ihr">
        <ThmIcon name="user" box :size="2" />
        <span>Ihr</span>
      </div>
      <LaufPfeil richtung="hoch" seite="rechts" :aktiv="aktiv('ergebnis')" :text="text('ergebnis')" />
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
      <LaufPfeil richtung="links" :zeilen="3" :aktiv="aktiv('zumModell')" :text="text('zumModell')" />
      <LaufPfeil richtung="rechts" seite="unten" :zeilen="3" :aktiv="aktiv('vomModell')" :text="text('vomModell')" />
    </div>

    <!-- Mitte: das Harness mit seiner Steuerung -->
    <div class="ad-harness">
      <div class="ad-harness-titel"><ThmIcon name="wrench" ton="weiss" :size="0.95" /> Harness</div>
      <div v-for="b in steuerung" :key="b.name" class="ad-baustein" :class="{ an: b.an }">
        <ThmIcon :name="b.icon" box :ton="b.an ? 'gruen' : 'grau'" :size="1.5" />
        <span class="ad-baustein-text">
          <strong>{{ b.name }}</strong>
          <span v-if="b.art === 'verlauf'" class="ad-verlauf">
            <i v-for="k in maxEintraege" :key="k" :class="{ voll: k <= eintraege }" />
          </span>
          <span v-else-if="b.art === 'runden'" class="ad-runden">
            {{ b.info }}
            <i v-for="k in maxRunden" :key="k" :class="{ voll: k <= runde }" />
          </span>
          <em v-else>{{ b.info }}</em>
        </span>
      </div>
    </div>

    <!-- Zwischen Harness und Werkzeugen -->
    <div class="ad-spalte">
      <LaufPfeil richtung="rechts" :zeilen="3" :aktiv="aktiv('zumWerkzeug')" :text="text('zumWerkzeug')" />
      <LaufPfeil richtung="links" seite="unten" :zeilen="3" :aktiv="aktiv('vomWerkzeug')" :text="text('vomWerkzeug')" />
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
      <Fenster titel="Referat.docx" kompakt class="ad-dok" :class="{ liest, geschrieben }">
        <div class="thm-dok kompakt">
          <div class="thm-zeile titel" />
          <div class="thm-zeile" />
          <div class="thm-zeile kurz" />
          <div class="thm-zeile absatz3" />
          <div class="thm-zeile absatz3 kurz" />
          <div class="thm-zeile" />
        </div>
      </Fenster>
    </div>

    <!-- Unten: was gerade passiert -->
    <SchrittZeile class="ad-text" :schritt="n" :schritte="schritte.length - 1" :text="s.text" :fertig="fertig">
      <strong>Jetzt ist das Harness die Brücke.</strong> Ihr gebt den Auftrag und bekommt das Ergebnis — kein Copy &amp; Paste dazwischen.
    </SchrittZeile>
  </div>
</template>

<style scoped>
.ad {
  display: grid;
  grid-template-columns: 8rem 8.6rem minmax(0, 1fr) 8.6rem 9.6rem;
  grid-template-rows: auto auto auto;
  column-gap: 0.6rem;
  align-items: center;
  font-size: 0.85rem;
}

/* ---- Pfeile ---- */

.ad-spalte {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.ad-dok { margin-top: 0.35rem; }

/* Beim Lesen läuft eine Markierung über die Zeilen */
.ad-dok.liest .thm-zeile:not(.titel) { animation: ad-lesen 1.6s ease-in-out infinite; }
.ad-dok.liest .thm-zeile:nth-child(3) { animation-delay: 0.15s; }
.ad-dok.liest .thm-zeile:nth-child(4) { animation-delay: 0.3s; }
.ad-dok.liest .thm-zeile:nth-child(5) { animation-delay: 0.45s; }
.ad-dok.liest .thm-zeile:nth-child(6) { animation-delay: 0.6s; }

@keyframes ad-lesen {
  0%, 100% { background: var(--thm-grey-200); }
  50% { background: var(--thm-green-200); }
}

/* Nach dem Schreiben: Absatz 3 ist neu */
.ad-dok.geschrieben .thm-zeile.absatz3 { background: var(--thm-green-400); }

/* ---- Erklärzeile, am Ende Merksatz ---- */

.ad-text { grid-column: 1 / -1; }
</style>
