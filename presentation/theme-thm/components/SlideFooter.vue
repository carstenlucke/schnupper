<!--
  Fußzeile jeder Folie: Veranstaltung und Dozent links, rechts die
  Seitenzahl und die StudiumPlus-Marke — so wie im Design-System
  „THM & StudiumPlus“. Die Titelfolie trägt keine Seitenzahl.

  Die Inhalte kommen aus dem Frontmatter der slides.md:
    veranstaltung: Schnuppervorlesung
    dozent: Prof. Dr. Carsten Lucke
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import marke from '../assets/studiumplus-logo.png'
import markeWeiss from '../assets/studiumplus-logo-white.png'

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
    <span class="ft-rechts">
      <span v-if="zeigeSeite">{{ $page }}</span>
      <img :src="dunkel ? markeWeiss : marke" class="ft-marke" alt="StudiumPlus · Duales Studium" />
    </span>
  </footer>
</template>
