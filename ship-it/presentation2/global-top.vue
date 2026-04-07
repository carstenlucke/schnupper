<script setup>
import { ref } from 'vue'

const showToc = ref(false)

function toggle() {
  showToc.value = !showToc.value
}
</script>

<template>
  <Teleport to="body">
    <button
      class="toc-btn"
      @click="toggle"
      :aria-label="showToc ? 'Gliederung ausblenden' : 'Gliederung einblenden'"
      :title="showToc ? 'Gliederung ausblenden' : 'Gliederung einblenden'"
    >
      <i class="fa-solid" :class="showToc ? 'fa-xmark' : 'fa-list'"></i>
    </button>
    <Transition name="toc-slide">
      <aside v-if="showToc" class="toc-overlay" @click.self="toggle">
        <div class="toc-panel">
          <h3>Gliederung</h3>
          <Toc />
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<style>
/* Slidev Goto-Dialog: Position korrigieren.
   Original nutzt -top-20 (nur -80px) zum Verstecken, das reicht bei manchen
   Aufloesungen nicht. Wir verschieben ihn weiter raus und setzen die offene
   Position auf top: 20px, damit Suchfeld + Slide 1 sichtbar sind. */
#slidev-goto-dialog {
  top: -100vh !important;
  transition: top 0.3s ease !important;
}
#slidev-goto-dialog.top-5 {
  top: 20px !important;
}

.toc-btn {
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 9999;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  background: #4A5C66;
  color: #fff;
  border: 2px solid rgba(255,255,255,0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  opacity: 0.5;
  transition: opacity 0.2s, background 0.2s;
}

.toc-btn:hover {
  opacity: 1;
  background: #80BA24;
  border-color: #80BA24;
}

.toc-btn .fa-solid {
  color: inherit;
  margin: 0;
}

.toc-overlay {
  position: fixed;
  inset: 0;
  z-index: 9998;
  display: flex;
  justify-content: flex-end;
  background: rgba(0, 0, 0, 0.3);
}

.toc-panel {
  width: 280px;
  height: 100%;
  background: #4A5C66;
  padding: 24px 20px;
  overflow-y: auto;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.25);
}

.toc-panel h3 {
  color: #80BA24;
  font-size: 12px;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.toc-panel .slidev-toc ol,
.toc-panel .slidev-toc ul {
  list-style: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

.toc-panel .slidev-toc li {
  margin: 0 !important;
  padding: 0 !important;
}

.toc-panel .slidev-toc li::before {
  display: none !important;
}

.toc-panel .slidev-toc a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 13px;
  display: block;
  padding: 7px 12px;
  border-left: 3px solid transparent;
  border-radius: 0 4px 4px 0;
  transition: all 0.15s;
  font-family: Arial, Helvetica, sans-serif;
}

.toc-panel .slidev-toc a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.06);
  border-left-color: rgba(255, 255, 255, 0.3);
}

.toc-panel .slidev-toc .slidev-toc-item-active > a {
  color: #80BA24;
  border-left-color: #80BA24;
  background: rgba(128, 186, 36, 0.08);
  font-weight: bold;
}

/* Transition */
.toc-slide-enter-active {
  transition: opacity 0.25s ease;
}
.toc-slide-enter-active .toc-panel {
  transition: transform 0.25s ease;
}
.toc-slide-leave-active {
  transition: opacity 0.2s ease;
}
.toc-slide-leave-active .toc-panel {
  transition: transform 0.2s ease;
}
.toc-slide-enter-from,
.toc-slide-leave-to {
  opacity: 0;
}
.toc-slide-enter-from .toc-panel,
.toc-slide-leave-to .toc-panel {
  transform: translateX(100%);
}
</style>
