<!--
  Ein Text, in Tokens zerlegt, wie ihn ein Tokenizer-Werkzeug zeigt: jedes
  Token ein Kästchen, abwechselnd grün und grau hinterlegt.

    <TokenKette :teile="[' Schn', 'upper', 'vor', 'les', 'ung']" legende />

  Ein Leerzeichen am Anfang eines Teils gehört zum Token — so zerlegen
  echte Tokenizer — und erscheint als blasses „␣“. Die Teile stehen also
  genau so da, wie der Tokenizer sie liefert. `legende` setzt
  „␣ = Leerzeichen“ dahinter.

  Ohne `block` steht die Kette im Textfluss und bricht nicht um; mit
  `block` steht sie als eigene Zeile und darf umbrechen. Schriftgröße und
  Abstände bestimmt die Umgebung (`class` am Aufruf).

  Slot `ende`: steht direkt hinter dem letzten Token und bleibt mit ihm auf
  einer Zeile — in <NaechstesWort> die Lücke für das nächste Token.
-->
<script setup lang="ts">
import { computed, useSlots } from 'vue'

const props = defineProps<{ teile: string[]; block?: boolean; legende?: boolean }>()
const slots = useSlots()

const tokens = computed(() => props.teile.map(t => ({ leer: t.startsWith(' '), text: t.replace(/^ /, '') })))
/* Mit Slot `ende` steht das letzte Token getrennt, zusammen mit dem Slot */
const vorne = computed(() => (slots.ende ? tokens.value.slice(0, -1) : tokens.value))
const letztes = computed(() => tokens.value.at(-1))
</script>

<template>
  <span class="tk" :class="{ block }">
    <span v-for="(t, i) in vorne" :key="i" class="tk-token" :class="{ zwei: i % 2 }"><i v-if="t.leer">␣</i>{{ t.text }}</span>
    <span v-if="$slots.ende && letztes" class="tk-ende">
      <span class="tk-token" :class="{ zwei: (tokens.length - 1) % 2 }"><i v-if="letztes.leer">␣</i>{{ letztes.text }}</span><slot name="ende" />
    </span>
    <span v-if="legende" class="tk-legende">␣ = Leerzeichen</span>
  </span>
</template>

<style scoped>
.tk {
  display: inline-flex;
  align-items: baseline;
  white-space: nowrap;
}

.tk.block {
  display: flex;
  flex-wrap: wrap;
  row-gap: 0.3rem;
}

.tk-token {
  padding: 0 0.15rem;
  background: var(--thm-green-100);
  color: var(--text-strong);
  font-weight: var(--fw-semibold);
}

.tk-token.zwei { background: var(--thm-grey-100); }

/* ␣ = Leerzeichen, das zum Token gehört */
.tk-token i {
  font-style: normal;
  font-weight: normal;
  color: var(--thm-grey-400);
}

.tk-ende { white-space: nowrap; }

.tk-legende {
  margin-left: 0.5em;
  font-size: 0.75em;
  color: var(--thm-grey-500);
}
</style>
