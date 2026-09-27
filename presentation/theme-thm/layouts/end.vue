<!--
  Schlussfolie im Aufbau der Titelfolie: dunkle Rasterfläche, der Dank
  links, das Foto rechts.

  Ohne `bild` bleibt die rechte Seite frei; der Textblock bekommt dann
  mehr Breite. Mit `::right::` wird die Folie zweispaltig: rechts steht
  der Inhalt des Slots (z.B. ein <QrCode>), statt Foto.

  Frontmatter:
    layout: end
    bild: /campus-friedberg.jpg      # optional

  Markdown (zweispaltig):
    # Danke!
    …
    ::right::
    <QrCode url="…" />
-->
<script setup lang="ts">
import { publicPfad } from '../public-pfad'

defineProps<{ bild?: string; rubrik?: string }>()
</script>

<template>
  <div class="slidev-layout thm-end thm-dark">
    <ThmLockup place="top-left" hell />
    <div class="cv-text" :class="{ breit: !bild && !$slots.right, zweispaltig: $slots.right }">
      <div v-if="rubrik" class="thm-eyebrow">{{ rubrik }}</div>
      <slot />
      <div class="thm-bar end-bar" />
    </div>
    <div v-if="$slots.right" class="cv-rechts">
      <div class="cv-rechts-inhalt"><slot name="right" /></div>
    </div>
    <template v-else-if="bild">
      <div class="cv-photo" :style="{ backgroundImage: `url(${publicPfad(bild)})` }" />
      <span class="cv-quad" aria-hidden="true" />
    </template>
    <SlideFooter dunkel />
  </div>
</template>

<style scoped>
.thm-end {
  padding: 0;
  overflow: hidden;
}

.cv-text {
  position: absolute;
  left: var(--slide-pad-x);
  top: 0;
  bottom: 0;
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.cv-text.breit { width: 78%; }
.cv-text.zweispaltig { width: 46%; }

.cv-text :deep(h1) {
  color: var(--white);
  font-size: 2.4rem;
  line-height: 1.12;
  margin: 0.2rem 0 0;
}

.cv-text :deep(p) {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.85);
  margin: 1rem 0 0;
}

.end-bar {
  width: 5.2rem;
  margin-top: 1.5rem;
}

.cv-rechts {
  position: absolute;
  right: var(--slide-pad-x);
  top: 0;
  bottom: 0;
  width: 43%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.cv-rechts-inhalt {
  padding-left: 2.4rem;
  border-left: 1px solid rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.85);
}

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

.cv-quad {
  position: absolute;
  width: 3.2rem;
  height: 3.2rem;
  right: calc(38% - 1.6rem);
  top: 5.2rem;
  background: var(--thm-green-500);
}
</style>
