// Motion tokens — docs/spec/ui-redesign.md row 18 (v2). Every animation in the app uses these.
// Nothing non-looping may run longer than 1200 ms; the only loops are the spinner and the diagram.
export const ease = {
  ui: [0.2, 0.8, 0.2, 1],
  entrance: [0.22, 1, 0.36, 1],
  camera: [0.65, 0, 0.35, 1],
}
export const ms = {
  press: 90, hoverIn: 150, hoverOut: 120, menu: 200, indicator: 240,
  routeOut: 120, routeIn: 240, drawer: 320, connector: 480, countRoll: 600,
  camera: 1200, dotFade: 200, ring: 420, dropBudget: 1200, phoneDropBudget: 600,
  checksStagger: 50, checksBudget: 700, stamp: 180, autoAdvance: 240, copyHold: 1600,
  diagramCycle: 3200, max: 1200,
}
export const spring = { type: 'spring', bounce: 0, duration: ms.drawer / 1000 }
export const t = (name, easeName = 'ui') => ({ duration: ms[name] / 1000, ease: ease[easeName] })
