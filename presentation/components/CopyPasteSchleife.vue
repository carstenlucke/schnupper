<!--
  Der Alltag mit einem Chatbot als Bild, Klick für Klick: links das
  Chatfenster, rechts euer Dokument, dazwischen ihr. Ihr tragt den Absatz
  hinüber, holt die Antwort zurück — und fangt beim nächsten Absatz von
  vorne an. Der Chatbot sieht dabei nur den Schnipsel, den ihr ihm gebt.

  Idee aus dem TecDay-Vortrag (Folie „Copy/Paste-Frustration“), dort mit
  Code und Editor; hier mit einem Referat, damit es ohne
  Programmiererfahrung trägt. Fenster und Pfeile sind HTML, damit Schrift
  und Farben im CD bleiben.

  Animiert wie das Gegenstück <AgentDurchlauf>: Jeder Klick schickt eine
  Nachricht über einen Pfeil; der aktive Pfeil wird grün, ein Punkt läuft
  darüber, die Nachricht steht daneben. Unten erklärt eine Zeile den
  Schritt; nach dem letzten wird sie zum Merksatz.

  Mit dem zweiten Schritt erscheint links das Modell hinter dem
  Chatfenster: ChatGPT ist nur die App, die eure Eingabe an das Modell
  schickt und dessen Antwort anzeigt. Der Platz dafür ist von Anfang an
  reserviert; vorher ist das Bild um die Hälfte davon nach links
  verschoben, damit es mittig steht, und gleitet dann an seinen Platz.

  Geblättert wird mit den Klicks der Folie: Die Folie braucht
  `clicks: 5` (Schritte 1 bis 5, Klick 0 ist das Ausgangsbild).
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

type Pfeil = 'rein' | 'raus' | 'zumModell' | 'vomModell'

interface Schritt {
  text: string
  pfeile?: Partial<Record<Pfeil, string>>
}

const schritte: Schritt[] = [
  { text: 'Absatz 3 im Referat soll besser werden — so, wie ihr es heute macht.' },
  {
    text: 'Ihr markiert Absatz 3, kopiert ihn und fügt ihn in den Chat ein.',
    pfeile: { rein: 'Absatz 3 reinkopieren' },
  },
  {
    text: 'ChatGPT ist nur die App. Sie schickt eure Eingabe an das Modell dahinter — nur diesen einen Absatz.',
    pfeile: { zumModell: 'nur Absatz 3' },
  },
  {
    text: 'Das Modell schreibt eine bessere Fassung, die App zeigt sie an.',
    pfeile: { vomModell: 'neuer Absatz 3' },
  },
  {
    text: 'Ihr kopiert die Antwort und fügt sie im Referat ein.',
    pfeile: { raus: 'Antwort rauskopieren' },
  },
  {
    text: '',
    pfeile: { rein: 'Absatz 4 reinkopieren' },
  },
]

/* Beschriftung der Pfeile, solange gerade nichts über sie läuft */
const ruhe: Record<Pfeil, string> = {
  rein: 'Absatz reinkopieren',
  raus: 'Antwort rauskopieren',
  zumModell: 'Eingabe',
  vomModell: 'Antwort',
}

const { $clicks } = useSlideContext()
const n = computed(() => Math.min(Math.max($clicks.value, 0), schritte.length - 1))
const s = computed(() => schritte[n.value])

const aktiv = (p: Pfeil) => s.value.pfeile?.[p] !== undefined
const text = (p: Pfeil) => s.value.pfeile?.[p] ?? ruhe[p]

const offen = computed(() => n.value >= 2)
const modellAktiv = computed(() => aktiv('zumModell') || aktiv('vomModell'))
const ihrAktiv = computed(() => aktiv('rein') || aktiv('raus'))
const fertig = computed(() => n.value === schritte.length - 1)

/* Absatz 3 ist kopiert, bis die Antwort zurück im Referat steht; danach
   ist er neu. Im letzten Schritt ist Absatz 4 an der Reihe. */
