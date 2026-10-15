<!--
  Pfeil, über den eine Nachricht läuft: Ruht er, ist er grau und trägt
  eine graue Beschriftung. Ist er aktiv, wird er grün, ein Punkt läuft
  in Pfeilrichtung darüber, und die Nachricht steht dunkel daneben.
  Wechselt der Text, blendet er über.

  Für Diagramme, die Klick für Klick zeigen, wer wem was schickt
  (<CopyPasteSchleife>, <AgentDurchlauf>). Den Text setzt die Komponente,
  die den Pfeil benutzt, je nach Schritt.

  Verwendung:
    <LaufPfeil richtung="rechts" text="Antwort" :aktiv="…" />
    <LaufPfeil richtung="links" seite="unten" :zeilen="3" text="…" />
    <LaufPfeil richtung="runter" seite="links" text="Auftrag" />
    <LaufPfeil richtung="links" text="…"><ThmIcon … /> {{ text }}</LaufPfeil>

  Waagrecht füllt der Pfeil die Breite; die Nachricht steht über
  (`seite="oben"`, Voreinstellung) oder unter der Linie und hält Platz
  für `zeilen` Zeilen frei, damit beim Wechsel nichts springt. Senkrecht
  ist er 3rem hoch, die Nachricht steht links oder rechts daneben
  (Voreinstellung rechts). Die Schrift der Nachricht ist 0.82em —
  größer oder kleiner per font-size am Pfeil.
-->
<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  richtung: 'links' | 'rechts' | 'hoch' | 'runter'
  text: string
  aktiv?: boolean
  seite?: 'oben' | 'unten' | 'links' | 'rechts'
  zeilen?: number
}>(), { aktiv: false, zeilen: 2 })

const senkrecht = computed(() => props.richtung === 'hoch' || props.richtung === 'runter')
const seite = computed(() => props.seite ?? (senkrecht.value ? 'rechts' : 'oben'))
</script>

<template>
  <div
    class="lauf-pfeil"
    :class="[richtung, `seite-${seite}`, senkrecht ? 'senkrecht' : 'waagrecht', { aktiv }]"
    :style="{ '--zeilen': zeilen }"
  >
    <Transition name="lauf-wechsel" mode="out-in">
      <span :key="text" class="lauf-nachricht"><slot>{{ text }}</slot></span>
    </Transition>
    <div class="lauf-linie"><span class="lauf-punkt" /></div>
  </div>
</template>

<style scoped>
.lauf-pfeil { --punkt: 0.55rem; }

.lauf-linie {
  position: relative;
  background: var(--thm-grey-300);
  transition: background 0.3s ease;
}

.aktiv > .lauf-linie { background: var(--thm-green-500); }

/* Pfeilspitze */
.lauf-linie::after {
  content: '';
  position: absolute;
  border: 0.38rem solid transparent;
  transition: border-color 0.3s ease;
}

/* Laufender Punkt: die Nachricht unterwegs */
.lauf-punkt {
  position: absolute;
  width: var(--punkt);
  height: var(--punkt);
  border-radius: 50%;
  background: var(--thm-green-700);
  opacity: 0;
}

.aktiv .lauf-punkt { opacity: 1; }

.lauf-nachricht {
  font-size: 0.82em;
  font-weight: var(--fw-semibold);
  line-height: 1.25;
  color: var(--thm-grey-400);
  transition: color 0.3s ease;
}

.aktiv > .lauf-nachricht,
.aktiv > .lauf-wechsel-enter-active {
  color: var(--text-strong);
}

/* ---- Waagrecht ---- */

.waagrecht {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.waagrecht.seite-unten { flex-direction: column-reverse; }

.waagrecht .lauf-linie { height: 2px; margin: 0 0.4rem; }
.waagrecht .lauf-punkt { top: 50%; margin-top: calc(var(--punkt) / -2); }

.rechts .lauf-linie::after { right: -0.4rem; top: -0.38rem; border-right: 0; border-left-width: 0.55rem; border-left-color: var(--thm-grey-300); }
.links .lauf-linie::after { left: -0.4rem; top: -0.38rem; border-left: 0; border-right-width: 0.55rem; border-right-color: var(--thm-grey-300); }
.rechts.aktiv .lauf-linie::after { border-left-color: var(--thm-green-500); }
.links.aktiv .lauf-linie::after { border-right-color: var(--thm-green-500); }

.rechts.aktiv .lauf-punkt { animation: lauf-rechts 1.4s ease-in-out infinite; }
.links.aktiv .lauf-punkt { animation: lauf-links 1.4s ease-in-out infinite; }

@keyframes lauf-rechts {
  from { left: 0; }
  to { left: calc(100% - var(--punkt)); }
}

@keyframes lauf-links {
  from { left: calc(100% - var(--punkt)); }
  to { left: 0; }
}

/* Platz für `zeilen` Zeilen, damit beim Wechsel nichts springt */
.waagrecht .lauf-nachricht {
  min-height: calc(var(--zeilen) * 1.25em);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 0.35rem;
  text-align: center;
}

.waagrecht.seite-unten .lauf-nachricht { align-items: flex-start; }

/* ---- Senkrecht ---- */

.senkrecht {
  position: relative;
  display: flex;
  justify-content: center;
  width: 1rem;
  height: 3rem;
}

.senkrecht .lauf-linie { width: 2px; height: calc(100% - 0.45rem); }
.runter .lauf-linie { margin-bottom: auto; }
.hoch .lauf-linie { margin-top: auto; }
.senkrecht .lauf-punkt { left: 50%; margin-left: calc(var(--punkt) / -2); }

.runter .lauf-linie::after { bottom: -0.45rem; left: -0.38rem; border-bottom: 0; border-top-width: 0.55rem; border-top-color: var(--thm-grey-300); }
.hoch .lauf-linie::after { top: -0.45rem; left: -0.38rem; border-top: 0; border-bottom-width: 0.55rem; border-bottom-color: var(--thm-grey-300); }
.runter.aktiv .lauf-linie::after { border-top-color: var(--thm-green-500); }
.hoch.aktiv .lauf-linie::after { border-bottom-color: var(--thm-green-500); }

.runter.aktiv .lauf-punkt { animation: lauf-runter 1.4s ease-in-out infinite; }
.hoch.aktiv .lauf-punkt { animation: lauf-hoch 1.4s ease-in-out infinite; }

@keyframes lauf-runter {
  from { top: 0; }
  to { top: calc(100% - var(--punkt)); }
}

@keyframes lauf-hoch {
  from { top: calc(100% - var(--punkt)); }
  to { top: 0; }
}

/* Die Nachricht steht neben dem Pfeil */
.senkrecht .lauf-nachricht {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: max-content;
  max-width: 13rem;
}

.senkrecht.seite-links .lauf-nachricht { right: 1.4rem; text-align: right; }
.senkrecht.seite-rechts .lauf-nachricht { left: 1.4rem; text-align: left; }

/* ---- Wechsel einer Nachricht ---- */

.lauf-wechsel-enter-active,
.lauf-wechsel-leave-active { transition: opacity 0.2s ease; }

.lauf-wechsel-enter-from,
.lauf-wechsel-leave-to { opacity: 0; }
</style>
