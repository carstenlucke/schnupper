<!--
  Der Agent-Kreislauf: vier Schritte in einer Reihe, darunter der
  gestrichelte Rückweg vom Prüfen zurück zum Verstehen. Ersetzt die
  frühere Grafik agent-kreislauf.svg, die nur auf dunklem Grund lesbar war.
-->
<script setup lang="ts">
const schritte = [
  { icon: 'scan-search', titel: 'Verstehen', text: 'Aufgabe lesen' },
  { icon: 'list-checks', titel: 'Planen', text: 'Schritte festlegen' },
  { icon: 'wrench', titel: 'Handeln', text: 'Werkzeuge nutzen, Dateien schreiben' },
  { icon: 'search-check', titel: 'Prüfen', text: 'Ergebnis kontrollieren' },
]
</script>

<template>
  <div class="kreislauf">
    <template v-for="(s, i) in schritte" :key="s.titel">
      <FlowArrow v-if="i > 0" class="kl-pfeil" />
      <Card :icon="s.icon" :titel="s.titel" :nummer="`0${i + 1}`" class="kl-schritt">
        {{ s.text }}
      </Card>
    </template>
    <div class="kl-zurueck">
      <span class="kl-label">
        <ThmIcon name="refresh-cw" ton="gruen" :size="1" />
        Nicht gut genug? Nochmal von vorne
      </span>
    </div>
  </div>
</template>

<style scoped>
.kreislauf {
  --pfeil: 3rem;
  display: grid;
  grid-template-columns:
    minmax(0, 1fr) var(--pfeil) minmax(0, 1fr) var(--pfeil)
    minmax(0, 1fr) var(--pfeil) minmax(0, 1fr);
  grid-template-rows: auto 3.2rem;
}

.kl-schritt { font-size: 0.95em; }

/* Rückweg: von der Mitte der letzten zur Mitte der ersten Karte */
.kl-zurueck {
  grid-column: 1 / -1;
  margin: 0 calc((100% - 3 * var(--pfeil)) / 8);
  border: 2px dashed var(--thm-green-500);
  border-top: 0;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  position: relative;
}

/* Pfeilspitze am linken Ende, zeigt nach oben auf „Verstehen“ */
.kl-zurueck::before {
  content: '';
  position: absolute;
  left: -0.45rem;
  top: -0.1rem;
  border: 0.4rem solid transparent;
  border-bottom: 0.55rem solid var(--thm-green-500);
  border-top: 0;
}

.kl-label {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  transform: translateY(50%);
  background: var(--surface-page);
  padding: 0 0.8rem;
  font-size: 0.85rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-500);
}
</style>
