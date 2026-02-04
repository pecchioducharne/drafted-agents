'use client'

import { useState } from 'react'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function Home() {
  const [taskRequest, setTaskRequest] = useState('')
  const [taskId, setTaskId] = useState<string | null>(null)
  
  const { data: health } = useSWR(
    `${process.env.ORCHESTRATOR_URL}/health`,
    fetcher,
    { refreshInterval: 10000 }
  )
  
  const { data: taskStatus } = useSWR(
    taskId ? `${process.env.ORCHESTRATOR_URL}/tasks/${taskId}` : null,
    fetcher,
    { refreshInterval: 2000 }
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const response = await fetch(`${process.env.ORCHESTRATOR_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request: taskRequest }),
    })
    
    const data = await response.json()
    setTaskId(data.task_id)
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Drafted Agents</h1>
        
        {/* Health Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          {health ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span>System: {health.status}</span>
              </div>
              {health.services && Object.entries(health.services).map(([key, value]) => (
                <div key={key} className="flex items-center gap-2 ml-5">
                  <div className={`w-2 h-2 rounded-full ${value === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="text-sm">{key}: {value as string}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">Loading...</p>
          )}
        </div>

        {/* Task Creation */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Create Task</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="task" className="block text-sm font-medium mb-2">
                Task Description
              </label>
              <textarea
                id="task"
                value={taskRequest}
                onChange={(e) => setTaskRequest(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={4}
                placeholder="e.g., Fix bug in candidate page where Safari crashes on video load"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Submit Task
            </button>
          </form>
        </div>

        {/* Task Status */}
        {taskId && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Task Status</h2>
            <div className="space-y-2">
              <p><strong>Task ID:</strong> {taskId}</p>
              {taskStatus && (
                <>
                  <p><strong>Status:</strong> {taskStatus.status}</p>
                  <p><strong>Progress:</strong> {taskStatus.progress}</p>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
