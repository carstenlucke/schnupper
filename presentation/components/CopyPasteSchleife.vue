<!--
  Der Alltag mit einem Chatbot als Bild: links das Chatfenster, rechts
  euer Dokument, dazwischen ihr. Ihr tragt den Text hinüber, holt die
  Antwort zurück — und fangt beim nächsten Absatz von vorne an. Der
  Chatbot sieht dabei nur den Schnipsel, den ihr ihm gebt.

  Idee aus dem TecDay-Vortrag (Folie „Copy/Paste-Frustration“), dort mit
  Code und Editor; hier mit einem Referat, damit es ohne
  Programmiererfahrung trägt. Fenster und Pfeile sind HTML, damit Schrift
  und Farben im CD bleiben.
-->
<template>
  <div class="cp">
    <div class="cp-fenster">
      <div class="cp-leiste"><span /><span /><span /><b>ChatGPT</b></div>
      <div class="cp-chat">
        <div class="cp-blase ich">Mach diesen Absatz besser: <em>„Der Klimawandel ist …“</em></div>
        <div class="cp-blase ki">Gern! Hier ist eine verbesserte Fassung:&nbsp;…</div>
        <div class="cp-eingabe" />
      </div>
    </div>

    <div class="cp-mitte">
      <div class="cp-weg">
        <span class="cp-schritt"><ThmIcon name="clipboard-paste" :size="0.95" /> Absatz reinkopieren</span>
        <span class="cp-pfeil links"><ThmIcon name="arrow-left" :size="1.5" /></span>
      </div>
      <div class="cp-ich">
        <ThmIcon name="user" box :size="3" />
        <span>Ihr</span>
      </div>
      <div class="cp-weg">
        <span class="cp-pfeil"><ThmIcon name="arrow-right" :size="1.5" /></span>
        <span class="cp-schritt"><ThmIcon name="clipboard-paste" :size="0.95" /> Antwort rauskopieren</span>
      </div>
    </div>

    <div class="cp-fenster">
      <div class="cp-leiste"><span /><span /><span /><b>Referat.docx</b></div>
      <div class="cp-dok">
        <div class="cp-zeile titel" />
        <div class="cp-zeile" />
        <div class="cp-zeile kurz" />
        <div class="cp-zeile markiert" />
        <div class="cp-zeile markiert kurz" />
        <div class="cp-zeile" />
        <div class="cp-zeile" />
        <div class="cp-zeile kurz" />
      </div>
    </div>

    <div class="cp-wieder">
      <ThmIcon name="refresh-cw" :size="1" />
      Nächster Absatz — und alles wieder von vorn
    </div>
  </div>
</template>

<style scoped>
.cp {
  display: grid;
  grid-template-columns: 1fr 13rem 1fr;
  grid-template-rows: auto auto;
  column-gap: 1.2rem;
  row-gap: 0.9rem;
  align-items: center;
}

.cp-fenster {
  background: var(--white);
  border: 1px solid var(--thm-grey-200);
  box-shadow: 0 0.4rem 1.2rem rgba(34, 44, 49, 0.08);
  height: 12.5rem;
  display: flex;
  flex-direction: column;
}

.cp-leiste {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.45rem 0.7rem;
  background: var(--thm-grey-50);
  border-bottom: 1px solid var(--thm-grey-200);
  font-size: 0.72rem;
}

.cp-leiste span {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: var(--thm-grey-200);
}

.cp-leiste b {
  margin-left: 0.5rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-600);
}

.cp-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.8rem;
  font-size: 0.78rem;
  line-height: 1.35;
}

.cp-blase {
  max-width: 85%;
  padding: 0.45rem 0.65rem;
  color: var(--text-strong);
}

.cp-blase.ich {
  align-self: flex-end;
  background: var(--thm-grey-100);
}

.cp-blase.ki {
  align-self: flex-start;
  background: var(--thm-green-50);
  border-left: 0.2rem solid var(--thm-green-500);
}

.cp-eingabe {
  margin-top: auto;
  height: 1.3rem;
  border: 1px solid var(--thm-grey-200);
}

.cp-dok {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  padding: 0.9rem 1rem;
}

.cp-zeile {
  height: 0.45rem;
  background: var(--thm-grey-200);
}

.cp-zeile.kurz { width: 65%; }
.cp-zeile.titel { width: 45%; height: 0.7rem; background: var(--thm-grey-400); margin-bottom: 0.2rem; }
.cp-zeile.markiert { background: var(--thm-green-300); }

.cp-mitte {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.9rem;
}

.cp-weg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
}

.cp-schritt {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.78rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-600);
  white-space: nowrap;
}

.cp-pfeil {
  display: flex;
  width: 100%;
  justify-content: center;
  color: var(--thm-green-500);
}

.cp-ich {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  font-weight: var(--fw-bold);
  color: var(--text-strong);
}

.cp-wieder {
  grid-column: 1 / -1;
  justify-self: center;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.85rem;
  font-weight: var(--fw-semibold);
  color: var(--thm-grey-500);
}
</style>
