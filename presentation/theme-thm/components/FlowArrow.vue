<!--
  Verbindungsglied zwischen zwei Karten in einer `.thm-flow`-Reihe:
  ein grüner Pfeil für „daraus folgt“, mit `text` stattdessen ein kurzes
  Wort wie „vs.“ für eine Gegenüberstellung.

  Verwendung:
    <div class="thm-flow">
      <Card …>…</Card>
      <FlowArrow />
      <Card …>…</Card>
    </div>
-->
<script setup lang="ts">
defineProps<{ text?: string }>()
</script>

<template>
  <div class="flow-arrow" aria-hidden="true">
    <span v-if="text" class="fa-text">{{ text }}</span>
    <ThmIcon v-else name="arrow-right" ton="gruen" :size="1.8" />
  </div>
</template>

<style scoped>
.flow-arrow {
  flex: none;
  display: grid;
  place-items: center;
  padding: 0 0.2rem;
}

.fa-text {
  font-size: 1.3rem;
  font-weight: var(--fw-bold);
  color: var(--thm-green-600);
}
</style>
