import { useState, useEffect } from 'react'
import api from '../services/api'

export default function LeadRadarPage() {
  const [activeTab, setActiveTab] = useState('funnel')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Funnel State
  const [funnelData, setFunnelData] = useState(null)
  const [selectedCity, setSelectedCity] = useState('Mumbai')
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.7)

  // Evaluator State
  const [evalForm, setEvalForm] = useState({
    name: 'Apollo Dental & Implant Centre',
    city: 'Mumbai',
    country_code: 'IN',
    category: 'Clinic',
    has_official_id: true,
    needed_task_unhosted: true,
    reviews_count_90d: 14,
    promotions_count_90d: 3,
    active_ad_campaign_7d: false,
    unanswered_customer_requests_90d: 4,
    orders_via_dm_only: true,
    public_request_website_help_30d: false,
  })
  const [evalResult, setEvalResult] = useState(null)

  // Revenue Calculator State
  const [revCategory, setRevCategory] = useState('RESTAURANT')
  const [revSignals, setRevSignals] = useState({
    seats_count: 70,
    avg_spend_per_cover: 30,
    open_days_per_year: 312,
    delivery_revenue_share: 0.20,
    doctors_count: 4,
    realised_consultation_fee: 90,
    rooms_count: 45,
    avg_room_rate: 130,
    new_reviews_90d: 18,
    avg_transaction_ticket: 35,
    calibrated_rates: true,
  })
  const [revResult, setRevResult] = useState(null)

  // Baselines State
  const [baselines, setBaselines] = useState([])
  const [baselineSearch, setBaselineSearch] = useState('')
  const [profiles, setProfiles] = useState(null)

  useEffect(() => {
    // Initial fetch of baselines
    loadBaselines()
    // Auto-run Mumbai Funnel on mount
    runMumbaiFunnel()
  }, [])

  const loadBaselines = async () => {
    try {
      const data = await api.leadRadar.cityBaselines()
      setBaselines(data)
      const profs = await api.leadRadar.regionalProfiles()
      setProfiles(profs)
    } catch (err) {
      console.error('Failed to load baselines', err)
    }
  }

  const runMumbaiFunnel = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.leadRadar.mumbaiFunnel({
        city: selectedCity,
        country: 'India',
        confidence_threshold: parseFloat(confidenceThreshold),
      })
      setFunnelData(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleEvaluate = async (e) => {
    e?.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const payload = {
        name: evalForm.name,
        city: evalForm.city,
        country_code: evalForm.country_code,
        category: evalForm.category,
        raw_signals: {
          official_reg_id: evalForm.has_official_id ? 'REG-MUMBAI-2026' : null,
          needed_task_unhosted: evalForm.needed_task_unhosted,
          reviews_count_90d: parseInt(evalForm.reviews_count_90d) || 0,
          promotions_count_90d: parseInt(evalForm.promotions_count_90d) || 0,
          active_ad_campaign_7d: evalForm.active_ad_campaign_7d,
          unanswered_customer_requests_90d: parseInt(evalForm.unanswered_customer_requests_90d) || 0,
          orders_via_dm_only: evalForm.orders_via_dm_only,
          public_request_website_help_30d: evalForm.public_request_website_help_30d,
          independent_activity_signals_90d: 2,
        },
      }
      const res = await api.leadRadar.evaluate(payload)
      setEvalResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCalculateRevenue = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.leadRadar.revenueEstimate({
        category: revCategory,
        signals: revSignals,
        currency: 'USD',
      })
      setRevResult(res)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const filteredBaselines = baselines.filter(b => 
    b.city.toLowerCase().includes(baselineSearch.toLowerCase()) ||
    b.country.toLowerCase().includes(baselineSearch.toLowerCase())
  )

  return (
    <div className="lead-radar-page">
      {/* ── Header ── */}
      <div className="page-header">
        <div>
          <h1 className="page-title flex-center gap-2">
            <span>⚡</span> Lead-Radar Condition Engine
          </h1>
          <p className="page-subtitle">
            Autonomous Global Sales Intelligence • 8-Stage Funnel • 6-Fact Profiling • 51 Conditions • 17 Sales Recipes • 45-City Baselines
          </p>
        </div>
        <div className="header-actions flex gap-2">
          <button 
            className={`btn ${activeTab === 'funnel' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('funnel')}
          >
            📉 8-Stage Pipeline
          </button>
          <button 
            className={`btn ${activeTab === 'evaluator' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('evaluator')}
          >
            🧪 6-Fact Evaluator
          </button>
          <button 
            className={`btn ${activeTab === 'revenue' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('revenue')}
          >
            💰 Revenue Estimator
          </button>
          <button 
            className={`btn ${activeTab === 'baselines' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('baselines')}
          >
            🌍 45-City Baselines
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger mb-4 flex justify-between items-center">
          <span>⚠️ {error}</span>
          <button className="btn btn-sm btn-outline" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      {/* ── TAB 1: 8-STAGE FUNNEL ── */}
      {activeTab === 'funnel' && (
        <div className="funnel-container space-y-6">
          <div className="card p-4 bg-base-200">
            <div className="flex flex-wrap gap-4 items-center justify-between">
              <div>
                <h3 className="font-bold text-lg">Section 1: Mumbai 2-Lakh Pipeline to Verified Shortlist</h3>
                <p className="text-sm opacity-80">
                  Data source: Overture Places + Meta open data. Eliminates junk, tests absence across 3 paths, verifies active demand and task gaps.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <select 
                  className="input select select-bordered" 
                  value={selectedCity} 
                  onChange={(e) => setSelectedCity(e.target.value)}
                >
                  <option value="Mumbai">Mumbai (1.48L Places)</option>
                  <option value="Pune">Pune (1.08L Places)</option>
                  <option value="Delhi">Delhi (1.83L Places)</option>
                  <option value="Bengaluru">Bengaluru (1.86L Places)</option>
                  <option value="Dallas">Dallas (72K Places)</option>
                  <option value="London">London (4.08L Places)</option>
                  <option value="Berlin">Berlin (1.89L Places)</option>
                </select>
                <div className="flex items-center gap-1">
                  <span className="text-xs">Conf:</span>
                  <input 
                    type="number" 
                    step="0.05" 
                    min="0.5" 
                    max="0.95" 
                    className="input input-sm w-20"
                    value={confidenceThreshold} 
                    onChange={(e) => setConfidenceThreshold(e.target.value)}
                  />
                </div>
                <button 
                  className="btn btn-primary" 
                  onClick={runMumbaiFunnel}
                  disabled={loading}
                >
                  {loading ? 'Processing...' : '▶ Run 8-Stage Funnel'}
                </button>
              </div>
            </div>
          </div>

          {funnelData && (
            <>
              {/* Funnel Stage Metric Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2">
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 0</div>
                  <div className="text-xl font-bold">{funnelData.stage_counts.stage_0_all_places}</div>
                  <div className="text-xs">All Places</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 1</div>
                  <div className="text-xl font-bold text-primary">{funnelData.stage_counts.stage_1_confident}</div>
                  <div className="text-xs">Conf ≥ {confidenceThreshold}</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 2</div>
                  <div className="text-xl font-bold text-warning">{funnelData.stage_counts.stage_2_no_website_on_file}</div>
                  <div className="text-xs">No Site On File</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 3</div>
                  <div className="text-xl font-bold text-primary">{funnelData.stage_counts.stage_3_reachable}</div>
                  <div className="text-xs">Reachable Info</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 4</div>
                  <div className="text-xl font-bold">{funnelData.stage_counts.stage_4_real_business_g1_g4}</div>
                  <div className="text-xs">G1-G4 Real Biz</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 5</div>
                  <div className="text-xl font-bold text-primary">{funnelData.stage_counts.stage_5_truly_no_site_w1}</div>
                  <div className="text-xs">W1 Truly Absent</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100">
                  <div className="text-xs uppercase font-semibold text-gray-500">Stage 6</div>
                  <div className="text-xl font-bold text-success">{funnelData.stage_counts.stage_6_alive_and_active_g7}</div>
                  <div className="text-xs">G7 Alive & Active</div>
                </div>
                <div className="stat-card p-3 border rounded text-center bg-base-100 border-primary">
                  <div className="text-xs uppercase font-semibold text-primary">Stage 7-8</div>
                  <div className="text-xl font-bold text-primary">{funnelData.stage_counts.stage_7_real_task_gap_w2_w13}</div>
                  <div className="text-xs">Qualified Shortlist</div>
                </div>
              </div>

              {/* Retention Bars */}
              <div className="card p-4 border bg-base-100">
                <h4 className="font-semibold text-sm mb-2">Stage Retention & Drop-off Flow</h4>
                <div className="space-y-2">
                  <div className="flex items-center text-xs">
                    <span className="w-40 font-mono">Stage 1 (Confident):</span>
                    <div className="w-full bg-base-300 rounded h-2 mr-2 overflow-hidden border border-color-border">
                      <div className="bg-zinc-400 h-full" style={{ width: `${funnelData.retention_rates_pct.confident_pct}%`, backgroundColor: '#a1a1aa' }}></div>
                    </div>
                    <span className="w-16 font-bold text-right">{funnelData.retention_rates_pct.confident_pct}%</span>
                  </div>
                  <div className="flex items-center text-xs">
                    <span className="w-40 font-mono">Stage 2 (No Site):</span>
                    <div className="w-full bg-base-300 rounded h-2 mr-2 overflow-hidden border border-color-border">
                      <div className="bg-amber-600 h-full" style={{ width: `${funnelData.retention_rates_pct.no_website_pct}%`, backgroundColor: '#d97706' }}></div>
                    </div>
                    <span className="w-16 font-bold text-right">{funnelData.retention_rates_pct.no_website_pct}%</span>
                  </div>
                  <div className="flex items-center text-xs">
                    <span className="w-40 font-mono">Stage 3 (Reachable):</span>
                    <div className="w-full bg-base-300 rounded h-2 mr-2 overflow-hidden border border-color-border">
                      <div className="bg-zinc-300 h-full" style={{ width: `${funnelData.retention_rates_pct.reachable_pct}%`, backgroundColor: '#d4d4d8' }}></div>
                    </div>
                    <span className="w-16 font-bold text-right">{funnelData.retention_rates_pct.reachable_pct}%</span>
                  </div>
                  <div className="flex items-center text-xs">
                    <span className="w-40 font-mono">Stage 5 (Truly Absent):</span>
                    <div className="w-full bg-base-300 rounded h-2 mr-2 overflow-hidden border border-color-border">
                      <div className="bg-white h-full" style={{ width: `${funnelData.retention_rates_pct.truly_absent_pct}%`, backgroundColor: '#ffffff' }}></div>
                    </div>
                    <span className="w-16 font-bold text-right">{funnelData.retention_rates_pct.truly_absent_pct}%</span>
                  </div>
                  <div className="flex items-center text-xs">
                    <span className="w-40 font-mono font-bold">Stage 8 (Shortlist):</span>
                    <div className="w-full bg-base-300 rounded h-2 mr-2 overflow-hidden border border-color-border">
                      <div className="bg-emerald-600 h-full" style={{ width: `${funnelData.retention_rates_pct.qualified_shortlist_pct}%`, backgroundColor: '#16a34a' }}></div>
                    </div>
                    <span className="w-16 font-bold text-right text-success">{funnelData.retention_rates_pct.qualified_shortlist_pct}%</span>
                  </div>
                </div>
              </div>

              {/* Shortlist Table */}
              <div className="card p-4 border bg-base-100">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="font-bold text-base">Top Ranked High-Confidence Opportunities ({funnelData.sample_shortlist.length})</h3>
                  <div className="flex gap-2">
                    <span className="badge badge-success">Segment B: Need Confirmed</span>
                    <span className="badge badge-warning">Warm: In Motion</span>
                    <span className="badge badge-primary">Segment A: Mandate</span>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="table table-compact w-full">
                    <thead>
                      <tr>
                        <th>Opportunity Class</th>
                        <th>Business Name</th>
                        <th>Category</th>
                        <th>Segment</th>
                        <th>Matched Recipe</th>
                        <th>Revenue Range</th>
                        <th>Observed Opening Fact</th>
                        <th>Pitch Angle</th>
                      </tr>
                    </thead>
                    <tbody>
                      {funnelData.sample_shortlist.map((lead) => (
                        <tr key={lead.record_id} className="hover">
                          <td>
                            <span className={`badge badge-sm ${
                              lead.rank_opportunity_class === 'OPEN_MANDATE' ? 'badge-primary' :
                              lead.rank_opportunity_class === 'BROKEN_TASK_WITH_DEMAND' ? 'badge-error' :
                              'badge-secondary'
                            }`}>
                              {lead.rank_opportunity_class}
                            </span>
                          </td>
                          <td className="font-bold">
                            {lead.name}
                            {lead.is_meta_source && <span className="ml-1 text-xs opacity-60">(Meta-src)</span>}
                          </td>
                          <td>{lead.category}</td>
                          <td>
                            <span className={`badge ${
                              lead.segment === 'A' ? 'badge-primary' :
                              lead.segment === 'B' ? 'badge-success' : 'badge-ghost'
                            }`}>
                              {lead.segment}
                            </span>
                            {lead.warm_context && <span className="ml-1 badge badge-xs badge-warning">WARM</span>}
                          </td>
                          <td className="font-semibold text-xs text-primary">
                            {lead.primary_recipe_name || 'Standard Gap'}
                          </td>
                          <td className="font-mono text-xs">
                            {lead.revenue_min ? `$${Math.round(lead.revenue_min).toLocaleString()} - $${Math.round(lead.revenue_max).toLocaleString()}` : 'Unavailable'}
                          </td>
                          <td className="text-xs max-w-xs truncate" title={lead.pitch_opening_fact}>
                            {lead.pitch_opening_fact}
                          </td>
                          <td className="text-xs max-w-xs truncate" title={lead.pitch_angle}>
                            {lead.pitch_angle}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* ── TAB 2: 6-FACT & 51-CONDITION EVALUATOR ── */}
      {activeTab === 'evaluator' && (
        <div className="evaluator-container grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Input Configuration Column */}
          <div className="card p-4 border bg-base-100 space-y-4">
            <h3 className="font-bold text-base border-b pb-2">Business Operating Signals</h3>
            <form onSubmit={handleEvaluate} className="space-y-3">
              <div>
                <label className="label-text text-xs">Business Name</label>
                <input 
                  type="text" 
                  className="input input-sm w-full"
                  value={evalForm.name}
                  onChange={(e) => setEvalForm({...evalForm, name: e.target.value})}
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="label-text text-xs">City</label>
                  <input 
                    type="text" 
                    className="input input-sm w-full"
                    value={evalForm.city}
                    onChange={(e) => setEvalForm({...evalForm, city: e.target.value})}
                  />
                </div>
                <div>
                  <label className="label-text text-xs">Category</label>
                  <select 
                    className="input input-sm w-full select"
                    value={evalForm.category}
                    onChange={(e) => setEvalForm({...evalForm, category: e.target.value})}
                  >
                    <option value="Clinic">Clinic / Healthcare</option>
                    <option value="Restaurant">Restaurant / Dining</option>
                    <option value="Salon">Salon / Spa</option>
                    <option value="Hotel">Hotel / Hospitality</option>
                    <option value="Manufacturer">Manufacturer / Exporter</option>
                    <option value="Retail">Retail Store</option>
                  </select>
                </div>
              </div>

              <div className="divider text-xs">Observed Conditions</div>

              <div className="space-y-2 text-xs">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={evalForm.has_official_id}
                    onChange={(e) => setEvalForm({...evalForm, has_official_id: e.target.checked})}
                    className="checkbox checkbox-sm checkbox-primary"
                  />
                  <span>G1: Official Registration ID / Tax ID Verified</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={evalForm.needed_task_unhosted}
                    onChange={(e) => setEvalForm({...evalForm, needed_task_unhosted: e.target.checked})}
                    className="checkbox checkbox-sm checkbox-primary"
                  />
                  <span>W2: Customer Task (Booking/Menu/Catalog) Unhosted</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={evalForm.orders_via_dm_only}
                    onChange={(e) => setEvalForm({...evalForm, orders_via_dm_only: e.target.checked})}
                    className="checkbox checkbox-sm checkbox-primary"
                  />
                  <span>D11: Messaging Bottleneck (Orders routed via DM/calls)</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={evalForm.active_ad_campaign_7d}
                    onChange={(e) => setEvalForm({...evalForm, active_ad_campaign_7d: e.target.checked})}
                    className="checkbox checkbox-sm checkbox-primary"
                  />
                  <span>D1: Active Paid Ads running into Gap</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={evalForm.public_request_website_help_30d}
                    onChange={(e) => setEvalForm({...evalForm, public_request_website_help_30d: e.target.checked})}
                    className="checkbox checkbox-sm checkbox-primary"
                  />
                  <span>I1: Explicit Public Help Request / RFP &lt; 30d</span>
                </label>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <label className="label-text text-xs">Reviews (90d)</label>
                  <input 
                    type="number" 
                    className="input input-sm w-full"
                    value={evalForm.reviews_count_90d}
                    onChange={(e) => setEvalForm({...evalForm, reviews_count_90d: e.target.value})}
                  />
                </div>
                <div>
                  <label className="label-text text-xs">Promotions (90d)</label>
                  <input 
                    type="number" 
                    className="input input-sm w-full"
                    value={evalForm.promotions_count_90d}
                    onChange={(e) => setEvalForm({...evalForm, promotions_count_90d: e.target.value})}
                  />
                </div>
              </div>

              <button 
                type="submit" 
                className="btn btn-primary w-full mt-4"
                disabled={loading}
              >
                {loading ? 'Evaluating...' : '⚡ Evaluate Lead & Generate Pitch'}
              </button>
            </form>
          </div>

          {/* Results Presentation Column (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            {evalResult ? (
              <>
                {/* 6 Facts Grid */}
                <div className="card p-4 border bg-base-100">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-bold text-sm">Section 2: The Six Stored Facts</h4>
                    <div className="flex gap-2">
                      <span className={`badge ${evalResult.segment === 'A' ? 'badge-primary' : evalResult.segment === 'B' ? 'badge-success' : 'badge-ghost'}`}>
                        Segment {evalResult.segment}
                      </span>
                      {evalResult.warm_context && <span className="badge badge-warning">WARM CONTEXT</span>}
                    </div>
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">1. Owned Presence</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.owned_presence}</div>
                    </div>
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">2. Availability</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.availability}</div>
                    </div>
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">3. Task Covered</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.customer_task_covered}</div>
                    </div>
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">4. Task Quality</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.task_quality}</div>
                    </div>
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">5. Buying Status</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.buying_status}</div>
                    </div>
                    <div className="p-2 border rounded bg-base-200">
                      <div className="text-gray-500 font-semibold">6. Authority</div>
                      <div className="font-mono font-bold mt-1">{evalResult.facts.authority}</div>
                    </div>
                  </div>
                </div>

                {/* Section 5 Factual Pitch & Matched Recipe */}
                <div className="card p-4 border bg-base-100 border-primary">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="font-bold text-sm text-primary">
                      {evalResult.primary_recipe ? `Recipe Match: ${evalResult.primary_recipe.name}` : 'Strategic Pitch Angle'}
                    </h4>
                    <span className="badge badge-sm badge-outline font-mono">
                      {evalResult.conditions_met_count} Conditions Met
                    </span>
                  </div>

                  <div className="space-y-3 text-xs">
                    <div className="p-3 bg-base-200 rounded">
                      <div className="font-bold text-gray-500 uppercase text-[10px]">Opening Line (Always an Observed Fact)</div>
                      <div className="text-sm font-semibold mt-1 text-base-content">
                        "{evalResult.pitch.opening_fact}"
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="p-3 bg-base-200 rounded">
                        <div className="font-bold text-gray-500 uppercase text-[10px]">Recommended Pitch Angle</div>
                        <div className="mt-1">{evalResult.pitch.pitch_angle}</div>
                      </div>
                      <div className="p-3 bg-error/10 border border-error/20 rounded">
                        <div className="font-bold text-error uppercase text-[10px]">Strict Rule: Never Say</div>
                        <div className="mt-1 text-error font-medium">{evalResult.pitch.never_say}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Section 8: The 4 Strategic Questions */}
                <div className="card p-4 border bg-base-100">
                  <h4 className="font-bold text-sm mb-2">Section 8: Four Strategic Rationale Answers</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                    <div className="p-2 border rounded">
                      <span className="font-bold text-primary">Why This Business: </span>
                      {evalResult.rank.why_this_business}
                    </div>
                    <div className="p-2 border rounded">
                      <span className="font-bold text-primary">Why This Project: </span>
                      {evalResult.rank.why_this_project}
                    </div>
                    <div className="p-2 border rounded">
                      <span className="font-bold text-primary">Why Now: </span>
                      {evalResult.rank.why_now}
                    </div>
                    <div className="p-2 border rounded">
                      <span className="font-bold text-warning">What Is Unknown: </span>
                      {evalResult.rank.what_is_unknown}
                    </div>
                  </div>
                </div>

                {/* Section 10: Cryptographic Absence Certificate */}
                {evalResult.absence_certificate && (
                  <div className="card p-3 border bg-base-200 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="font-mono font-bold text-primary">
                        🛡️ {evalResult.absence_certificate.certificate_id}
                      </span>
                      <span className="text-[10px] opacity-70">
                        SHA-256: {evalResult.absence_certificate.signature_hash.substring(0, 16)}...
                      </span>
                    </div>
                    <p className="mt-1 opacity-80">
                      {evalResult.absence_certificate.notes} Tested {evalResult.absence_certificate.queries_executed.length} queries across 3 canonical absence paths.
                    </p>
                  </div>
                )}
              </>
            ) : (
              <div className="card p-12 border text-center text-gray-500 bg-base-100">
                <span className="text-4xl mb-2">🧪</span>
                <p>Configure business signals on the left and click "Evaluate Lead" to run the 6-fact engine, test 51 conditions, and generate factual pitch copy.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── TAB 3: CATEGORY REVENUE ESTIMATOR ── */}
      {activeTab === 'revenue' && (
        <div className="revenue-container grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card p-4 border bg-base-100 space-y-4">
            <h3 className="font-bold text-base border-b pb-2">Section 7: Operating Inputs</h3>
            <div>
              <label className="label-text text-xs">Industry Category</label>
              <select 
                className="input input-sm w-full select"
                value={revCategory}
                onChange={(e) => setRevCategory(e.target.value)}
              >
                <option value="RESTAURANT">Restaurant / Dining</option>
                <option value="CLINIC">Clinic / Doctor Practice</option>
                <option value="SALON">Salon / Spa</option>
                <option value="HOTEL">Hotel / Lodging</option>
                <option value="RETAIL">Retail Store</option>
                <option value="MANUFACTURER_EXPORTER">Manufacturer / Exporter</option>
                <option value="OTHER">Review-Velocity Model (Any category)</option>
              </select>
            </div>

            {revCategory === 'RESTAURANT' && (
              <div className="space-y-2 text-xs">
                <div>
                  <label>Seats Count: {revSignals.seats_count}</label>
                  <input 
                    type="range" min="20" max="250" 
                    value={revSignals.seats_count} 
                    onChange={(e) => setRevSignals({...revSignals, seats_count: parseInt(e.target.value)})}
                    className="range range-xs range-primary"
                  />
                </div>
                <div>
                  <label>Average Spend / Cover: ${revSignals.avg_spend_per_cover}</label>
                  <input 
                    type="number" className="input input-sm w-full"
                    value={revSignals.avg_spend_per_cover} 
                    onChange={(e) => setRevSignals({...revSignals, avg_spend_per_cover: parseFloat(e.target.value)})}
                  />
                </div>
              </div>
            )}

            {revCategory === 'CLINIC' && (
              <div className="space-y-2 text-xs">
                <div>
                  <label>Practicing Doctors: {revSignals.doctors_count}</label>
                  <input 
                    type="range" min="1" max="25" 
                    value={revSignals.doctors_count} 
                    onChange={(e) => setRevSignals({...revSignals, doctors_count: parseInt(e.target.value)})}
                    className="range range-xs range-primary"
                  />
                </div>
                <div>
                  <label>Realised Consultation Fee: ${revSignals.realised_consultation_fee}</label>
                  <input 
                    type="number" className="input input-sm w-full"
                    value={revSignals.realised_consultation_fee} 
                    onChange={(e) => setRevSignals({...revSignals, realised_consultation_fee: parseFloat(e.target.value)})}
                  />
                </div>
              </div>
            )}

            {revCategory === 'HOTEL' && (
              <div className="space-y-2 text-xs">
                <div>
                  <label>Rooms Inventory: {revSignals.rooms_count}</label>
                  <input 
                    type="range" min="10" max="200" 
                    value={revSignals.rooms_count} 
                    onChange={(e) => setRevSignals({...revSignals, rooms_count: parseInt(e.target.value)})}
                    className="range range-xs range-primary"
                  />
                </div>
                <div>
                  <label>Average Daily Rate (ADR): ${revSignals.avg_room_rate}</label>
                  <input 
                    type="number" className="input input-sm w-full"
                    value={revSignals.avg_room_rate} 
                    onChange={(e) => setRevSignals({...revSignals, avg_room_rate: parseFloat(e.target.value)})}
                  />
                </div>
              </div>
            )}

            <div className="divider text-xs">Review Velocity Model</div>
            <div className="space-y-2 text-xs">
              <div>
                <label>New Reviews in 90 Days: {revSignals.new_reviews_90d}</label>
                <input 
                  type="number" className="input input-sm w-full"
                  value={revSignals.new_reviews_90d} 
                  onChange={(e) => setRevSignals({...revSignals, new_reviews_90d: parseInt(e.target.value)})}
                />
              </div>
              <div>
                <label>Average Transaction Ticket: ${revSignals.avg_transaction_ticket}</label>
                <input 
                  type="number" className="input input-sm w-full"
                  value={revSignals.avg_transaction_ticket} 
                  onChange={(e) => setRevSignals({...revSignals, avg_transaction_ticket: parseFloat(e.target.value)})}
                />
              </div>
            </div>

            <button 
              className="btn btn-primary w-full mt-4"
              onClick={handleCalculateRevenue}
              disabled={loading}
            >
              {loading ? 'Calculating...' : '💰 Calculate Annual Revenue Range'}
            </button>
          </div>

          <div className="md:col-span-2 space-y-4">
            {revResult ? (
              <div className="card p-6 border bg-base-100 space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="font-bold text-lg">Calibrated Commercial Deal Valuation</h3>
                  <span className={`badge ${
                    revResult.confidence === 'HIGH' ? 'badge-success' :
                    revResult.confidence === 'MEDIUM' ? 'badge-primary' :
                    revResult.confidence === 'LOW' ? 'badge-warning' : 'badge-ghost'
                  }`}>
                    Confidence: {revResult.confidence}
                  </span>
                </div>

                <div className="p-6 bg-base-200 rounded text-center">
                  <div className="text-xs uppercase font-semibold text-gray-500">Estimated Annual Revenue Range</div>
                  <div className="text-3xl font-extrabold text-primary font-mono mt-2">
                    {revResult.min_annual_revenue ? (
                      `$${Math.round(revResult.min_annual_revenue).toLocaleString()} – $${Math.round(revResult.max_annual_revenue).toLocaleString()} ${revResult.currency}`
                    ) : (
                      'UNAVAILABLE (Unbounded Signals)'
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    *Never report a single point estimate. Revenue range reflects an 80% confidence interval.
                  </p>
                </div>

                <div className="p-3 border rounded text-xs space-y-1">
                  <div className="font-bold text-gray-600">Formula Specification:</div>
                  <div className="font-mono bg-base-300 p-2 rounded">{revResult.formula_used}</div>
                  <div className="opacity-80 mt-1">{revResult.notes}</div>
                </div>
              </div>
            ) : (
              <div className="card p-12 border text-center text-gray-500 bg-base-100">
                <span className="text-4xl mb-2">📊</span>
                <p>Select operating parameters on the left and click "Calculate Annual Revenue Range" to view calibrated formula bands.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── TAB 4: 45-CITY BASELINES & REGIONAL PROFILES ── */}
      {activeTab === 'baselines' && (
        <div className="baselines-container space-y-6">
          <div className="card p-4 border bg-base-100">
            <div className="flex flex-wrap gap-4 justify-between items-center mb-4">
              <div>
                <h3 className="font-bold text-base">Section 11.9: Measured Baselines Across 45 Global Cities</h3>
                <p className="text-xs opacity-75">
                  Source: Overture Places 2026-10-21.0 release. Notice correlation: Meta first-source % strongly predicts "no website on file".
                </p>
              </div>
              <input 
                type="text" 
                placeholder="Search city or country..."
                className="input input-sm w-64"
                value={baselineSearch}
                onChange={(e) => setBaselineSearch(e.target.value)}
              />
            </div>

            <div className="overflow-x-auto max-h-96">
              <table className="table table-compact table-zebra w-full text-xs">
                <thead>
                  <tr>
                    <th>City</th>
                    <th>Country</th>
                    <th>Total Places</th>
                    <th>Confident Places</th>
                    <th>Meta First %</th>
                    <th>No Website %</th>
                    <th>Phone %</th>
                    <th>Email %</th>
                    <th>Social %</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredBaselines.map((b) => (
                    <tr key={b.city}>
                      <td className="font-bold">{b.city}</td>
                      <td>{b.country}</td>
                      <td className="font-mono">{b.places.toLocaleString()}</td>
                      <td className="font-mono">{b.confident_places.toLocaleString()}</td>
                      <td className="font-mono font-semibold text-primary">{b.meta_first_pct}%</td>
                      <td className="font-mono font-bold text-warning">{b.confident_no_website_pct}%</td>
                      <td className="font-mono">{b.phone_pct}%</td>
                      <td className="font-mono">{b.email_pct}%</td>
                      <td className="font-mono">{b.social_pct}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Regional Priority Profiles */}
          {profiles && (
            <div className="card p-4 border bg-base-100">
              <h3 className="font-bold text-base mb-3">Section 11.5 & 11.6: Regional Priorities & Source Grounding</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
                {Object.entries(profiles.indian_states).slice(0, 6).map(([code, prof]) => (
                  <div key={code} className="p-3 border rounded bg-base-200">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-bold text-primary">{prof.region_name}</span>
                      <span className="badge badge-xs">{prof.economic_type || 'SERVICES'}</span>
                    </div>
                    <div className="text-[11px] space-y-1">
                      <div><strong className="text-success">Check First ↑:</strong> {prof.check_first.slice(0, 4).join(', ')}</div>
                      <div><strong className="text-error">Trust Less ↓:</strong> {prof.trust_less.slice(0, 1).join(', ')}</div>
                      <div><strong>Local Sources:</strong> {prof.local_sources.slice(0, 2).join(', ')}</div>
                      <div><strong>Languages:</strong> {prof.local_languages.join(', ')}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

