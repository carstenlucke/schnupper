<!--
  Titelfolie: dunkle Rasterfläche in THM Grau, links Rubrik (die
  Veranstaltung), Titel und Angaben, rechts das randabfallende Foto.

  Ohne `bild` steht rechts statt des Fotos ein kleines neuronales Netz,
  wie auf der Titelfolie des Design-Systems „THM & StudiumPlus“.

  Frontmatter:
    layout: cover
    bild: /campus-friedberg.jpg      # optional

  Inhalt:
    # Einführung in die Softwaretechnik
    <div class="cover-meta">Prof. Dr. Carsten Lucke</div>
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

defineProps<{ bild?: string; rubrik?: string }>()

const { $slidev } = useSlideContext()

/* Neuronales Netz als Dekor: Schichten mit 3, 5, 5 und 2 Knoten.
   Koordinaten im viewBox-Raster 400 × 400. */
const schichten = [3, 5, 5, 2]
const knoten = schichten.map((n, s) =>
  Array.from({ length: n }, (_, i) => ({
    x: 30 + s * (340 / (schichten.length - 1)),
    y: 200 + (i - (n - 1) / 2) * 78,
    rand: s === 0 || s === schichten.length - 1,
  })),
)
const kanten = knoten.slice(0, -1).flatMap((schicht, s) =>
  schicht.flatMap(a => knoten[s + 1].map(b => ({ a, b }))),
)
const veranstaltung = computed(() => ($slidev?.configs as Record<string, unknown>)?.veranstaltung as string | undefined)
</script>

<template>
  <div class="slidev-layout thm-cover thm-dark">
    <ThmLockup place="top-left" hell />
    <div class="cv-text">
      <div class="thm-eyebrow">{{ rubrik ?? veranstaltung }}</div>
      <slot />
    </div>
    <template v-if="bild">
      <div class="cv-photo" :style="{ backgroundImage: `url(${bild})` }" />
      <span class="cv-quad gross" aria-hidden="true" />
      <span class="cv-quad klein" aria-hidden="true" />
    </template>
    <svg v-else class="cv-netz" viewBox="0 0 400 400" aria-hidden="true">
      <line
        v-for="(k, i) in kanten" :key="`k${i}`"
        :x1="k.a.x" :y1="k.a.y" :x2="k.b.x" :y2="k.b.y"
      />
      <template v-for="(schicht, s) in knoten" :key="`s${s}`">
        <circle
          v-for="(n, i) in schicht" :key="i"
          :cx="n.x" :cy="n.y" r="15" :class="{ rand: n.rand }"
        />
      </template>
    </svg>
    <div class="cv-strich" aria-hidden="true" />
    <SlideFooter dunkel />
  </div>
</template>

<style scoped>
.thm-cover {
  padding: 0;
  overflow: hidden;
}

.cv-text {
  position: absolute;
  left: var(--slide-pad-x);
  top: 0;
  bottom: 0;
  width: 52%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-bottom: 1rem;
}

.cv-text :deep(h1) {
  color: var(--white);
  font-size: 2.55rem;
  line-height: 1.08;
  letter-spacing: -0.01em;
  margin: 0.2rem 0 0;
}

.cv-text :deep(.cover-meta) {
  margin-top: 1.4rem;
  font-size: 0.95rem;
  font-weight: var(--fw-semibold);
  color: var(--white);
  line-height: 1.5;
}

.cv-text :deep(.cover-meta p) { margin: 0; }

.cv-photo {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 38%;
  background-size: cover;
  background-position: center 60%;
  background-color: var(--thm-grey-500);
}

.cv-netz {
  position: absolute;
  right: 4.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 17rem;
  height: 17rem;
}

.cv-netz line {
  stroke: var(--thm-grey-400);
  stroke-width: 1.5;
  opacity: 0.55;
}

.cv-netz circle {
  fill: var(--thm-green-400);
  stroke: var(--white);
  stroke-width: 2;
}

.cv-netz circle.rand { fill: var(--thm-green-500); }

/* Die beiden Quadrate aus dem Design-System, an der Fotokante */
.cv-quad {
  position: absolute;
  background: var(--thm-green-500);
}

.cv-quad.gross {
  width: 3.2rem;
  height: 3.2rem;
  right: calc(38% - 1.6rem);
  bottom: 5.2rem;
}

.cv-quad.klein {
  width: 1.3rem;
  height: 1.3rem;
  right: calc(38% + 2.1rem);
  bottom: 3.9rem;
  background: var(--thm-green-400);
}

/* Grüner Strich vom linken Rand, unter dem Textblock */
.cv-strich {
  position: absolute;
  left: 0;
  bottom: var(--footer-h);
  width: 9rem;
  height: 0.28rem;
  background: var(--thm-green-500);
}
</style>
