import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import BusinessesPage from './pages/BusinessesPage'
import DiscoveryPage from './pages/DiscoveryPage'
import SourcesPage from './pages/SourcesPage'
import OpportunitiesPage from './pages/OpportunitiesPage'
import ContactsPage from './pages/ContactsPage'
import QualificationPage from './pages/QualificationPage'
import CampaignsPage from './pages/CampaignsPage'
import Sidebar from './components/Sidebar'

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard': return <Dashboard onNavigate={setCurrentPage} />
      case 'businesses': return <BusinessesPage onNavigate={setCurrentPage} />
      case 'discovery': return <DiscoveryPage onNavigate={setCurrentPage} />
      case 'sources': return <SourcesPage onNavigate={setCurrentPage} />
      case 'opportunities': return <OpportunitiesPage onNavigate={setCurrentPage} />
      case 'contacts': return <ContactsPage onNavigate={setCurrentPage} />
      case 'qualification':
      case 'compliance':
        return <QualificationPage onNavigate={setCurrentPage} />
      case 'campaigns':
      case 'outreach':
        return <CampaignsPage onNavigate={setCurrentPage} />
      default: return <Dashboard onNavigate={setCurrentPage} />
    }
  }

  return (
    <div className="app-layout">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  )
}
