"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ImageAnalysis } from '@/components/analysis/image-analysis'
import { AnalysisHistory } from '@/components/analysis/analysis-history'
import { History, ArrowLeft } from 'lucide-react'

export default function AnalysisDashboard() {
  const [showHistory, setShowHistory] = useState(false)
  const [analysisCount, setAnalysisCount] = useState(0)

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
            <ImageAnalysis onAnalysisComplete={handleAnalysisComplete} />
          )}
        </div>
      </div>
    </div>
  )
}