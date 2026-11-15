<!--
  Infotafel, die sich über die Folie legt — für eine Begriffserklärung, die
  nicht dauerhaft auf der Folie stehen soll. Geöffnet wird sie über ein
  Wort im Folientext:

    … in Tokens <button type="button" data-info="tokens">zerlegt</button> …

    <InfoTafel wort="tokens" titel="Tokens in Wirklichkeit">

    Text der Tafel.

    </InfoTafel>

  Das Wort kann auch in einer Komponente stehen (so „Wort = Token“ in
  <NaechstesWort token>); es muss nur auf derselben Folie liegen. Ein
  `<span data-info>` funktioniert mit der Maus ebenso, der Knopf lässt sich
  zusätzlich mit Tab und Enter bedienen.

  Ein Klick auf das Wort öffnet die Tafel, ein Klick auf die Tafel, erneut
  auf das Wort oder Escape schließt sie; beim Verlassen der Folie schließt
  sie von selbst. Die Folie scheint blass durch. Referentenansicht und
  Publikumsfenster öffnen und schließen die Tafel gemeinsam (über einen
  BroadcastChannel, also im selben Browser) — Slidev selbst gleicht nur
  Folie und Klicks ab. Im Export erscheint die Tafel
  nicht, und das Wort steht dort als gewöhnlicher Text — der Inhalt gehört
  deshalb auch in die Foliennotiz.

  Das Aussehen des Worts (`.info-wort`) steht in `styles/slides.css`, weil
  es auch in Text anderer Komponenten greifen muss.

  Übernommen aus dem Theme der Softwaretechnik-Vorlesung, dort zusätzlich
  mit eigener Schaltfläche (`knopf`) und eingebettet in Abbildungen; hier
  nur der Auslöser über ein Wort.
-->
<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { onSlideLeave, useNav, useSlideContext } from '@slidev/client'

const props = defineProps<{ titel: string; wort: string }>()

const { isPrintMode } = useNav()
const { $page } = useSlideContext()
const offen = ref(false)
const anker = ref<HTMLElement>()

onSlideLeave(() => { offen.value = false })

/* Auslösewörter derselben Folie — in der Referentenansicht steht die Folie
   mehrfach im Dokument, jede Tafel hört nur auf ihre eigene. */
const folie = () => anker.value?.closest('.slidev-layout')
const woerter = () => [...(folie()?.querySelectorAll<HTMLElement>(`[data-info="${props.wort}"]`) ?? [])]

function aufKlick(e: MouseEvent) {
  const ziel = (e.target as HTMLElement).closest?.(`[data-info="${props.wort}"]`)
  if (!ziel || ziel.closest('.slidev-layout') !== folie()) return
  e.stopPropagation()
  offen.value = !offen.value
  /* Nach einem Mausklick den Fokus abgeben, sonst blättert die Leertaste
     nicht weiter; mit der Tastatur geöffnet (detail 0) bleibt er stehen. */
  if (e.detail > 0) (ziel as HTMLElement).blur?.()
}

function taste(e: KeyboardEvent) {
  if (e.key === 'Escape') offen.value = false
}

/* Gleichlauf mit den anderen Fenstern derselben Präsentation. Jede
   Nachricht trägt Folie und Wort; eine Tafel übernimmt nur ihre eigene.
   Eine Tafel, die neu erscheint, fragt nach dem aktuellen Stand. */
interface Nachricht { seite: number; wort: string; offen?: boolean; frage?: boolean }
let kanal: BroadcastChannel | undefined
let empfangen = false

function senden(n: Partial<Nachricht>) {
  kanal?.postMessage({ seite: $page.value, wort: props.wort, ...n })
}

function aufNachricht({ data: n }: MessageEvent<Nachricht>) {
  if (n.seite !== $page.value || n.wort !== props.wort) return
  if (n.frage) {
    if (offen.value) senden({ offen: true })
  }
  else if (n.offen !== undefined && n.offen !== offen.value) {
    empfangen = true
    offen.value = n.offen
  }
}

/* Erscheint das Wort erst nach der Tafel oder setzt eine Komponente ihren
   Inhalt neu, trägt der Beobachter die Auszeichnung nach. */
function auszeichnen() {
  woerter().forEach((w) => {
    w.classList.add('info-wort')
    w.classList.toggle('aktiv', offen.value)
    w.title = props.titel
  })
}
const beobachter = new MutationObserver(auszeichnen)

onMounted(() => {
  if (isPrintMode.value) return
  auszeichnen()
  const f = folie()
  if (f) beobachter.observe(f, { childList: true, subtree: true })
  document.addEventListener('click', aufKlick, true)
  kanal = new BroadcastChannel('thm-infotafel')
  kanal.addEventListener('message', aufNachricht)
  senden({ frage: true })
})
onBeforeUnmount(() => {
  beobachter.disconnect()
  document.removeEventListener('click', aufKlick, true)
  window.removeEventListener('keydown', taste)
  kanal?.close()
})
watch(offen, (o) => {
  auszeichnen()
  if (o) window.addEventListener('keydown', taste)
  else window.removeEventListener('keydown', taste)
  /* Was von einem anderen Fenster kam, nicht zurückschicken */
  if (empfangen) empfangen = false
  else senden({ offen: o })
})
</script>

<template>
  <span ref="anker" hidden />
  <div v-if="!isPrintMode && offen" class="info-tafel" @click.stop="offen = false">
    <div class="info-tafel-blatt">
      <div class="info-tafel-kopf">
        <ThmIcon name="info" box :size="1.7" />{{ titel }}<ThmIcon name="x" ton="grau" :size="1.1" class="info-tafel-zu" />
      </div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
/* Liegt über der Folie, die blass durchscheint; die Fußzeile bleibt frei */
.info-tafel {
  position: absolute;
  inset: 0 0 var(--footer-h) 0;
  display: grid;
  place-items: center;
  background: color-mix(in srgb, var(--white) 78%, transparent);
  cursor: pointer;
  z-index: 20;
}

.info-tafel-blatt {
  width: 66%;
  padding: 1.1rem 1.4rem 1.2rem;
  background: var(--white);
  border-left: 0.3rem solid var(--thm-green-500);
  box-shadow: 0 0.5rem 2rem color-mix(in srgb, var(--thm-grey-900) 22%, transparent);
  color: var(--text-body);
  font-size: 0.98rem;
  line-height: var(--lh-snug);
}

.info-tafel-blatt :deep(p) { margin: 0 0 0.7rem; }
.info-tafel-blatt :deep(p:last-child) { margin-bottom: 0; }

.info-tafel-kopf {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.8rem;
  color: var(--text-strong);
  font-size: 1.15rem;
  font-weight: var(--fw-bold);
}

.info-tafel-zu { margin-left: auto; }
</style>
