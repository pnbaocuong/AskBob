import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../../lib/api'

export default function ProjectDetailPage() {
  const { id } = useParams()
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [status, setStatus] = useState('todo')
  const [assignee, setAssignee] = useState('')
  const [error, setError] = useState('')

  const [editingId, setEditingId] = useState('')
  const [editTitle, setEditTitle] = useState('')
  const [editStatus, setEditStatus] = useState('todo')
  const [editAssignee, setEditAssignee] = useState('')

  // Filters / Sort / Pagination
  const [statusFilter, setStatusFilter] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('')
  const [sort, setSort] = useState('-created_at')
  const [limit, setLimit] = useState(20)
  const [offset, setOffset] = useState(0)

  const load = async () => {
    try {
      const params = { project_id: id, sort, limit, offset }
      if (statusFilter) params.status_filter = statusFilter
      if (priorityFilter) params.priority_filter = priorityFilter
      const { data } = await api.get('/tasks/', { params })
      setTasks(Array.isArray(data?.items) ? data.items : (Array.isArray(data) ? data : []))
    } catch (e) {
      setError('Failed to load tasks')
    }
  }

  useEffect(() => { load() }, [id, statusFilter, priorityFilter, sort, limit, offset])

  const createTask = async (e) => {
    e.preventDefault()
    try {
      await api.post('/tasks/', { title, status, assignee: assignee || null, project_id: id })
      setTitle('')
      setStatus('todo')
      setAssignee('')
      load()
    } catch (e) {
      setError('Failed to create task')
    }
  }

  const startEdit = (t) => {
    setEditingId(t.id)
    setEditTitle(t.title)
    setEditStatus(t.status)
    setEditAssignee(t.assignee || '')
  }

  const cancelEdit = () => {
    setEditingId('')
    setEditTitle('')
    setEditStatus('todo')
    setEditAssignee('')
  }

  const saveEdit = async () => {
    if (!editingId) return
    try {
      await api.put(`/tasks/${editingId}`, {
        title: editTitle,
        status: editStatus,
        assignee: editAssignee || null,
      })
      cancelEdit()
      load()
    } catch (e) {
      setError('Failed to update task')
    }
  }

  const updateStatus = async (taskId, newStatus) => {
    try {
      await api.put(`/tasks/${taskId}`, { status: newStatus })
      load()
    } catch (e) {
      setError('Failed to update')
    }
  }

  const deleteTask = async (taskId) => {
    try {
      await api.delete(`/tasks/${taskId}`)
      load()
    } catch (e) {
      setError('Failed to delete')
    }
  }

  return (
    <div className="panel">
      <h2>Project Detail</h2>

      <div className="form-row" style={{ marginBottom: 12 }}>
        <select value={statusFilter} onChange={(e) => { setOffset(0); setStatusFilter(e.target.value) }}>
          <option value="">All Status</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <select value={priorityFilter} onChange={(e) => { setOffset(0); setPriorityFilter(e.target.value) }}>
          <option value="">All Priority</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <select value={sort} onChange={(e) => { setOffset(0); setSort(e.target.value) }}>
          <option value="-created_at">Newest created</option>
          <option value="created_at">Oldest created</option>
          <option value="due_date">Due date asc</option>
          <option value="-due_date">Due date desc</option>
          <option value="priority">Priority asc</option>
          <option value="-priority">Priority desc</option>
        </select>
      </div>

      <form onSubmit={createTask}>
        <div className="form-row" style={{ marginBottom: 12 }}>
          <input placeholder="Task title" value={title} onChange={(e) => setTitle(e.target.value)} />
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="todo">Todo</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
          <input placeholder="Assignee" value={assignee} onChange={(e) => setAssignee(e.target.value)} />
          <button type="submit">Add task</button>
        </div>
      </form>

      {error && <p style={{ color: 'tomato' }}>{error}</p>}

      <ul className="list">
        {tasks.map(t => (
          <li key={t.id}>
            {editingId === t.id ? (
              <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'space-between' }}>
                <div className="form-row" style={{ flex: 1 }}>
                  <input placeholder="Task title" value={editTitle} onChange={(e) => setEditTitle(e.target.value)} />
                  <select value={editStatus} onChange={(e) => setEditStatus(e.target.value)}>
                    <option value="todo">Todo</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                  </select>
                  <input placeholder="Assignee" value={editAssignee} onChange={(e) => setEditAssignee(e.target.value)} />
                </div>
                <div>
                  <button onClick={saveEdit}>Save</button>
                  <button className="danger" style={{ marginLeft: 8 }} onClick={cancelEdit} type="button">Cancel</button>
                </div>
              </div>
            ) : (
              <>
                <div>
                  <b>{t.title}</b> — {t.status} {t.assignee ? `(${t.assignee})` : ''}
                </div>
                <div>
                  <button onClick={() => startEdit(t)}>Edit</button>
                  <button style={{ marginLeft: 8 }} onClick={() => updateStatus(t.id, 'todo')}>Todo</button>
                  <button style={{ marginLeft: 8 }} onClick={() => updateStatus(t.id, 'in_progress')}>Doing</button>
                  <button style={{ marginLeft: 8 }} onClick={() => updateStatus(t.id, 'done')}>Done</button>
                  <button className="danger" style={{ marginLeft: 12 }} onClick={() => deleteTask(t.id)}>Delete</button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
