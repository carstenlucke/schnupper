<!--
  Standardlayout: Rubrik, Titel, optionaler Untertitel, grüner Balken,
  darunter freier Inhalt.

  Mit `dunkel: true` steht die Folie auf der dunklen Rasterfläche der
  Abschnittstrenner, Logos und Titel in Weiß — für eine Folie, die sich
  von den Inhaltsfolien abheben soll, ohne eine Frage zu sein (Gelb bleibt
  den Fragen vorbehalten). Karten und Callouts behalten ihre Farben, nur
  das graue Kartenband wird dunkler.

  Frontmatter:
    layout: default
    rubrik: Was ist Software?              # optional, grüne Versalien
    titel: Charakteristika von Software
    untertitel: Die sechs Merkmale        # optional
    dunkel: true                          # optional
-->
<script setup lang="ts">
defineProps<{ rubrik?: string; titel?: string; untertitel?: string; dunkel?: boolean }>()
</script>

<template>
  <div class="slidev-layout thm-default" :class="{ 'thm-dark deep': dunkel }">
    <ThmLockup :hell="dunkel" />
    <SlideHead :rubrik="rubrik" :titel="titel" :untertitel="untertitel" />
    <div class="thm-body">
      <slot />
    </div>
    <SlideFooter :dunkel="dunkel" />
  </div>
</template>

<style scoped>
.thm-dark :deep(.thm-head h1) { color: var(--white); }
.thm-dark :deep(.thm-head .slide-subtitle) { color: var(--thm-grey-200); }

/* Das graue Kartenband verschwände sonst im Grund */
.thm-dark :deep(.card-band.grau) { background: var(--thm-grey-800); }
</style>
