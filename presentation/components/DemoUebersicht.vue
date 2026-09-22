<!--
  Die Übersichtsfolie der Demos: drei Karten, ein Klick springt an den
  Anfang der Demo (routeAlias `demo-<id>` auf deren erster Folie).
-->
<script setup lang="ts">
const demos = [
  { id: 'ship-it', titel: 'Ship It!', icon: 'rocket', text: 'Fünf Agenten bringen euer Produkt auf den Markt — bis zur fertigen Website.' },
  { id: 'counting-agents', titel: 'The Counting Agents', icon: 'list-ordered', text: 'Fünf Agenten zählen gemeinsam — und wir sehen ihnen bei der Arbeit zu.' },
  { id: 'agent-party', titel: 'Agent Party', icon: 'messages-square', text: 'Ihr schreibt die Agenten selbst — und sie diskutieren miteinander.' },
]
</script>

<template>
  <div class="uebersicht">
    <Link v-for="d in demos" :key="d.id" :to="`demo-${d.id}`" class="ziel">
      <Card band="gruen" :icon="d.icon" :titel="d.titel">
        <p>{{ d.text }}</p>
        <div class="los">
          <span>Demo starten</span>
          <ThmIcon name="arrow-right" ton="gruen" :size="1.1" />
        </div>
      </Card>
    </Link>
  </div>
</template>

<style scoped>
.uebersicht {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.2rem;
}

.ziel {
  display: flex;
  border: none !important;
  color: inherit !important;
  text-decoration: none;
  transition: transform 0.15s ease;
}

.ziel > :deep(.thm-card) { flex: 1; }
.ziel:hover { transform: translateY(-3px); }

.los {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 1rem;
  font-weight: var(--fw-bold);
  color: var(--thm-green-600);
}
</style>