const absatz3 = computed(() => (n.value >= 4 ? 'neu' : n.value >= 1 ? 'kopiert' : ''))
const absatz4 = computed(() => (fertig.value ? 'kopiert' : ''))
</script>

<template>
  <div class="cp-rahmen">
    <div class="cp" :class="{ offen }">
      <div class="cp-modell" :class="{ aktiv: modellAktiv }">
        <ThmIcon name="brain" box :size="2.4" />
        <div class="cp-modell-titel">Modell</div>
        <div class="cp-modell-text">das LLM, <span class="nw">z.&nbsp;B. GPT-5.6</span></div>
        <div class="cp-denkt" :class="{ an: aktiv('zumModell') }">denkt nach <i /><i /><i /></div>
      </div>

      <div class="cp-mitte cp-auto-spalte">
        <div class="cp-pfeil links" :class="{ aktiv: aktiv('zumModell') }">
          <Transition name="cp-wechsel" mode="out-in">
            <span :key="text('zumModell')" class="cp-nachricht">{{ text('zumModell') }}</span>
          </Transition>
          <div class="cp-linie"><span class="cp-punkt" /></div>
        </div>
        <div class="cp-auto">automatisch</div>
        <div class="cp-pfeil rechts unten" :class="{ aktiv: aktiv('vomModell') }">
          <div class="cp-linie"><span class="cp-punkt" /></div>
          <Transition name="cp-wechsel" mode="out-in">
            <span :key="text('vomModell')" class="cp-nachricht">{{ text('vomModell') }}</span>
          </Transition>
        </div>
      </div>

      <Fenster titel="ChatGPT" class="cp-fenster">
        <template #leiste><i class="cp-app">App</i></template>
        <div class="cp-chat">
          <div class="cp-blase ich" :class="{ da: n >= 1 }">Mach diesen Absatz besser: <em>„Der Klimawandel ist …“</em></div>
          <div class="cp-blase ki" :class="{ da: n >= 3 }">Gern! Hier ist eine verbesserte Fassung:&nbsp;…</div>
          <div class="cp-eingabe" />
        </div>
      </Fenster>

      <div class="cp-mitte">
        <div class="cp-pfeil links" :class="{ aktiv: aktiv('rein') }">
          <Transition name="cp-wechsel" mode="out-in">
            <span :key="text('rein')" class="cp-nachricht">
              <ThmIcon name="clipboard-paste" :size="0.95" /> {{ text('rein') }}
            </span>
          </Transition>
          <div class="cp-linie"><span class="cp-punkt" /></div>
        </div>
        <div class="cp-ich">
          <ThmIcon name="user" box :ton="ihrAktiv ? 'gruen' : 'grau'" :size="3" />
          <span>Ihr</span>
        </div>
        <div class="cp-pfeil rechts unten" :class="{ aktiv: aktiv('raus') }">
          <div class="cp-linie"><span class="cp-punkt" /></div>
          <Transition name="cp-wechsel" mode="out-in">
            <span :key="text('raus')" class="cp-nachricht">
              <ThmIcon name="clipboard-paste" :size="0.95" /> {{ text('raus') }}
            </span>
          </Transition>
        </div>
      </div>

      <Fenster titel="Referat.docx" class="cp-fenster">
        <div class="thm-dok">
          <div class="thm-zeile titel" />
          <div class="thm-zeile" />
          <div class="thm-zeile kurz" />
          <div class="thm-zeile" :class="absatz3" />
          <div class="thm-zeile kurz" :class="absatz3" />
          <div class="thm-zeile" />
          <div class="thm-zeile" :class="absatz4" />
          <div class="thm-zeile kurz" :class="absatz4" />
        </div>
      </Fenster>

      <div class="cp-wieder" :class="{ an: fertig }">
        <ThmIcon name="refresh-cw" :size="1" />
        Nächster Absatz — und alles wieder von vorn
      </div>
    </div>

    <!-- Unten: was gerade passiert -->
    <div class="cp-text" :class="{ fertig }">
      <template v-if="fertig">
        <ThmIcon name="user" ton="weiss" :size="1.35" />
        <span><strong>Ihr seid die Brücke.</strong> Das Modell sieht nur den Schnipsel, den ihr hineinkopiert — nicht eure ganze Arbeit.</span>
      </template>
      <template v-else>
        <span class="cp-nr">{{ n ? `${n} / ${schritte.length - 1}` : 'Start' }}</span>
        <Transition name="cp-wechsel" mode="out-in">
          <span :key="n">{{ s.text }}</span>
        </Transition>
      </template>
    </div>
  </div>
