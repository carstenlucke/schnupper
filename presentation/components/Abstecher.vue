<!--
  Kleiner Link auf eine Zusatzfolie — eine Folie für Fragen, die vielleicht
  kommen. Zusatzfolien tragen im Frontmatter `zusatz: <routeAlias der
  Herkunftsfolie>` und werden beim Blättern übersprungen (setup/main.ts).

  Auf der Herkunftsfolie:  <Abstecher to="ki-gegen-ki">KI gegen KI?</Abstecher>
  Auf der Zusatzfolie:     <Abstecher to="herkunft" zurueck>Zurück</Abstecher>
-->
<script setup lang="ts">
defineProps<{
  to: string
  zurueck?: boolean
}>()
</script>

<template>
  <Link :to="to" class="abstecher">
    <ThmIcon :name="zurueck ? 'arrow-left' : 'message-circle'" :size="0.8" />
    <span><slot /></span>
    <ThmIcon v-if="!zurueck" name="arrow-right" :size="0.8" />
  </Link>
</template>

<style scoped>
.abstecher {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.2rem 0.55rem;
  font-size: 0.68rem;
  font-weight: var(--fw-bold);
  color: var(--thm-green-600) !important;
  background: var(--thm-grey-50);
  border: none !important;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s ease;
}

.abstecher:hover {
  background: var(--thm-green-100);
}
</style>
