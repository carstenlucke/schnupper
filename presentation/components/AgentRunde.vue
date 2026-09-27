<!--
  Die Agent Party als Bild: vier KI-Agenten im Kreis um ein gemeinsames
  Thema, reihum verbunden, jeder mit einer Sprechblase. Die Rollen sind die
  mitgelieferten Profile aus agent-party/profile/ — ihre Sätze greifen
  jeweils die Beschreibung des Profils auf.

  Aufbau: ein Rahmen mit festem Seitenverhältnis, darin ein SVG für Tisch
  und Bögen (Koordinaten im viewBox 880 × 380) und darüber HTML-Knoten, die
  in Prozent derselben Fläche liegen. So bleiben die Icons aus dem Theme
  und die Schrift aus dem CD, und nichts verzerrt.
-->
<script setup lang="ts">
const B = 880
const H = 380
const M = { x: 440, y: 200 }       // Mitte des Tisches
const R = { x: 175, y: 115 }       // Halbachsen der Runde

/* Uhrzeigersinn ab oben: so ist die Reihenfolge der Beiträge */
const agenten = [
  { winkel: -90, name: 'Skeptische Ökonomin', satz: 'Klingt gut. Und was kostet das?', ton: 'gruen', blase: 'oben' },
  { winkel: 0, name: 'Technik-Optimist', satz: 'Stellt euch vor, was damit alles möglich wird!', ton: 'grau', blase: 'rechts' },
  { winkel: 90, name: 'Ethikerin', satz: 'Wer profitiert — und wer zahlt?', ton: 'gruen', blase: 'unten' },
  { winkel: 180, name: 'Praktiker', satz: 'Schön. Und wer macht das am Montag?', ton: 'grau', blase: 'links' },
]

const punkt = (grad: number) => {
  const w = (grad * Math.PI) / 180
  return { x: M.x + R.x * Math.cos(w), y: M.y + R.y * Math.sin(w) }
}

const pct = (p: { x: number; y: number }) => ({ left: `${(p.x / B) * 100}%`, top: `${(p.y / H) * 100}%` })

/* Bogen vom einen Agenten zum nächsten, an beiden Enden gekürzt */
const LUECKE = 27
const boegen = agenten.map((a) => {
  const von = punkt(a.winkel + LUECKE)
  const bis = punkt(a.winkel + 90 - LUECKE)
  return `M ${von.x} ${von.y} A ${R.x} ${R.y} 0 0 1 ${bis.x} ${bis.y}`
})

const reihum = punkt(-45)
</script>

<template>
  <div class="runde">
    <svg class="ar-svg" :viewBox="`0 0 ${B} ${H}`" aria-hidden="true">
      <defs>
        <marker id="ar-spitze" viewBox="0 0 10 10" refX="7" refY="5"
                markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" class="ar-spitze" />
        </marker>
      </defs>
      <ellipse :cx="M.x" :cy="M.y" rx="92" ry="54" class="ar-tisch" />
      <path v-for="(d, i) in boegen" :key="i" :d="d" class="ar-bogen" marker-end="url(#ar-spitze)" />
    </svg>

    <div class="ar-thema" :style="pct(M)">
      <ThmIcon name="message-square" :size="1.4" />
      <strong>Ein Thema</strong>
      <span>für alle am Tisch</span>
    </div>

    <div class="ar-reihum" :style="pct({ x: reihum.x + 34, y: reihum.y - 14 })">reihum</div>

    <div v-for="a in agenten" :key="a.name" class="ar-agent" :style="pct(punkt(a.winkel))">
      <ThmIcon name="bot" box :ton="a.ton" :size="2.9" />
      <div class="ar-blase" :class="a.blase">
        <div class="ar-name">{{ a.name }}</div>
        <div class="ar-satz">„{{ a.satz }}“</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.runde {
  position: relative;
  aspect-ratio: 880 / 380;
  height: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.ar-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.ar-tisch {
  fill: var(--thm-green-50);
  stroke: var(--thm-green-300);
  stroke-width: 1.5;
  stroke-dasharray: 5 4;
}

.ar-bogen {
  fill: none;
  stroke: var(--thm-green-500);
  stroke-width: 2.5;
}

.ar-spitze { fill: var(--thm-green-500); }

.ar-thema {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--thm-green-800);
  font-size: 0.8rem;
  line-height: 1.25;
  text-align: center;
}

.ar-thema strong {
  font-size: 1.05rem;
  color: var(--text-strong);
}

.ar-reihum {
  position: absolute;
  transform: translate(0, -50%);
  font-size: 0.8rem;
  font-weight: var(--fw-bold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.ar-agent {
  position: absolute;
  transform: translate(-50%, -50%);
}

/* Sprechblase: eine Ecke spitz, zeigt auf den Agenten */
.ar-blase {
  position: absolute;
  width: max-content;
  max-width: 14rem;
  padding: 0.45rem 0.7rem;
  background: var(--white);
  border: 1px solid var(--border-default);
  border-radius: 0.5rem;
  font-size: 0.85rem;
  line-height: 1.3;
  color: var(--text-body);
}

.ar-name {
  font-weight: var(--fw-bold);
  color: var(--text-strong);
  margin-bottom: 0.1rem;
}

.ar-satz { font-style: italic; }

.ar-blase.oben   { bottom: calc(100% + 0.4rem); left: 50%; transform: translateX(-50%); border-bottom-left-radius: 0.5rem; }
.ar-blase.rechts { left: calc(100% + 0.6rem); top: 50%; transform: translateY(-50%); border-top-left-radius: 0; }
.ar-blase.unten  { left: calc(100% + 0.6rem); top: 62%; border-top-left-radius: 0; }
.ar-blase.links  { right: calc(100% + 0.6rem); top: 50%; transform: translateY(-50%); border-top-right-radius: 0; }
</style>
