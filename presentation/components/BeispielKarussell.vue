<!--
  Mehrere Beispiele auf einer Folie, eins nach dem anderen: Die Beispiele
  liegen übereinander, sichtbar ist immer nur eins. Darunter eine Leiste
  mit Punkten und „Beispiel 2 von 3“ — wie viele es gibt und wo man steht.

  Geblättert wird mit den Klicks der Folie, also mit → und dem Presenter:
  Klick 0 zeigt Beispiel 1, Klick 1 Beispiel 2 und so weiter; nach dem
  letzten Beispiel geht es zur nächsten Folie. Die Folie braucht deshalb
  `clicks: <Anzahl − 1>` im Frontmatter. Punkte und Pfeile in der Leiste
  springen direkt auf ein Beispiel.

  Die Beispiele kommen als benannte Slots `#1`, `#2`, … — je ein Slot pro
  Eintrag in `titel`. Weil alle Beispiele im selben Rasterfeld liegen, hat
  der Block immer die Höhe des größten; beim Blättern springt nichts.

  Verwendung (Folie mit `clicks: 1`):
    <BeispielKarussell :titel="['Erstes', 'Zweites']">
      <template #1>…</template>
      <template #2>…</template>
    </BeispielKarussell>
-->
<script setup lang="ts">
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

const props = defineProps<{ titel: string[] }>()

const { $clicks, $page } = useSlideContext()
const { go } = useNav()

const anzahl = computed(() => props.titel.length)
const aktiv = computed(() => Math.min(Math.max($clicks.value, 0), anzahl.value - 1))

function zeige(i: number, e: MouseEvent) {
  go($page.value, i);
  /* Sonst löst die Leertaste zum Weiterblättern den Knopf erneut aus */
  (e.currentTarget as HTMLElement).blur()
}
</script>

<template>
  <div class="bk">
    <div class="bk-buehne">
      <div
        v-for="(_, i) in titel"
        :key="i"
        class="bk-seite"
        :class="{ aktiv: i === aktiv }"
        :aria-hidden="i !== aktiv"
      >
        <slot :name="String(i + 1)" />
      </div>
    </div>

    <div class="bk-leiste">
      <button class="bk-pfeil" :disabled="aktiv === 0" aria-label="Voriges Beispiel" @click="zeige(aktiv - 1, $event)">
        <ThmIcon name="chevron-left" :size="1" />
      </button>
      <button
        v-for="(t, i) in titel"
        :key="i"
        class="bk-punkt"
        :class="{ aktiv: i === aktiv }"
        :aria-label="t"
        @click="zeige(i, $event)"
      />
      <button class="bk-pfeil" :disabled="aktiv === anzahl - 1" aria-label="Nächstes Beispiel" @click="zeige(aktiv + 1, $event)">
        <ThmIcon name="chevron-right" :size="1" />
      </button>
      <span class="bk-stand">Beispiel {{ aktiv + 1 }} von {{ anzahl }}<span class="bk-titel">: {{ titel[aktiv] }}</span></span>
    </div>
  </div>
</template>

<style scoped>
.bk {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  min-height: 0;
}

.bk-buehne {
  display: grid;
  min-height: 0;
}

.bk-seite {
  grid-area: 1 / 1;
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transform: translateX(1.5rem);
  transition: opacity 0.3s ease, transform 0.3s ease, visibility 0s 0.3s;
}

/* Kein transform am aktiven Beispiel: Sonst fängt es Overlays mit
   `position: fixed` ein (z. B. <CodeKlappe>) */
.bk-seite.aktiv {
  opacity: 1;
  visibility: visible;
  transform: none;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.bk-seite > :slotted(*) { flex: 1; }

.bk-leiste {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
}

.bk-pfeil {
  display: grid;
  place-items: center;
  padding: 0.1rem;
  background: none;
  border: none;
  color: var(--thm-grey-600);
  cursor: pointer;
}

.bk-pfeil:hover:not(:disabled) { color: var(--thm-green-700); }
.bk-pfeil:disabled { color: var(--thm-grey-300); cursor: default; }

.bk-punkt {
  width: 0.55rem;
  height: 0.55rem;
  padding: 0;
  background: var(--thm-grey-300);
  border: none;
  border-radius: 999px;
  cursor: pointer;
  transition: width 0.3s ease, background 0.3s ease;
}

.bk-punkt:hover { background: var(--thm-grey-400); }

.bk-punkt.aktiv {
  width: 1.6rem;
  background: var(--thm-green-500);
}

.bk-stand {
  margin-left: 0.5rem;
  font-size: 0.62rem;
  font-weight: var(--fw-bold);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.bk-titel { color: var(--thm-grey-600); }
</style>
