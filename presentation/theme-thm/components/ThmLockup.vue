<!--
  Logo der THM oben auf der Folie. Die StudiumPlus-Marke steht nach dem
  Aufbau des Design-Systems „THM & StudiumPlus“ unten rechts in der
  Fußzeile (SlideFooter.vue). Auf dunklen Flächen (`hell`) erscheint das
  Logo einfarbig weiß, wie es das CD für farbige Hintergründe vorsieht.
-->
<script setup lang="ts">
import logo from '../assets/thm-logo.png'
import logoWeiss from '../assets/thm-logo-white.png'

defineProps<{ place?: 'top-right' | 'top-left'; hell?: boolean }>()
</script>

<template>
  <img
    :src="hell ? logoWeiss : logo"
    class="thm-lockup"
    :class="place ?? 'top-right'"
    alt="THM · Technische Hochschule Mittelhessen"
  />
</template>
