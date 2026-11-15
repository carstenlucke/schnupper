<!--
  KI-Agent = Modell + Harness, als Bild: in der Mitte das Modell (das
  Gehirn: denkt, plant, entscheidet), darum der Rahmen des Harness. Das
  Harness hat zwei Seiten:

  - Werkzeuge (links): die Hände und Augen — womit der Agent in die Welt
    greift.
  - Steuerung (rechts): was das Harness selbst leistet — die Schleife, die
    das Modell immer wieder aufruft, die Anweisungen, der Verlauf und
    die Leitplanken.

  Die vier Werkzeuge sind nur Beispiele; ein Chip „und viele mehr“
  darunter sagt das auch.

  Mit `schrittweise` baut sich das Bild Klick für Klick auf: zuerst
  Gleichung und Modell, der Rahmen des Harness steht nur gestrichelt als
  Platzhalter da. Mit Klick 1 bekommt er grüne Fläche, durchgezogenen
  Rand und Etikett, danach kommen die Werkzeuge und die vier Bausteine
  der Steuerung einzeln. Unten erklärt eine
  <SchrittZeile>, was gerade dazukommt; nach dem letzten Baustein wird sie
  zum Merksatz. Die Folie braucht dann `clicks: 7` und keinen eigenen
  Callout. Ohne `schrittweise` steht alles sofort da.

  Der Baustein heißt bewusst „Verlauf“ und nicht „Gedächtnis“: Gemeint
  ist nur, was das Harness in jeder Runde ins Kontextfenster schickt,
  kein Langzeitgedächtnis über den Auftrag hinaus.

  Idee aus dem TecDay-Vortrag (Folie „Agent = Model + Harness“). Die
  Auswahl folgt den üblichen Bausteinen eines Agent Harness (Schleife,
  Werkzeuge, Anweisungen, Kontext, Leitplanken); das Prüfen
  zeigt die Folie mit dem Agent-Kreislauf davor.
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { werkzeuge, steuerung as baustein } from './harness'

const props = defineProps<{ schrittweise?: boolean }>()

/* `schritt`: mit welchem Klick der Baustein erscheint (nur schrittweise) */
const steuerung = [
  { ...baustein.schleife, info: 'fragt das Modell immer wieder', schritt: 3 },
  { ...baustein.anweisungen, info: 'Rolle und Aufgabe', schritt: 4 },
  { ...baustein.verlauf, info: 'Auftrag, Antworten, Ergebnisse', schritt: 5 },
  { ...baustein.leitplanken, info: 'was erlaubt ist', schritt: 6 },
]

/* Was unten in der Erklärzeile steht; Index = Klick */
const erklaerung = [
  'Ein KI-Agent hat zwei Teile. In der Mitte das Modell: das Gehirn, es denkt, plant und entscheidet.',
  'Um das Modell herum liegt das Harness: alles, was aus dem Modell einen Agenten macht.',
  'Werkzeuge sind Hände und Augen, damit greift der Agent in die Welt. Diese vier sind nur Beispiele.',
  'Die Schleife fragt das Modell immer wieder, Runde für Runde, bis die Aufgabe erledigt ist.',
  'Die Anweisungen legen Rolle und Aufgabe fest. Sie gehen in jeder Runde mit.',
  'Der Verlauf sammelt Auftrag, Antworten und Ergebnisse. Das Modell selbst merkt sich nichts.',
  'Die Leitplanken legen fest, was der Agent ohne Nachfrage darf und was nicht.',
]
const schritte = erklaerung.length

const { $clicks } = useSlideContext()
const n = computed(() =>
  props.schrittweise ? Math.min(Math.max($clicks.value, 0), schritte) : schritte,
)
const fertig = computed(() => n.value === schritte)

/* Ohne `schrittweise` ist alles da und nichts hervorgehoben */
const da = (schritt: number) => n.value >= schritt
const jetzt = (schritt: number) => !!props.schrittweise && n.value === schritt
</script>

<template>
  <div class="an">
    <div class="an-gleichung">
      <span class="an-teil dunkel"><ThmIcon name="bot" ton="weiss" :size="1.3" /> KI-Agent</span>
      <span class="an-op">=</span>
      <span class="an-teil"><ThmIcon name="brain" :size="1.3" /> Modell</span>
      <span class="an-op">+</span>
      <span class="an-teil gruen"><ThmIcon name="wrench" ton="weiss" :size="1.3" /> Harness</span>
    </div>

    <div class="an-harness" :class="{ da: da(1) }">
      <div class="an-etikett an-teilbild" :class="{ da: da(1) }">Harness · alles um das Modell herum</div>

      <div class="an-gruppe an-teilbild" :class="{ da: da(2) }">
        <div class="an-gruppe-titel">Werkzeuge · Hände und Augen</div>
        <div v-for="f in werkzeuge" :key="f.text" class="an-werkzeug">
          <ThmIcon :name="f.icon" :size="1.05" /> {{ f.text }}
        </div>
        <div class="an-werkzeug mehr">
          <ThmIcon name="plug" ton="grau" :size="0.9" />
          <span><strong>und viele mehr:</strong> E-Mail, Kalender …</span>
        </div>
      </div>

      <div class="an-modell">
        <ThmIcon name="brain" box :size="3.2" />
        <div class="an-modell-titel">Modell</div>
        <div class="an-modell-text">das Gehirn: denkt, plant, entscheidet</div>
      </div>

      <div class="an-gruppe">
        <div class="an-gruppe-titel an-teilbild" :class="{ da: da(3) }">Steuerung · der Rahmen</div>
        <div
          v-for="f in steuerung"
          :key="f.name"
          class="an-steuerung an-teilbild"
          :class="{ da: da(f.schritt), jetzt: jetzt(f.schritt) }"
        >
          <ThmIcon :name="f.icon" box :size="1.6" />
          <span><strong>{{ f.name }}</strong> <em>{{ f.info }}</em></span>
        </div>
      </div>
    </div>

    <SchrittZeile
      v-if="schrittweise"
      class="an-zeile"
      :schritt="n"
      :schritte="schritte - 1"
      :text="erklaerung[n] ?? ''"
      :fertig="fertig"
      icon="wrench"
    >
      <strong>Das Harness macht den Unterschied.</strong> Ein mittelmäßiges Modell mit gutem Harness schlägt oft ein besseres Modell mit schlechtem Harness.
    </SchrittZeile>
  </div>
