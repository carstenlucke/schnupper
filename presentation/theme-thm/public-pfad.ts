/*
  Pfade auf Dateien in public/ („/bild.jpg“) um den Basispfad des Builds
  ergänzen — auf GitHub Pages liegt die Präsentation unter /schnupper/.
  Vite ergänzt ihn nur in fest notierten <img src="…">, nicht in Props wie
  `bild` oder `foto`. Im Dev-Server ist der Basispfad „/“, dort ändert sich
  nichts. Externe URLs bleiben unverändert.
*/
export function publicPfad(pfad: string): string {
  if (!pfad.startsWith('/') || pfad.startsWith('//')) return pfad
  return import.meta.env.BASE_URL + pfad.slice(1)
}
