import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'

// Pages
import Dashboard from './pages/Dashboard'
import Catalog from './pages/Catalog'
import AssetDetail from './pages/AssetDetail'
import Glossary from './pages/Glossary'
import CDEs from './pages/CDEs'
import Assessments from './pages/Assessments'
import Gaps from './pages/Gaps'
import Certifications from './pages/Certifications'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1>Enterprise Data Catalog & Governance</h1>
            <nav className="main-nav">
              <a href="/">Dashboard</a>
              <a href="/catalog">Data Catalog</a>
              <a href="/cdes">Critical Data Elements</a>
              <a href="/glossary">Glossary</a>
              <a href="/assessments">Assessments</a>
              <a href="/gaps">Governance Gaps</a>
              <a href="/certifications">Certifications</a>
            </nav>
          </div>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/catalog" element={<Catalog />} />
            <Route path="/assets/:id" element={<AssetDetail />} />
            <Route path="/glossary" element={<Glossary />} />
            <Route path="/cdes" element={<CDEs />} />
            <Route path="/assessments" element={<Assessments />} />
            <Route path="/gaps" element={<Gaps />} />
            <Route path="/certifications" element={<Certifications />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
