import { useState, useEffect } from 'react'
import './App.css'
import CreateSystemModal from './components/CreateSystemModal'
import EditSystemModal from './components/EditSystemModal'

interface DesignSystem {
  id: string
  name: string
  description: string
  color: string
  path: string
}

const designSystems: DesignSystem[] = [
  {
    id: 'index',
    name: 'Modern Design System',
    description: 'Clean, refined and minimal with good typography',
    color: '#3b82f6',
    path: '/systems/index.html'
  },
  {
    id: 'fresh',
    name: 'FRESH',
    description: 'Bold, modern, and unapologetically vibrant with neon gradients',
    color: '#00f5ff',
    path: '/systems/fresh.html'
  },
  {
    id: 'refined',
    name: 'Studio',
    description: 'Refined, minimal, and sophisticated - Awwwards worthy',
    color: '#8b9d83',
    path: '/systems/refined.html'
  },
  {
    id: 'doodle',
    name: 'Doodle DS',
    description: 'Hand-drawn, sketchy design like Excalidraw',
    color: '#4a90e2',
    path: '/systems/doodle.html'
  },
  {
    id: 'watercolor',
    name: 'Aquarelle',
    description: 'Soft edges and gentle opacity inspired by watercolor paintings',
    color: '#b4a7d6',
    path: '/systems/watercolor.html'
  }
]

function App() {
  const [allSystems, setAllSystems] = useState<DesignSystem[]>(designSystems)
  const [selectedSystem, setSelectedSystem] = useState<DesignSystem>(designSystems[0])
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [iframeKey, setIframeKey] = useState(0)

  // Function to generate a color for a new system
  const generateColor = (index: number): string => {
    const colors = ['#3b82f6', '#00f5ff', '#8b9d83', '#4a90e2', '#b4a7d6', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#ec4899']
    return colors[index % colors.length]
  }

  // Handle successful creation of new design system
  const handleCreateSuccess = (fileName: string, path: string) => {
    const name = fileName.replace('.html', '').replace(/-/g, ' ')
    const newSystem: DesignSystem = {
      id: fileName.replace('.html', ''),
      name: name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
      description: 'Custom generated design system',
      color: generateColor(allSystems.length),
      path: path
    }

    setAllSystems([...allSystems, newSystem])
    setSelectedSystem(newSystem)
  }

  // Handle successful edit of design system
  const handleEditSuccess = () => {
    // Force iframe reload by changing key
    setIframeKey(prev => prev + 1)
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <button
            className="menu-btn"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            aria-label="Toggle sidebar"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
          </button>
          <h1 className="title">Design System Showcase</h1>
          <div className="header-right">
            <button
              className="btn-create"
              onClick={() => setIsCreateModalOpen(true)}
              title="Create new design system"
            >
              + New System
            </button>
            <span className="current-system">{selectedSystem.name}</span>
          </div>
        </div>
      </header>

      <div className="main-container">
        {/* Sidebar */}
        <aside className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
          <div className="sidebar-content">
            <h2 className="sidebar-title">Systems ({allSystems.length})</h2>
            <nav className="nav">
              {allSystems.map((system) => (
                <div key={system.id} className="nav-item-wrapper">
                  <button
                    className={`nav-item ${selectedSystem.id === system.id ? 'active' : ''}`}
                    onClick={() => setSelectedSystem(system)}
                    style={{
                      borderLeftColor: selectedSystem.id === system.id ? system.color : 'transparent'
                    }}
                  >
                    <div className="nav-item-content">
                      <div
                        className="nav-item-indicator"
                        style={{ backgroundColor: system.color }}
                      ></div>
                      <div className="nav-item-text">
                        <div className="nav-item-name">{system.name}</div>
                        <div className="nav-item-description">{system.description}</div>
                      </div>
                    </div>
                  </button>
                  {selectedSystem.id === system.id && (
                    <button
                      className="btn-edit-system"
                      onClick={() => setIsEditModalOpen(true)}
                      title="Edit this design system"
                    >
                      ✎
                    </button>
                  )}
                </div>
              ))}
            </nav>

            <div className="sidebar-footer">
              <p>Built with React + TypeScript + Vite</p>
              <p>{allSystems.length} design systems</p>
            </div>
          </div>
        </aside>

        {/* Main content - iframe */}
        <main className="content">
          <div className="iframe-container">
            <iframe
              key={`${selectedSystem.id}-${iframeKey}`}
              src={selectedSystem.path}
              title={selectedSystem.name}
              className="design-system-frame"
            />
          </div>

          {/* Info overlay */}
          <div className="info-overlay">
            <div className="info-content">
              <h3>{selectedSystem.name}</h3>
              <p>{selectedSystem.description}</p>
              <a
                href={selectedSystem.path}
                target="_blank"
                rel="noopener noreferrer"
                className="open-new-tab"
              >
                Open in new tab →
              </a>
            </div>
          </div>
        </main>
      </div>

      {/* Modals */}
      <CreateSystemModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={handleCreateSuccess}
      />

      <EditSystemModal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        onSuccess={handleEditSuccess}
        fileName={selectedSystem.path.split('/').pop() || ''}
        systemName={selectedSystem.name}
      />
    </div>
  )
}

export default App