</template>

<style scoped>
.an {
  display: flex;
  flex-direction: column;
  /* Platz für das Etikett, das auf der Rahmenkante sitzt */
  gap: 2.3rem;
}

.an-gleichung {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  font-size: 1.15em;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.an-teil {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.9rem;
  background: var(--thm-grey-50);
}

.an-teil.dunkel { background: var(--thm-grey-600); color: var(--white); }
.an-teil.gruen { background: var(--thm-green-500); color: var(--white); }

.an-op { color: var(--thm-green-600); font-size: 1.2em; }

/* minmax(0, 1fr) statt 1fr: Sonst bestimmt der breiteste Inhalt die
   Mindestbreite seiner Spalte, und das Modell rutscht aus der Mitte. */
.an-harness {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  gap: 2rem;
  padding: 1.5rem 2rem 1.1rem;
  background: transparent;
  border: 2px dashed var(--thm-grey-200);
  transition: background 0.4s ease, border-color 0.4s ease;
}

.an-harness.da {
  background: var(--thm-green-50);
  border: 2px solid var(--thm-green-500);
}

/* Schrittweise: Teile, die noch nicht dran sind, sind unsichtbar, nehmen
   aber schon ihren Platz ein — so springt beim Aufbau nichts. */
.an-teilbild {
  opacity: 0;
  translate: 0 0.3rem;
  transition: opacity 0.35s ease, translate 0.35s ease, background 0.3s ease, box-shadow 0.3s ease;
}

.an-teilbild.da { opacity: 1; translate: 0 0; }

/* Etikett: sitzt per transform auf der Rahmenkante, translate kommt dazu */
.an-etikett.an-teilbild { translate: 0 -0.3rem; }
.an-etikett.an-teilbild.da { translate: 0 0; }

/* Weniger Luft zwischen Bild und Erklärzeile; Platz für den zweizeiligen
   Merksatz von Anfang an, sonst springt beim letzten Klick das ganze Bild
   nach oben. */
.an .an-zeile { margin-top: -1rem; min-height: 4.3rem; }

.an-etikett {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 0.15rem 0.8rem;
  background: var(--thm-green-500);
  color: var(--white);
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  white-space: nowrap;
}

.an-gruppe {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.an-gruppe-titel {
  margin-bottom: 0.15rem;
  font-size: 0.68em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

/* Werkzeuge: schlichte Chips, wie Dinge in einem Werkzeugkasten */
.an-werkzeug {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0.32rem 0.8rem;
  background: var(--white);
  border: 1px dashed var(--thm-grey-300);
  font-size: 0.88em;
  font-weight: var(--fw-semibold);
  color: var(--text-strong);
}

/* Am Ende der Werkzeuge: Die vier oben sind nur eine Auswahl */
.an-werkzeug.mehr {
  gap: 0.5rem;
  padding: 0.2rem 0.8rem;
  background: transparent;
  border-color: var(--thm-grey-200);
  font-size: 0.72em;
  font-weight: var(--fw-regular);
  line-height: 1.2;
  color: var(--thm-grey-500);
}

.an-werkzeug.mehr strong {
  margin-right: 0.25rem;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

/* Steuerung: Bausteine des Harness selbst, mit grünem Icon-Quadrat.
   Polster mit negativem Rand, damit die Hervorhebung nichts verschiebt. */
.an-steuerung {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: -0.25rem -0.5rem;
  padding: 0.25rem 0.5rem;
  font-size: 0.88em;
  line-height: 1.2;
  color: var(--text-strong);
}

.an-steuerung.jetzt {
  background: var(--white);
  box-shadow: 0 0.2rem 0.8rem rgba(34, 44, 49, 0.08);
}

.an-steuerung strong { font-weight: var(--fw-bold); }

.an-steuerung em {
  display: block;
  font-style: normal;
  font-size: 0.82em;
  color: var(--thm-grey-500);
}

.an-modell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  width: 12rem;
  padding: 1.1rem 1rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
  text-align: center;
}

.an-modell-titel {
  font-size: 1.1em;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.an-modell-text {
  font-size: 0.8em;
  line-height: 1.3;
  color: var(--thm-grey-500);
}
</style>
