import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import Badge from '../components/Badge'
import api from '../services/api'

export default function DiscoveryPage() {
  const [jobs, setJobs] = useState([])
  const [loadingJobs, setLoadingJobs] = useState(true)
  const [running, setRunning] = useState(false)
  const [activeTab, setActiveTab] = useState('osm') // 'osm' | 'csv'
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // OSM form state
  const [osmForm, setOsmForm] = useState({
    country_code: 'GB',
    city: 'London',
    category: 'restaurant',
    radius_km: '',
    latitude: '',
    longitude: '',
    max_results: 100,
  })

  // CSV form state
  const [csvFile, setCsvFile] = useState(null)
  const [csvCountry, setCsvCountry] = useState('')
  const [csvDelimiter, setCsvDelimiter] = useState(',')

  useEffect(() => {
    loadJobs()
    const interval = setInterval(loadJobs, 10000)
    return () => clearInterval(interval)
  }, [])

  async function loadJobs() {
    try {
      const data = await api.discovery.jobs(20)
      setJobs(data || [])
    } catch {
      // Ignore if API offline
    } finally {
      setLoadingJobs(false)
    }
  }

  async function runOsmDiscovery(e) {
    e.preventDefault()
    setRunning(true)
    setResult(null)
    setError(null)
    try {
      const payload = {
        source_slug: 'openstreetmap',
        country_code: osmForm.country_code || undefined,
        city: osmForm.city || undefined,
        category: osmForm.category || undefined,
        max_results: parseInt(osmForm.max_results) || 100,
        query_params: {},
      }
      if (osmForm.latitude && osmForm.longitude) {
        payload.latitude = parseFloat(osmForm.latitude)
        payload.longitude = parseFloat(osmForm.longitude)
        payload.radius_km = parseFloat(osmForm.radius_km) || 5
      }
      const res = await api.discovery.run(payload)
      setResult(res)
      loadJobs()
    } catch (e) {
      setError(e.message)
    } finally {
      setRunning(false)
    }
  }

  async function runCsvImport(e) {
    e.preventDefault()
    if (!csvFile) { setError('Please select a CSV file'); return }
    setRunning(true)
    setResult(null)
    setError(null)
    try {
      const res = await api.discovery.importCsv(csvFile, csvCountry, csvDelimiter)
      setResult(res)
      loadJobs()
    } catch (e) {
      setError(e.message)
    } finally {
      setRunning(false)
    }
  }

  const COUNTRIES = [
    { code: 'GB', name: 'United Kingdom' },
    { code: 'US', name: 'United States' },
    { code: 'AU', name: 'Australia' },
    { code: 'CA', name: 'Canada' },
    { code: 'DE', name: 'Germany' },
    { code: 'FR', name: 'France' },
    { code: 'IN', name: 'India' },
    { code: 'AE', name: 'United Arab Emirates' },
    { code: 'SG', name: 'Singapore' },
    { code: 'NZ', name: 'New Zealand' },
  ]

  const CATEGORIES = [
    '', 'restaurant', 'cafe', 'hotel', 'shop', 'bar', 'pub',
    'clinic', 'dentist', 'gym', 'salon', 'school',
    'lawyer', 'accountant', 'estate_agent', 'it',
    'car_repair', 'plumber', 'electrician',
  ]

  return (
    <>
      <PageHeader
        title="Discovery Engine"
        subtitle="Phase 1 — Find businesses from permitted sources"
        actions={
          running && (
            <div className="flex items-center gap-2" style={{ color: 'var(--color-accent-primary)', fontSize: '0.85rem' }}>
              <div className="spinner" />
              Running…
            </div>
          )
        }
      />

      <div className="page-body animate-fadeIn">
        <div className="grid-2" style={{ gap: '24px', alignItems: 'start' }}>

          {/* Discovery Form */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">Configure Discovery</div>
            </div>

            {/* Tab switcher */}
            <div style={{ display: 'flex', gap: '4px', marginBottom: '20px', background: 'var(--color-bg-tertiary)', padding: '4px', borderRadius: 'var(--radius-md)' }}>
              {[
                { id: 'osm', label: '🗺️ OpenStreetMap', desc: 'ODbL — Open License' },
                { id: 'csv', label: '📄 CSV Import', desc: 'Manual / Opt-in' },
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className="btn"
                  style={{
                    flex: 1, fontSize: '0.8rem',
                    background: activeTab === tab.id ? 'var(--gradient-primary)' : 'transparent',
                    color: activeTab === tab.id ? 'white' : 'var(--color-text-secondary)',
                    border: 'none', padding: '8px 12px',
                  }}
                >
                  {tab.label}
                  <br />
                  <span style={{ fontSize: '0.65rem', opacity: 0.75 }}>{tab.desc}</span>
                </button>
              ))}
            </div>

            {/* OSM Form */}
            {activeTab === 'osm' && (
              <form onSubmit={runOsmDiscovery}>
                <div style={{ background: 'rgba(34, 197, 94, 0.08)', border: '1px solid rgba(34, 197, 94, 0.15)', borderRadius: 'var(--radius-md)', padding: '10px 14px', marginBottom: '16px', fontSize: '0.78rem', color: 'var(--color-text-secondary)' }}>
                  ✓ <strong style={{ color: 'var(--color-accent-success)' }}>ODbL License</strong> — Data is freely reusable with attribution. © OpenStreetMap contributors.
                </div>

                <div className="input-group">
                  <label className="input-label">Country *</label>
                  <select className="input" value={osmForm.country_code} onChange={e => setOsmForm(p => ({ ...p, country_code: e.target.value }))}>
                    {COUNTRIES.map(c => <option key={c.code} value={c.code}>{c.name} ({c.code})</option>)}
                  </select>
                </div>

                <div className="input-group">
                  <label className="input-label">City</label>
                  <input className="input" placeholder="e.g. London, Manchester, Glasgow…" value={osmForm.city} onChange={e => setOsmForm(p => ({ ...p, city: e.target.value }))} />
                </div>

                <div className="input-group">
                  <label className="input-label">Business Category</label>
                  <select className="input" value={osmForm.category} onChange={e => setOsmForm(p => ({ ...p, category: e.target.value }))}>
                    <option value="">All categories</option>
                    {CATEGORIES.filter(Boolean).map(c => <option key={c} value={c}>{c.replace(/_/g, ' ')}</option>)}
                  </select>
                </div>

                <div style={{ padding: '12px', background: 'var(--color-bg-tertiary)', borderRadius: 'var(--radius-md)', marginBottom: '16px' }}>
                  <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '10px' }}>OR SEARCH BY COORDINATES</div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                    <div className="input-group" style={{ marginBottom: 0 }}>
                      <label className="input-label">Latitude</label>
                      <input className="input" placeholder="51.5074" type="number" step="any" value={osmForm.latitude} onChange={e => setOsmForm(p => ({ ...p, latitude: e.target.value }))} />
                    </div>
                    <div className="input-group" style={{ marginBottom: 0 }}>
                      <label className="input-label">Longitude</label>
                      <input className="input" placeholder="-0.1278" type="number" step="any" value={osmForm.longitude} onChange={e => setOsmForm(p => ({ ...p, longitude: e.target.value }))} />
                    </div>
                    <div className="input-group" style={{ marginBottom: 0, gridColumn: 'span 2' }}>
                      <label className="input-label">Radius (km)</label>
                      <input className="input" placeholder="5" type="number" min="0.1" max="100" value={osmForm.radius_km} onChange={e => setOsmForm(p => ({ ...p, radius_km: e.target.value }))} />
                    </div>
                  </div>
                </div>

                <div className="input-group">
                  <label className="input-label">Max Results</label>
                  <select className="input" value={osmForm.max_results} onChange={e => setOsmForm(p => ({ ...p, max_results: e.target.value }))}>
                    {[50, 100, 200, 500, 1000].map(n => <option key={n} value={n}>{n} businesses</option>)}
                  </select>
                </div>

                {error && activeTab === 'osm' && (
                  <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: 'var(--radius-md)', padding: '10px 14px', marginBottom: '14px', fontSize: '0.8rem', color: 'var(--color-accent-danger)' }}>
                    ❌ {error}
                  </div>
                )}

                <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={running}>
                  {running ? <><div className="spinner" /> Running Discovery…</> : '🔍 Start OSM Discovery'}
                </button>
              </form>
            )}

            {/* CSV Import Form */}
            {activeTab === 'csv' && (
              <form onSubmit={runCsvImport}>
                <div style={{ background: 'rgba(148, 163, 184, 0.08)', border: '1px solid rgba(148, 163, 184, 0.15)', borderRadius: 'var(--radius-md)', padding: '10px 14px', marginBottom: '16px', fontSize: '0.78rem', color: 'var(--color-text-secondary)' }}>
                  ℹ️ <strong>Manual / Opt-in</strong> — Data provenance and usage rights are your responsibility.
                </div>

                <div className="input-group">
                  <label className="input-label">CSV File *</label>
                  <div
                    style={{
                      border: '2px dashed var(--color-border)',
                      borderRadius: 'var(--radius-md)',
                      padding: '24px',
                      textAlign: 'center',
                      cursor: 'pointer',
                      transition: 'border-color 0.2s',
                    }}
                    onDragOver={e => { e.preventDefault(); e.currentTarget.style.borderColor = 'var(--color-accent-primary)' }}
                    onDragLeave={e => { e.currentTarget.style.borderColor = 'var(--color-border)' }}
                    onDrop={e => { e.preventDefault(); e.currentTarget.style.borderColor = 'var(--color-border)'; setCsvFile(e.dataTransfer.files[0]) }}
                    onClick={() => document.getElementById('csv-file-input').click()}
                  >
                    <input id="csv-file-input" type="file" accept=".csv,.txt" style={{ display: 'none' }} onChange={e => setCsvFile(e.target.files[0])} />
                    {csvFile ? (
                      <div>
                        <div style={{ fontSize: '1.5rem', marginBottom: '6px' }}>📄</div>
                        <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{csvFile.name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>{(csvFile.size / 1024).toFixed(1)} KB</div>
                      </div>
                    ) : (
                      <div>
                        <div style={{ fontSize: '1.5rem', marginBottom: '6px' }}>📂</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)' }}>Drop CSV file here or click to browse</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                          Supports: name, address, city, country, phone, email, website, category
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div className="input-group" style={{ marginBottom: 0 }}>
                    <label className="input-label">Default Country</label>
                    <select className="input" value={csvCountry} onChange={e => setCsvCountry(e.target.value)}>
                      <option value="">Auto-detect</option>
                      {COUNTRIES.map(c => <option key={c.code} value={c.code}>{c.code} — {c.name}</option>)}
                    </select>
                  </div>
                  <div className="input-group" style={{ marginBottom: 0 }}>
                    <label className="input-label">Delimiter</label>
                    <select className="input" value={csvDelimiter} onChange={e => setCsvDelimiter(e.target.value)}>
                      <option value=",">Comma (,)</option>
                      <option value=";">Semicolon (;)</option>
                      <option value="\t">Tab</option>
                    </select>
                  </div>
                </div>

                {error && activeTab === 'csv' && (
                  <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', borderRadius: 'var(--radius-md)', padding: '10px 14px', marginTop: '14px', fontSize: '0.8rem', color: 'var(--color-accent-danger)' }}>
                    ❌ {error}
                  </div>
                )}

                <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '16px' }} disabled={running || !csvFile}>
                  {running ? <><div className="spinner" /> Importing…</> : '📤 Import CSV'}
                </button>
              </form>
            )}

            {/* Result */}
            {result && (
              <div style={{ marginTop: '16px', background: result.status === 'FAILED' ? 'rgba(239, 68, 68, 0.08)' : 'rgba(34, 197, 94, 0.08)', border: `1px solid ${result.status === 'FAILED' ? 'rgba(239,68,68,0.2)' : 'rgba(34,197,94,0.2)'}`, borderRadius: 'var(--radius-md)', padding: '14px 16px' }}>
                <div style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '8px', color: result.status === 'FAILED' ? 'var(--color-accent-danger)' : 'var(--color-accent-success)' }}>
                  {result.status === 'FAILED' ? '❌ Job Failed' : '✓ Job Complete'} — Job #{result.job_id}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px' }}>
                  {[
                    { label: 'New', value: result.records_new, color: 'var(--color-accent-success)' },
                    { label: 'Duplicate', value: result.records_duplicate, color: 'var(--color-accent-warning)' },
                    { label: 'Errors', value: result.records_error, color: 'var(--color-accent-danger)' },
                  ].map(({ label, value, color }) => (
                    <div key={label} style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: '1.3rem', fontWeight: 800, color }}>{value ?? 0}</div>
                      <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>{label}</div>
                    </div>
                  ))}
                </div>
                {result.error && <div style={{ fontSize: '0.78rem', color: 'var(--color-accent-danger)', marginTop: '8px' }}>{result.error}</div>}
              </div>
            )}
          </div>

          {/* Jobs History */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">Discovery Jobs</div>
              <button className="btn btn-ghost btn-sm" onClick={loadJobs}>↻</button>
            </div>

            {loadingJobs ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                <div className="spinner spinner-lg" />
              </div>
            ) : jobs.length === 0 ? (
              <div className="empty-state" style={{ padding: '40px 20px' }}>
                <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>🔍</div>
                <div className="empty-state-title">No discovery jobs yet</div>
                <div className="empty-state-description">Run a discovery to see results here</div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {jobs.map(job => (
                  <div key={job.job_id} style={{
                    padding: '12px 14px', background: 'var(--color-bg-tertiary)',
                    borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                      <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>
                        {job.source_name} <span style={{ color: 'var(--color-text-muted)', fontWeight: 400 }}>#{job.job_id}</span>
                      </div>
                      <Badge status={job.status} />
                    </div>
                    <div style={{ display: 'flex', gap: '12px', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                      <span style={{ color: 'var(--color-accent-success)' }}>+{job.records_new} new</span>
                      <span>{job.records_duplicate} dup</span>
                      {job.records_error > 0 && <span style={{ color: 'var(--color-accent-danger)' }}>{job.records_error} errors</span>}
                    </div>
                    {job.error_message && (
                      <div style={{ fontSize: '0.72rem', color: 'var(--color-accent-danger)', marginTop: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {job.error_message}
                      </div>
                    )}
                    {job.started_at && (
                      <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                        {new Date(job.started_at).toLocaleString()}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
