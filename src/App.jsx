import { useCallback, useEffect, useMemo, useState } from 'react'

const API = '/api'

async function api(path, { method = 'GET', params, token } = {}) {
  const url = new URL(`${API}${path}`, window.location.origin)
  if (params) Object.entries(params).forEach(([key, value]) => url.searchParams.set(key, value))
  const response = await fetch(url, {
    method,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(payload.message || `Request failed (${response.status})`)
  return payload
}

function monthLabel() {
  return new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(new Date())
}

function initials(name = '?') {
  return name.split(/\s+/).slice(0, 2).map((part) => part[0]?.toUpperCase()).join('')
}

function App() {
  const [nominations, setNominations] = useState([])
  const [winner, setWinner] = useState(null)
  const [token, setToken] = useState(() => localStorage.getItem('spotlight-token') || '')
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('spotlight-user') || 'null') } catch { return null }
  })
  const [tab, setTab] = useState('community')
  const [modal, setModal] = useState('')
  const [busy, setBusy] = useState(false)
  const [notice, setNotice] = useState(null)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')

  const load = useCallback(async () => {
    setError('')
    try {
      const [nominationData, hallData] = await Promise.all([
        api('/nominations'), api('/hall-of-fame'),
      ])
      setNominations(nominationData.nominations || [])
      setWinner(hallData.winner || null)
    } catch (err) {
      setError(err.message || 'Could not connect to the community API.')
    }
  }, [])

  useEffect(() => { load() }, [load])
  useEffect(() => {
    if (!notice) return undefined
    const timer = window.setTimeout(() => setNotice(null), 3800)
    return () => window.clearTimeout(timer)
  }, [notice])

  const filtered = useMemo(() => {
    const term = query.trim().toLowerCase()
    return nominations.filter((item) => !term || [item.title, item.nominee_name, item.description, item.category]
      .some((value) => String(value || '').toLowerCase().includes(term)))
  }, [nominations, query])

  async function submitAuth(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const form = new FormData(event.currentTarget)
    const values = Object.fromEntries(form.entries())
    try {
      if (modal === 'signup') {
        await api('/signup', { method: 'POST', params: values })
        const username = values.email.split('@')[0]
        const result = await api('/login', { method: 'POST', params: { username, password: values.password } })
        saveSession(result)
        setNotice({ kind: 'success', text: `Welcome in, ${result.user.name.split(' ')[0]}!` })
      } else {
        const result = await api('/login', { method: 'POST', params: values })
        saveSession(result)
        setNotice({ kind: 'success', text: `Good to see you, ${result.user.name.split(' ')[0]}!` })
      }
      setModal('')
    } catch (err) { setError(err.message) }
    finally { setBusy(false) }
  }

  function saveSession(result) {
    localStorage.setItem('spotlight-token', result.token)
    localStorage.setItem('spotlight-user', JSON.stringify(result.user))
    setToken(result.token)
    setUser(result.user)
  }

  async function submitNomination(event) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const values = Object.fromEntries(new FormData(event.currentTarget).entries())
    try {
      await api('/nominations', { method: 'POST', params: values, token })
      setModal('')
      setNotice({ kind: 'success', text: 'Your good deed nomination is in. Thanks for noticing!' })
      await load()
    } catch (err) { setError(err.message) }
    finally { setBusy(false) }
  }

  async function castVote(item) {
    if (!token) { setModal('login'); return }
    setBusy(true)
    setError('')
    try {
      const result = await api('/votes', { method: 'POST', params: { post_id: item.post_id }, token })
      setNotice({ kind: 'success', text: result.message || 'Your vote has been counted!' })
      await load()
    } catch (err) { setNotice({ kind: 'error', text: err.message }) }
    finally { setBusy(false) }
  }

  function signOut() {
    localStorage.removeItem('spotlight-token')
    localStorage.removeItem('spotlight-user')
    setToken('')
    setUser(null)
    setNotice({ kind: 'success', text: 'You are signed out.' })
  }

  const ordered = tab === 'top' ? [...filtered].sort((a, b) => b.vote_count - a.vote_count) : filtered

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#home" onClick={() => setTab('community')}>
          <span className="brand-mark"><span>✳</span></span>
          <span className="brand-name">good<span>neighbors</span></span>
        </a>
        <div className="top-location"><span className="pin">●</span> Sammamish, WA <span className="location-chevron">⌄</span></div>
        <div className="top-actions">
          <button className="icon-button" aria-label="Search nominations" onClick={() => document.querySelector('#search')?.focus()}>⌕</button>
          {user ? <button className="profile-button" onClick={signOut}><span className="avatar tiny">{initials(user.name)}</span><span className="profile-name">{user.name.split(' ')[0]}</span><span className="chevron">⌄</span></button>
            : <><button className="login-link" onClick={() => { setError(''); setModal('login') }}>Log in</button><button className="button button-dark small" onClick={() => { setError(''); setModal('signup') }}>Join the community <span>↗</span></button></>}
        </div>
      </header>

      <main id="home">
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow"><span className="eyebrow-dot" /> A LITTLE GOOD GOES A LONG WAY</div>
            <h1>Good things<br />happen <em>here.</em></h1>
            <p>A place to notice the neighbors who make Sammamish a little brighter. Share a good deed, give someone their flowers, and help us celebrate the good.</p>
            <div className="hero-actions">
              <button className="button button-lime" onClick={() => token ? setModal('nomination') : setModal('login')}>＋ &nbsp;Shout out a neighbor</button>
              <button className="text-button" onClick={() => document.querySelector('#community')?.scrollIntoView({ behavior: 'smooth' })}>See what’s happening <span>↓</span></button>
            </div>
            <div className="community-proof"><div className="proof-avatars"><span>🌼</span><span>🧡</span><span>🌿</span><b>+</b></div><span>Small acts. <strong>Big community.</strong></span></div>
          </div>
          <div className="hero-art" aria-label="Illustration of neighbors celebrating kindness">
            <div className="sun-disc" /><div className="art-spark spark-one">✳</div><div className="art-spark spark-two">✦</div>
            <div className="hill hill-back" /><div className="hill hill-front" />
            <div className="tree tree-one"><i /><b /></div><div className="tree tree-two"><i /><b /></div>
            <div className="person person-one"><span className="head" /><span className="body" /><span className="arm" /></div>
            <div className="person person-two"><span className="head" /><span className="body" /><span className="arm" /></div>
            <div className="person person-three"><span className="head" /><span className="body" /><span className="arm" /></div>
            <div className="art-note"><span>♡</span><div><strong>Kindness<br />lives here</strong><small>SAMMAMISH, WA</small></div></div>
            <div className="art-badge">GOOD<br />NEIGHBORS <span>✳</span></div>
          </div>
          <div className="hero-bottom"><span>✳ &nbsp; ROOTED IN COMMUNITY</span><span>EST. WITH HEART &nbsp; · &nbsp; SAMMAMISH</span></div>
        </section>

        <section className="community-section" id="community">
          <div className="section-heading">
            <div><div className="eyebrow muted"><span className="eyebrow-dot" /> THE GOOD, RIGHT NOW</div><h2>Good is going around.</h2><p>Real people. Real good. All happening right here at home.</p></div>
            <button className="button button-outline" onClick={() => token ? setModal('nomination') : setModal('login')}>＋ &nbsp;Add a shout-out</button>
          </div>
          <div className="stats-row">
            <div className="stat"><span className="stat-icon lime-icon">✳</span><div><strong>{nominations.length}</strong><small>good deeds shared</small></div></div>
            <div className="stat"><span className="stat-icon peach-icon">♡</span><div><strong>{nominations.reduce((sum, row) => sum + Number(row.vote_count || 0), 0)}</strong><small>neighbor votes</small></div></div>
            <div className="stat"><span className="stat-icon blue-icon">⌂</span><div><strong>1</strong><small>community, showing up</small></div></div>
            <div className="stat-month"><span>{monthLabel()}</span><span className="live-dot" /> VOTING OPEN</div>
          </div>

          <div className="content-grid">
            <div className="feed-column">
              <div className="feed-tools">
                <div className="tabs"><button className={tab === 'community' ? 'active' : ''} onClick={() => setTab('community')}>Latest <span>{nominations.length}</span></button><button className={tab === 'top' ? 'active' : ''} onClick={() => setTab('top')}>Most loved <span>♡</span></button></div>
                <label className="search-box"><span>⌕</span><input id="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Find a good thing..." /></label>
              </div>
              {error && <div className="inline-error"><span>!</span><div><strong>Couldn’t load that</strong><small>{error}</small></div><button onClick={load}>Try again</button></div>}
              {ordered.length ? <div className="nomination-list">{ordered.map((item, index) => <article className="deed-card" key={item.post_id}>
                <div className={`deed-avatar color-${index % 5}`}>{initials(item.nominee_name)}</div>
                <div className="deed-content"><div className="deed-meta"><span className="category-tag">{item.category || 'COMMUNITY'}</span><span>·</span><span>{item.month_cycle}</span></div><h3>{item.title}</h3><p className="deed-description">{item.description}</p><div className="deed-byline"><span className="byline-avatar">{initials(item.nominated_by)}</span><span>Celebrated by <strong>{item.nominated_by}</strong></span></div></div>
                <button className="vote-button" disabled={busy} onClick={() => castVote(item)}><span className="vote-heart">♡</span><strong>{item.vote_count}</strong><small>VOTE</small></button>
              </article>)}</div> : !error && <div className="empty-state"><div className="empty-illustration">✳</div><h3>{query ? 'No good deeds found' : 'It starts with noticing.'}</h3><p>{query ? 'Try another search, or clear the field.' : 'Know someone who made a difference? Their story belongs here.'}</p>{!query && <button className="button button-dark" onClick={() => token ? setModal('nomination') : setModal('login')}>Share the first shout-out <span>↗</span></button>}</div>}
              <div className="load-more"><span>✳</span> YOU’RE ALL CAUGHT UP <span>✳</span></div>
            </div>

            <aside className="side-column">
              <div className="winner-card"><div className="winner-top"><span className="winner-label"><span>✦</span> THIS MONTH’S SPOTLIGHT</span><span className="winner-month">{new Intl.DateTimeFormat('en-US', { month: 'short' }).format(new Date()).toUpperCase()}</span></div><div className="winner-graphic"><div className="winner-rays">✳</div><div className="winner-person">{winner ? initials(winner.nominee_name) : '♡'}</div><span className="laurel left">❧</span><span className="laurel right">❧</span><span className="winner-star star-left">✦</span><span className="winner-star star-right">✦</span></div><div className="winner-info"><span className="winner-small">SAMMAMISH HALL OF FAME</span><h3>{winner?.nominee_name || 'Your neighbor could be here'}</h3><p>{winner ? `${winner.vote_count} neighbor ${Number(winner.vote_count) === 1 ? 'vote' : 'votes'} so far. Keep the love going.` : 'Every month, we celebrate the neighbor whose good deed moved our community.'}</p><button className="winner-link" onClick={() => setTab('top')}>Meet this month’s good <span>↗</span></button></div></div>
              <div className="prompt-card"><span className="prompt-flower">✿</span><div><span className="prompt-overline">SEE SOMEONE DO GOOD?</span><h3>Don’t let the<br />good go unnoticed.</h3><p>A small shout-out can make someone’s whole week.</p><button onClick={() => token ? setModal('nomination') : setModal('login')}>Tell their story <span>→</span></button></div><span className="prompt-doodle">〰</span></div>
              <div className="kindness-note"><span>“</span><p>No act of kindness,<br />no matter how small,<br />is ever wasted.</p><small>— AESOP</small><i>✳</i></div>
            </aside>
          </div>
        </section>
      </main>

      <footer><a className="brand footer-brand" href="#home"><span className="brand-mark"><span>✳</span></span><span className="brand-name">good<span>neighbors</span></span></a><span>Made with a little extra love in Sammamish. <b>♡</b></span><span>GOOD THINGS GROW HERE</span></footer>

      {notice && <div className={`toast ${notice.kind}`}><span>{notice.kind === 'success' ? '✓' : '!'}</span>{notice.text}<button onClick={() => setNotice(null)}>×</button></div>}
      {modal && <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) { setModal(''); setError('') } }}><section className="modal" role="dialog" aria-modal="true">
        <button className="modal-close" onClick={() => { setModal(''); setError('') }} aria-label="Close">×</button>
        <div className="modal-mark">✳</div>
        {modal === 'nomination' ? <><div className="eyebrow muted">SPREAD A LITTLE GOOD</div><h2>Give them their flowers.</h2><p className="modal-intro">Tell Sammamish what your neighbor did. The little things count, too.</p><form onSubmit={submitNomination}>
          <label>Your neighbor’s name<input name="nominee_name" required maxLength="150" placeholder="e.g. Jordan Lee" /></label>
          <label>What did they do?<input name="title" required maxLength="200" placeholder="e.g. Showed up for the food bank" /></label>
          <label>Tell us a little more<textarea name="description" required maxLength="5000" rows="4" placeholder="Share the story behind the good deed..." /></label>
          <label>What kind of good? <select name="category" defaultValue="volunteering"><option value="volunteering">Volunteering</option><option value="neighborly">Neighborly kindness</option><option value="environment">Caring for our environment</option><option value="youth">Youth & education</option><option value="community">Community spirit</option><option value="other">Something else</option></select></label>
          {error && <div className="form-error">{error}</div>}<button className="button button-lime submit-button" disabled={busy}>{busy ? 'Sharing...' : 'Share this good deed  →'}</button>
        </form></> : <><div className="eyebrow muted">{modal === 'signup' ? 'COME ON IN' : 'WELCOME BACK'}</div><h2>{modal === 'signup' ? 'Join the good.' : 'Good to see you.'}</h2><p className="modal-intro">{modal === 'signup' ? 'Make an account to nominate neighbors and vote.' : 'Log in to help celebrate your community.'}</p><form onSubmit={submitAuth}>
          {modal === 'signup' && <label>Your name<input name="name" required maxLength="150" placeholder="e.g. Alex Morgan" autoComplete="name" /></label>}
          {modal === 'signup' ? <label>Email address<input name="email" required type="email" placeholder="you@example.com" autoComplete="email" /></label> : <label>Username<input name="username" required placeholder="Your username" autoComplete="username" /></label>}
          <label>Password<input name="password" required type="password" minLength="8" placeholder="At least 8 characters" autoComplete={modal === 'signup' ? 'new-password' : 'current-password'} /></label>
          {error && <div className="form-error">{error}</div>}<button className="button button-lime submit-button" disabled={busy}>{busy ? 'One moment...' : modal === 'signup' ? 'Create my account  →' : 'Log in  →'}</button>
        </form><p className="switch-auth">{modal === 'signup' ? 'Already part of the neighborhood?' : 'New around here?'} <button onClick={() => { setError(''); setModal(modal === 'signup' ? 'login' : 'signup') }}>{modal === 'signup' ? 'Log in' : 'Join us'}</button></p></>}
      </section></div>}
    </div>
  )
}

export default App
