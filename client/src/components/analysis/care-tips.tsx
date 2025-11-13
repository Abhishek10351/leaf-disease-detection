"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Loader } from '@/components/ui/loader'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { AnalysisService } from '@/lib/analysis-service'
import { CareResponse } from '@/types/analysis'
import { Sprout, Clock, Bot, AlertCircle, Heart, Lightbulb, Copy, Printer } from 'lucide-react'

interface CareTipsProps {
  onCareTipsComplete?: (tips: CareResponse) => void
}

const COMMON_PLANTS = [
  'Tomato', 'Rose', 'Sunflower', 'Basil', 'Mint', 'Lettuce', 
  'Pepper', 'Cucumber', 'Strawberry', 'Lavender', 'Geranium', 
  'Marigold', 'Apple tree', 'Lemon tree', 'Orchid', 'Succulent'
]

export function CareTips({ onCareTipsComplete }: CareTipsProps) {
  const [plantType, setPlantType] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [careTips, setCareTips] = useState<CareResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGetTips = async () => {
    if (!plantType.trim()) {
      setError('Please specify a plant type')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const tipsResponse = await AnalysisService.getCareTips({
        plant_type: plantType
      })
      setCareTips(tipsResponse)
      onCareTipsComplete?.(tipsResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get care tips')
    } finally {
      setIsLoading(false)
    }
  }

  const reset = () => {
    setPlantType('')
    setCareTips(null)
    setError(null)
  }

  const selectPlant = (plant: string) => {
    setPlantType(plant)
  }

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sprout className="size-5 text-primary" />
            <CardTitle>Plant Care Guide</CardTitle>
          </div>
          <CardDescription>
            Get comprehensive care instructions and tips for keeping your plants healthy
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="plant-type">Plant Type *</Label>
            <Input
              id="plant-type"
              placeholder="e.g., Tomato, Rose, Apple tree..."
              value={plantType}
              onChange={(e) => setPlantType(e.target.value)}
              disabled={isLoading}
            />
            <p className="text-xs text-muted-foreground">
              Enter the name of the plant you want care tips for
            </p>
          </div>

          {/* Quick Select Common Plants */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Lightbulb className="size-4 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">Quick select:</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {COMMON_PLANTS.map((plant) => (
                <Button
                  key={plant}
                  variant="outline"
                  size="sm"
                  onClick={() => selectPlant(plant)}
                  disabled={isLoading}
                  className="text-xs"
                >
                  {plant}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Button 
              onClick={handleGetTips}
              disabled={isLoading || !plantType.trim()}
              className="w-full"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader size="sm" />
                  Getting Care Tips...
                </>
              ) : (
                <>
                  <Heart className="size-4" />
                  Get Care Tips
                </>
              )}
            </Button>

            {(careTips || plantType) && (
              <Button 
                variant="ghost"
                onClick={reset}
                className="w-full"
              >
                Clear & Search New Plant
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="size-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Care Tips Results */}
      {careTips && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Heart className="size-5 text-primary" />
                <CardTitle>Care Guide</CardTitle>
              </div>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Clock className="size-4" />
                <span>{new Date(careTips.timestamp).toLocaleString()}</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline">
                {careTips.model_used}
              </Badge>
              <Badge variant="secondary">
                Care Guide
              </Badge>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-4">
            {/* Plant Type Display */}
            <div className="p-3 bg-muted/50 rounded-lg">
              <p className="text-sm font-medium text-muted-foreground">Plant:</p>
              <p className="text-lg font-semibold capitalize">{careTips.plant_type}</p>
            </div>

            <div className="prose prose-sm max-w-none">
              <div className="whitespace-pre-wrap text-foreground">
                {careTips.care_tips}
              </div>
            </div>
          </CardContent>

          <CardFooter className="border-t">
            <div className="flex gap-2 w-full">
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  navigator.clipboard?.writeText(careTips.care_tips)
                }}
                className="flex-1"
              >
                <Copy className="size-4 mr-2" />
                Copy Tips
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  window.print()
                }}
                className="flex-1"
              >
                <Printer className="size-4 mr-2" />
                Print Guide
              </Button>
            </div>
          </CardFooter>
        </Card>
      )}
    </div>
  )
}