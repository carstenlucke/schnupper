<!--
  Logo der THM oben auf der Folie. Die StudiumPlus-Marke steht nach dem
  Aufbau des Design-Systems „THM & StudiumPlus“ unten rechts in der
  Fußzeile (SlideFooter.vue). Auf dunklen Flächen (`hell`) erscheint das
  Logo einfarbig weiß, wie es das CD für farbige Hintergründe vorsieht.

  `marke` stellt die StudiumPlus-Marke neben das THM-Logo, getrennt durch
  einen feinen Strich — nur für die Titelfolie; die Fußzeile lässt die
  Marke dann weg (`<SlideFooter ohne-marke />`).
-->
<script setup lang="ts">
import logo from '../assets/thm-logo.png'
import logoWeiss from '../assets/thm-logo-white.png'
import spLogo from '../assets/studiumplus-logo.png'
import spLogoWeiss from '../assets/studiumplus-logo-white.png'

defineProps<{ place?: 'top-right' | 'top-left'; hell?: boolean; marke?: boolean }>()
</script>

<template>
  <div v-if="marke" class="thm-lockup mit-marke" :class="[place ?? 'top-right', { hell }]">
    <img :src="hell ? logoWeiss : logo" alt="THM · Technische Hochschule Mittelhessen" />
    <span class="lk-strich" aria-hidden="true" />
    <img :src="hell ? spLogoWeiss : spLogo" alt="StudiumPlus · Duales Studium" />
  </div>
  <img
    v-else
    :src="hell ? logoWeiss : logo"
    class="thm-lockup"
    :class="place ?? 'top-right'"
    alt="THM · Technische Hochschule Mittelhessen"
  />
</template>
