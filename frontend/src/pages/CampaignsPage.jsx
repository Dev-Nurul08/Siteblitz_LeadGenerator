import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import StatCard from '../components/StatCard'
import Badge from '../components/Badge'
import api from '../services/api'

const STAGES = [
  { id: 'PROSPECT', label: 'Prospect', icon: '🎯', color: 'var(--color-text-secondary)' },
  { id: 'CONTACTED', label: 'Contacted', icon: '📨', color: 'var(--color-accent-info)' },
  { id: 'MEETING_SCHEDULED', label: 'Meeting Set', icon: '📅', color: 'var(--color-accent-primary)' },
  { id: 'PROPOSAL_SENT', label: 'Proposal Sent', icon: '📋', color: 'var(--color-accent-warning)' },
  { id: 'NEGOTIATION', label: 'Negotiation', icon: '🤝', color: 'var(--color-accent-secondary)' },
  { id: 'WON', label: 'Closed Won', icon: '🏆', color: 'var(--color-accent-success)' },
  { id: 'LOST', label: 'Lost / Closed', icon: '📁', color: 'var(--color-text-muted)' },
]

export default function CampaignsPage() {
  const [activeTab, setActiveTab] = useState('pipeline') // 'pipeline' | 'campaigns'
  const [pipeline, setPipeline] = useState(null)
  const [campaigns, setCampaigns] = useState([])
  const [funnel, setFunnel] = useState(null)
  const [loading, setLoading] = useState(false)

  // Actions state
  const [enrolling, setEnrolling] = useState(false)
  const [dispatching, setDispatching] = useState(false)

  // New Campaign Modal
  const [showNewCampaignModal, setShowNewCampaignModal] = useState(false)
  const [campaignName, setCampaignName] = useState('')
  const [campaignTarget, setCampaignTarget] = useState('WEBSITE_REDESIGN')
  const [campaignLimit, setCampaignLimit] = useState(50)
  const [creatingCampaign, setCreatingCampaign] = useState(false)

  // Reply Simulator Modal
  const [showReplyModal, setShowReplyModal] = useState(false)
  const [replyMessageId, setReplyMessageId] = useState(1)
  const [replyText, setReplyText] = useState('')
  const [replyLoading, setReplyLoading] = useState(false)
  const [replyResult, setReplyResult] = useState(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    setLoading(true)
    try {
      const [pipeData, campData, funnelData] = await Promise.all([
        api.campaigns.getPipeline().catch(() => null),
        api.campaigns.list().catch(() => ({ items: [] })),
        api.campaigns.getFunnel().catch(() => null),
      ])
      setPipeline(pipeData)
      setCampaigns(campData.items || [])
      setFunnel(funnelData)
    } catch (e) {
      console.error('Failed to load campaigns data:', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleCreateCampaign(e) {
    e.preventDefault()
    if (!campaignName.trim()) return
    setCreatingCampaign(true)
    try {
      await api.campaigns.create({
        name: campaignName.trim(),
        target_service_category: campaignTarget,
        daily_send_limit: Number(campaignLimit),
      })
      setShowNewCampaignModal(false)
      setCampaignName('')
      await loadData()
    } catch (err) {
      alert(`Create campaign error: ${err.message}`)
    } finally {
      setCreatingCampaign(false)
    }
  }

  async function handleEnrollLeads(campaignId) {
    setEnrolling(true)
    try {
      const res = await api.campaigns.enroll(campaignId, 50)
      alert(`Successfully enrolled ${res.enrolled_count} qualified leads into schedule!`)
      await loadData()
    } catch (err) {
      alert(`Enroll error: ${err.message}`)
    } finally {
      setEnrolling(false)
    }
  }

  async function handleDispatchBatch(campaignId) {
    setDispatching(true)
    try {
      const res = await api.campaigns.dispatch(campaignId, 10)
      alert(`Dispatched ${res.dispatched_count} messages across rotating mailboxes!`)
      await loadData()
    } catch (err) {
      alert(`Dispatch error: ${err.message}`)
    } finally {
      setDispatching(false)
    }
  }

  async function handleMoveDealStage(dealId, newStage) {
    try {
      await api.campaigns.updateDealStage(dealId, { stage: newStage })
      await loadData()
    } catch (err) {
      alert(`Stage update error: ${err.message}`)
    }
  }

  async function handleSimulateReply(e) {
    e.preventDefault()
    if (!replyText.trim()) return
    setReplyLoading(true)
    setReplyResult(null)
    try {
      const res = await api.campaigns.simulateReply({
        message_id: Number(replyMessageId),
        reply_text: replyText.trim(),
      })
      setReplyResult(res)
      await loadData()
    } catch (err) {
      alert(`Simulation error: ${err.message}`)
    } finally {
      setReplyLoading(false)
    }
  }

  const PRESET_REPLIES = [
    { label: '💰 Interested (Pricing)', text: "Hi, sounds interesting. Can you send over your pricing and packages?" },
    { label: '📅 Interested (Demo)', text: "Let's discuss next Tuesday at 2pm. Can you share a calendar link?" },
    { label: '🚫 Unsubscribe (Opt-out)', text: "Please remove our company from your list immediately and do not contact us again." },
    { label: '✋ Not Interested', text: "No thank you, we already have an internal development agency." },
    { label: '🌴 Out of Office', text: "I am out of the office on annual leave returning next Monday." },
  ]

  return (
    <div className="page-container">
      <PageHeader
        title="Conversion Engine & Pipeline"
        subtitle="Phase 5: Outreach Orchestration, Throttled Multi-Mailbox Delivery, CRM Pipeline & Reply Classifier"
        actions={
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowReplyModal(true)
                setReplyResult(null)
              }}
            >
              <span style={{ marginRight: '6px' }}>🤖</span>
              Inbound Reply Sandbox
            </button>
            <button
              className="btn btn-primary"
              onClick={() => setShowNewCampaignModal(true)}
            >
              <span style={{ marginRight: '6px' }}>➕</span>
              New Campaign
            </button>
          </div>
        }
      />

      {/* Conversion Funnel Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--color-text-primary)' }}>
              Full-Lifecycle Conversion Funnel
            </span>
            <div style={{ fontSize: '0.8rem', color: 'var(--color-text-secondary)', marginTop: '2px' }}>
              Phase 1 Discovery → Phase 2 Audit → Phase 3 Enrichment → Phase 4 Qualification → Phase 5 Closed Revenue
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--color-accent-success)' }}>
              ${funnel?.revenue_won?.toLocaleString() || '0'}
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>Closed Revenue Won</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '0.5rem', textAlign: 'center' }}>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Ph. 1 Discovered</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>
              {funnel?.funnel?.phase1_discovered_businesses || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Ph. 2 Audited</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>
              {funnel?.funnel?.phase2_identified_opportunities || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Ph. 3 Enriched</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>
              {funnel?.funnel?.phase3_enriched_contacts || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Ph. 4 Qualified</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>
              {funnel?.funnel?.phase4_qualified_leads || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Dispatched</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px', color: 'var(--color-accent-info)' }}>
              {funnel?.funnel?.phase5_sent_messages || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Replied</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px', color: 'var(--color-accent-warning)' }}>
              {funnel?.funnel?.phase5_replied_prospects || 0}
            </div>
          </div>
          <div style={{ background: 'var(--color-bg-primary)', padding: '0.6rem 0.4rem', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>Deals Won</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 800, marginTop: '2px', color: 'var(--color-accent-success)' }}>
              {funnel?.funnel?.phase5_deals_won || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--color-border)', paddingBottom: '0.5rem' }}>
        <button
          className={`btn ${activeTab === 'pipeline' ? 'btn-primary' : 'btn-ghost'}`}
          onClick={() => setActiveTab('pipeline')}
        >
          <span>💼</span> CRM Sales Pipeline ({pipeline?.total_deals || 0})
        </button>
        <button
          className={`btn ${activeTab === 'campaigns' ? 'btn-primary' : 'btn-ghost'}`}
          onClick={() => setActiveTab('campaigns')}
        >
          <span>🚀</span> Campaigns & Dispatchers ({campaigns.length})
        </button>
      </div>

      {/* TAB 1: CRM Sales Pipeline Kanban */}
      {activeTab === 'pipeline' && (
        <div style={{ overflowX: 'auto', paddingBottom: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, minmax(240px, 1fr))', gap: '1rem', minWidth: '1200px' }}>
            {STAGES.map((stg) => {
              const deals = pipeline?.stages?.[stg.id] || []
              const columnSum = deals.reduce((acc, d) => acc + (d.estimated_value || 0), 0)

              return (
                <div
                  key={stg.id}
                  style={{
                    background: 'var(--color-bg-secondary)',
                    borderRadius: '10px',
                    border: '1px solid var(--color-border)',
                    display: 'flex',
                    flexDirection: 'column',
                    minHeight: '480px',
                  }}
                >
                  {/* Column Header */}
                  <div style={{ padding: '0.85rem 1rem', borderBottom: '1px solid var(--color-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span>{stg.icon}</span>
                      <span style={{ fontWeight: 600, fontSize: '0.9rem', color: stg.color }}>{stg.label}</span>
                      <span className="badge badge-secondary" style={{ fontSize: '0.72rem', padding: '0.1rem 0.4rem' }}>
                        {deals.length}
                      </span>
                    </div>
                    {columnSum > 0 && (
                      <div style={{ fontSize: '0.78rem', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)' }}>
                        ${Math.round(columnSum).toLocaleString()}
                      </div>
                    )}
                  </div>

                  {/* Deals Cards */}
                  <div style={{ padding: '0.75rem', flex: 1, display: 'flex', flexDirection: 'column', gap: '0.75rem', overflowY: 'auto', maxHeight: '600px' }}>
                    {deals.length === 0 ? (
                      <div style={{ textAlign: 'center', padding: '2rem 0.5rem', color: 'var(--color-text-muted)', fontSize: '0.8rem' }}>
                        No deals in this stage
                      </div>
                    ) : (
                      deals.map((deal) => (
                        <div
                          key={deal.id}
                          className="card"
                          style={{
                            padding: '0.85rem',
                            background: 'var(--color-bg-card)',
                            border: '1px solid var(--color-border)',
                            borderRadius: '8px',
                            cursor: 'default',
                          }}
                        >
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                            <div style={{ fontWeight: 600, fontSize: '0.92rem', color: 'var(--color-text-primary)' }}>
                              {deal.business_name}
                            </div>
                            <span style={{ fontSize: '0.8rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--color-accent-success)' }}>
                              ${deal.estimated_value?.toLocaleString()}
                            </span>
                          </div>

                          <div style={{ fontSize: '0.78rem', color: 'var(--color-text-secondary)', marginBottom: '0.6rem' }}>
                            {deal.title}
                          </div>

                          {deal.notes && (
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', background: 'var(--color-bg-primary)', padding: '0.4rem', borderRadius: '4px', marginBottom: '0.6rem' }}>
                              📝 {deal.notes}
                            </div>
                          )}

                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--color-border)', paddingTop: '0.5rem', fontSize: '0.75rem' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>
                              Score: {Math.round(deal.lead_score || 0)}%
                            </span>

                            {/* Move Stage Selector */}
                            <select
                              value={deal.stage}
                              onChange={(e) => handleMoveDealStage(deal.id, e.target.value)}
                              style={{
                                background: 'var(--color-bg-tertiary)',
                                color: 'var(--color-text-primary)',
                                border: '1px solid var(--color-border)',
                                borderRadius: '4px',
                                fontSize: '0.75rem',
                                padding: '0.2rem 0.4rem',
                              }}
                            >
                              {STAGES.map((s) => (
                                <option key={s.id} value={s.id}>
                                  Move: {s.label}
                                </option>
                              ))}
                            </select>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* TAB 2: Campaigns & Dispatchers */}
      {activeTab === 'campaigns' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {campaigns.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3.5rem 1rem' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>🚀</div>
              <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>No Active Campaigns</div>
              <p style={{ color: 'var(--color-text-secondary)', maxWidth: '400px', margin: '0 auto 1.5rem' }}>
                Create a campaign with humanized sending schedules, randomized jitter delays, and multi-mailbox rotation.
              </p>
              <button className="btn btn-primary" onClick={() => setShowNewCampaignModal(true)}>
                Create First Campaign
              </button>
            </div>
          ) : (
            campaigns.map((camp) => (
              <div key={camp.id} className="card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <h3 style={{ margin: 0, fontSize: '1.2rem' }}>{camp.name}</h3>
                      <Badge variant={camp.status === 'RUNNING' ? 'success' : 'secondary'} label={camp.status} />
                      {camp.target_service_category && (
                        <span className="badge badge-secondary">{camp.target_service_category.replace(/_/g, ' ')}</span>
                      )}
                    </div>
                    {camp.description && (
                      <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem', margin: '4px 0 0' }}>
                        {camp.description}
                      </p>
                    )}
                  </div>

                  <div style={{ display: 'flex', gap: '0.75rem' }}>
                    <button
                      className="btn btn-secondary"
                      onClick={() => handleEnrollLeads(camp.id)}
                      disabled={enrolling}
                    >
                      {enrolling ? 'Enrolling...' : '👥 Enroll Qualified Leads (50)'}
                    </button>
                    <button
                      className="btn btn-primary"
                      onClick={() => handleDispatchBatch(camp.id)}
                      disabled={dispatching}
                    >
                      {dispatching ? (
                        <>
                          <span className="spinner" style={{ marginRight: '6px' }} />
                          Dispatching...
                        </>
                      ) : (
                        '⚡ Dispatch Next Batch (10)'
                      )}
                    </button>
                  </div>
                </div>

                {/* Performance Metrics Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1rem', background: 'var(--color-bg-primary)', padding: '0.85rem', borderRadius: '8px', fontSize: '0.85rem' }}>
                  <div>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>Enrolled Leads</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>{camp.total_leads_count}</div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>Dispatched Messages</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px', color: 'var(--color-accent-info)' }}>
                      {camp.sent_count}
                    </div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>Inbound Replies</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px', color: 'var(--color-accent-warning)' }}>
                      {camp.replied_count}
                    </div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>Converted Leads</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px', color: 'var(--color-accent-success)' }}>
                      {camp.converted_count}
                    </div>
                  </div>
                  <div>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>Daily Throttle Limit</div>
                    <div style={{ fontSize: '1.1rem', fontWeight: 700, marginTop: '2px' }}>{camp.daily_send_limit} / day</div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Modal: New Campaign */}
      {showNewCampaignModal && (
        <div className="modal-backdrop" onClick={() => setShowNewCampaignModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '520px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ margin: 0 }}>Create Outbound Campaign</h3>
              <button className="btn btn-ghost" onClick={() => setShowNewCampaignModal(false)} style={{ padding: '0.25rem 0.5rem' }}>
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateCampaign} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', display: 'block', marginBottom: '4px' }}>
                  Campaign Name:
                </label>
                <input
                  type="text"
                  required
                  className="input-field"
                  placeholder="e.g. Q4 Modernization Sprint"
                  value={campaignName}
                  onChange={(e) => setCampaignName(e.target.value)}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', display: 'block', marginBottom: '4px' }}>
                  Target Opportunity Category:
                </label>
                <select
                  className="input-field"
                  value={campaignTarget}
                  onChange={(e) => setCampaignTarget(e.target.value)}
                >
                  <option value="NEW_WEBSITE">🌐 New Website</option>
                  <option value="WEBSITE_REDESIGN">🔄 Website Redesign</option>
                  <option value="MOBILE_APP">📱 Mobile App</option>
                  <option value="ECOMMERCE_EXPANSION">🛒 E-Commerce Expansion</option>
                  <option value="ONLINE_BOOKING">📅 Online Booking Engine</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', display: 'block', marginBottom: '4px' }}>
                  Daily Send Throttle (Prevents Mailbox Burn):
                </label>
                <input
                  type="number"
                  min="10"
                  max="150"
                  className="input-field"
                  value={campaignLimit}
                  onChange={(e) => setCampaignLimit(e.target.value)}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowNewCampaignModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={creatingCampaign}>
                  {creatingCampaign ? 'Creating...' : 'Launch Campaign'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal: Inbound Reply Simulator */}
      {showReplyModal && (
        <div className="modal-backdrop" onClick={() => setShowReplyModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '620px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.4rem' }}>🤖</span>
                <h3 style={{ margin: 0 }}>Inbound Reply Intent Classifier</h3>
              </div>
              <button className="btn btn-ghost" onClick={() => setShowReplyModal(false)} style={{ padding: '0.25rem 0.5rem' }}>
                ✕
              </button>
            </div>

            <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem', marginBottom: '1rem' }}>
              Simulate an incoming response from a prospect to test instant sentiment classification, automatic CRM deal advancement, and suppression list enforcement.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '1rem' }}>
              {PRESET_REPLIES.map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="btn btn-secondary"
                  style={{ fontSize: '0.78rem', padding: '0.3rem 0.6rem' }}
                  onClick={() => setReplyText(p.text)}
                >
                  {p.label}
                </button>
              ))}
            </div>

            <form onSubmit={handleSimulateReply} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <textarea
                rows={4}
                required
                className="input-field"
                placeholder="Enter email response text..."
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                style={{ fontFamily: 'var(--font-family)', lineHeight: '1.5' }}
              />

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                  Targeting Outreach Message #{replyMessageId}
                </div>
                <button type="submit" className="btn btn-primary" disabled={replyLoading}>
                  {replyLoading ? 'Analyzing...' : 'Simulate & Classify'}
                </button>
              </div>
            </form>

            {replyResult && (
              <div style={{ marginTop: '1.25rem', background: 'var(--color-bg-primary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', borderBottom: '1px solid var(--color-border)', paddingBottom: '0.5rem' }}>
                  <div style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>
                    Intent Classification:
                  </div>
                  <span className={`badge ${replyResult.intent === 'INTERESTED' ? 'badge-success' : replyResult.intent === 'UNSUBSCRIBE_REQUEST' ? 'badge-danger' : 'badge-warning'}`}>
                    {replyResult.intent} ({Math.round(replyResult.confidence * 100)}%)
                  </span>
                </div>
                <div style={{ fontSize: '0.85rem', color: 'var(--color-text-secondary)', lineHeight: '1.5' }}>
                  {replyResult.action_summary}
                </div>
                {replyResult.recommended_stage && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.82rem', color: 'var(--color-accent-primary)' }}>
                    ➔ CRM Deal Stage Updated to: <strong>{replyResult.recommended_stage}</strong>
                  </div>
                )}
                {replyResult.suppressed && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.82rem', color: 'var(--color-accent-danger)' }}>
                    🛡️ Automatically registered in Global Suppression Registry
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
