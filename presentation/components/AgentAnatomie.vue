<!--
  KI-Agent = Modell + Harness, als Bild: in der Mitte das Modell (das
  Gehirn: denkt, plant, entscheidet), darum der Rahmen des Harness. Das
  Harness hat zwei Seiten:

  - Werkzeuge (links): die Hände und Augen — womit der Agent in die Welt
    greift.
  - Steuerung (rechts): was das Harness selbst leistet — die Schleife, die
    das Modell immer wieder aufruft, die Anweisungen, das Gedächtnis und
    die Leitplanken.

  Idee aus dem TecDay-Vortrag (Folie „Agent = Model + Harness“). Die
  Auswahl folgt den üblichen Bausteinen eines Agent Harness (Schleife,
  Werkzeuge, Anweisungen, Gedächtnis/Kontext, Leitplanken); das Prüfen
  zeigt die folgende Folie mit dem Agent-Kreislauf.
-->
<script setup lang="ts">
const werkzeuge = [
  { icon: 'eye', text: 'Dateien lesen' },
  { icon: 'pen-line', text: 'Dateien schreiben' },
  { icon: 'square-terminal', text: 'Programme starten' },
  { icon: 'globe', text: 'Im Web suchen' },
]
const steuerung = [
  { icon: 'refresh-cw', text: 'Schleife', info: 'fragt das Modell immer wieder' },
  { icon: 'file-text', text: 'Anweisungen', info: 'Rolle und Aufgabe' },
  { icon: 'notebook-pen', text: 'Gedächtnis', info: 'Verlauf und Notizen' },
  { icon: 'shield-check', text: 'Leitplanken', info: 'was erlaubt ist' },
]
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

    <div class="an-harness">
      <div class="an-etikett">Harness · alles um das Modell herum</div>

      <div class="an-gruppe">
        <div class="an-gruppe-titel">Werkzeuge · Hände und Augen</div>
        <div v-for="f in werkzeuge" :key="f.text" class="an-werkzeug">
          <ThmIcon :name="f.icon" :size="1.05" /> {{ f.text }}
        </div>
      </div>

      <div class="an-modell">
        <ThmIcon name="brain" box :size="3.2" />
        <div class="an-modell-titel">Modell</div>
        <div class="an-modell-text">das Gehirn: denkt, plant, entscheidet</div>
      </div>

      <div class="an-gruppe">
        <div class="an-gruppe-titel">Steuerung · der Rahmen</div>
        <div v-for="f in steuerung" :key="f.text" class="an-steuerung">
          <ThmIcon :name="f.icon" box :size="1.6" />
          <span><strong>{{ f.text }}</strong> <em>{{ f.info }}</em></span>
        </div>
      </div>
    </div>
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

.an-harness {
  position: relative;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 2rem;
  padding: 1.5rem 2rem 1.1rem;
  background: var(--thm-green-50);
  border: 2px solid var(--thm-green-500);
}

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
  gap: 0.45rem;
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
  padding: 0.42rem 0.8rem;
  background: var(--white);
  border: 1px dashed var(--thm-grey-300);
  font-size: 0.88em;
  font-weight: var(--fw-semibold);
  color: var(--text-strong);
}

/* Steuerung: Bausteine des Harness selbst, mit grünem Icon-Quadrat */
.an-steuerung {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.88em;
  line-height: 1.2;
  color: var(--text-strong);
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
