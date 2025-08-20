import React, { useState } from 'react'
import api from '../../lib/api'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [tenant, setTenant] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const doLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const form = new URLSearchParams()
      form.append('username', email)
      form.append('password', password)
      const { data } = await api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      localStorage.setItem('token', data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const doRegister = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await api.post('/auth/register', { email, password, tenant_name: tenant || 'Default Tenant' })
      localStorage.setItem('token', data.access_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="panel">
        <h2>Login</h2>
        <form onSubmit={doLogin}>
          <div className="form-row">
            <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button disabled={loading} type="submit">{loading ? 'Processing...' : 'Login'}</button>
          </div>
        </form>
        <hr style={{ borderColor: '#242a33', margin: '16px 0' }} />
        <h3>Or Quick Register</h3>
        <form onSubmit={doRegister}>
          <div className="form-row">
            <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <input placeholder="Tenant name (optional)" value={tenant} onChange={(e) => setTenant(e.target.value)} />
            <button disabled={loading} type="submit">{loading ? 'Processing...' : 'Register & Login'}</button>
          </div>
        </form>
        {error && <p style={{ color: 'tomato' }}>{error}</p>}
      </div>
    </div>
  )
}
