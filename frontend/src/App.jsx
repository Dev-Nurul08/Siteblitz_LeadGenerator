// App shell — header + stepper (spec row 12), hash routes (row 13), session entrance and
// route transitions (row 18), progress line signature, reduced motion (row 19).
import { Fragment, lazy, Suspense, useCallback, useEffect, useState } from 'react'
import { AnimatePresence, MotionConfig, motion, useReducedMotion } from 'motion/react'
import { Flame, ListChecks, Search, Send, Settings } from 'lucide-react'
import api from './services/api'
import { STEPS, useRoute } from './lib/router'
import { Ticker } from './components/ui'
import { refreshStats } from './lib/stats'
import { ease, ms } from './motion'

const FindPage = lazy(() => import('./pages/FindPage'))
const ReviewPage = lazy(() => import('./pages/ReviewPage'))
const HotLeadsPage = lazy(() => import('./pages/HotLeadsPage'))
const OutreachPage = lazy(() => import('./pages/OutreachPage'))
const SettingsPage = lazy(() => import('./pages/SettingsPage'))
const PAGES = { find: FindPage, review: ReviewPage, leads: HotLeadsPage, outreach: OutreachPage, settings: SettingsPage }
const STEP_ICONS = { find: Search, review: ListChecks, leads: Flame, outreach: Send }

function useStats() {
  const [stats, setStats] = useState(null)
  const load = useCallback(() => { api.intelligence.stats().then(setStats).catch(() => {}) }, [])
  useEffect(() => {
    load()
    window.addEventListener('sb:stats', load)
    return () => window.removeEventListener('sb:stats', load)
  }, [load])
  return stats
}

// The session entrance plays once per browser session, never on route changes.
const entrance = !sessionStorage.getItem('sb.entered')
sessionStorage.setItem('sb.entered', '1')

function Connector({ index, done }) {
  const reduce = useReducedMotion()
  const key = `sb.drawn.${index}`
  const already = localStorage.getItem(key) === '1'
  useEffect(() => { if (done) localStorage.setItem(key, '1') }, [done, key])
  return (
    <span className="connector" aria-hidden="true">
      <motion.span className="connector-fill"
        initial={{ scaleX: done && (already || reduce) ? 1 : 0 }}
        animate={{ scaleX: done ? 1 : 0 }}
        transition={{ duration: already || reduce ? 0 : ms.connector / 1000, ease: ease.entrance }} />
    </span>
  )
}

function Header({ route, stats }) {
  const counts = {
    find: stats?.jobs, review: (stats?.needs_review ?? 0) + (stats?.unassessed ?? 0),
    leads: stats?.by_tier?.HOT ?? 0, outreach: stats?.contacted ?? 0,
  }
  const produced = [counts.find > 0, (stats?.assessed ?? 0) > 0, counts.leads > 0]
  return (
    <>
      <motion.header className="header"
        initial={entrance ? { '--bar': 0 } : false} animate={{ '--bar': 1 }}
        transition={{ duration: 0.6, ease: ease.entrance }}>
        <a className="brand" href="#/find" style={{ color: 'var(--ink)', textDecoration: 'none' }}>
          <span className="brand-tile">S</span><span>SiteBlitz Lead Generator</span>
        </a>
        <ol className="steps" aria-label="Workflow">
          {STEPS.map((s, i) => (
            <Fragment key={s.id}>
              <motion.li className="step"
                initial={entrance ? { opacity: 0, y: 12 } : false} animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.52, delay: entrance ? 0.6 + i * 0.06 : 0, ease: ease.entrance }}>
                <a href={`#/${s.id}`} aria-current={route === s.id ? 'page' : undefined}>
                  <span className="step-index">{s.index}</span><span>{s.label}</span>
                  <span className="step-count"><Ticker value={counts[s.id] ?? 0} /></span>
                </a>
                {route === s.id && <motion.span className="step-bar" layoutId="step-bar" transition={{ duration: ms.indicator / 1000, ease: ease.ui }} />}
              </motion.li>
              {i < STEPS.length - 1 && <Connector index={i} done={produced[i]} />}
            </Fragment>
          ))}
        </ol>
        <div className="header-end">
          <a className="btn btn-sm" href="#/settings" aria-current={route === 'settings' ? 'page' : undefined}>
            <Settings size={16} strokeWidth={1.75} aria-hidden="true" /><span className="label-text">Settings</span>
          </a>
        </div>
      </motion.header>
      <nav className="bottombar" aria-label="Workflow">
        {STEPS.map((s) => {
          const Icon = STEP_ICONS[s.id]
          return (
            <a key={s.id} href={`#/${s.id}`} aria-current={route === s.id ? 'page' : undefined}>
              <Icon size={20} strokeWidth={1.75} aria-hidden="true" />{s.label}
            </a>
          )
        })}
      </nav>
    </>
  )
}

export default function App() {
  const { route, params } = useRoute()
  const stats = useStats()
  const reduce = useReducedMotion()
  const Page = PAGES[route]
  useEffect(() => { refreshStats() }, [route])
  return (
    <MotionConfig reducedMotion="user">
      <Header route={route} stats={stats} />
      <AnimatePresence mode="wait" initial={false}>
        <motion.main key={route} className="page"
          initial={{ opacity: 0, y: reduce ? 0 : 8 }} animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, transition: { duration: ms.routeOut / 1000, ease: ease.ui } }}
          transition={{ duration: (reduce ? ms.routeOut : ms.routeIn) / 1000, ease: ease.entrance }}>
          <Suspense fallback={null}>
            <Page params={params} stats={stats} entrance={entrance} />
          </Suspense>
        </motion.main>
      </AnimatePresence>
    </MotionConfig>
  )
}
