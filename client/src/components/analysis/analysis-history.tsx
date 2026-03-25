"use client"

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AnalysisService } from '@/lib/analysis-service'
import { AnalysisResultViewer } from '@/components/analysis/analysis-result-viewer'
import { MarkdownViewer } from '@/components/ui/markdown-viewer'
import { finalBaseURL } from '@/app/utils/api'
import {
  AnalysisHistory as AnalysisHistoryType,
  ImageAnalysisResponse,
  PlantCareResponse,
  SymptomsAnalysisResponse,
} from '@/types/analysis'
import { 
  History, 
  Scan, 
  FileText, 
  Sprout, 
  Clock, 
  AlertCircle, 
  RefreshCw,
  Eye,
  Trash2
} from 'lucide-react'

export function AnalysisHistory() {
  const [history, setHistory] = useState<AnalysisHistoryType[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [loadingDetailId, setLoadingDetailId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [expandedItem, setExpandedItem] = useState<string | null>(null)

  const loadHistory = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await AnalysisService.getAnalysisHistory(50, 0)
      setHistory(response.history)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load history')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const getAnalysisIcon = (type: string) => {
    switch (type) {
      case 'image':
        return <Scan className="size-4" />
      case 'symptoms':
        return <FileText className="size-4" />
      case 'care':
        return <Sprout className="size-4" />
      default:
        return <History className="size-4" />
    }
  }

  const getAnalysisLabel = (type: string) => {
    switch (type) {
      case 'image':
        return 'Image Analysis'
      case 'symptoms':
        return 'Symptoms Analysis'
      case 'care':
        return 'Care Tips'
      default:
        return 'Analysis'
    }
  }

  const fetchDetailForItem = async (id: string) => {
    try {
      setLoadingDetailId(id)
      const detail = await AnalysisService.getAnalysisDetail(id)
      setHistory(prev =>
        prev.map(item => {
          if (item.id !== id) {
            return item
          }

          const previewSource =
            (typeof detail.response_data?.quick_summary === 'string' && detail.response_data.quick_summary) ||
            (typeof detail.response_data?.quick_overview === 'string' && detail.response_data.quick_overview) ||
            (typeof detail.response_data?.analysis === 'string' && detail.response_data.analysis) ||
            item.preview ||
            ''

          return {
            ...item,
            request_data: detail.request_data,
            response_data: detail.response_data,
            preview: previewSource ? `${previewSource}`.slice(0, 200) + (`${previewSource}`.length > 200 ? '...' : '') : item.preview,
          }
        })
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analysis details')
    } finally {
      setLoadingDetailId(null)
    }
  }

  const toggleExpanded = (id: string) => {
    if (expandedItem === id) {
      setExpandedItem(null)
      return
    }

    setExpandedItem(id)
    void fetchDetailForItem(id)
  }

  const handleDelete = async (id: string) => {
    try {
      await AnalysisService.deleteAnalysis(id)
      setHistory(prev => prev.filter(item => item.id !== id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete analysis')
    }
  }

  const isImageResponse = (value: unknown): value is ImageAnalysisResponse => {
    if (!value || typeof value !== 'object') {
      return false
    }
    const data = value as Record<string, unknown>
    return (
      typeof data.plant_identification === 'string' &&
      typeof data.health_status === 'string' &&
      typeof data.confidence === 'string'
    )
  }

  const isSymptomsResponse = (value: unknown): value is SymptomsAnalysisResponse => {
    if (!value || typeof value !== 'object') {
      return false
    }
    const data = value as Record<string, unknown>
    return (
      typeof data.likely_condition === 'string' &&
      typeof data.severity === 'string' &&
      typeof data.confidence === 'string'
    )
  }

  const isCareResponse = (value: unknown): value is PlantCareResponse => {
    if (!value || typeof value !== 'object') {
      return false
    }
    const data = value as Record<string, unknown>
    return (
      typeof data.care_difficulty === 'string' &&
      typeof data.quick_overview === 'string' &&
      typeof data.essential_care === 'object' &&
      data.essential_care !== null
    )
  }

  const getRenderableResult = (
    item: AnalysisHistoryType
  ): ImageAnalysisResponse | SymptomsAnalysisResponse | PlantCareResponse | null => {
    const payload = item.response_data
    if (!payload || typeof payload !== 'object') {
      return null
    }

    if (item.analysis_type === 'image' && isImageResponse(payload)) {
      return payload
    }
    if (item.analysis_type === 'symptoms' && isSymptomsResponse(payload)) {
      return payload
    }
    if (item.analysis_type === 'care' && isCareResponse(payload)) {
      return payload
    }

    return null
  }

  const getLegacyResultText = (responseData: Record<string, unknown>): string | null => {
    const candidates = [
      responseData.analysis,
      responseData.care_tips,
      responseData.detailed_analysis,
      responseData.detailed_guide,
      responseData.quick_summary,
      responseData.quick_overview,
    ]

    for (const value of candidates) {
      if (typeof value === 'string' && value.trim()) {
        return value
      }
    }

    return null
  }

  const getImageId = (requestData: Record<string, unknown>): string | null => {
    const imageId = requestData.image_id
    return typeof imageId === 'string' ? imageId : null
  }

  if (isLoading && history.length === 0) {
    return (
      <Card>
        <CardContent className="p-12 text-center">
          <Loader size="lg" text="Loading your analysis history..." />
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="size-5 text-primary" />
              <CardTitle className="text-lg">Analysis History</CardTitle>
              {history.length > 0 && (
                <Badge variant="secondary">{history.length} items</Badge>
              )}
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={loadHistory}
              disabled={isLoading}
            >
              {isLoading ? (
                <Loader size="sm" />
              ) : (
                <RefreshCw className="size-4" />
              )}
              Refresh
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="size-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* History Items */}
      {history.length === 0 && !isLoading ? (
        <Card>
          <CardContent className="p-12 text-center">
            <History className="size-12 text-muted-foreground mx-auto mb-4" />
            <CardTitle className="text-lg text-muted-foreground mb-2">No Analysis History</CardTitle>
            <CardDescription>
              Your analysis history will appear here after you perform image analysis, symptoms analysis, or get care tips.
            </CardDescription>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {history.map((item) => {
            const renderableResult = getRenderableResult(item)

            return (
              <Card key={item.id} className="transition-all hover:shadow-md">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                    <div className="flex items-center justify-center size-10 bg-primary/10 text-primary rounded-lg">
                      {getAnalysisIcon(item.analysis_type)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="outline" className="text-xs">
                          {getAnalysisLabel(item.analysis_type)}
                        </Badge>
                        <div className="flex items-center gap-1 text-xs text-muted-foreground">
                          <Clock className="size-3" />
                          {new Date(item.timestamp).toLocaleDateString()} at{' '}
                          {new Date(item.timestamp).toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </div>
                      </div>
                      
                      {item.preview && (
                        <CardDescription className="line-clamp-2">
                          {item.preview}
                        </CardDescription>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExpanded(item.id)}
                    >
                      <Eye className="size-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(item.id)}
                      className="text-muted-foreground hover:text-destructive"
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>

              {/* Expanded Content */}
              {expandedItem === item.id && (
                <CardContent className="pt-0">
                  <div className="space-y-3 border-t pt-4">
                    {/* Analysis Result */}
                    <div className="space-y-2">
                      <p className="text-sm font-medium text-muted-foreground">Analysis Result:</p>
                      {loadingDetailId === item.id ? (
                        <div className="p-4 rounded-lg border bg-muted/20">
                          <Loader size="sm" text="Loading full analysis..." />
                        </div>
                      ) : renderableResult ? (
                        <AnalysisResultViewer
                          result={renderableResult}
                          showMetadata
                        />
                      ) : getLegacyResultText(item.response_data) ? (
                        <div className="p-4 bg-card border rounded-lg">
                          <MarkdownViewer content={getLegacyResultText(item.response_data) || ''} />
                        </div>
                      ) : (
                        <div className="p-4 rounded-lg border bg-muted/20 text-sm text-muted-foreground">
                          Detailed analysis content is not available for this older record.
                        </div>
                      )}
                    </div>

                    {/* Uploaded Image Preview */}
                    {item.analysis_type === 'image' && getImageId(item.request_data) && (
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-muted-foreground">Uploaded Leaf Image:</p>
                        <div className="p-3 border rounded-lg bg-muted/20">
                          <Image
                            src={`${finalBaseURL}analysis/images/${getImageId(item.request_data)}/view`}
                            alt="Uploaded leaf for this analysis"
                            width={420}
                            height={300}
                            unoptimized
                            className="w-full max-w-md h-auto object-cover rounded-md border"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              )}
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}