</template>

<style scoped>
.cp-rahmen { --punkt: 0.55rem; }

.cp {
  display: grid;
  grid-template-columns: 7.5rem 5.5rem 1fr 10.5rem 1fr;
  grid-template-rows: auto auto;
  column-gap: 1.2rem;
  /* Halbe Breite der beiden Modell-Spalten samt Abständen */
  transform: translateX(calc(-0.5 * (7.5rem + 5.5rem + 2 * 1.2rem)));
  transition: transform 0.5s ease;
  row-gap: 0.9rem;
  align-items: center;
}

.cp.offen { transform: none; }

/* Modell und der Weg dorthin kommen erst mit dem zweiten Schritt dazu */
.cp-modell,
.cp-auto-spalte,
.cp-app {
  opacity: 0;
  transition: opacity 0.4s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.cp.offen .cp-modell,
.cp.offen .cp-auto-spalte,
.cp.offen .cp-app { opacity: 1; }

.cp-fenster { height: 14rem; }

.cp-app {
  margin-left: auto;
  padding: 0 0.35rem;
  border: 1px solid var(--thm-grey-300);
  font-style: normal;
  font-size: 0.62rem;
  font-weight: var(--fw-bold);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--thm-grey-500);
}

.cp-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.8rem;
  font-size: 0.78rem;
  line-height: 1.35;
}

