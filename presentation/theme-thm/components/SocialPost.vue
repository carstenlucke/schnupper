<!--
  Beitrag aus einem beruflichen Netzwerk, als Karte nachgestellt — für
  Motivationsfolien, die mit einem echten Fundstück einsteigen. Kein Logo:
  Profilbild oder Initialen im Kreis genügen, damit der Beitrag als solcher
  erkennbar ist. Die Quelle gehört als .thm-note unter die Karte.
  `foto` ersetzt die Initialen durch ein Profilbild (quadratisch, liegt in
  public/).

  Verwendung:
    <SocialPost autor="Alex Wang" zeile="Learn AI Together" datum="25.09.2026"
                bild="/linkedin-jobsuche-2026.jpg" reaktionen="1.023" kommentare="51">
      Nice visual - I’ve actually used most of these.
    </SocialPost>

  Das Bild wird oben bündig beschnitten und füllt die Resthöhe der Karte.
  `kommentar` zeigt einen Kommentar unter einem Beitrag: ohne Folgen-Knopf
  und Aktionsleiste, die Reaktionen als schlichte Zahl.
-->
<script setup lang="ts">
import { computed } from 'vue'
import { publicPfad } from '../public-pfad'

const props = defineProps<{
  autor: string
  zeile?: string
  foto?: string
  datum?: string
  bild?: string
  bildAlt?: string
  reaktionen?: string
  kommentare?: string
  kommentar?: boolean
}>()

const initialen = computed(() =>
  props.autor.split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase())
</script>

<template>
  <article class="sp" :class="{ 'sp-kommentar': kommentar }">
    <header class="sp-kopf">
      <img v-if="foto" class="sp-avatar" :src="publicPfad(foto)" alt="" />
      <div v-else class="sp-avatar" aria-hidden="true">{{ initialen }}</div>
      <div class="sp-wer">
        <div class="sp-autor">{{ autor }}</div>
        <div v-if="zeile" class="sp-zeile">{{ zeile }}</div>
        <div v-if="datum" class="sp-datum">{{ datum }} · <ThmIcon name="globe" :size="0.62" /></div>
      </div>
      <div v-if="!kommentar" class="sp-folgen">+ Folgen</div>
    </header>

    <div class="sp-text"><slot /></div>

    <img v-if="bild" class="sp-bild" :src="publicPfad(bild)" :alt="bildAlt ?? ''" />

    <div v-if="reaktionen || kommentare" class="sp-zahlen">
      <span v-if="reaktionen"><span class="sp-daumen"><ThmIcon name="thumbs-up" :size="0.5" /></span> {{ reaktionen }}</span>
      <span v-if="kommentare">{{ kommentare }} Kommentare</span>
    </div>

    <footer v-if="!kommentar" class="sp-aktionen">
      <span><ThmIcon name="thumbs-up" :size="0.8" /> Gefällt mir</span>
      <span><ThmIcon name="message-circle" :size="0.8" /> Kommentieren</span>
      <span><ThmIcon name="repeat-2" :size="0.8" /> Reposten</span>
      <span><ThmIcon name="send" :size="0.8" /> Senden</span>
    </footer>
  </article>
</template>

<style scoped>
.sp {
  display: flex;
  flex-direction: column;
  min-height: 0;
  background: var(--white);
  border: 1px solid var(--border-default);
  border-radius: 0.3rem;
  overflow: hidden;
  font-size: 0.62rem;
  line-height: var(--lh-snug);
  color: var(--text-strong);
}

.sp-kopf {
  flex: none;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.6rem 0.7rem 0.4rem;
}

.sp-avatar {
  flex: none;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--thm-grey-600);
  color: var(--white);
  font-weight: var(--fw-bold);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  object-fit: cover;
}

.sp-wer { flex: 1; min-width: 0; }

.sp-autor {
  font-weight: var(--fw-bold);
  font-size: 0.72rem;
  color: var(--thm-grey-800);
}

.sp-zeile,
.sp-datum {
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sp-datum {
  display: flex;
  align-items: center;
  gap: 0.25em;
}

.sp-folgen {
  flex: none;
  color: var(--thm-blue);
  font-weight: var(--fw-bold);
}

.sp-text {
  flex: none;
  padding: 0 0.7rem 0.5rem;
}

.sp-text :deep(p) { margin: 0 0 0.3rem; }
.sp-text :deep(p:last-child) { margin-bottom: 0; }

.sp-bild {
  flex: 1;
  min-height: 0;
  width: 100%;
  object-fit: cover;
  object-position: top;
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
}

.sp-zahlen {
  flex: none;
  display: flex;
  justify-content: space-between;
  padding: 0.35rem 0.7rem;
  color: var(--text-muted);
}

.sp-zahlen > span {
  display: inline-flex;
  align-items: center;
  gap: 0.3em;
}

.sp-daumen {
  display: inline-grid;
  place-items: center;
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 50%;
  background: var(--thm-blue);
  color: var(--white);
}

.sp-aktionen {
  flex: none;
  display: flex;
  justify-content: space-around;
  padding: 0.35rem 0.4rem 0.45rem;
  border-top: 1px solid var(--border-subtle);
  color: var(--thm-grey-500);
  font-weight: var(--fw-semibold);
}

.sp-aktionen > span {
  display: inline-flex;
  align-items: center;
  gap: 0.3em;
}
.sp-kommentar { background: var(--thm-grey-50); }
.sp-kommentar .sp-zahlen { justify-content: flex-start; padding-top: 0; }
</style>
