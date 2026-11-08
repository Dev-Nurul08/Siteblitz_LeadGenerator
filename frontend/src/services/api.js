/**
 * API client for SiteBlitz Lead Intelligence OS
 * Communicates with FastAPI backend via Vite proxy (/api and /health)
 */

async function request(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  const res = await fetch(endpoint, {
    ...options,
    headers,
  })

  if (!res.ok) {
    let errorDetail = `Request failed (${res.status})`
    try {
      const err = await res.json()
      errorDetail = err.detail || err.message || errorDetail
    } catch (_) {}
    throw new Error(errorDetail)
  }

  return res.json()
}

export const api = {
  health: async () => {
    const res = await fetch('/health')
    if (!res.ok) throw new Error('Backend offline')
    return res.json()
  },

  businesses: {
    list: async (params = {}) => {
      const query = new URLSearchParams()
      for (const [key, val] of Object.entries(params)) {
        if (val !== undefined && val !== null && val !== '') {
          query.append(key, val)
        }
      }
      const qs = query.toString()
      return request(`/api/v1/businesses${qs ? `?${qs}` : ''}`)
    },
    get: async (id) => request(`/api/v1/businesses/${id}`),
    update: async (id, data) => request(`/api/v1/businesses/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    stats: async () => request('/api/v1/businesses/stats/overview'),
  },

  sources: {
    list: async () => request('/api/v1/sources'),
    get: async (id) => request(`/api/v1/sources/${id}`),
    create: async (data) => request('/api/v1/sources', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: async (id, data) => request(`/api/v1/sources/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    jobs: async (sourceId, limit = 20) => request(`/api/v1/sources/${sourceId}/jobs?limit=${limit}`),
  },

  discovery: {
    run: async (payload) => request('/api/v1/discovery/run', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
    importCsv: async (file, countryCode = '', delimiter = ',') => {
      const formData = new FormData()
      formData.append('file', file)
      if (countryCode) formData.append('country_code', countryCode)
      formData.append('delimiter', delimiter)

      const res = await fetch('/api/v1/discovery/import-csv', {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        let errorDetail = `Upload failed (${res.status})`
        try {
          const err = await res.json()
          errorDetail = err.detail || err.message || errorDetail
        } catch (_) {}
        throw new Error(errorDetail)
      }

      return res.json()
    },
    jobs: async (limit = 20) => request(`/api/v1/discovery/jobs?limit=${limit}`),
    jobStatus: async (jobId) => request(`/api/v1/discovery/jobs/${jobId}`),
  },

  opportunities: {
    list: async (params = {}) => {
      const query = new URLSearchParams()
      for (const [key, val] of Object.entries(params)) {
        if (val !== undefined && val !== null && val !== '') {
          query.append(key, val)
        }
      }
      const qs = query.toString()
      return request(`/api/v1/opportunities${qs ? `?${qs}` : ''}`)
    },
    get: async (id) => request(`/api/v1/opportunities/${id}`),
    update: async (id, data) => request(`/api/v1/opportunities/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    stats: async () => request('/api/v1/opportunities/stats/overview'),
    evaluate: async (businessId) => request(`/api/v1/opportunities/evaluate-business/${businessId}`, {
      method: 'POST',
    }),
    batchEvaluate: async (limit = 25) => request(`/api/v1/opportunities/batch-evaluate?limit=${limit}`, {
      method: 'POST',
    }),
    audits: async (businessId) => request(`/api/v1/opportunities/audits/${businessId}`),
  },

  contacts: {
    list: async (params = {}) => {
      const q = new URLSearchParams()
      if (params.page) q.set('page', params.page)
      if (params.pageSize) q.set('page_size', params.pageSize)
      if (params.roleLevel) q.set('role_level', params.roleLevel)
      if (params.emailStatus) q.set('email_status', params.emailStatus)
      if (params.minScore) q.set('min_score', params.minScore)
      if (params.search) q.set('search', params.search)
      if (params.businessId) q.set('business_id', params.businessId)
      return request(`/api/v1/contacts?${q.toString()}`)
    },
    stats: async () => request('/api/v1/contacts/stats/overview'),
    enrichBusiness: async (businessId) => request(`/api/v1/contacts/enrich-business/${businessId}`, {
      method: 'POST',
    }),
    batchEnrich: async (limit = 25) => request(`/api/v1/contacts/batch-enrich?limit=${limit}`, {
      method: 'POST',
    }),
    verifyEmail: async (email) => request('/api/v1/contacts/verify-email', {
      method: 'POST',
      body: JSON.stringify({ email }),
    }),
  },

  qualification: {
    listLeads: async (params = {}) => {
      const q = new URLSearchParams()
      if (params.page) q.set('page', params.page)
      if (params.pageSize) q.set('page_size', params.pageSize)
      if (params.status) q.set('status', params.status)
      if (params.minScore) q.set('min_score', params.minScore)
      if (params.country) q.set('country', params.country)
      if (params.search) q.set('search', params.search)
      return request(`/api/v1/qualification/leads?${q.toString()}`)
    },
    getLead: async (id) => request(`/api/v1/qualification/leads/${id}`),
    stats: async () => request('/api/v1/qualification/leads/stats/overview'),
    updateStatus: async (id, data) => request(`/api/v1/qualification/leads/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    qualifyBusiness: async (businessId) => request(`/api/v1/qualification/qualify-business/${businessId}`, {
      method: 'POST',
    }),
    batchQualify: async (limit = 25) => request(`/api/v1/qualification/batch-qualify?limit=${limit}`, {
      method: 'POST',
    }),
    listOptOuts: async (params = {}) => {
      const q = new URLSearchParams()
      if (params.page) q.set('page', params.page)
      if (params.pageSize) q.set('page_size', params.pageSize)
      if (params.search) q.set('search', params.search)
      return request(`/api/v1/qualification/opt-outs?${q.toString()}`)
    },
    addOptOut: async (data) => request('/api/v1/qualification/opt-outs', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  },

  campaigns: {
    list: async () => request('/api/v1/campaigns'),
    get: async (id) => request(`/api/v1/campaigns/${id}`),
    create: async (data) => request('/api/v1/campaigns', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    enroll: async (id, limit = 50) => request(`/api/v1/campaigns/${id}/enroll?limit=${limit}`, {
      method: 'POST',
    }),
    dispatch: async (id, batchSize = 10) => request(`/api/v1/campaigns/${id}/dispatch?batch_size=${batchSize}`, {
      method: 'POST',
    }),
    getPipeline: async () => request('/api/v1/campaigns/pipeline/crm'),
    updateDealStage: async (dealId, data) => request(`/api/v1/campaigns/pipeline/crm/${dealId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    simulateReply: async (data) => request('/api/v1/campaigns/replies/simulate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    getFunnel: async () => request('/api/v1/campaigns/analytics/funnel'),
  },

  leadRadar: {
    evaluate: async (data) => request('/api/v1/lead-radar/evaluate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    absenceCertificate: async (data) => request('/api/v1/lead-radar/absence-certificate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    revenueEstimate: async (data) => request('/api/v1/lead-radar/revenue-estimate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    mumbaiFunnel: async (data = {}) => request('/api/v1/lead-radar/mumbai-funnel', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    cityBaselines: async () => request('/api/v1/lead-radar/regions/baselines'),
    cityBaseline: async (city) => request(`/api/v1/lead-radar/regions/baselines/${encodeURIComponent(city)}`),
    regionalProfiles: async () => request('/api/v1/lead-radar/regions/profiles'),
    evaluations: async (params = {}) => {
      const q = new URLSearchParams()
      if (params.segment) q.set('segment', params.segment)
      if (params.recipe) q.set('recipe', params.recipe)
      if (params.limit) q.set('limit', params.limit)
      const qs = q.toString()
      return request(`/api/v1/lead-radar/evaluations${qs ? `?${qs}` : ''}`)
    },
  },
}

export default api
