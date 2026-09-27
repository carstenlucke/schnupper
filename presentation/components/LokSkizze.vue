<!--
  Eine Dampflok, mit Bleistift auf kariertes Papier gekritzelt — der Anhang
  zum Satz „Mach aus meiner Skizze ein 3D-Modell“ auf „Vom Code zur
  Sprache“. Sie soll aussehen wie schnell hingezeichnet, nicht wie eine
  Konstruktionszeichnung.

  Die Linien sind sauber gezeichnet; das Zittern des Strichs macht ein
  SVG-Filter (Rauschen verschiebt die Pixel ein wenig). Farben aus den
  Tokens, damit die Skizze im CD bleibt.
-->
<template>
  <svg class="lok" viewBox="0 0 160 96" role="img" aria-label="Skizze einer Dampflok">
    <defs>
      <pattern id="lok-karo" width="8" height="8" patternUnits="userSpaceOnUse">
        <path d="M8 0H0V8" class="lok-karo" />
      </pattern>
      <filter id="lok-strich" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="3" />
        <feDisplacementMap in="SourceGraphic" scale="2.2" />
      </filter>
    </defs>

    <rect width="160" height="96" fill="url(#lok-karo)" />

    <g class="lok-strich" filter="url(#lok-strich)">
      <!-- Führerhaus mit Dach und Fenster -->
      <path d="M14 64V22H40V64" />
      <path d="M9 22H45" />
      <path d="M19 29H33V40H19Z" />
      <!-- Kessel -->
      <path d="M40 38H104Q113 38 113 51Q113 64 104 64H40" />
      <!-- Dampfdom und Schornstein -->
      <path d="M62 38Q68 28 74 38" />
      <path d="M92 38V22M101 38V22M89 22H104" />
      <!-- Rahmen und Schienenräumer -->
      <path d="M10 64H116" />
      <path d="M113 64L124 82H112" />
      <!-- Räder mit Kuppelstange -->
      <circle cx="34" cy="74" r="10" />
      <circle cx="62" cy="74" r="10" />
      <circle cx="90" cy="74" r="10" />
      <circle cx="108" cy="78" r="5.5" />
      <path d="M34 74H90" />
      <!-- Schiene -->
      <path d="M4 85H156" />
      <!-- Rauch -->
      <path d="M97 18Q92 10 99 8Q103 1 111 5Q118 -1 125 5Q134 3 134 11Q140 17 131 19" />
    </g>
  </svg>
</template>

<style scoped>
.lok {
  display: block;
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
}

.lok-karo {
  fill: none;
  stroke: var(--thm-cyan);
  stroke-width: 0.35;
  opacity: 0.35;
}

.lok-strich {
  fill: none;
  stroke: var(--thm-grey-600);
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>
