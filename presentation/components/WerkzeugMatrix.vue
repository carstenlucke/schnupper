<!--
  Wer darf was bei den Counting Agents? Zeilen sind Handgriffe, Spalten die
  Agenten. Entspricht den `tools:`-Zeilen in the-counting-agents/agents/*.md;
  die allgemeinen Werkzeuge von pi (bash, read, write) nimmt run-agent.sh
  allen weg — die letzte Zeile.

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
  { was: 'Alles andere', werkzeug: 'bash · read · write', darf: [false, false, false], keiner: true },
]
</script>

<template>
  <div class="matrix" role="table" aria-label="Welcher Agent welches Werkzeug hat">
    <div class="kopfzeile" role="row">
      <div role="columnheader" />
      <div v-for="a in agenten" :key="a.titel" class="kopf" role="columnheader">
        <ThmIcon :name="a.icon" box :size="1.4" />
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

.kopfzeile,
.zeile {
  display: grid;
  grid-template-columns: 2.4fr 1fr 1fr 1fr;
  align-items: center;
}

.kopfzeile { padding-bottom: 0.2rem; }

.kopf {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
}

.k-titel {
  font-weight: var(--fw-bold);
  font-size: 1rem;
  line-height: 1.1;
  color: var(--text-strong);
}

.k-zusatz {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.zeile {
  background: var(--thm-grey-50);
  min-height: 2.15rem;
}

.was {
  display: flex;
  align-items: baseline;
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
  justify-content: center;
}

.nein { opacity: 0.5; }

.zeile.keiner {
  background: color-mix(in srgb, var(--thm-red) 8%, var(--white));
}

.zeile.keiner .w-text { color: var(--thm-red); }
.zeile.keiner .nein { opacity: 1; }
</style>
