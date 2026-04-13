import React, { useState } from 'react'
import { addComplaint } from '../utils/api'
import styles from './AddComplaint.module.css'

const CATEGORIES = ['general', 'delivery', 'billing', 'product', 'support', 'account', 'returns']

interface Props {
  onAdded: () => void
}

export default function AddComplaint({ onAdded }: Props) {
  const [text, setText]           = useState('')
  const [category, setCategory]   = useState('general')
  const [customerId, setCustomerId] = useState('')
  const [loading, setLoading]     = useState(false)
  const [success, setSuccess]     = useState<string | null>(null)
  const [error, setError]         = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = text.trim()
    if (!trimmed) return
    setLoading(true)
    setError(null)
    setSuccess(null)
    try {
      const res = await addComplaint({
        text: trimmed,
        category,
        customer_id: customerId.trim() || undefined,
      })
      setSuccess(`Stored in Endee — ID: ${res.id.slice(0, 8)}…`)
      setText('')
      setCustomerId('')
      onAdded()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Failed to add complaint. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className={styles.panel}>
      <header className={styles.head}>
        <span className={styles.icon}>+</span>
        <div>
          <h2 className={styles.title}>Ingest Complaint</h2>
          <p className={styles.sub}>
            Text → SentenceTransformer embedding → stored in Endee
          </p>
        </div>
      </header>

      <form onSubmit={handleSubmit} className={styles.form}>

        {/* Complaint text */}
        <div className={styles.field}>
          <label className={styles.label} htmlFor="complaint-text">
            Complaint text <span className={styles.required}>*</span>
          </label>
          <textarea
            id="complaint-text"
            className={styles.textarea}
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder="Describe the customer complaint in plain language…"
            rows={5}
            maxLength={2000}
            required
          />
          <span className={styles.charCount}>{text.length} / 2000</span>
        </div>

        {/* Category + Customer ID row */}
        <div className={styles.row}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="category">Category</label>
            <select
              id="category"
              className={styles.select}
              value={category}
              onChange={e => setCategory(e.target.value)}
            >
              {CATEGORIES.map(c => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div className={styles.field}>
            <label className={styles.label} htmlFor="customer-id">
              Customer ID <span className={styles.optional}>(optional)</span>
            </label>
            <input
              id="customer-id"
              type="text"
              className={styles.input}
              value={customerId}
              onChange={e => setCustomerId(e.target.value)}
              placeholder="cust_123"
            />
          </div>
        </div>

        {/* Feedback */}
        {success && <p className={styles.success}>{success}</p>}
        {error   && <p className={styles.error}>{error}</p>}

        <button
          type="submit"
          className={styles.btn}
          disabled={loading || !text.trim()}
        >
          {loading
            ? <><span className={styles.spinner} /> Embedding &amp; storing…</>
            : 'Store in Endee →'}
        </button>

      </form>
    </section>
  )
}
