<!--
  QR-Code zu einer Adresse, als SVG aus Vue gerechnet (uqr) — bleibt am
  Beamer scharf und ändert sich mit der Adresse. Dunkle Module auf weißer
  Kachel, auch auf dunklen Folien: invertierte Codes lesen nicht alle
  Kamera-Apps.

  Verwendung:
    <QrCode url="https://carstenlucke.github.io/schnupper/" />
    <QrCode url="…" :size="8" />

  `size` ist die Kantenlänge in rem (Voreinstellung 10), die Ruhezone von
  vier Modulen eingeschlossen.
-->
<script setup lang="ts">
import { computed } from 'vue'
import { encode } from 'uqr'

const props = withDefaults(defineProps<{ url: string; size?: number }>(), { size: 10 })

// Ein Pfad aus einem Quadrat je dunklem Modul. `border: 4` ist die Ruhezone,
// die der Standard verlangt — sie bildet die weiße Kachel.
const qr = computed(() => {
  const { size, data } = encode(props.url, { ecc: 'M', border: 4 })
  let d = ''
  data.forEach((zeile, y) => zeile.forEach((dunkel, x) => {
    if (dunkel) d += `M${x} ${y}h1v1h-1z`
  }))
  return { size, d }
})
</script>

<template>
  <div class="thm-qr" :style="{ width: `${size}rem`, height: `${size}rem` }">
    <svg :viewBox="`0 0 ${qr.size} ${qr.size}`" shape-rendering="crispEdges" role="img" :aria-label="`QR-Code: ${url}`">
      <path :d="qr.d" />
    </svg>
  </div>
</template>

<style scoped>
.thm-qr {
  background: var(--white);
  border-radius: var(--radius-icon);
}

.thm-qr svg {
  display: block;
  width: 100%;
  height: 100%;
}

.thm-qr path { fill: var(--thm-grey-900); }
</style>
