"use client"

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { FileInput } from '@/components/ui/file-input'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { AnalysisService } from '@/lib/analysis-service'
import { ImageUploadResponse, ImageAnalysisResponse, AnalysisLocation } from '@/types/analysis'
import { AnalysisResultViewer } from '@/components/analysis/analysis-result-viewer'
import { Scan, AlertCircle, CheckCircle } from 'lucide-react'
import { finalBaseURL } from '@/app/utils/api'

type ResponseLanguage = 'en' | 'hi' | 'as' | 'brx'

type SampleImage = {
  id: string
  name: string
  src: string
}

const SAMPLE_IMAGES: SampleImage[] = [
  { id: 'sample-1', name: 'Sample Leaf 1', src: 'sample-1.jpg' },
  { id: 'sample-2', name: 'Sample Leaf 2', src: 'sample-2.jpg' },
  { id: 'sample-3', name: 'Sample Leaf 3', src: 'sample-3.jpg' },
]

interface ImageAnalysisProps {
  responseLanguage?: ResponseLanguage
  analysisLocation?: AnalysisLocation | null
  onAnalysisComplete?: (analysis: ImageAnalysisResponse) => void
}

export function ImageAnalysis({
  responseLanguage = 'en',
  analysisLocation = null,
  onAnalysisComplete,
}: ImageAnalysisProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStatus, setAnalysisStatus] = useState<string | null>(null)
  const [uploadedImage, setUploadedImage] = useState<ImageUploadResponse | null>(null)
  const [analysis, setAnalysis] = useState<ImageAnalysisResponse | null>(null)
  const [highlightResult, setHighlightResult] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sampleUploads, setSampleUploads] = useState<Record<string, ImageUploadResponse>>({})
  const resultRef = useRef<HTMLDivElement>(null)

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setAnalysisStatus('Uploading image...')
    setError(null)

    try {
      const uploadResponse = await AnalysisService.uploadImage(selectedFile)
      setUploadedImage(uploadResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setIsUploading(false)
      setAnalysisStatus(null)
    }
  }

  const handleAnalyze = async () => {
    if (!uploadedImage) return

    setIsAnalyzing(true)
    setAnalysisStatus('Analyzing leaf image...')
    setError(null)

    try {
      const analysisResponse = await AnalysisService.analyzeImage({
        image_id: uploadedImage.image_id,
        language: responseLanguage,
        location: analysisLocation
          ? {
              latitude: analysisLocation.latitude,
              longitude: analysisLocation.longitude,
            }
          : undefined,
      })
      setAnalysisStatus('Preparing diagnosis...')
      await new Promise(resolve => setTimeout(resolve, 180))
      setAnalysis(analysisResponse)
      onAnalysisComplete?.(analysisResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setIsAnalyzing(false)
      setAnalysisStatus(null)
    }
  }

  const handleUseSample = async (sample: SampleImage) => {
    if (isUploading || isAnalyzing) return

    setError(null)
    setAnalysis(null)
    setHighlightResult(false)

    const cached = sampleUploads[sample.id]
    if (cached) {
      setUploadedImage(cached)
      setSelectedFile(null)
      return
    }

    setIsUploading(true)
    setAnalysisStatus(`Loading ${sample.name}...`)

    try {
      const response = await fetch(`/sample-images/${sample.src}`)
      if (!response.ok) {
        throw new Error(`Failed to load ${sample.name}`)
      }

      const blob = await response.blob()
      const file = new File([blob], `${sample.id}.jpg`, { type: blob.type || 'image/jpeg' })
      const uploadResponse = await AnalysisService.uploadImage(file)

      setSampleUploads((prev) => ({ ...prev, [sample.id]: uploadResponse }))
      setUploadedImage(uploadResponse)
      setSelectedFile(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load sample image')
    } finally {
      setIsUploading(false)
      setAnalysisStatus(null)
    }
  }

  const handlePrimaryAction = async () => {
    if (isUploading || isAnalyzing) return
    if (!uploadedImage) {
      await handleUpload()
      return
    }
    await handleAnalyze()
  }

  useEffect(() => {
    if (!analysis || !resultRef.current) return

    resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    setHighlightResult(true)
    const timeout = setTimeout(() => setHighlightResult(false), 1200)

    return () => clearTimeout(timeout)
  }, [analysis])

  const reset = () => {
    setSelectedFile(null)
    setUploadedImage(null)
    setAnalysis(null)
    setAnalysisStatus(null)
    setHighlightResult(false)
    setError(null)
  }

  const canRunPrimary = Boolean(selectedFile || uploadedImage)

  const primaryButtonLabel = isUploading || isAnalyzing
    ? analysisStatus ?? 'Processing...'
    : uploadedImage
      ? 'Analyze Now'
      : 'Upload and Continue'

  const locationLabel = analysisLocation?.label ??
    (analysisLocation ? `${analysisLocation.latitude}, ${analysisLocation.longitude}` : null)

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Upload Section */}
      <Card className="rounded-xl shadow-sm border-emerald-100/80 bg-gradient-to-br from-white via-white to-emerald-50/40">
        <CardHeader className="pb-3 sm:pb-6">
          <div className="flex items-center gap-2">
            <Scan className="size-5 text-emerald-700" />
            <CardTitle className="text-lg sm:text-xl">Image Analysis</CardTitle>
          </div>
          <CardDescription className="text-sm">
            Upload clear photos of affected plant leaves for AI-powered disease detection
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4 sm:space-y-6">
          {!uploadedImage ? (
            <div className="space-y-4 sm:space-y-5">
              {locationLabel && (
                <div className="rounded-lg border border-emerald-200/80 bg-emerald-50/60 px-3 py-2 text-xs text-emerald-900">
                  <p className="font-medium">Location detected</p>
                  <p>{locationLabel}</p>
                </div>
              )}

              <div className="space-y-2">
                <p className="text-sm font-medium text-foreground">Try default samples</p>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                  {SAMPLE_IMAGES.map((sample) => (
                    <button
                      key={sample.id}
                      type="button"
                      onClick={() => void handleUseSample(sample)}
                      disabled={isUploading || isAnalyzing}
                      className="group overflow-hidden rounded-lg border bg-white text-left transition hover:border-emerald-400 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      <div className="relative h-24 w-full">
                        <Image
                          src={`/sample-images/${sample.src}`}
                          alt={sample.name}
                          fill
                          className="object-cover"
                          sizes="(max-width: 640px) 100vw, 33vw"
                        />
                      </div>
                      <div className="p-2 text-xs font-medium text-muted-foreground group-hover:text-foreground">
                        {sample.name}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span className="h-px flex-1 bg-border" />
                <span>or upload your own image</span>
                <span className="h-px flex-1 bg-border" />
              </div>

              <FileInput
                selectedFile={selectedFile}
                onFileSelect={setSelectedFile}
                accept="image/*"
                showCameraButton
                cameraCapture="environment"
                cameraLabel="Take Photo"
              />

              <Button
                onClick={handlePrimaryAction}
                disabled={!canRunPrimary || isUploading || isAnalyzing}
                className="w-full font-medium bg-emerald-600 hover:bg-emerald-700 text-white"
                size="default"
              >
                {isUploading || isAnalyzing ? (
                  <>
                    <Loader size="sm" />
                    {primaryButtonLabel}
                  </>
                ) : (
                  primaryButtonLabel
                )}
              </Button>
            </div>
          ) : (
            <div className="space-y-4 sm:space-y-5">
              {locationLabel && (
                <div className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-700">
                  <p className="font-medium text-slate-900">Analyzing for location</p>
                  <p>{locationLabel}</p>
                </div>
              )}

              <div className="flex flex-col gap-3 p-3 sm:p-4 bg-emerald-50/50 rounded-xl border border-emerald-100 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-center gap-2 min-w-0">
                  <CheckCircle className="size-4 text-green-600" />
                  <span className="text-sm font-medium">Image uploaded successfully</span>
                </div>

                <div className="flex items-center gap-3 self-start sm:self-auto">
                  <Image
                    src={`${finalBaseURL}analysis/images/${uploadedImage.image_id}/view`}
                    alt="Uploaded plant"
                    width={128}
                    height={128}
                    unoptimized
                    className="w-20 h-20 sm:w-32 sm:h-32 object-cover rounded-md"
                  />
                  <Button variant="outline" size="sm" onClick={reset}>
                    Upload New
                  </Button>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2 text-sm text-muted-foreground bg-muted/20 rounded-lg px-3 py-2">
                <span className="break-all font-medium">{uploadedImage.filename}</span>
                <Badge variant="secondary">
                  {(uploadedImage.file_size / 1024 / 1024).toFixed(2)} MB
                </Badge>
              </div>

              <Button
                onClick={handlePrimaryAction}
                disabled={isUploading || isAnalyzing}
                className="w-full font-medium bg-slate-900 hover:bg-slate-800 text-white"
                size="default"
              >
                {isAnalyzing ? (
                  <>
                    <Loader size="sm" />
                    {primaryButtonLabel}
                  </>
                ) : (
                  primaryButtonLabel
                )}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="size-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Analysis Results */}
      {analysis && (
        <div
          ref={resultRef}
          className={highlightResult ? 'rounded-xl ring-2 ring-emerald-400/60 ring-offset-2 ring-offset-background transition-all duration-500' : 'rounded-xl transition-all duration-500'}
        >
          <AnalysisResultViewer result={analysis} />
        </div>
      )}
    </div>
  )
}