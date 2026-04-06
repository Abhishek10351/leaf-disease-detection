"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ImageAnalysis } from '@/components/analysis/image-analysis'
import { AnalysisHistory } from '@/components/analysis/analysis-history'
import { History, ArrowLeft, LocateFixed } from 'lucide-react'
import { AnalysisLocation } from '@/types/analysis'

type ResponseLanguage = 'en' | 'hi' | 'as' | 'brx'

const formatLocationLabel = (location: AnalysisLocation): string => {
  if (location.label) return location.label
  return `${location.latitude}, ${location.longitude}`
}

const reverseGeocode = async (latitude: number, longitude: number): Promise<Partial<AnalysisLocation>> => {
  const endpoint = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}&zoom=10&addressdetails=1`
  const response = await fetch(endpoint, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Reverse geocoding failed')
  }

  const data = await response.json()
  const address = data?.address ?? {}

  const locality =
    address.city ||
    address.town ||
    address.village ||
    address.municipality ||
    address.county ||
    'Current area'

  const region = address.state || address.region || address.state_district || ''
  const country = address.country || ''
  const label = [locality, region, country].filter(Boolean).join(', ')

  return {
    label,
    region,
    country,
  }
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
      async (position) => {
        const latitude = Number(position.coords.latitude.toFixed(4))
        const longitude = Number(position.coords.longitude.toFixed(4))

        const baseLocation: AnalysisLocation = {
          latitude,
          longitude,
          accuracyMeters: Number(position.coords.accuracy.toFixed(0)),
          capturedAt: new Date().toISOString(),
        }

        try {
          const place = await reverseGeocode(latitude, longitude)
          const enrichedLocation: AnalysisLocation = {
            ...baseLocation,
            ...place,
          }
          setAnalysisLocation(enrichedLocation)
          setLocationStatus('ready')
          setLocationMessage(`Using location: ${formatLocationLabel(enrichedLocation)}`)
        } catch {
          setAnalysisLocation(baseLocation)
          setLocationStatus('ready')
          setLocationMessage(`Using coordinates: ${latitude}, ${longitude}`)
        }
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

              {analysisLocation && (
                <div className="rounded-md border bg-muted/20 px-3 py-2 text-xs text-muted-foreground">
                  <p className="font-medium text-foreground">Analysis location</p>
                  <p>{formatLocationLabel(analysisLocation)}</p>
                  <p>
                    Lat {analysisLocation.latitude}, Lon {analysisLocation.longitude}
                    {analysisLocation.accuracyMeters ? `, ±${analysisLocation.accuracyMeters}m` : ''}
                  </p>
                </div>
              )}
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