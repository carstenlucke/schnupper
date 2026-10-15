/*
  Die Bausteine des Harness an einer Stelle: <AgentAnatomie> stellt sie
  vor, <AgentDurchlauf> zeigt sie bei der Arbeit, <GrosserAuftrag> färbt
  seine Runden nach den Werkzeugen. Die Folien laufen kurz nacheinander
  und müssen dieselben Icons und Namen zeigen. Den Text unter dem Namen
  setzt jede Komponente selbst.
*/

export const werkzeuge = [
  { id: 'lesen', icon: 'eye', text: 'Dateien lesen' },
  { id: 'schreiben', icon: 'pen-line', text: 'Dateien schreiben' },
  { id: 'starten', icon: 'square-terminal', text: 'Programme starten' },
  { id: 'web', icon: 'globe', text: 'Im Web suchen' },
]

export const steuerung = {
  schleife: { icon: 'refresh-cw', name: 'Schleife' },
  anweisungen: { icon: 'file-text', name: 'Anweisungen' },
  verlauf: { icon: 'notebook-pen', name: 'Verlauf' },
  leitplanken: { icon: 'shield-check', name: 'Leitplanken' },
}
