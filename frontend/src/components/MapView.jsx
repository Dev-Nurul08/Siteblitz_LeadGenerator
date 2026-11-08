// Live business map — spec row 25 + Find signature "Businesses land on the map".
// Lazy-loaded (maplibre is the heaviest dependency). One map instance; removed on unmount.
import { useEffect, useRef, useState } from 'react'
import { Map as MapLibreMap, setWorkerUrl } from 'maplibre-gl'
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?url'
import 'maplibre-gl/dist/maplibre-gl.css'

// MapLibre v6 loads its worker as a separate module; Vite must be told its real URL.
setWorkerUrl(workerUrl)
import { useReducedMotion } from 'motion/react'
import { MapPinOff } from 'lucide-react'
import { StateBlock } from './ui'
import { ms } from '../motion'

const STYLE_URL = 'https://tiles.openfreemap.org/styles/dark'

const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim()
const DOT = { lead: '--dot-lead', review: '--dot-review', notlead: '--dot-notlead', unchecked: '--dot-unchecked' }
const VERDICT_DOT = {
  NO_SITE_VERIFIED: 'lead', SOCIAL_ONLY_VERIFIED: 'lead', SITE_DOWN_CONFIRMED: 'lead',
  UNKNOWN: 'review', OWN_SITE_VERIFIED: 'notlead', SKIP: 'notlead', UNCHECKED: 'unchecked',
}

// cubic-bezier(.65,0,.35,1) — the camera-travel curve (spec row 18).
function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by
  const sx = (u) => ((ax * u + bx) * u + cx) * u
  const sy = (u) => ((ay * u + by) * u + cy) * u
  return (x) => {
    let u = x
    for (let i = 0; i < 8; i++) {
      const d = 3 * ax * u * u + 2 * bx * u + cx
      if (Math.abs(d) < 1e-6) break
      u -= (sx(u) - x) / d
    }
    return sy(Math.min(1, Math.max(0, u)))
  }
}
const cameraEase = bezier(0.65, 0, 0.35, 1)

const toFeatures = (points, extra = () => ({})) => ({
  type: 'FeatureCollection',
  features: points.filter((p) => p.lat !== null && p.lon !== null).map((p) => ({
    type: 'Feature',
    id: p.id,
    geometry: { type: 'Point', coordinates: [p.lon, p.lat] },
    properties: { id: p.id, name: p.name, dot: VERDICT_DOT[p.verdict] || 'unchecked', ...extra(p) },
  })),
})

