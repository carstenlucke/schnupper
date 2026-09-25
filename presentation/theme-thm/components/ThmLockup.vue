<!--
  Logos oben auf jeder Folie: THM-Logo und StudiumPlus-Marke nebeneinander,
  getrennt durch einen feinen Strich. Auf dunklen Flächen (`hell`)
  erscheinen beide einfarbig weiß, wie es das CD für farbige Hintergründe
  vorsieht. Die Fußzeile trägt keine Marke.
-->
<script setup lang="ts">
import logo from '../assets/thm-logo.png'
import logoWeiss from '../assets/thm-logo-white.png'
import spLogo from '../assets/studiumplus-logo.png'
import spLogoWeiss from '../assets/studiumplus-logo-white.png'

defineProps<{ place?: 'top-right' | 'top-left'; hell?: boolean }>()
</script>

<template>
  <div class="thm-lockup" :class="[place ?? 'top-right', { hell }]">
    <img :src="hell ? logoWeiss : logo" alt="THM · Technische Hochschule Mittelhessen" />
    <span class="lk-strich" aria-hidden="true" />
    <img :src="hell ? spLogoWeiss : spLogo" alt="StudiumPlus · Duales Studium" />
  </div>
</template>
