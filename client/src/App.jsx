import { useState } from 'react'
import './App.css'

/** Emoji for API sentiment label: positive | neutral | negative */
function sentimentEmoji(label) {
  switch (String(label ?? '').toLowerCase()) {
    case 'positive':
      return '😀'
    case 'negative':
      return '😠'
    case 'neutral':
    default:
      return '😐'
  }
}

function App() {
  const [text, setText] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleAnalyze(e) {
    e.preventDefault()
    setError(null)
    setResults(null)
    const trimmed = text.trim()

    if (!trimmed) {
      setError('Please enter text to analyze')
      return
    }
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: trimmed}),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        setError(errorData.detail || 'Failed to analyze text')
        return
      }
      
      const data = await response.json()
      setResults(data)
    } catch (error) {
      setError(error.message || 'An error occurred while analyzing text')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1 className="app-title">Text analysis</h1>
        <p className="app-subtitle">Paste text, run analyze, review stats.</p>
      </header>

      <main className="app-main">
        <section className="panel panel-input" aria-label="Input area">
          <div className="panel-head">
            <h2 className="panel-title">Input</h2>
            <p className="panel-desc">Enter or paste the text you want analyzed.</p>
          </div>
          <form className="input-form" onSubmit={handleAnalyze}>
            <label htmlFor="text-input" className="field-label">
              Your text
            </label>
            <textarea
              id="text-input"
              className="text-input"
              rows={12}
              placeholder="Paste or type your text here…"
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={loading}
            />
            <div className="form-actions">
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? 'Analyzing…' : 'Analyze text'}
              </button>
            </div>
          </form>
          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}
        </section>

        <section className="panel panel-output" aria-label="Results area">
          <div className="panel-head">
            <h2 className="panel-title">Results</h2>
            <p className="panel-desc">Statistics from the last successful run.</p>
          </div>

          <div className="panel-body">
            {!results && !loading && (
              <div className="empty-state">
                <p className="empty-state-title">No results yet</p>
                <p className="muted">Run an analysis to see word counts, sentiment, and more.</p>
              </div>
            )}
            {loading && (
              <div className="empty-state">
                <p className="empty-state-title">Analyzing…</p>
                <p className="muted">This usually takes a moment.</p>
              </div>
            )}
            {results && (
              <div className="results-grid">
                <div className="results-col">
                  <h3 className="results-section-title">Overview</h3>
                  <dl className="stat-list">
                    <dt>Words</dt>
                    <dd className="stat-value">{results.word_count}</dd>
                    <dt>Characters (with spaces)</dt>
                    <dd className="stat-value">{results.character_count}</dd>
                    <dt>Characters (no spaces)</dt>
                    <dd className="stat-value">{results.character_count_no_spaces}</dd>
                    <dt>Sentences</dt>
                    <dd className="stat-value">{results.sentence_count}</dd>
                    <dt>Avg word length</dt>
                    <dd className="stat-value">{results.average_word_length}</dd>
                    <dt>Avg sentence length</dt>
                    <dd className="stat-value">{results.average_sentence_length}</dd>
                    <dt>Unique words</dt>
                    <dd className="stat-value">{results.unique_words}</dd>
                    <dt>Reading time (min)</dt>
                    <dd className="stat-value">{results.reading_time_minutes}</dd>
                    <dt>Sentiment</dt>
                    <dd className="stat-value">
                      <span className="sentiment-emoji" aria-hidden="true">
                        {sentimentEmoji(results.sentiment)}
                      </span>{' '}
                      {results.sentiment}
                      <span className="stat-sub muted">
                        {' '}
                        ({(results.sentiment_confidence * 100).toFixed(0)}% confidence)
                      </span>
                    </dd>
                    <dt>Readability</dt>
                    <dd className="stat-value">{results.readability_score}</dd>
                  </dl>
                </div>
                <div className="results-col">
                  <h3 className="results-section-title">Most common words</h3>
                  {Array.isArray(results.most_common_words) &&
                  results.most_common_words.length > 0 ? (
                    <ul className="word-list">
                      {results.most_common_words.map((pair, i) => {
                        const [w, c] = Array.isArray(pair) ? pair : [pair, '?']
                        return (
                          <li key={`${w}-${i}`}>
                            <span className="word-term">{w}</span>
                            <span className="word-count">{c}</span>
                          </li>
                        )
                      })}
                    </ul>
                  ) : (
                    <p className="muted">None</p>
                  )}
                  <h3 className="results-section-title results-section-title--spaced">
                    Language statistics
                  </h3>
                  <pre className="json-block">
                    {JSON.stringify(results.language_statistics ?? {}, null, 2)}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <div className="footer-social">
          <a
            href="https://tiktok.com/@ericbleo"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="TikTok"
            className="footer-social-link footer-social-link--tiktok"
          >
            {/* TikTok SVG icon */}
            <svg width="28" height="28" viewBox="0 0 448 512" fill="white" aria-hidden="true">
              <path d="M448,209.9c-23.4,0-46-7.1-65.1-20.5V344c0,92.6-75.4,168-168,168S47.9,436.6,47.9,344
                s75.4-168,168-168c11.4,0,22.5,1.1,33.3,3.3v83.5c-10.3-3.4-21.3-5.3-32.9-5.3c-54.1,0-98,43.9-98,98s43.9,98,98,98s98-43.9,98-98
                V0h73.1c8.4,58.8,56.5,104.7,115.1,109.6V209.9z"/>
            </svg>
          </a>
          <a
            href="https://instagram.com/ericbleo"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Instagram"
            className="footer-social-link footer-social-link--instagram"
          >
            {/* Instagram SVG icon */}
            <svg width="28" height="28" viewBox="0 0 448 512" fill="white" aria-hidden="true">
              <path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9
            114.9-51.3 114.9-114.9-51.3-114.9-114.9-114.9zm0 186c-39.6 0-71.7-32.1-71.7-71.7s32.1-71.7
            71.7-71.7 71.7 32.1 71.7 71.7-32.1 71.7-71.7 71.7zm146.4-194.3c0 14.9-12
            26.9-26.9 26.9-14.9 0-26.9-12-26.9-26.9s12-26.9
            26.9-26.9 26.9 12 26.9 26.9zm76.1 27.2c-1.7-35.3-9.9-66.7-36.1-92.9S372.7
            1.7 337.4 0c-35.3-1.7-141.2-1.7-176.5 0-35.3 1.7-66.7 9.9-92.9 36.1S1.7
            75.3 0 110.6c-1.7 35.3-1.7 141.2 0 176.5 1.7 35.3 9.9 66.7
            36.1 92.9s57.6 34.4 92.9 36.1c35.3 1.7 141.2 1.7 176.5 0
            35.3-1.7 66.7-9.9 92.9-36.1s34.4-57.6
            36.1-92.9c1.7-35.3 1.7-141.2 0-176.5zm-48.5
            218.5c-7.8 19.6-22.9 34.7-42.5 42.5-29.4 11.7-99.2 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.5-42.5-11.7-29.4-9-99.2-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.5-42.5 29.4-11.7 99.2-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.5 42.5 11.7 29.4 9 99.2 9 132.1s2.7 102.7-9 132.1z"/>
            </svg>
          </a>
     
        </div>
   
      </footer>
    </div>
  )
}

export default App