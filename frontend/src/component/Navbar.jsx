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
    <>
      <Link to="/" className="navbar-title">AskBob PMS</Link>
      <div>
        {token ? <button onClick={logout}>Logout</button> : <Link to="/login">Login</Link>}
      </div>
    </>
  )
}
