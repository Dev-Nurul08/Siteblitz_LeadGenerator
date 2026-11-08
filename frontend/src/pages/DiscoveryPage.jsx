import { useState, useEffect } from 'react'
import api from '../services/api'
import Badge from '../components/Badge'

export default function DiscoveryPage({ onNavigate }) {
  const [jobs, setJobs] = useState([])
  const [loadingJobs, setLoadingJobs] = useState(true)
  const [running, setRunning] = useState(false)
  const [activeSource, setActiveSource] = useState('openstreetmap') // 'openstreetmap' | 'wikidata' | 'csv_import'
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // Query Parameters
  const [form, setForm] = useState({
    country_code: 'IN',
    city: 'Mumbai',
    category: 'restaurant',
    max_results: 100,
  })

  // CSV Ingestion
  const [csvFile, setCsvFile] = useState(null)
  const [csvCountry, setCsvCountry] = useState('IN')
  const [csvDelimiter, setCsvDelimiter] = useState(',')

  useEffect(() => {
    loadJobs()
    const timer = setInterval(loadJobs, 8000)
    return () => clearInterval(timer)
  }, [])

  async function loadJobs() {
    try {
      const data = await api.discovery.jobs(15)
      setJobs(data || [])
    } catch (_) {}
    finally {
      setLoadingJobs(false)
    }
  }

  async function handleRunDiscovery(e) {
    e.preventDefault()
    setRunning(true)
    setResult(null)
    setError(null)
    try {
      if (activeSource === 'csv_import') {
        if (!csvFile) throw new Error('Please select a valid CSV file')
        const res = await api.discovery.importCsv(csvFile, csvCountry, csvDelimiter)
        setResult(res)
      } else {
        const payload = {
          source_slug: activeSource,
          country_code: form.country_code || undefined,
          city: form.city || undefined,
          category: form.category || undefined,
          max_results: parseInt(form.max_results) || 100,
          query_params: {},
        }
        const res = await api.discovery.run(payload)
        setResult(res)
      }
      await loadJobs()
    } catch (err) {
      setError(err.message)
    } finally {
      setRunning(false)
    }
  }

  // Aggregate matrix stats
  const totalDiscovered = jobs.reduce((acc, j) => acc + (j.records_extracted || 0), 0)
  const totalJobsCompleted = jobs.filter(j => j.status === 'COMPLETED').length

  return (
    <div className="page-body space-y-4">
      {/* ── Header ── */}
      <div className="flex justify-between items-center pb-3 border-b border-color-border">
        <div>
          <h1 className="page-title">Phase 1 — Discovery Engine</h1>
          <p className="page-subtitle">Spatial registry adapters, multi-source ingestion, and canonical deduplication.</p>
        </div>
        <div className="flex gap-2">
          {onNavigate && (
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => onNavigate('opportunities')}
            >
              Go to Phase 2 (Opportunities) →
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="alert alert-danger flex justify-between items-center">
          <span>Error: {error}</span>
          <button className="btn btn-sm btn-outline" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      {/* ── KPI Matrix ── */}
      <div className="stats-grid">
        <div className="stat-card accent-primary">
          <div className="stat-value">{totalDiscovered.toLocaleString()}</div>
          <div className="stat-label">Total Records Ingested</div>
        </div>
        <div className="stat-card accent-success">
          <div className="stat-value">{totalJobsCompleted}</div>
          <div className="stat-label">Discovery Jobs Completed</div>
        </div>
        <div className="stat-card accent-secondary">
          <div className="stat-value">{activeSource.toUpperCase()}</div>
          <div className="stat-label">Active Extraction Engine</div>
        </div>
        <div className="stat-card accent-warning">
          <div className="stat-value font-mono">CANONICAL</div>
          <div className="stat-label">Deduplication Mode</div>
        </div>
      </div>

      {/* ── Query Matrix Control Panel ── */}
      <div className="card">
        <div className="card-header">
          <div className="flex gap-2">
            <button 
              className={`btn btn-sm ${activeSource === 'openstreetmap' ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setActiveSource('openstreetmap')}
            >
              OpenStreetMap (Overpass API)
            </button>
            <button 
              className={`btn btn-sm ${activeSource === 'wikidata' ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setActiveSource('wikidata')}
            >
              Wikidata (SPARQL)
            </button>
            <button 
              className={`btn btn-sm ${activeSource === 'csv_import' ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setActiveSource('csv_import')}
            >
              CSV File Ingestion
            </button>
          </div>
          <span className="text-xs font-mono text-gray-500">API RATE SAFEGUARD: ACTIVE</span>
        </div>

        <form onSubmit={handleRunDiscovery} className="space-y-3">
          {activeSource === 'csv_import' ? (
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label>CSV File</label>
                <input 
                  type="file" 
                  accept=".csv,.tsv" 
                  className="input input-sm w-full"
                  onChange={(e) => setCsvFile(e.target.files[0])}
                  required
                />
              </div>
              <div>
                <label>Country Code</label>
                <input 
                  type="text" 
                  className="input input-sm w-full font-mono uppercase"
                  value={csvCountry}
                  onChange={(e) => setCsvCountry(e.target.value)}
                />
              </div>
              <div>
                <label>Delimiter</label>
                <select 
                  className="input input-sm w-full"
                  value={csvDelimiter}
                  onChange={(e) => setCsvDelimiter(e.target.value)}
                >
                  <option value=",">Comma (,)</option>
                  <option value=";">Semicolon (;)</option>
                  <option value="\t">Tab (\t)</option>
                </select>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-4 gap-3">
              <div>
                <label>Target Country</label>
                <select 
                  className="input input-sm w-full"
                  value={form.country_code}
                  onChange={(e) => setForm({...form, country_code: e.target.value})}
                >
                  <option value="IN">India (IN)</option>
                  <option value="US">United States (US)</option>
                  <option value="GB">United Kingdom (GB)</option>
                  <option value="DE">Germany (DE)</option>
                  <option value="AU">Australia (AU)</option>
                  <option value="CA">Canada (CA)</option>
                  <option value="AE">UAE (AE)</option>
                </select>
              </div>
              <div>
                <label>Target City</label>
                <input 
                  type="text" 
                  className="input input-sm w-full"
                  value={form.city}
                  onChange={(e) => setForm({...form, city: e.target.value})}
                  placeholder="e.g. Mumbai, London, Dallas"
                  required
                />
              </div>
              <div>
                <label>Business Category</label>
                <select 
                  className="input input-sm w-full"
                  value={form.category}
                  onChange={(e) => setForm({...form, category: e.target.value})}
                >
                  <option value="restaurant">Restaurants & Dining</option>
                  <option value="clinic">Clinics & Healthcare</option>
                  <option value="hairdresser">Salons & Spas</option>
                  <option value="hotel">Hotels & Lodging</option>
                  <option value="industrial">Manufacturers & Suppliers</option>
                  <option value="retail">Retail & Wholesale</option>
                </select>
              </div>
              <div>
                <label>Max Results</label>
                <input 
                  type="number" 
                  className="input input-sm w-full font-mono"
                  value={form.max_results}
                  onChange={(e) => setForm({...form, max_results: e.target.value})}
                  min="10" max="1000"
                />
              </div>
            </div>
          )}

          <div className="flex justify-between items-center pt-2">
            <span className="text-xs text-gray-500">
              Adapters automatically normalize names, parse geo-coordinates, and deduplicate against database.
            </span>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={running}
            >
              {running ? 'Extracting Data...' : 'Execute Phase 1 Discovery'}
            </button>
          </div>
        </form>

        {result && (
          <div className={`alert ${result.found > 0 ? 'alert-success' : result.errors > 0 ? 'alert-warning' : 'alert-info'} mt-3 flex justify-between items-center text-xs`}>
            <div>
              <strong>Extraction Status:</strong> Discovered {result.found ?? result.records_found ?? result.records_extracted ?? 0} entities, normalized {result.new ?? result.records_new ?? 0} records, merged {result.duplicate ?? result.records_duplicate ?? 0} duplicates.
              {result.errors > 0 && <span className="text-amber-400 ml-2">({result.errors} endpoint errors/timeouts recorded in job log)</span>}
            </div>
            {result.found > 0 && onNavigate && (
              <button 
                className="btn btn-sm btn-outline text-white"
                onClick={() => onNavigate('opportunities')}
              >
                Proceed to Phase 2 (Audit) →
              </button>
            )}
          </div>
        )}
      </div>

      {/* ── Ingestion Jobs Matrix Table ── */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">Discovery Ingestion Matrix Log</span>
          <span className="text-xs font-mono text-gray-500">{jobs.length} jobs logged</span>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Job ID</th>
                <th>Source</th>
                <th>Target Parameters</th>
                <th>Records Extracted</th>
                <th>Normalized</th>
                <th>Duplicates Merged</th>
                <th>Status</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {loadingJobs && jobs.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-6 text-gray-500">Loading discovery execution log...</td>
                </tr>
              ) : jobs.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-6 text-gray-500">No discovery jobs executed yet. Run a search above to populate.</td>
                </tr>
              ) : (
                jobs.map((job) => (
                  <tr key={job.job_id || job.id}>
                    <td className="font-mono text-xs">#{job.job_id || job.id}</td>
                    <td>
                      <span className="font-semibold text-primary font-mono text-xs">
                        {job.source_name || job.source_slug || 'OpenStreetMap'}
                      </span>
                    </td>
                    <td className="text-xs">
                      {job.city ? `${job.city}, ` : ''}{job.country_code || 'Global'} — {job.category || 'All categories'}
                    </td>
                    <td className="font-mono text-xs font-bold text-primary">
                      {job.records_found ?? job.records_extracted ?? 0}
                    </td>
                    <td className="font-mono text-xs text-success">
                      {job.records_new ?? job.records_normalized ?? 0}
                    </td>
                    <td className="font-mono text-xs text-warning">
                      {job.records_duplicate ?? job.duplicates_found ?? 0}
                    </td>
                    <td>
                      <Badge status={job.status} />
                    </td>
                    <td className="font-mono text-xs text-gray-500">
                      {job.completed_at ? new Date(job.completed_at).toLocaleTimeString() : job.started_at ? new Date(job.started_at).toLocaleTimeString() : '—'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
