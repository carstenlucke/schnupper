<template>
  <div />
</template>

<style>
/* Slidev Goto-Dialog: Position korrigieren.
   Original nutzt -top-20 (nur -80px) zum Verstecken, das reicht bei manchen
   Auflösungen nicht. Wir verschieben ihn weiter raus und setzen die offene
   Position auf top: 20px, damit Suchfeld + Slide 1 sichtbar sind. */
#slidev-goto-dialog {
  top: -100vh !important;
  transition: top 0.3s ease !important;
}
#slidev-goto-dialog.top-5 {
  top: 20px !important;
}
</style>
