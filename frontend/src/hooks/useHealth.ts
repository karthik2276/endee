import { useEffect, useState } from 'react'
import { getHealth, HealthResponse } from '../utils/api'

export function useHealth() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [error, setError] = useState<boolean>(false)

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setError(true))
  }, [])

  return { health, error }
}
