<!--
  Wer wartet auf wen? Die fünf Agenten von Ship It! und ihre
  Eingaben, wie sie in ship-it/server.py (AGENT_PATHS) festgelegt sind.
  Die beiden Startpunkte sind grün hinterlegt. Ersetzt die frühere
  Grafik agent-abhaengigkeiten.svg, die nur auf dunklem Grund lesbar war.
-->
<script setup lang="ts">
import { icons } from '../theme-thm/icons'

const B = 176
const H = 56

const agenten = [
  { id: 'zielgruppe', titel: 'Zielgruppe', icon: 'users', x: 40, y: 30, start: true },
  { id: 'marketing', titel: 'Marketing', icon: 'megaphone', x: 312, y: 30 },
  { id: 'social', titel: 'Social Media', icon: 'hash', x: 584, y: 30 },
  { id: 'kalkulation', titel: 'Kalkulation', icon: 'calculator', x: 40, y: 170 },
  { id: 'website', titel: 'Website', icon: 'code', x: 400, y: 262, ziel: true },
]
</script>

<template>
  <svg class="abh" viewBox="0 0 800 350" role="img"
       aria-label="Zielgruppe und Kalkulation starten sofort; Marketing wartet auf die Zielgruppe, Social Media auf das Marketing, die Website auf Zielgruppe, Marketing und Kalkulation.">
    <defs>
      <marker id="abh-pfeil" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" class="spitze" />
      </marker>
    </defs>

    <!-- Kanten -->
    <g class="kanten" marker-end="url(#abh-pfeil)">
      <line :x1="40 + B" y1="58" x2="306" y2="58" />
      <line :x1="312 + B" y1="58" x2="578" y2="58" />
      <line x1="400" :y1="30 + H" x2="486" y2="256" />
      <line :x1="40 + B" y1="198" x2="436" y2="256" />
      <path d="M 40 58 L 22 58 Q 12 58 12 68 L 12 280 Q 12 290 22 290 L 394 290" />
    </g>

    <!-- Knoten -->
    <g v-for="a in agenten" :key="a.id" :class="['knoten', { start: a.start, ziel: a.ziel }]">
      <rect :x="a.x" :y="a.y" :width="B" :height="H" />
      <rect :x="a.x + 12" :y="a.y + 12" width="32" height="32" rx="4" class="icon-box" />
      <component :is="icons[a.icon]" :x="a.x + 19" :y="a.y + 19" width="18" height="18" class="icon" />
      <text :x="a.x + 56" :y="a.y + H / 2 + 6">{{ a.titel }}</text>
    </g>

    <text x="128" y="126" class="hinweis" text-anchor="middle">starten sofort</text>
    <text :x="400 + B + 14" y="296" class="hinweis">braucht alle drei Ergebnisse</text>
  </svg>
</template>

<style scoped>
.abh {
  width: 100%;
  height: 100%;
  font-family: var(--font-sans);
  overflow: visible;
}

.kanten line,
.kanten path {
  fill: none;
  stroke: var(--thm-grey-400);
  stroke-width: 2.2;
}

.spitze { fill: var(--thm-grey-400); }

.knoten rect { fill: var(--card-bg); }
.knoten.start rect { fill: var(--thm-green-50); stroke: var(--thm-green-500); stroke-width: 2; }
.knoten.ziel rect { fill: var(--thm-grey-600); }
.knoten rect.icon-box { fill: var(--thm-green-500); stroke: none; }

.knoten text {
  font-size: 17px;
  font-weight: var(--fw-bold);
  fill: var(--text-strong);
}

.knoten.ziel text { fill: var(--white); }

.icon { color: var(--white); }

.hinweis {
  font-size: 14px;
  font-weight: var(--fw-semibold);
  fill: var(--thm-green-700);
}
</style>
