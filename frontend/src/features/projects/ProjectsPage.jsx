import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../lib/api'

export default function ProjectsPage() {
  const [items, setItems] = useState([])
  const [name, setName] = useState('')
  const [desc, setDesc] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [editingId, setEditingId] = useState('')
  const [editName, setEditName] = useState('')
  const [editDesc, setEditDesc] = useState('')

  const load = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.get('/projects/')
      setItems(Array.isArray(data?.items) ? data.items : (Array.isArray(data) ? data : []))
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

  const startEdit = (p) => {
    setEditingId(p.id)
    setEditName(p.name)
    setEditDesc(p.description || '')
  }

  const cancelEdit = () => {
    setEditingId('')
    setEditName('')
    setEditDesc('')
  }

  const saveEdit = async () => {
    if (!editingId) return
    try {
      await api.put(`/projects/${editingId}`, { name: editName, description: editDesc || null })
      cancelEdit()
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
    <div className="panel">
      <h2>Projects</h2>
      <form onSubmit={create}>
        <div className="form-row" style={{ marginBottom: 12 }}>
          <input placeholder="Project name" value={name} onChange={(e) => setName(e.target.value)} />
          <input placeholder="Description" value={desc} onChange={(e) => setDesc(e.target.value)} />
          <button type="submit">Create</button>
        </div>
      </form>

      {loading && <p className="muted">Loading...</p>}
      {error && <p style={{ color: 'tomato' }}>{error}</p>}

      <ul className="list">
        {items.map(p => (
          <li key={p.id}>
            {editingId === p.id ? (
              <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'space-between' }}>
                <div className="form-row" style={{ flex: 1 }}>
                  <input placeholder="Project name" value={editName} onChange={(e) => setEditName(e.target.value)} />
                  <input placeholder="Description" value={editDesc} onChange={(e) => setEditDesc(e.target.value)} />
                </div>
                <div>
                  <button onClick={saveEdit}>Save</button>
                  <button className="danger" style={{ marginLeft: 8 }} onClick={cancelEdit} type="button">Cancel</button>
                </div>
              </div>
            ) : (
              <>
                <div>
                  <Link to={`/projects/${p.id}`}>{p.name}</Link>
                  {p.description && <span className="muted" style={{ marginLeft: 8 }}>— {p.description}</span>}
                </div>
                <div>
                  <button onClick={() => startEdit(p)}>Edit</button>
                  <button className="danger" style={{ marginLeft: 8 }} onClick={() => remove(p.id)}>Delete</button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
