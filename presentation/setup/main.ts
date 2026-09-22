/*
  Die Demos sind Abzweige von der Übersichtsfolie (routeAlias `demos`),
  keine Folge. Beim Blättern Folie für Folie gilt deshalb:

  - Vorwärts über das Ende einer Demo hinaus geht es nicht in die nächste
    Demo, sondern weiter im gemeinsamen Strang (routeAlias `nach-demos`).
  - Rückwärts aus einer Demo heraus — oder von `nach-demos` zurück in eine
    Demo — geht es zur Übersicht.

  Sprünge über Links oder `G` bleiben unberührt — außer ihr Ziel ist
  zufällig die Nachbarfolie: Der Router sieht nur Start und Ziel, nicht,
  wie der Wechsel ausgelöst wurde. Welche Demo eine Folie
  gehört, steht in ihrem Frontmatter als `demo:` (gesetzt am `src:`-Eintrag
  in slides.md). Gilt für Publikums- und Moderatoransicht, nicht für
  Übersicht und Export.
*/
import { defineAppSetup } from '@slidev/types'
import { slides } from '#slidev/slides'

function demoVon(no: number): string | undefined {
  return slides.value.find(s => s.no === no)?.meta.slide?.frontmatter.demo
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

    const nach = nummer(to.params.no)
    const von = nummer(from.params.no)
    if (nach === undefined || von === undefined || Math.abs(nach - von) !== 1)
      return true

    const demoVorher = demoVon(von)
    const demoNachher = demoVon(nach)
    if (demoVorher === demoNachher)
      return true

    let ziel: number | undefined
    if (nach > von && demoVorher)
      ziel = folieMitAlias('nach-demos')
    else if (nach < von && demoNachher)
      ziel = folieMitAlias('demos')

    if (ziel === undefined || ziel === nach)
      return true

    return {
      name: to.name,
      params: { ...to.params, no: String(ziel) },
      query: { ...to.query, clicks: undefined },
    }
  })
})
