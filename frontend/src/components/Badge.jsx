/**
 * Status badge component
 */

const STATUS_MAP = {
  // Business status
  DISCOVERED: { label: 'Discovered', variant: 'info' },
  ACTIVE: { label: 'Active', variant: 'success' },
  INACTIVE: { label: 'Inactive', variant: 'secondary' },
  DUPLICATE: { label: 'Duplicate', variant: 'warning' },
  INVALID: { label: 'Invalid', variant: 'danger' },
  ARCHIVED: { label: 'Archived', variant: 'secondary' },

  // Website status
  UNKNOWN: { label: 'Unknown', variant: 'secondary' },
  NOT_FOUND: { label: 'No Website', variant: 'danger' },
  SOCIAL_ONLY: { label: 'Social Only', variant: 'warning' },
  FOUND: { label: 'Has Website', variant: 'success' },
  BROKEN: { label: 'Broken', variant: 'danger' },
  UNDER_CONSTRUCTION: { label: 'Under Construction', variant: 'warning' },

  // Job status
  PENDING: { label: 'Pending', variant: 'secondary' },
  RUNNING: { label: 'Running', variant: 'info' },
  COMPLETED: { label: 'Completed', variant: 'success' },
  FAILED: { label: 'Failed', variant: 'danger' },
  CANCELLED: { label: 'Cancelled', variant: 'secondary' },
  PARTIAL: { label: 'Partial', variant: 'warning' },

  // License
  OPEN_LICENSE: { label: 'Open License', variant: 'success' },
  LICENSED_COMMERCIAL: { label: 'Commercial', variant: 'info' },
  API_RESTRICTED: { label: 'API Restricted', variant: 'warning' },
  MANUAL_OR_OPT_IN: { label: 'Manual/Opt-in', variant: 'secondary' },
}

export default function Badge({ status, label, variant }) {
  const mapped = STATUS_MAP[status] || {}
  const finalVariant = variant || mapped.variant || 'secondary'
  const finalLabel = label || mapped.label || status || '—'

  return (
    <span className={`badge badge-${finalVariant}`}>
      {finalLabel}
    </span>
  )
}
