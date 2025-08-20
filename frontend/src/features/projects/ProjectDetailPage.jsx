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

  const load = async () => {
    try {
      const { data } = await api.get('/tasks/', { params: { project_id: id } })
      setTasks(data)
    } catch (e) {
      setError('Failed to load tasks')
    }
  }

  useEffect(() => { load() }, [id])

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
    <div>
      <h2>Project Detail</h2>
      <form onSubmit={createTask} style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <input placeholder="Task title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <input placeholder="Assignee" value={assignee} onChange={(e) => setAssignee(e.target.value)} />
        <button type="submit">Add task</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {tasks.map(t => (
          <li key={t.id}>
            <b>{t.title}</b> — {t.status} {t.assignee ? `(${t.assignee})` : ''}
            <span style={{ marginLeft: 8 }}>
              <button onClick={() => updateStatus(t.id, 'todo')}>Todo</button>
              <button onClick={() => updateStatus(t.id, 'in_progress')}>Doing</button>
              <button onClick={() => updateStatus(t.id, 'done')}>Done</button>
              <button style={{ marginLeft: 8 }} onClick={() => deleteTask(t.id)}>Delete</button>
            </span>
          </li>
        ))}
      </ul>
    </div>
  )
}
