import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import ErrorBoundary from './ErrorBoundary'
import './index.css'

// Explicit null-check: tells you exactly what went wrong instead of a blank page
const rootElement = document.getElementById('root')

if (!rootElement) {
  document.body.innerHTML = `
    <div style="padding:2rem;font-family:monospace;color:red">
      <h2>FATAL: Could not find #root element</h2>
      <p>Check that <code>index.html</code> contains <code>&lt;div id="root"&gt;&lt;/div&gt;</code></p>
    </div>
  `
  throw new Error('Missing #root element in index.html')
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    {/* ErrorBoundary catches any runtime crash and shows it on screen */}
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
