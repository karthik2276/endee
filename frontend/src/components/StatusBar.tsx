import React from 'react'
import { useHealth } from '../hooks/useHealth'
import styles from './StatusBar.module.css'

export default function StatusBar() {
  const { health, error } = useHealth()

  return (
    <div className={styles.bar}>
      <span className={styles.brand}>
        <span className={styles.logo}>⬡</span>
        <span className={styles.name}>Endee</span>
        <span className={styles.sep}>/</span>
        RAG Complaint System
      </span>

      <div className={styles.stats}>
        {error ? (
          <span className={`${styles.pill} ${styles.offline}`}>
            <span className={styles.dot} />
            Backend offline
          </span>
        ) : health ? (
          <>
            <span className={`${styles.pill} ${styles.online}`}>
              <span className={styles.dot} />
              {health.status}
            </span>
            <span className={styles.stat}>
              <span className={styles.statLabel}>complaints</span>
              <strong>{health.total_complaints}</strong>
            </span>
            <span className={styles.stat}>
              <span className={styles.statLabel}>emb</span>
              <span className={styles.mono}>{health.embedding_model}</span>
            </span>
            <span className={styles.stat}>
              <span className={styles.statLabel}>llm</span>
              <span className={styles.mono}>
                {health.llm_model.split('/').pop()}
              </span>
            </span>
          </>
        ) : (
          <span className={styles.connecting}>connecting…</span>
        )}
      </div>
    </div>
  )
}