export default function MapView({ points, animate = true, onSelect, height }) {
  const box = useRef(null)
  const mapRef = useRef(null)
  const seen = useRef(new Set())
  const raf = useRef(0)
  const [ready, setReady] = useState(false)
  const [failed, setFailed] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const reduce = useReducedMotion()
  const onSelectRef = useRef(onSelect)
  onSelectRef.current = onSelect

  useEffect(() => {
    setFailed(false)
    setReady(false)
    seen.current = new Set()
    const map = new MapLibreMap({
      container: box.current, style: STYLE_URL, center: [78.9, 22.5], zoom: 3.6,
      dragRotate: false, pitchWithRotate: false, touchPitch: false, attributionControl: { compact: false,
        customAttribution: 'Businesses: Overture Maps Foundation · © OpenStreetMap contributors' },
    })
    map.touchZoomRotate.disableRotation()
    mapRef.current = map
    if (import.meta.env.DEV) window.__sbMap = map // lets the screenshot checks inspect layers
    const colorExpr = ['match', ['get', 'dot'],
      'lead', css(DOT.lead), 'review', css(DOT.review), 'notlead', css(DOT.notlead), css(DOT.unchecked)]
    map.on('error', (e) => { if (!map.isStyleLoaded() || /style|tile/i.test(String(e?.error?.message))) setFailed(true) })
    map.on('load', () => {
      // Page-coloured ground (spec row 25): background and land fills take --map-land.
      for (const layer of map.getStyle().layers) {
        if (layer.type === 'background') map.setPaintProperty(layer.id, 'background-color', css('--map-land'))
        if (layer.type === 'fill' && /land|park|wood|grass/i.test(layer.id)) map.setPaintProperty(layer.id, 'fill-color', css('--map-land'))
      }
      map.addSource('biz', { type: 'geojson', data: toFeatures([]), cluster: true, clusterMaxZoom: 12, clusterRadius: 40 })
      map.addLayer({ id: 'clusters', type: 'circle', source: 'biz', filter: ['has', 'point_count'],
        paint: { 'circle-color': css('--surface-3'), 'circle-stroke-color': css('--dot-unchecked'), 'circle-stroke-width': 1,
          'circle-radius': ['step', ['get', 'point_count'], 14, 25, 18, 100, 24] } })
      map.addLayer({ id: 'cluster-count', type: 'symbol', source: 'biz', filter: ['has', 'point_count'],
        layout: { 'text-field': ['get', 'point_count_abbreviated'], 'text-font': ['Noto Sans Regular'], 'text-size': 12 },
        paint: { 'text-color': css('--ink') } })
      map.addLayer({ id: 'dots', type: 'circle', source: 'biz', filter: ['!', ['has', 'point_count']],
        paint: { 'circle-color': colorExpr, 'circle-radius': 5, 'circle-stroke-color': css('--bg'), 'circle-stroke-width': 1 } })
      map.addSource('arrivals', { type: 'geojson', data: toFeatures([]) })
      map.addLayer({ id: 'arrival-dots', type: 'circle', source: 'arrivals', paint: { 'circle-color': colorExpr, 'circle-radius': 5, 'circle-opacity': 0 } })
      map.addLayer({ id: 'arrival-rings', type: 'circle', source: 'arrivals', paint: {
        'circle-color': 'rgba(0,0,0,0)', 'circle-stroke-color': css('--accent'), 'circle-stroke-width': 1.5,
        'circle-radius': 18, 'circle-stroke-opacity': 0 } })
      for (const id of ['dots', 'arrival-dots']) {
        map.on('click', id, (e) => onSelectRef.current && onSelectRef.current(e.features[0].properties.id))
        map.on('mouseenter', id, () => { map.getCanvas().style.cursor = 'pointer' })
        map.on('mouseleave', id, () => { map.getCanvas().style.cursor = '' })
      }
      map.on('click', 'clusters', (e) => map.easeTo({ center: e.features[0].geometry.coordinates, zoom: map.getZoom() + 2, duration: reduce ? 0 : ms.indicator }))
      setReady(true)
    })
    return () => { cancelAnimationFrame(raf.current); map.remove(); mapRef.current = null }
  }, [attempt]) // eslint-disable-line react-hooks/exhaustive-deps

  // New points land with a ring; known points recolour in place.
  useEffect(() => {
    const map = mapRef.current
    if (!ready || !map) return
    const withCoords = points.filter((p) => p.lat !== null && p.lon !== null)
    const fresh = withCoords.filter((p) => !seen.current.has(p.id))
    const known = withCoords.filter((p) => seen.current.has(p.id))
    fresh.forEach((p) => seen.current.add(p.id))

    if (fresh.length && seen.current.size === fresh.length) {
      const lons = withCoords.map((p) => p.lon), lats = withCoords.map((p) => p.lat)
      map.fitBounds([[Math.min(...lons), Math.min(...lats)], [Math.max(...lons), Math.max(...lats)]],
        { padding: 48, maxZoom: 14, duration: reduce ? 0 : ms.camera, easing: cameraEase })
    }
    if (!animate || reduce || !fresh.length) {
      map.getSource('biz').setData(toFeatures(withCoords))
      map.getSource('arrivals').setData(toFeatures([]))
      return
    }
    // Stagger = min(24 ms, budget ÷ batch) so any batch lands within 1.2 s (0.6 s on phones).
    const budget = window.innerWidth < 768 ? ms.phoneDropBudget : ms.dropBudget
    const step = Math.min(24, budget / fresh.length)
    map.getSource('biz').setData(toFeatures(known))
    const withT0 = toFeatures(fresh.map((p, i) => ({ ...p, _i: i })), (p) => ({ t0: p._i * step }))
    map.getSource('arrivals').setData(withT0)
    const start = performance.now()
    const end = (fresh.length - 1) * step + ms.ring
    const age = (clock) => ['-', clock, ['get', 't0']]
    cancelAnimationFrame(raf.current)
    const frame = (now) => {
      const clock = now - start
      map.setPaintProperty('arrival-dots', 'circle-opacity', ['interpolate', ['linear'], age(clock), 0, 0, ms.dotFade, 1])
      map.setPaintProperty('arrival-rings', 'circle-radius', ['interpolate', ['linear'], age(clock), 0, 18, ms.ring, 5])
      map.setPaintProperty('arrival-rings', 'circle-stroke-opacity', ['interpolate', ['linear'], age(clock), -1, 0, 0, 0.9, ms.ring, 0])
      if (clock < end) raf.current = requestAnimationFrame(frame)
      else {
        map.getSource('biz').setData(toFeatures(withCoords))
        map.getSource('arrivals').setData(toFeatures([]))
      }
    }
    raf.current = requestAnimationFrame(frame)
  }, [points, ready, animate, reduce])

  const count = points.length
  return (
    <div className="map-frame" style={height ? { height, minHeight: height } : undefined}>
      <div ref={box} className="map-canvas" role="img" aria-label={`Map of ${count} businesses`} />
      {failed && (
        <div className="lanes" style={{ background: 'var(--map-land)' }}>
          <StateBlock icon={MapPinOff} title="Map tiles did not load" text="The list still works."
            action={<button className="btn" onClick={() => setAttempt((a) => a + 1)}>Retry map</button>} />
        </div>
      )}
      <div className="map-legend" aria-hidden="true">
        <span><i className="legend-dot" style={{ background: 'var(--dot-lead)' }} />Possible lead</span>
        <span><i className="legend-dot" style={{ background: 'var(--dot-review)' }} />Needs review</span>
        <span><i className="legend-dot" style={{ background: 'var(--dot-notlead)' }} />Not a lead</span>
        <span><i className="legend-dot" style={{ background: 'var(--dot-unchecked)' }} />Not checked yet</span>
      </div>
    </div>
  )
}
