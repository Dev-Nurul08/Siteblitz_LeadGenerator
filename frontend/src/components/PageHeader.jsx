/**
 * Page header component
 */
export default function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="page-header">
      <div className="page-header-inner">
        <div>
          <h1 className="page-title">{title}</h1>
          {subtitle && <p className="page-subtitle">{subtitle}</p>}
        </div>
        {actions && <div className="flex gap-3 items-center">{actions}</div>}
      </div>
    </div>
  )
}
