<!--
  Standardlayout: Rubrik, Titel, optionaler Untertitel, grüner Balken,
  darunter freier Inhalt.

  Frontmatter:
    layout: default
    rubrik: Was ist Software?              # optional, grüne Versalien
    titel: Charakteristika von Software
    untertitel: Die sechs Merkmale        # optional
-->
<script setup lang="ts">
defineProps<{ rubrik?: string; titel?: string; untertitel?: string }>()
</script>

<template>
  <div class="slidev-layout thm-default">
    <ThmLockup />
    <SlideHead :rubrik="rubrik" :titel="titel" :untertitel="untertitel" />
    <div class="thm-body">
      <slot />
    </div>
    <SlideFooter />
  </div>
</template>
