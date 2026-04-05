"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ImageAnalysis } from '@/components/analysis/image-analysis'
import { AnalysisHistory } from '@/components/analysis/analysis-history'
import { History, ArrowLeft, LocateFixed } from 'lucide-react'

type ResponseLanguage = 'en' | 'hi' | 'as' | 'brx'

type AnalysisLocation = {
  latitude: number
  longitude: number
}

export default function AnalysisDashboard() {
  const [showHistory, setShowHistory] = useState(false)
  const [analysisCount, setAnalysisCount] = useState(0)
  const [responseLanguage, setResponseLanguage] = useState<ResponseLanguage>('en')
  const [analysisLocation, setAnalysisLocation] = useState<AnalysisLocation | null>(null)
  const [locationStatus, setLocationStatus] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [locationMessage, setLocationMessage] = useState<string>('')

  const requestLocation = () => {
    if (!navigator.geolocation) {
      setLocationStatus('error')
      setLocationMessage('Geolocation is not supported in this browser.')
      return
    }

    setLocationStatus('loading')
    setLocationMessage('Getting your location...')

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = Number(position.coords.latitude.toFixed(4))
        const longitude = Number(position.coords.longitude.toFixed(4))
        setAnalysisLocation({ latitude, longitude })
        setLocationStatus('ready')
        setLocationMessage(`Using your location: ${latitude}, ${longitude}`)
      },
      (error) => {
        setAnalysisLocation(null)
        setLocationStatus('error')
        if (error.code === error.PERMISSION_DENIED) {
          setLocationMessage('Location permission denied. Analysis will use fallback weather context.')
          return
        }
        setLocationMessage('Could not fetch location right now. Analysis will use fallback weather context.')
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 300000 }
    )
  }

  const handleAnalysisComplete = () => {
    setAnalysisCount(prev => prev + 1)
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-2 sm:px-3 lg:px-4 py-3 sm:py-6">
        <div className="mb-2 sm:mb-4 flex items-start justify-between gap-3 sm:gap-4">
          <div>
          <h1 className="text-xl sm:text-3xl font-semibold tracking-tight text-foreground">Leaf Disease Detection</h1>
          <p className="text-sm text-muted-foreground mt-0.5 sm:mt-1">Upload a leaf photo and get a diagnosis in one flow.</p>
          {!showHistory && (
            <div className="mt-3 space-y-2">
              <div className="flex items-center gap-2 rounded-md border p-1 w-fit">
                <span className="px-2 text-xs font-medium text-muted-foreground">Response</span>
                <Button
                  type="button"
                  size="sm"
                  className="h-7 px-2"
                  variant={responseLanguage === 'en' ? 'default' : 'ghost'}
                  onClick={() => setResponseLanguage('en')}
                  aria-label="English response"
                >
                  EN
                </Button>
                <Button
                  type="button"
                  size="sm"
                  className="h-7 px-2"
                  variant={responseLanguage === 'hi' ? 'default' : 'ghost'}
                  onClick={() => setResponseLanguage('hi')}
                  aria-label="Hindi response"
                >
                  HI
                </Button>
                <Button
                  type="button"
                  size="sm"
                  className="h-7 px-2"
                  variant={responseLanguage === 'as' ? 'default' : 'ghost'}
                  onClick={() => setResponseLanguage('as')}
                  aria-label="Assamese response"
                >
                  AS
                </Button>
                <Button
                  type="button"
                  size="sm"
                  className="h-7 px-2"
                  variant={responseLanguage === 'brx' ? 'default' : 'ghost'}
                  onClick={() => setResponseLanguage('brx')}
                  aria-label="Boro response"
                >
                  BRX
                </Button>
              </div>

              <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="w-fit"
                  onClick={requestLocation}
                  disabled={locationStatus === 'loading'}
                >
                  <LocateFixed className="size-4" />
                  {locationStatus === 'loading' ? 'Fetching location...' : analysisLocation ? 'Refresh Location' : 'Use Current Location'}
                </Button>
                {(locationStatus !== 'idle' || locationMessage) && (
                  <p className={`text-xs ${locationStatus === 'error' ? 'text-red-600' : 'text-muted-foreground'}`}>
                    {locationMessage}
                  </p>
                )}
              </div>
            </div>
          )}
          </div>
          <Button
            variant="outline"
            onClick={() => setShowHistory(prev => !prev)}
            size="sm"
            className="shrink-0"
          >
            {showHistory ? (
              <>
                <ArrowLeft className="size-4" />
                Back to Analysis
              </>
            ) : (
              <>
                <History className="size-4" />
                View History
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-2 sm:px-3 lg:px-4 pb-5 sm:pb-10">
        <div className="max-w-3xl mx-auto">
          {showHistory ? (
            <AnalysisHistory key={analysisCount} />
          ) : (
            <ImageAnalysis
              responseLanguage={responseLanguage}
              analysisLocation={analysisLocation}
              onAnalysisComplete={handleAnalysisComplete}
            />
          )}
        </div>
      </div>
    </div>
  )
}