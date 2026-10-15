<!--
  Erklärzeile unter einem Diagramm, das Klick für Klick läuft: links der
  Stand („Start“, „3 / 5“), daneben, was gerade passiert. Wechselt der
  Schritt, blendet der Text über. Mit `fertig` wird die Zeile zum
  grünen Merksatz-Band; den Merksatz gibt der Slot.

  `schritte` zählt nur die Schritte mit Zähler. Der `fertig`-Schritt
  danach zeigt den Merksatz und zählt nicht mit — so steht am Ende
  „4 / 4“, nicht „4 / 5“.

  Verwendung:
    <SchrittZeile :schritt="n" :schritte="4" :text="…" :fertig="n === 5" icon="user">
      <strong>Ihr seid die Brücke.</strong> …
    </SchrittZeile>

  In <CopyPasteSchleife>, <AgentDurchlauf> und <GrosserAuftrag>.
-->
<script setup lang="ts">
withDefaults(defineProps<{
  schritt: number
  schritte: number
  text: string
  fertig?: boolean
  icon?: string
}>(), { fertig: false, icon: 'check' })
</script>

<template>
  <div class="schritt-zeile" :class="{ fertig }">
    <template v-if="fertig">
      <ThmIcon :name="icon" ton="weiss" :size="1.35" />
      <span><slot /></span>
    </template>
    <template v-else>
      <span class="schritt-nr">{{ schritt ? `${schritt} / ${schritte}` : 'Start' }}</span>
      <Transition name="schritt-wechsel" mode="out-in">
        <span :key="schritt">{{ text }}</span>
      </Transition>
    </template>
  </div>
</template>

<style scoped>
.schritt-zeile {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  min-height: 3.1rem;
  margin-top: 1.1rem;
  padding: 0.55rem 1.1rem;
  background: var(--thm-grey-50);
  border-left: 0.25rem solid var(--thm-green-500);
  font-size: 1.05em;
  line-height: var(--lh-snug);
  color: var(--text-strong);
  transition: background 0.3s ease, color 0.3s ease;
}

.schritt-zeile.fertig {
  background: var(--thm-green-500);
  color: var(--white);
}

.schritt-zeile.fertig :deep(strong) { color: inherit; }

.schritt-nr {
  flex: none;
  min-width: 3.2rem;
  font-size: 0.72em;
  font-weight: var(--fw-bold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--thm-green-700);
}

.schritt-wechsel-enter-active,
.schritt-wechsel-leave-active { transition: opacity 0.2s ease; }

.schritt-wechsel-enter-from,
.schritt-wechsel-leave-to { opacity: 0; }
</style>
