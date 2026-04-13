import React, { useState } from 'react'
import { searchComplaints, ComplaintResult } from '../utils/api'
import ComplaintCard from './ComplaintCard'
import styles from './SearchPanel.module.css'

const CATEGORIES = ['delivery', 'billing', 'product', 'support', 'account', 'returns', 'general']

export default function SearchPanel() {
  const [query, setQuery]               = useState('')
  const [category, setCategory]         = useState('')
  const [topK, setTopK]                 = useState(5)
  const [loading, setLoading]           = useState(false)
  const [results, setResults]           = useState<ComplaintResult[] | null>(null)
  const [searchedQuery, setSearchedQuery] = useState('')
  const [error, setError]               = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    const q = query.trim()
    if (!q) return
    setLoading(true)
    setError(null)
    try {
      const res = await searchComplaints({
        query: q,
        top_k: topK,
        category_filter: category || undefined,
      })
      setResults(res.results)
      setSearchedQuery(res.query)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Search failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className={styles.panel}>
      <header className={styles.head}>
        <span className={styles.icon}>⌕</span>
        <div>
          <h2 className={styles.title}>Semantic Search</h2>
          <p className={styles.sub}>Endee cosine-similarity over all stored embeddings</p>
        </div>
      </header>

      {/* Search form */}
      <form onSubmit={handleSearch} className={styles.form}>
        <div className={styles.searchRow}>
          <input
            type="text"
            className={styles.queryInput}
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="e.g. late delivery damaged package…"
            required
          />
          <button
            type="submit"
            className={styles.searchBtn}
            disabled={loading || !query.trim()}
          >
            {loading ? <span className={styles.spinner} /> : 'Search'}
          </button>
        </div>

        <div className={styles.filterRow}>
          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Category</label>
            <select
              className={styles.select}
              value={category}
              onChange={e => setCategory(e.target.value)}
            >
              <option value="">All</option>
              {CATEGORIES.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div className={styles.filterGroup}>
            <label className={styles.filterLabel}>Top-K</label>
            <select
              className={styles.select}
              value={topK}
              onChange={e => setTopK(Number(e.target.value))}
            >
              {[3, 5, 8, 10].map(n => (
                <option key={n} value={n}>{n} results</option>
              ))}
            </select>
          </div>
        </div>
      </form>

      {/* Error */}
      {error && <p className={styles.error}>{error}</p>}

      {/* Results */}
      {results !== null && (
        <div className={styles.results}>
          <div className={styles.resultsHeader}>
            <span className={styles.resultsCount}>
              {results.length} result{results.length !== 1 ? 's' : ''}
            </span>
            <span className={styles.resultsFor}>for</span>
            <span className={styles.resultsQuery}>"{searchedQuery}"</span>
          </div>

          {results.length === 0 ? (
            <p className={styles.empty}>
              No similar complaints found. Try a different query or add more complaints.
            </p>
          ) : (
            <div className={styles.list}>
              {results.map((r, i) => (
                <ComplaintCard key={r.id} result={r} rank={i + 1} animate />
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  )
}
