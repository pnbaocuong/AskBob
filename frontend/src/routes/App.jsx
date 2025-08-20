import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from '../features/auth/Login'
import ProjectsPage from '../features/projects/ProjectsPage'
import ProjectDetailPage from '../features/projects/ProjectDetailPage'
import Navbar from '../component/Navbar'

function RequireAuth({ children }) {
  const token = localStorage.getItem('token')
  if (!token) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <div style={{ fontFamily: 'Inter, system-ui, Arial' }}>
      <Navbar />
      <div style={{ maxWidth: 960, margin: '24px auto', padding: '0 16px' }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<RequireAuth><ProjectsPage /></RequireAuth>} />
          <Route path="/projects/:id" element={<RequireAuth><ProjectDetailPage /></RequireAuth>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </div>
  )
}
