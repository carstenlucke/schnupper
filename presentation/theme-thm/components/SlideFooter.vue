<!--
  Fußzeile jeder Folie: Veranstaltung und Dozent links, rechts die
  Seitenzahl. Die Titelfolie trägt keine Seitenzahl. Die StudiumPlus-Marke
  steht oben neben dem THM-Logo (ThmLockup.vue), nicht hier.

  Die Inhalte kommen aus dem Frontmatter der slides.md:
    veranstaltung: Schnuppervorlesung
    dozent: Prof. Dr. Carsten Lucke
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

defineProps<{ dunkel?: boolean }>()

const { $slidev, $page } = useSlideContext()

const config = computed(() => ($slidev?.configs ?? {}) as Record<string, unknown>)
const zeile = computed(() =>
  [config.value.veranstaltung, config.value.dozent].filter(Boolean).join(' · '),
)
const zeigeSeite = computed(() => ($page?.value ?? 1) > 1)
</script>

<template>
  <footer class="thm-footer" :class="{ dark: dunkel }">
    <span>{{ zeile }}</span>
    <span v-if="zeigeSeite">{{ $page }}</span>
  </footer>
</template>
