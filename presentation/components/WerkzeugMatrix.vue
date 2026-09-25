<!--
  Wer darf was bei den Counting Agents? Zeilen sind Handgriffe, Spalten die
  Agenten. Entspricht den `tools:`-Zeilen in the-counting-agents/agents/*.md;
  die allgemeinen Werkzeuge von pi (bash, read, write) nimmt run-agent.sh
  allen weg — die letzte Zeile. Ihr Hinweis erscheint erst, wenn die Maus
  auf der Zeile steht: im Vortrag ein Aha-Moment statt eines Kastens, den
  alle schon gelesen haben.

  Als Grid statt <table>, damit die Tabellenstile von Slidev nicht greifen.
-->
<script setup lang="ts">
const agenten = [
  { titel: 'Zähler', icon: 'list-ordered' },
  { titel: 'Sammler', zusatz: 'ungerade · gerade · prim', icon: 'filter' },
  { titel: 'Steuerung', icon: 'sliders-horizontal' },
]

const zeilen = [
  { was: 'Zahlen veröffentlichen', werkzeug: 'bus_publish', darf: [true, false, false] },
  { was: 'Zahlen lesen', werkzeug: 'bus_read', darf: [false, true, true] },
  { was: 'Befehle lesen', werkzeug: 'control_read', darf: [true, true, false] },
  { was: 'Befehle schicken', werkzeug: 'control_send', darf: [false, false, true] },
  { was: 'Eigenen Stand merken', werkzeug: 'state_write', darf: [true, true, false] },
  { was: 'Alles andere', werkzeug: 'bash · read · write · …', darf: [false, false, false], keiner: true },
]
</script>

<template>
  <div class="matrix" role="table" aria-label="Welcher Agent welches Werkzeug hat">
    <div class="kopfzeile" role="row">
      <div role="columnheader" />
      <div v-for="a in agenten" :key="a.titel" class="kopf" role="columnheader">
        <ThmIcon :name="a.icon" box ton="grau" :size="1.4" />
        <div>
          <div class="k-titel">{{ a.titel }}</div>
          <div v-if="a.zusatz" class="k-zusatz">{{ a.zusatz }}</div>
        </div>
      </div>
    </div>
    <div v-for="z in zeilen" :key="z.werkzeug" class="zeile" :class="{ keiner: z.keiner }" role="row">
      <div class="was" role="rowheader">
        <span class="w-text">{{ z.was }}</span>
        <span class="w-code">{{ z.werkzeug }}</span>
      </div>
      <div v-for="(d, i) in z.darf" :key="i" class="zelle" role="cell">
        <ThmIcon v-if="d" name="check" box ton="gruen" :size="1.2" />
        <ThmIcon v-else name="x" :ton="z.keiner ? 'rot' : 'grau'" :size="1.1" class="nein" />
      </div>
      <div v-if="z.keiner" class="hinweis" role="tooltip">
        <ThmIcon name="info" ton="weiss" :size="1" />
        <span>„Alles andere“ ist <strong>nicht verboten</strong> — die Werkzeuge sind <strong>gar nicht da</strong>. Das wirkt stärker als jedes Verbot im Text.</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.matrix {
  display: grid;
  gap: 0.25rem;
  width: 100%;
  font-size: 0.95rem;
}

/* Spalten wie Zeilen durch eine weiße Fuge getrennt: jede Zelle hat ihre
   eigene Fläche, die Zeile selbst ist durchsichtig. */
.kopfzeile,
.zeile {
  display: grid;
  grid-template-columns: 2.4fr 1fr 1fr 1fr;
  column-gap: 0.25rem;
}

/* Die Köpfe sitzen als eigene Felder bündig über ihrer Spalte */
.kopfzeile { align-items: stretch; }

.kopf {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.35rem 0.5rem;
  background: var(--thm-grey-100);
  border-bottom: 0.2rem solid var(--thm-grey-600);
}

.k-titel {
  font-weight: var(--fw-bold);
  font-size: 1rem;
  line-height: 1.1;
  color: var(--text-strong);
}

.k-zusatz {
  font-size: 0.7rem;
  white-space: nowrap;
  color: var(--text-muted);
}

.zeile {
  min-height: 2.15rem;
}

.zeile > * { background: var(--thm-grey-50); }

.was {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0 1rem;
}

.w-text {
  font-weight: var(--fw-semibold);
  color: var(--text-strong);
}

.w-code {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-muted);
}

.zelle {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nein { opacity: 0.5; }

.zeile.keiner > * {
  background: color-mix(in srgb, var(--thm-red) 8%, var(--white));
}

.zeile.keiner .w-text { color: var(--thm-red); }

/* Hinweis zur letzten Zeile: Tooltip über „Alles andere“, nur bei Hover */
.zeile.keiner {
  position: relative;
  cursor: help;
}

.zeile.keiner > .hinweis {
  position: absolute;
  bottom: calc(100% + 0.7rem);
  left: 0.6rem;
  z-index: 1;
  width: max-content;
  max-width: 24rem;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--thm-grey-800);
  border-radius: 0.3rem;
  font-size: 0.72rem;
  line-height: var(--lh-snug);
  color: var(--white);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease;
}

.zeile.keiner > .hinweis :deep(strong) { color: inherit; }

/* Spitze nach unten, zeigt auf die Zeile */
.zeile.keiner > .hinweis::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 1.2rem;
  border: 0.4rem solid transparent;
  border-top-color: var(--thm-grey-800);
}

.zeile.keiner:hover > .hinweis { opacity: 1; }
.zeile.keiner .nein { opacity: 1; }
</style>
