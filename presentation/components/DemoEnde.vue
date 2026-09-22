<!--
  Abschluss eines Demo-Blocks: zurück zur Übersicht für eine weitere Demo
  oder weiter zu „Was nehmen wir mit?". Die Pfeiltaste führt ebenfalls
  weiter (setup/main.ts).
-->
<template>
  <div class="ende">
    <Link to="demos" class="knopf zurueck">
      <ThmIcon name="layout-grid" ton="gruen" :size="1.6" />
      <span>
        <span class="k-titel">Noch eine Demo</span>
        <span class="k-text">zurück zur Übersicht</span>
      </span>
    </Link>
    <Link to="nach-demos" class="knopf weiter">
      <span>
        <span class="k-titel">Was nehmen wir mit?</span>
        <span class="k-text">weiter zum Schluss der Vorlesung</span>
      </span>
      <ThmIcon name="arrow-right" ton="weiss" :size="1.6" />
    </Link>
  </div>
</template>

<style scoped>
.ende {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
}

.knopf {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.3rem 1.6rem;
  border: none !important;
  text-decoration: none;
  transition: transform 0.15s ease;
}

.knopf:hover { transform: translateY(-3px); }

.zurueck {
  background: var(--thm-grey-50);
  color: var(--text-strong) !important;
}

.weiter {
  justify-content: space-between;
  background: var(--thm-green-500);
  color: var(--white) !important;
}

.k-titel {
  display: block;
  font-size: 1.3rem;
  font-weight: var(--fw-bold);
}

.k-text {
  display: block;
  font-size: 0.9rem;
  opacity: 0.8;
}
</style>
