"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { FileInput } from '@/components/ui/file-input'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { AnalysisService } from '@/lib/analysis-service'
import { ImageUploadResponse, ImageAnalysisResponse } from '@/types/analysis'
import { AnalysisResultViewer } from '@/components/analysis/analysis-result-viewer'
import { Scan, Clock, Bot, AlertCircle, CheckCircle, Upload } from 'lucide-react'

interface ImageAnalysisProps {
  onAnalysisComplete?: (analysis: ImageAnalysisResponse) => void
}

export function ImageAnalysis({ onAnalysisComplete }: ImageAnalysisProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadedImage, setUploadedImage] = useState<ImageUploadResponse | null>(null)
  const [analysis, setAnalysis] = useState<ImageAnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setError(null)

    try {
      const uploadResponse = await AnalysisService.uploadImage(selectedFile)
      setUploadedImage(uploadResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  const handleAnalyze = async () => {
    if (!uploadedImage) return

    setIsAnalyzing(true)
    setError(null)

    try {
      const analysisResponse = await AnalysisService.analyzeImage({
        image_id: uploadedImage.image_id
      })
      setAnalysis(analysisResponse)
      onAnalysisComplete?.(analysisResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const reset = () => {
    setSelectedFile(null)
    setUploadedImage(null)
    setAnalysis(null)
    setError(null)
  }

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Scan className="size-5 text-primary" />
            <CardTitle>Image Analysis</CardTitle>
          </div>
          <CardDescription>
            Upload clear photos of affected plant leaves for AI-powered disease detection
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {!uploadedImage ? (
            <div className="space-y-4">
              <FileInput
                selectedFile={selectedFile}
                onFileSelect={setSelectedFile}
                accept="image/*"
              />

              {selectedFile && (
                <Button 
                  onClick={handleUpload}
                  disabled={isUploading}
                  className="w-full"
                  size="lg"
                >
                  {isUploading ? (
                    <>
                      <Loader size="sm" />
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Upload className="size-4 mr-2" />
                      Upload Image
                    </>
                  )}
                </Button>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                <div className="flex items-center gap-2">
                  <CheckCircle className="size-4 text-green-600" />
                    <span className="text-sm font-medium">Image uploaded successfully</span>
                    
                  </div>
                  <img
                    src={`http://localhost:8000/analysis/images/${uploadedImage.image_id}/view`}
                    alt="Uploaded plant"
                    className="w-32 h-32 object-cover rounded-md"
                  />
                <Button variant="outline" size="sm" onClick={reset}>
                  Upload New
                </Button>
              </div>

              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <span>{uploadedImage.filename}</span>
                <Badge variant="secondary">
                  {(uploadedImage.file_size / 1024 / 1024).toFixed(2)} MB
                </Badge>
              </div>

              <Button 
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                className="w-full"
                size="lg"
              >
                {isAnalyzing ? (
                  <>
                    <Loader size="sm" />
                    Analyzing with AI...
                  </>
                ) : (
                  <>
                    <Bot className="size-4" />
                    Analyze Plant Disease
                  </>
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
        <AnalysisResultViewer result={analysis} />
      )}
    </div>
  )
}