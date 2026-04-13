import React, { useState, useCallback } from 'react'
import StatusBar from './components/StatusBar'
import AddComplaint from './components/AddComplaint'
import SearchPanel from './components/SearchPanel'
import AskPanel from './components/AskPanel'
import styles from './App.module.css'

type Tab = 'ask' | 'search' | 'add'

const TABS: { id: Tab; label: string; icon: string; badge: string }[] = [
  { id: 'ask',    label: 'AI Chat',        icon: '✦', badge: 'RAG' },
  { id: 'search', label: 'Semantic Search', icon: '⌕', badge: 'Endee' },
  { id: 'add',    label: 'Add Complaint',   icon: '+', badge: 'Ingest' },
]

export default function App() {
  const [tab, setTab] = useState<Tab>('ask')
  // increment to force StatusBar to re-fetch /health after a complaint is added
  const [refreshKey, setRefreshKey] = useState(0)

  const onAdded = useCallback(() => setRefreshKey(k => k + 1), [])

  return (
    <div className={styles.shell}>

      {/* Sticky top bar showing backend health */}
      <StatusBar key={refreshKey} />

      {/* Hero header */}
      <header className={styles.hero}>
        <div className={styles.heroInner}>
          <p className={styles.heroBadge}>
            <span className={styles.badgeDot} />
            Powered by Endee Vector Database
          </p>
          <h1 className={styles.heroTitle}>
            AI Complaint<br />
            <span className={styles.heroAccent}>Assistant</span>
          </h1>
          <p className={styles.heroSub}>
            Semantic search and RAG-based analysis over customer complaints.
            Embeddings stored in Endee. Answers from FLAN-T5.
          </p>

          {/* Architecture flow */}
          <div className={styles.arch}>
            {['User Query', 'SentenceTransformer', 'Endee DB', 'FLAN-T5', 'Response'].map(
              (step, i, arr) => (
                <React.Fragment key={step}>
                  <span className={styles.archStep}>{step}</span>
                  {i < arr.length - 1 && (
                    <span className={styles.archArrow}>→</span>
                  )}
                </React.Fragment>
              )
            )}
          </div>
        </div>
      </header>

      {/* Tab navigation */}
      <nav className={styles.tabs} role="tablist">
        {TABS.map(t => (
          <button
            key={t.id}
            role="tab"
            aria-selected={tab === t.id}
            className={`${styles.tab} ${tab === t.id ? styles.tabActive : ''}`}
            onClick={() => setTab(t.id)}
          >
            <span className={styles.tabIcon}>{t.icon}</span>
            <span className={styles.tabLabel}>{t.label}</span>
            <span className={styles.tabBadge}>{t.badge}</span>
          </button>
        ))}
      </nav>

      {/* Page content */}
      <main className={styles.main} role="tabpanel">
        {tab === 'ask'    && <AskPanel />}
        {tab === 'search' && <SearchPanel />}
        {tab === 'add'    && <AddComplaint onAdded={onAdded} />}
      </main>

      <footer className={styles.footer}>
        <span>AI Complaint Assistant</span>
        <span className={styles.dot}>·</span>
        <span>Endee + SentenceTransformers + FLAN-T5</span>
        <span className={styles.dot}>·</span>
        <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
          API Docs ↗
        </a>
      </footer>

    </div>
  )
}
