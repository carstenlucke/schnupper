<!--
  Wie reden die Counting Agents miteinander? Gar nicht direkt: Der Zähler
  hängt Zahlen an eine Datei an, die drei Sammler lesen sie dort. Die
  Steuerung schreibt Befehle in eine zweite Datei, in die alle schauen.
  Entspricht _bus/numbers.log und _bus/control.log in the-counting-agents/.
-->
<script setup lang="ts">
import { icons } from '../theme-thm/icons'

const B = 176
const H = 56

const knoten = [
  { id: 'counter', titel: 'Zähler', icon: 'list-ordered', x: 40, y: 100, start: true },
  { id: 'zahlen', titel: 'Zahlen-Datei', icon: 'file-text', x: 312, y: 100, datei: true },
  { id: 'odd', titel: 'Ungerade', icon: 'filter', x: 584, y: 20 },
  { id: 'even', titel: 'Gerade', icon: 'filter', x: 584, y: 100 },
  { id: 'prime', titel: 'Primzahlen', icon: 'brain', x: 584, y: 180 },
  { id: 'control', titel: 'Steuerung', icon: 'sliders-horizontal', x: 40, y: 270, start: true },
  { id: 'befehle', titel: 'Befehls-Datei', icon: 'file-text', x: 312, y: 270, datei: true },
]
</script>

<template>
  <svg class="bus" viewBox="0 0 800 346" role="img"
       aria-label="Der Zähler schreibt Zahlen in eine Datei, aus der die Agenten für ungerade, gerade und Primzahlen lesen. Die Steuerung schreibt Befehle in eine zweite Datei, in die alle Agenten schauen.">
    <defs>
      <marker id="bus-pfeil" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" class="spitze" />
      </marker>
    </defs>

    <!-- Kanten -->
    <g class="kanten" marker-end="url(#bus-pfeil)">
      <line :x1="40 + B" y1="128" x2="306" y2="128" />
      <line :x1="312 + B" y1="128" x2="578" y2="48" />
      <line :x1="312 + B" y1="128" x2="578" y2="128" />
      <line :x1="312 + B" y1="128" x2="578" y2="208" />
      <line :x1="40 + B" y1="298" x2="306" y2="298" />
    </g>

    <!-- Knoten -->
    <g v-for="k in knoten" :key="k.id" :class="['knoten', { start: k.start, datei: k.datei }]">
      <rect :x="k.x" :y="k.y" :width="B" :height="H" />
      <rect :x="k.x + 12" :y="k.y + 12" width="32" height="32" rx="4" class="icon-box" />
      <component :is="icons[k.icon]" :x="k.x + 19" :y="k.y + 19" width="18" height="18" class="icon" />
      <text :x="k.x + 56" :y="k.y + H / 2 + 6">{{ k.titel }}</text>
    </g>

    <text x="261" y="118" class="hinweis" text-anchor="middle">schreibt</text>
    <text x="261" y="288" class="hinweis" text-anchor="middle">schreibt</text>
    <text x="533" y="152" class="hinweis" text-anchor="middle">lesen</text>
    <text :x="312 + B + 18" y="296" class="hinweis">alle schauen hier nach Befehlen:</text>
    <text :x="312 + B + 18" y="316" class="hinweis leise">Pause, weiter, Neustart …</text>
  </svg>
</template>

<style scoped>
.bus {
  width: 100%;
  height: 100%;
  font-family: var(--font-sans);
  overflow: visible;
}

.kanten line {
  fill: none;
  stroke: var(--thm-grey-400);
  stroke-width: 2.2;
}

.spitze { fill: var(--thm-grey-400); }

.knoten rect { fill: var(--card-bg); }
.knoten.start rect { fill: var(--thm-green-50); stroke: var(--thm-green-500); stroke-width: 2; }
.knoten.datei rect { fill: var(--thm-grey-600); }
.knoten rect.icon-box { fill: var(--thm-green-500); stroke: none; }

.knoten text {
  font-size: 17px;
  font-weight: var(--fw-bold);
  fill: var(--text-strong);
}

.knoten.datei text { fill: var(--white); }

.icon { color: var(--white); }

.hinweis {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  fill: var(--thm-green-700);
}

.hinweis.leise {
  font-weight: var(--fw-regular);
  fill: var(--text-muted);
}
</style>
