/*
  Die Demos sind Abzweige von der Übersichtsfolie (routeAlias `demos`),
  keine Folge. Beim Blättern Folie für Folie gilt deshalb:

  - Vorwärts über das Ende einer Demo hinaus geht es nicht in die nächste
    Demo, sondern weiter im gemeinsamen Strang (routeAlias `nach-demos`).
  - Rückwärts aus einer Demo heraus — oder von `nach-demos` zurück in eine
    Demo — geht es zur Übersicht.

  Zusatzfolien (Frontmatter `zusatz: <routeAlias der Herkunftsfolie>`)
  liegen außerhalb des Verlaufs: Beim Blättern werden sie übersprungen,
  erreichbar sind sie nur per Link (<Abstecher>). Von einer Zusatzfolie
  aus führt ← zurück zur Herkunftsfolie und → zu deren Nachfolgerin.

  Sprünge über Links oder `G` bleiben unberührt — außer ihr Ziel ist
  zufällig die Nachbarfolie: Der Router sieht nur Start und Ziel, nicht,
  wie der Wechsel ausgelöst wurde. Zu welcher Demo eine Folie gehört, steht
  in ihrem Frontmatter als `demo:` (gesetzt am `src:`-Eintrag in slides.md).
  Gilt für Publikums- und Moderatoransicht, nicht für Übersicht und Export.
*/
import { defineAppSetup } from '@slidev/types'
import { slides } from '#slidev/slides'

function frontmatter(no: number): Record<string, any> | undefined {
  return slides.value.find(s => s.no === no)?.meta.slide?.frontmatter
}

function demoVon(no: number): string | undefined {
  return frontmatter(no)?.demo
}

function folieMitAlias(alias: string): number | undefined {
  return slides.value.find(s => s.meta.slide?.frontmatter.routeAlias === alias)?.no
}

/* Nach einem Sprung per Link steht in der Route der Alias, nicht die Nummer. */
function nummer(param: unknown): number | undefined {
  if (typeof param !== 'string')
    return undefined
  return /^\d+$/.test(param) ? Number(param) : folieMitAlias(param)
}

export default defineAppSetup(({ router }) => {
  router.beforeEach((to, from) => {
    if (to.name !== 'play' && to.name !== 'presenter')
      return true

    const angefragt = nummer(to.params.no)
    const von = nummer(from.params.no)
    if (angefragt === undefined || von === undefined || Math.abs(angefragt - von) !== 1)
      return true
    const schritt = angefragt - von

    let ziel: number | undefined
    const herkunft = frontmatter(von)?.zusatz
    if (herkunft) {
      const h = folieMitAlias(herkunft)
      ziel = h === undefined ? undefined : schritt < 0 ? h : h + 1
    }
    else {
      let nach = angefragt
      while (frontmatter(nach)?.zusatz)
        nach += schritt
      ziel = nach

      const demoVorher = demoVon(von)
      const demoNachher = demoVon(nach)
      if (demoVorher !== demoNachher) {
        if (schritt > 0 && demoVorher)
          ziel = folieMitAlias('nach-demos') ?? nach
        else if (schritt < 0 && demoNachher)
          ziel = folieMitAlias('demos') ?? nach
      }
    }

    if (ziel === undefined || ziel === angefragt)
      return true

    return {
      name: to.name,
      params: { ...to.params, no: String(ziel) },
      query: { ...to.query, clicks: undefined },
    }
  })
})