.cp-blase {
  max-width: 85%;
  padding: 0.45rem 0.65rem;
  color: var(--text-strong);
  opacity: 0;
  transform: translateY(0.4rem);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.cp-blase.da {
  opacity: 1;
  transform: none;
}

.cp-blase.ich {
  align-self: flex-end;
  background: var(--thm-grey-100);
}

.cp-blase.ki {
  align-self: flex-start;
  background: var(--thm-green-50);
  border-left: 0.2rem solid var(--thm-green-500);
}

.cp-eingabe {
  margin-top: auto;
  height: 1.3rem;
  border: 1px solid var(--thm-grey-200);
}

.thm-zeile { transition: background 0.3s ease; }
.thm-zeile.kopiert { background: var(--thm-green-200); }
.thm-zeile.neu { background: var(--thm-green-400); }

.cp-mitte {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.9rem;
}

.cp-ich {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.cp-modell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  padding: 0.9rem 0.6rem 0.7rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
  text-align: center;
}

.cp-modell.aktiv {
  border-color: var(--thm-green-500);
  box-shadow: 0 0 0 2px var(--thm-green-200), 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
}

.cp-modell-titel {
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.cp-modell-text {
  font-size: 0.72rem;
  line-height: 1.3;
  color: var(--thm-grey-500);
}

.cp-modell-text .nw { white-space: nowrap; }

.cp-denkt {
  display: flex;
  align-items: center;
  gap: 0.18rem;
  margin-top: 0.2rem;
  font-size: 0.62rem;
  font-weight: var(--fw-bold);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--thm-green-700);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.cp-denkt.an { opacity: 1; }

.cp-denkt i {
  width: 0.25rem;
  height: 0.25rem;
  border-radius: 50%;
  background: currentColor;
  animation: cp-puls 1.2s ease-in-out infinite;
}

.cp-denkt i:nth-child(2) { animation-delay: 0.2s; }
.cp-denkt i:nth-child(3) { animation-delay: 0.4s; }

@keyframes cp-puls {
  0%, 100% { opacity: 0.25; }
  50% { opacity: 1; }
}

/* Den Weg zwischen App und Modell geht niemand von Hand: graues Etikett */
.cp-auto {
  font-size: 0.7rem;
  font-weight: var(--fw-bold);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--thm-grey-400);
}

/* ---- Pfeile ---- */

.cp-pfeil {
  align-self: stretch;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.cp-linie {
  position: relative;
  height: 2px;
  margin: 0 0.4rem;
  background: var(--thm-grey-300);
  transition: background 0.3s ease;
}

.aktiv > .cp-linie { background: var(--thm-green-500); }

/* Pfeilspitze */
.cp-linie::after {
  content: '';
  position: absolute;
  top: -0.38rem;
  border: 0.38rem solid transparent;
  transition: border-color 0.3s ease;
}

.cp-pfeil.rechts .cp-linie::after { right: -0.4rem; border-right: 0; border-left-width: 0.55rem; border-left-color: var(--thm-grey-300); }
.cp-pfeil.links .cp-linie::after { left: -0.4rem; border-left: 0; border-right-width: 0.55rem; border-right-color: var(--thm-grey-300); }
.cp-pfeil.rechts.aktiv .cp-linie::after { border-left-color: var(--thm-green-500); }
.cp-pfeil.links.aktiv .cp-linie::after { border-right-color: var(--thm-green-500); }

/* Laufender Punkt: die Nachricht unterwegs */
.cp-punkt {
  position: absolute;
  top: 50%;
  width: var(--punkt);
  height: var(--punkt);
  margin-top: calc(var(--punkt) / -2);
  border-radius: 50%;
  background: var(--thm-green-700);
  opacity: 0;
}

.aktiv .cp-punkt { opacity: 1; }

.cp-pfeil.rechts.aktiv .cp-punkt { animation: cp-rechts 1.4s ease-in-out infinite; }
.cp-pfeil.links.aktiv .cp-punkt { animation: cp-links 1.4s ease-in-out infinite; }

@keyframes cp-rechts {
  from { left: 0; }
  to { left: calc(100% - var(--punkt)); }
}

@keyframes cp-links {
  from { left: calc(100% - var(--punkt)); }
  to { left: 0; }
}

/* Platz für zwei Zeilen, damit beim Wechsel nichts springt */
.cp-nachricht {
  min-height: 2.5em;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 0.35rem;
  text-align: center;
  font-size: 0.78rem;
  font-weight: var(--fw-semibold);
  line-height: 1.25;
  color: var(--thm-grey-400);
  transition: color 0.3s ease;
}

.cp-pfeil.unten .cp-nachricht { align-items: flex-start; }

.aktiv > .cp-nachricht,
.aktiv > .cp-wechsel-enter-active {
  color: var(--text-strong);
}

/* ---- Wiederholung ---- */

.cp-wieder {
  grid-column: 3 / -1;
  justify-self: center;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.2rem 0.6rem;
  font-size: 0.85rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-500);
  transition: color 0.3s ease;
}

.cp-wieder.an { color: var(--thm-green-700); }
.cp-wieder.an :deep(.thm-icon) { animation: cp-drehen 2s linear infinite; }

@keyframes cp-drehen {
  to { transform: rotate(360deg); }
}

/* ---- Erklärzeile, am Ende Merksatz ---- */

.cp-text {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  min-height: 3.1rem;
  margin-top: 1.1rem;
  padding: 0.55rem 1.1rem;
  background: var(--thm-grey-50);
  border-left: 0.25rem solid var(--thm-green-500);
  font-size: 0.9rem;
  line-height: var(--lh-snug);
  color: var(--text-strong);
  transition: background 0.3s ease, color 0.3s ease;
}

.cp-text.fertig {
  background: var(--thm-green-500);
  color: var(--white);
}

.cp-text.fertig strong { color: inherit; }

.cp-nr {
  flex: none;
  min-width: 3.2rem;
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

/* ---- Wechsel einer Nachricht ---- */

.cp-wechsel-enter-active,
.cp-wechsel-leave-active { transition: opacity 0.2s ease; }

.cp-wechsel-enter-from,
.cp-wechsel-leave-to { opacity: 0; }
</style>
