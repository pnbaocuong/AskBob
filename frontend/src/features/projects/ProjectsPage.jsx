import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../lib/api'

export default function ProjectsPage() {
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [desc, setDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.get('/projects/')
      setItems(data)
    } catch (e) {
      setError('Failed to load projects')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const create = async (e) => {
    e.preventDefault()
    if (!name) return
    try {
      await api.post('/projects/', { name, description: desc || null })
      setName('')
      setDesc('')
      load()
    } catch (e) {
      setError('Failed to create project')
    }
  }

  const update = async (id) => {
    const newName = prompt('New name:')
    if (!newName) return
    try {
      await api.put(`/projects/${id}`, { name: newName })
      load()
    } catch (e) {
      setError('Failed to update project')
    }
  }

  const remove = async (id) => {
    if (!confirm('Delete this project?')) return
    try {
      await api.delete(`/projects/${id}`)
      load()
    } catch (e) {
      setError('Failed to delete project')
    }
  }

  return (
    <div>
      <h2>Projects</h2>
      <form onSubmit={create} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input placeholder="Project name" value={name} onChange={(e) => setName(e.target.value)} />
        <input placeholder="Description" value={desc} onChange={(e) => setDesc(e.target.value)} />
        <button type="submit">Create</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {items.map(p => (
          <li key={p.id}>
            <Link to={`/projects/${p.id}`}>{p.name}</Link>
            <button style={{ marginLeft: 8 }} onClick={() => update(p.id)}>Edit</button>
            <button style={{ marginLeft: 4 }} onClick={() => remove(p.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
