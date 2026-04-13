import React, { useRef, useState } from 'react'
import { askQuestion, AskResponse } from '../utils/api'
import ComplaintCard from './ComplaintCard'
import styles from './AskPanel.module.css'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  text: string
  response?: AskResponse
}

const EXAMPLES = [
  'What are the most common delivery problems?',
  'Are there billing complaints about duplicate charges?',
  'How should I handle damaged product complaints?',
  'What account issues do customers report?',
]

export default function AskPanel() {
  const [input, setInput]       = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState<string | null>(null)
  const [expanded, setExpanded] = useState<Record<number, boolean>>({})
  const bottomRef               = useRef<HTMLDivElement>(null)

  const scrollToBottom = () =>
    setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 60)

  const toggleExpanded = (id: number) =>
    setExpanded(prev => ({ ...prev, [id]: !prev[id] }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const q = input.trim()
    if (!q || loading) return

    const userMsg: ChatMessage = { id: Date.now(), role: 'user', text: q }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setError(null)
    setLoading(true)
    scrollToBottom()

    try {
      const res = await askQuestion({ question: q, top_k: 5 })
      const aiMsg: ChatMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        text: res.answer,
        response: res,
      }
      setMessages(prev => [...prev, aiMsg])
      scrollToBottom()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Request failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  const handleExample = (q: string) => setInput(q)

  return (
    <section className={styles.panel}>

      {/* Panel header */}
      <header className={styles.head}>
        <div className={styles.headLeft}>
          <span className={styles.icon}>✦</span>
          <div>
            <h2 className={styles.title}>AI Chat Assistant</h2>
            <p className={styles.sub}>RAG: Endee retrieval → FLAN-T5 generation</p>
          </div>
        </div>

        {/* Pipeline diagram — FIX: use className instead of data-active attribute */}
        <div className={styles.pipeline}>
          <span className={styles.pipeStep}>Query</span>
          <span className={styles.pipeArrow}>→</span>
          <span className={`${styles.pipeStep} ${styles.pipeStepActive}`}>Endee</span>
          <span className={styles.pipeArrow}>→</span>
          <span className={styles.pipeStep}>FLAN-T5</span>
          <span className={styles.pipeArrow}>→</span>
          <span className={styles.pipeStep}>Answer</span>
        </div>
      </header>

      {/* Chat window */}
      <div className={styles.chatWindow}>

        {/* Empty state with example queries */}
        {messages.length === 0 && !loading && (
          <div className={styles.emptyState}>
            <div className={styles.emptyHex}>⬡</div>
            <h3 className={styles.emptyTitle}>Ask anything about complaints</h3>
            <p className={styles.emptySub}>
              The RAG pipeline retrieves the most relevant complaints from Endee
              and feeds them as context to FLAN-T5 to generate an answer.
            </p>
            <div className={styles.examples}>
              {EXAMPLES.map(q => (
                <button
                  key={q}
                  className={styles.exampleBtn}
                  onClick={() => handleExample(q)}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message list */}
        {messages.map(msg => (
          <div
            key={msg.id}
            className={`${styles.msgRow} ${msg.role === 'user' ? styles.userRow : styles.aiRow} animate-fade-up`}
          >
            {msg.role === 'user' ? (
              /* User bubble */
              <div className={styles.userBubble}>
                <span className={styles.avatarUser}>U</span>
                <p className={styles.userText}>{msg.text}</p>
              </div>
            ) : (
              /* AI bubble + retrieved context */
              <div className={styles.aiMessage}>
                <div className={styles.aiBubble}>
                  <span className={styles.avatarAi}>✦</span>
                  <p className={styles.aiText}>{msg.text}</p>
                </div>

                {msg.response && msg.response.retrieved_complaints.length > 0 && (
                  <div className={styles.context}>
                    <button
                      className={styles.contextToggle}
                      onClick={() => toggleExpanded(msg.id)}
                    >
                      <span className={styles.chevron}>
                        {expanded[msg.id] ? '▾' : '▸'}
                      </span>
                      {msg.response.retrieved_complaints.length} complaints retrieved from Endee
                      <span className={styles.modelTag}>
                        {msg.response.model_used.split('/').pop()}
                      </span>
                    </button>

                    {expanded[msg.id] && (
                      <div className={styles.contextCards}>
                        {msg.response.retrieved_complaints.map((r, i) => (
                          <ComplaintCard key={r.id} result={r} rank={i + 1} animate />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className={`${styles.msgRow} ${styles.aiRow}`}>
            <div className={styles.aiBubble}>
              <span className={styles.avatarAi}>✦</span>
              <div className={styles.typing}>
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}

        {/* Inline error */}
        {error && <p className={styles.errorMsg}>{error}</p>}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <form onSubmit={handleSubmit} className={styles.inputBar}>
        <input
          type="text"
          className={styles.input}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask about complaints…"
          disabled={loading}
        />
        <button
          type="submit"
          className={styles.sendBtn}
          disabled={loading || !input.trim()}
          aria-label="Send"
        >
          {loading ? <span className={styles.spinner} /> : '↑'}
        </button>
      </form>

    </section>
  )
}
