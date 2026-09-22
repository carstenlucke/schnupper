<!--
  Auf jeder Folie einer Demo (Frontmatter `demo:`) ein kleiner Weg zurück
  zur Übersicht der Demos, mittig in der Fußzeile.
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

const { $frontmatter } = useSlideContext()
const zeigen = computed(() => Boolean($frontmatter?.demo))
</script>

<template>
  <Link v-if="zeigen" to="demos" class="demo-zurueck" aria-label="Zur Übersicht der Demos">
    <ThmIcon name="layout-grid" ton="grau" :size="0.8" />
    <span>Demos</span>
  </Link>
</template>

<style scoped>
.demo-zurueck {
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  height: var(--footer-h);
  display: flex;
  align-items: center;
  gap: 0.35rem;
  z-index: 30;
  font-size: 0.55rem;
  color: var(--thm-grey-400) !important;
  border: none !important;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.15s ease, color 0.15s ease;
}

.demo-zurueck:hover {
  opacity: 1;
  color: var(--thm-green-600) !important;
}
</style>
