import React from 'react'

interface State {
  error: Error | null
}

/**
 * ErrorBoundary
 * -------------
 * Wraps the entire app so that any unhandled component crash is caught and
 * displayed on screen instead of producing a silent blank page.
 */
export default class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  State
> {
  constructor(props: { children: React.ReactNode }) {
    super(props)
    this.state = { error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[ErrorBoundary] App crashed:', error)
    console.error('[ErrorBoundary] Component stack:', info.componentStack)
  }

  render() {
    if (this.state.error) {
      return (
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'center',
            background: '#fdf6f0',
            padding: '3rem 1rem',
            fontFamily: 'monospace',
          }}
        >
          <div
            style={{
              maxWidth: 700,
              width: '100%',
              background: '#fff',
              border: '2px solid #e53e3e',
              borderRadius: 8,
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                background: '#e53e3e',
                color: '#fff',
                padding: '12px 20px',
                fontWeight: 700,
                fontSize: 15,
              }}
            >
              ⚠️ Application Error — check the browser console for details
            </div>
            <div style={{ padding: '20px' }}>
              <p style={{ color: '#c53030', fontWeight: 600, marginBottom: 12 }}>
                {this.state.error.message}
              </p>
              <pre
                style={{
                  background: '#fff5f5',
                  border: '1px solid #fed7d7',
                  borderRadius: 4,
                  padding: '1rem',
                  fontSize: 12,
                  overflowX: 'auto',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  color: '#742a2a',
                }}
              >
                {this.state.error.stack}
              </pre>
              <button
                onClick={() => this.setState({ error: null })}
                style={{
                  marginTop: 16,
                  padding: '8px 18px',
                  background: '#e53e3e',
                  color: '#fff',
                  border: 'none',
                  borderRadius: 4,
                  cursor: 'pointer',
                  fontFamily: 'monospace',
                  fontSize: 13,
                }}
              >
                Try again
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
