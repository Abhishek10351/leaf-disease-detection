"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AnalysisService } from '@/lib/analysis-service'
import { AnalysisHistory as AnalysisHistoryType } from '@/types/analysis'
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

  const toggleExpanded = (id: string) => {
    setExpandedItem(expandedItem === id ? null : id)
  }

  const handleDelete = async (id: string) => {
    try {
      await AnalysisService.deleteAnalysis(id)
      setHistory(prev => prev.filter(item => item.id !== id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete analysis')
    }
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
          {history.map((item) => (
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
                    {/* Request Data */}
                    <div className="space-y-2">
                      <p className="text-sm font-medium text-muted-foreground">Request Details:</p>
                      <div className="p-3 bg-muted/50 rounded-lg text-sm">
                        <pre className="whitespace-pre-wrap font-mono text-xs">
                          {JSON.stringify(item.request_data, null, 2)}
                        </pre>
                      </div>
                    </div>
                    
                    <CardFooter className="px-0 pb-0">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          navigator.clipboard?.writeText(
                            JSON.stringify(item, null, 2)
                          )
                        }}
                      >
                        Copy Data
                      </Button>
                    </CardFooter>
                  </div>
                </CardContent>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}