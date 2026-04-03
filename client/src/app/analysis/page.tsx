"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ImageAnalysis } from '@/components/analysis/image-analysis'
import { AnalysisHistory } from '@/components/analysis/analysis-history'
import { History, ArrowLeft } from 'lucide-react'

type ResponseLanguage = 'en' | 'hi'

export default function AnalysisDashboard() {
  const [showHistory, setShowHistory] = useState(false)
  const [analysisCount, setAnalysisCount] = useState(0)
  const [responseLanguage, setResponseLanguage] = useState<ResponseLanguage>('en')

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
              onAnalysisComplete={handleAnalysisComplete}
            />
          )}
        </div>
      </div>
    </div>
  )
}