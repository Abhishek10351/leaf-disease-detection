"use client"

import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card } from '@/components/ui/card'
import { ImageAnalysis } from '@/components/analysis/image-analysis'
import { SymptomsAnalysis } from '@/components/analysis/symptoms-analysis'
import { CareTips } from '@/components/analysis/care-tips'
import { AnalysisHistory } from '@/components/analysis/analysis-history'
import { Scan, FileText, Sprout, History, Bot } from 'lucide-react'

export default function AnalysisDashboard() {
  const [activeTab, setActiveTab] = useState("image")
  const [analysisCount, setAnalysisCount] = useState(0)

  const handleAnalysisComplete = () => {
    setAnalysisCount(prev => prev + 1)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center size-12 bg-primary text-primary-foreground rounded-xl">
              <Bot className="size-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">Leaf Disease Detection</h1>
              <p className="text-muted-foreground">AI-powered plant health analysis and care recommendations</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          {/* Tab Navigation */}
          <div className="flex justify-center">
            <TabsList className="grid w-full max-w-2xl grid-cols-4 bg-muted/50">
              <TabsTrigger value="image" className="flex items-center gap-2">
                <Scan className="size-4" />
                <span className="hidden sm:inline">Image Analysis</span>
                <span className="sm:hidden">Image</span>
              </TabsTrigger>
              <TabsTrigger value="symptoms" className="flex items-center gap-2">
                <FileText className="size-4" />
                <span className="hidden sm:inline">Symptoms</span>
                <span className="sm:hidden">Text</span>
              </TabsTrigger>
              <TabsTrigger value="care" className="flex items-center gap-2">
                <Sprout className="size-4" />
                <span className="hidden sm:inline">Care Tips</span>
                <span className="sm:hidden">Care</span>
              </TabsTrigger>
              <TabsTrigger value="history" className="flex items-center gap-2">
                <History className="size-4" />
                <span className="hidden sm:inline">History</span>
                <span className="sm:hidden">History</span>
              </TabsTrigger>
            </TabsList>
          </div>

          {/* Tab Content */}
          <div className="max-w-4xl mx-auto">
            <TabsContent value="image" className="mt-6">
              <div className="space-y-4">
                <Card className="p-6 bg-muted/20 border-dashed">
                  <div className="text-center space-y-2">
                    <Scan className="size-8 text-primary mx-auto" />
                    <h3 className="text-lg font-semibold">Upload Plant Image</h3>
                    <p className="text-muted-foreground text-sm">
                      Take a clear photo of the affected plant leaves for AI-powered disease detection and diagnosis.
                    </p>
                  </div>
                </Card>
                <ImageAnalysis onAnalysisComplete={handleAnalysisComplete} />
              </div>
            </TabsContent>

            <TabsContent value="symptoms" className="mt-6">
              <div className="space-y-4">
                <Card className="p-6 bg-muted/20 border-dashed">
                  <div className="text-center space-y-2">
                    <FileText className="size-8 text-primary mx-auto" />
                    <h3 className="text-lg font-semibold">Describe Symptoms</h3>
                    <p className="text-muted-foreground text-sm">
                      Describe the symptoms you've observed on your plant for text-based analysis and recommendations.
                    </p>
                  </div>
                </Card>
                <SymptomsAnalysis onAnalysisComplete={handleAnalysisComplete} />
              </div>
            </TabsContent>

            <TabsContent value="care" className="mt-6">
              <div className="space-y-4">
                <Card className="p-6 bg-muted/20 border-dashed">
                  <div className="text-center space-y-2">
                    <Sprout className="size-8 text-primary mx-auto" />
                    <h3 className="text-lg font-semibold">Plant Care Guide</h3>
                    <p className="text-muted-foreground text-sm">
                      Get comprehensive care instructions and tips for keeping your plants healthy and thriving.
                    </p>
                  </div>
                </Card>
                <CareTips onCareTipsComplete={handleAnalysisComplete} />
              </div>
            </TabsContent>

            <TabsContent value="history" className="mt-6">
              <div className="space-y-4">
                <Card className="p-6 bg-muted/20 border-dashed">
                  <div className="text-center space-y-2">
                    <History className="size-8 text-primary mx-auto" />
                    <h3 className="text-lg font-semibold">Analysis History</h3>
                    <p className="text-muted-foreground text-sm">
                      Review your previous analyses, care tips, and track your plant health journey.
                    </p>
                  </div>
                </Card>
                <AnalysisHistory key={analysisCount} />
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>

      {/* Footer */}
      <footer className="border-t bg-card/50 mt-16">
        <div className="container mx-auto px-4 py-8 text-center">
          <p className="text-muted-foreground text-sm">
            Powered by AI • Keep your plants healthy with expert analysis and care recommendations
          </p>
        </div>
      </footer>
    </div>
  )
}