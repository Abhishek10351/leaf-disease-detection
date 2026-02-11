"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { AnalysisService } from '@/lib/analysis-service'
import { SymptomsAnalysisResponse } from '@/types/analysis'
import { AnalysisResultViewer } from '@/components/analysis/analysis-result-viewer'
import { FileText, Clock, Bot, AlertCircle } from 'lucide-react'

interface SymptomsAnalysisProps {
  onAnalysisComplete?: (analysis: SymptomsAnalysisResponse) => void
}

export function SymptomsAnalysis({ onAnalysisComplete }: SymptomsAnalysisProps) {
  const [symptomsDescription, setSymptomsDescription] = useState('')
  const [plantType, setPlantType] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysis, setAnalysis] = useState<SymptomsAnalysisResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!symptomsDescription.trim()) {
      setError('Please describe the symptoms you observed')
      return
    }

    setIsAnalyzing(true)
    setError(null)

    try {
      const analysisResponse = await AnalysisService.analyzeSymptoms({
        symptoms_description: symptomsDescription,
        plant_type: plantType || undefined
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
    setSymptomsDescription('')
    setPlantType('')
    setAnalysis(null)
    setError(null)
  }

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <FileText className="size-5 text-primary" />
            <CardTitle className="text-lg">Symptoms Analysis</CardTitle>
          </div>
          <CardDescription>Describe the symptoms you've observed on your plant</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">

          <div className="space-y-2">
            <Label htmlFor="plant-type">Plant Type (Optional)</Label>
            <Input
              id="plant-type"
              placeholder="e.g., Tomato, Rose, Apple tree..."
              value={plantType}
              onChange={(e) => setPlantType(e.target.value)}
              disabled={isAnalyzing}
            />
            <p className="text-xs text-muted-foreground">
              Specify the plant type for more accurate diagnosis
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="symptoms">Symptoms Description *</Label>
            <Textarea
              id="symptoms"
              placeholder="Describe the symptoms you've observed on your plant. Include details about leaf color changes, spots, wilting, growth patterns, etc. The more detailed your description, the better the analysis will be."
              value={symptomsDescription}
              onChange={(e) => setSymptomsDescription(e.target.value)}
              disabled={isAnalyzing}
              rows={6}
              className="min-h-[120px]"
            />
            <p className="text-xs text-muted-foreground">
              Be as specific as possible about colors, locations, patterns, and progression
            </p>
          </div>

          <Button 
            onClick={handleAnalyze}
            disabled={isAnalyzing || !symptomsDescription.trim()}
            className="w-full"
            size="lg"
          >
            {isAnalyzing ? (
              <>
                <Loader size="sm" />
                Analyzing Symptoms...
              </>
            ) : (
              <>
                <Bot className="size-4" />
                Analyze Symptoms
              </>
            )}
          </Button>

          {(analysis || symptomsDescription || plantType) && (
            <Button 
              variant="ghost"
              onClick={reset}
              className="w-full"
            >
              Clear & Start New Analysis
            </Button>
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
        <>
          {/* Input Summary */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Analysis Input</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {plantType && (
                <p className="text-sm"><span className="font-medium">Plant Type:</span> {plantType}</p>
              )}
              <p className="text-sm">
                <span className="font-medium">Symptoms:</span> 
                <span className="block mt-1 text-muted-foreground">
                  {symptomsDescription.length > 200 
                    ? `${symptomsDescription.substring(0, 200)}...`
                    : symptomsDescription
                  }
                </span>
              </p>
            </CardContent>
          </Card>
          
          <AnalysisResultViewer result={analysis} title="Symptoms Analysis" />
        </>
      )}
    </div>
  )
}