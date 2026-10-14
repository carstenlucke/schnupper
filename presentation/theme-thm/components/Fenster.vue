<!--
  Ein Programmfenster als Skizze: Leiste mit drei Punkten und Titel,
  darunter der Inhalt. Für Bilder, die zeigen, wo etwas passiert — ein
  Chat, ein Dokument.

  Verwendung:
    <Fenster titel="Referat.docx">
      <div class="thm-dok">
        <div class="thm-zeile titel" />
        <div class="thm-zeile" />
        <div class="thm-zeile kurz" />
      </div>
    </Fenster>
    <Fenster titel="ChatGPT" kompakt>
      …
      <template #leiste><i class="…">App</i></template>
    </Fenster>

  kompakt: kleinere Leiste, für enge Diagramme; der Inhalt zieht mit
  `.thm-dok.kompakt` nach. Der Slot `leiste` steht rechts neben dem Titel.
  Zeilen einzeln hervorheben (markiert, neu, …) macht die Folie selbst.
-->
<script setup lang="ts">
defineProps<{ titel: string; kompakt?: boolean }>()
</script>

<template>
  <div class="fenster" :class="{ kompakt }">
    <div class="fe-leiste">
      <span /><span /><span />
      <b>{{ titel }}</b>
      <slot name="leiste" />
    </div>
    <slot />
  </div>
</template>

<style scoped>
.fenster {
  display: flex;
  flex-direction: column;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
}

.fe-leiste {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.45rem 0.7rem;
  background: var(--thm-grey-50);
  border-bottom: 1px solid var(--thm-grey-200);
  font-size: 0.72rem;
}

.fe-leiste span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--thm-grey-200);
}

.fe-leiste b {
  margin-left: 0.5rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-600);
}

.kompakt .fe-leiste {
  gap: 0.25rem;
  padding: 0.3rem 0.5rem;
  font-size: 0.72em;
}

.kompakt .fe-leiste span {
  width: 0.4rem;
  height: 0.4rem;
}

.kompakt .fe-leiste b { margin-left: 0.35rem; }
</style>
