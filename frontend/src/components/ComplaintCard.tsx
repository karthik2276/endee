import React from 'react'
import { ComplaintResult } from '../utils/api'
import styles from './ComplaintCard.module.css'

const CATEGORY_COLORS: Record<string, string> = {
  delivery: '#3b82f6',
  billing:  '#f59e0b',
  product:  '#8b5cf6',
  support:  '#06b6d4',
  account:  '#10b981',
  returns:  '#ec4899',
  general:  '#6b7280',
}

interface Props {
  result: ComplaintResult
  rank: number
  animate?: boolean
}

export default function ComplaintCard({ result, rank, animate }: Props) {
  const score = Math.round(result.similarity_score * 100)
  const color = CATEGORY_COLORS[result.category] ?? CATEGORY_COLORS['general']

  const date = result.timestamp
    ? new Date(result.timestamp).toLocaleDateString('en-GB', {
        day: '2-digit', month: 'short', year: 'numeric',
      })
    : '—'

  return (
    <div
      className={`${styles.card} ${animate ? styles.animated : ''}`}
      style={{ animationDelay: `${rank * 55}ms` }}
    >
      {/* colour rail on the left */}
      <div className={styles.rail} style={{ background: color }} />

      <div className={styles.body}>
        <div className={styles.header}>
          <span className={styles.rank}>#{rank}</span>

          <span
            className={styles.category}
            style={{ color, borderColor: color + '44' }}
          >
            {result.category}
          </span>

          {/* Similarity score bar */}
          <span className={styles.score}>
            <span className={styles.scoreBar}>
              <span
                className={styles.scoreFill}
                style={{ width: `${score}%`, background: color }}
              />
            </span>
            {score}%
          </span>

          <span className={styles.date}>{date}</span>
        </div>

        <p className={styles.text}>{result.text}</p>

        <p className={styles.idRow}>
          id: <span className={styles.mono}>{result.id.slice(0, 8)}…</span>
        </p>
      </div>
    </div>
  )
}
