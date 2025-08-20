import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()
  const token = localStorage.getItem('token')
  const logout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', background: '#121212', color: 'white' }}>
      <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 600 }}>AskBob PMS</Link>
      <div>
        {token ? <button onClick={logout}>Logout</button> : <Link to="/login" style={{ color: 'white' }}>Login</Link>}
      </div>
    </div>
  )
}
