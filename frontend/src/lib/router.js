// Hash routes (spec row 13): #/find #/review #/leads #/outreach #/settings — no router package.
import { useEffect, useState } from 'react'

export const STEPS = [
  { id: 'find', index: '01', label: 'Find' },
  { id: 'review', index: '02', label: 'Review' },
  { id: 'leads', index: '03', label: 'Hot leads' },
  { id: 'outreach', index: '04', label: 'Outreach' },
]
const ROUTES = ['find', 'review', 'leads', 'outreach', 'settings']

function parse() {
  const raw = window.location.hash.replace(/^#\/?/, '')
  const [path, query = ''] = raw.split('?')
  const route = ROUTES.includes(path) ? path : null
  return { route, params: Object.fromEntries(new URLSearchParams(query)) }
}

export function go(route, params = {}) {
  const qs = new URLSearchParams(Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')).toString()
  window.location.hash = `#/${route}${qs ? `?${qs}` : ''}`
}

export function useRoute() {
  const [state, setState] = useState(parse)
  useEffect(() => {
    const onChange = () => setState(parse())
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
  useEffect(() => {
    if (state.route) localStorage.setItem('sb.lastStep', state.route)
  }, [state.route])
  // First visit opens on Find; later visits on the last step used.
  const route = state.route || localStorage.getItem('sb.lastStep') || 'find'
  return { route, params: state.params }
}
