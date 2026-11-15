<!--
  Wie ein Sprachmodell schreibt, als Bild: ein angefangener Satz und die
  Wörter, die als Nächstes infrage kommen, mit ihrer Wahrscheinlichkeit.
  Das Modell nimmt eines davon, hängt es an und macht weiter — Wort für
  Wort.

  Die Zahlen sind ausgedacht und nur zur Anschauung; sie summieren sich
  nicht auf 100 %, weil der Rest auf viele seltene Wörter entfällt.

  Mit `token` in der Fachsprache: der Satz in Tokens zerlegt, über der
  Liste P(nächstes Token | Text davor) und der Hinweis, dass die Werte
  ausgedacht sind. Vereinfacht ist dabei ein Wort ein Token; „Wort = Token“
  trägt `data-info="tokens"`, eine `<InfoTafel wort="tokens">` auf der Folie
  kann dort die echte Zerlegung zeigen.
-->
<script setup lang="ts">
defineProps<{ token?: boolean }>()

const anfang = 'Nach der Vorlesung gehe ich noch schnell zum'
const woerter = [
  { wort: 'Bäcker', p: 34 },
  { wort: 'Training', p: 22 },
  { wort: 'Supermarkt', p: 17 },
  { wort: 'Arzt', p: 9 },
  { wort: 'Mond', p: 0.01 },
]
/* Das letzte Wort bleibt mit der Lücke auf einer Zeile */
const tokens = anfang.split(' ')
const vorne = anfang.slice(0, anfang.lastIndexOf(' '))
const letztes = anfang.slice(anfang.lastIndexOf(' ') + 1)
const max = Math.max(...woerter.map(w => w.p))
const prozent = (p: number) => (p < 1 ? '< 1 %' : `${p} %`)
</script>

<template>
  <div class="nw">
    <div v-if="token" class="nw-satz nw-tokens">
      <span v-for="(t, i) in tokens.slice(0, -1)" :key="i" class="nw-token">{{ t }}</span>
      <span class="nw-ende"><span class="nw-token">{{ tokens.at(-1) }}</span><span class="nw-luecke">…</span></span>
    </div>
    <div v-else class="nw-satz">
      {{ vorne }} <span class="nw-ende">{{ letztes }} <span class="nw-luecke">…</span></span>
    </div>
    <div v-if="token" class="nw-formel">
      <span><i>P</i>( nächstes Token <span class="nw-strich">|</span> Text davor )</span>
      <span class="nw-hinweis"><span data-info="tokens">Wort = Token</span> · Werte ausgedacht</span>
    </div>
    <div class="nw-liste">
      <div v-for="(w, i) in woerter" :key="w.wort" class="nw-zeile" :class="{ erstes: i === 0 }">
        <span class="nw-wort">{{ w.wort }}</span>
        <span class="nw-balken"><span :style="{ width: `${Math.max((w.p / max) * 100, 1.5)}%` }" /></span>
        <span class="nw-p">{{ prozent(w.p) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nw {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
  padding: 1.1rem 1.3rem;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
}

.nw-satz {
  font-size: 1.05em;
  font-weight: var(--fw-semibold);
  line-height: 1.35;
  color: var(--text-strong);
}

.nw-ende { white-space: nowrap; }

/* Tokens wie in einem Tokenizer-Werkzeug: abwechselnd hinterlegt */
.nw-tokens {
  display: flex;
  flex-wrap: wrap;
  row-gap: 0.3rem;
}

.nw-token {
  padding: 0 0.15rem;
  background: var(--thm-green-100);
}

.nw-token:nth-child(even),
.nw-ende .nw-token { background: var(--thm-grey-100); }

.nw-tokens .nw-luecke { margin-left: 0.35rem; }

.nw-formel {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.8rem;
  white-space: nowrap;
  font-size: 0.8em;
  color: var(--thm-grey-500);
}

.nw-formel i {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 1.15em;
  color: var(--text-strong);
}

.nw-strich { margin: 0 0.2rem; }

.nw-hinweis {
  font-size: 0.8em;
  color: var(--thm-grey-400);
}

.nw-luecke {
  display: inline-block;
  min-width: 3.5em;
  border-bottom: 0.15rem solid var(--thm-green-500);
  color: var(--thm-green-600);
}

.nw-liste {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.nw-zeile {
  display: grid;
  grid-template-columns: 6.5em 1fr 3.4em;
  align-items: center;
  gap: 0.7rem;
  font-size: 0.85em;
  color: var(--thm-grey-600);
}

.nw-balken {
  height: 0.7em;
  background: var(--thm-grey-50);
}

.nw-balken span {
  display: block;
  height: 100%;
  background: var(--thm-grey-300);
}

.nw-p {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.nw-zeile.erstes {
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.nw-zeile.erstes .nw-balken span { background: var(--thm-green-500); }
</style>
