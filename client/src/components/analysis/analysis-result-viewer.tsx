"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { MarkdownViewer } from "@/components/ui/markdown-viewer";
import { Button } from "@/components/ui/button";
import {
    Bot,
    AlertCircle,
    CheckCircle,
    AlertTriangle,
    XCircle,
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ImageAnalysisResponse, SymptomsAnalysisResponse, PlantCareResponse } from "@/types/analysis";

type AnalysisResult = ImageAnalysisResponse | SymptomsAnalysisResponse | PlantCareResponse;

interface AnalysisResultViewerProps {
    result: AnalysisResult;
    title?: string;
    showMetadata?: boolean;
}

const getSeverityIcon = (severity?: string) => {
    switch (severity?.toLowerCase()) {
        case "healthy":
            return <CheckCircle className="h-4 w-4 text-green-500" />;
        case "mild":
            return <AlertCircle className="h-4 w-4 text-yellow-500" />;
        case "moderate":
            return <AlertTriangle className="h-4 w-4 text-orange-500" />;
        case "severe":
            return <XCircle className="h-4 w-4 text-red-500" />;
        default:
            return <AlertCircle className="h-4 w-4 text-gray-500" />;
    }
};

const getSeverityColor = (severity?: string) => {
    switch (severity?.toLowerCase()) {
        case "healthy":
            return "bg-green-100 text-green-800 border-green-200";
        case "mild":
            return "bg-yellow-100 text-yellow-800 border-yellow-200";
        case "moderate":
            return "bg-orange-100 text-orange-800 border-orange-200";
        case "severe":
            return "bg-red-100 text-red-800 border-red-200";
        default:
            return "bg-gray-100 text-gray-800 border-gray-200";
    }
};

const getDifficultyColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
        case "easy":
            return "bg-green-100 text-green-800 border-green-200";
        case "moderate":
            return "bg-yellow-100 text-yellow-800 border-yellow-200";
        case "difficult":
            return "bg-red-100 text-red-800 border-red-200";
        default:
            return "bg-gray-100 text-gray-800 border-gray-200";
    }
};

const isImageAnalysis = (result: AnalysisResult): result is ImageAnalysisResponse => {
    return 'plant_identification' in result;
};

const isSymptomsAnalysis = (result: AnalysisResult): result is SymptomsAnalysisResponse => {
    return 'likely_condition' in result;
};

const isPlantCare = (result: AnalysisResult): result is PlantCareResponse => {
    return 'care_difficulty' in result;
};

export function AnalysisResultViewer({
    result,
    title,
    showMetadata = true,
}: AnalysisResultViewerProps) {
    const [activeTab, setActiveTab] = useState("basic");

    const summaryText =
        isImageAnalysis(result) || isSymptomsAnalysis(result)
            ? result.quick_summary
                  .replace(/see full report below\.?/gi, "")
                  .replace(/\s{2,}/g, " ")
                  .trim()
            : "";

    const detailedContent = isImageAnalysis(result) || isSymptomsAnalysis(result) 
        ? result.detailed_analysis 
        : result.detailed_guide;

    return (
        <Card className="w-full">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Bot className="h-5 w-5 text-primary" />
                        <CardTitle className="text-lg">
                            {title ||
                                (isPlantCare(result)
                                    ? "Care Instructions"
                                    : "Analysis Results")}
                        </CardTitle>
                    </div>
                </div>
                {(isImageAnalysis(result) || isSymptomsAnalysis(result)) && (
                    <div className="space-y-2">
                        <CardDescription className="text-base">
                            {summaryText}
                        </CardDescription>
                    </div>
                )}
                {isPlantCare(result) && (
                    <div className="mt-2">
                        <MarkdownViewer
                            content={result.quick_overview}
                            compact
                            className="prose prose-sm max-w-none text-sm"
                        />
                    </div>
                )}
                {showMetadata && (
                    <div className="flex flex-wrap items-center gap-2 mt-4 pt-3 border-t">
                        {isImageAnalysis(result) && (
                            <>
                                <Badge
                                    variant="outline"
                                    className={`text-xs flex items-center gap-1 ${getSeverityColor(
                                        result.health_status
                                    )}`}
                                >
                                    {getSeverityIcon(result.health_status)}
                                    {result.health_status}
                                </Badge>
                                <Badge variant="outline" className="text-xs">
                                    Confidence: {result.confidence}
                                </Badge>
                            </>
                        )}

                        {isSymptomsAnalysis(result) && (
                            <>
                                <Badge
                                    variant="outline"
                                    className={`text-xs flex items-center gap-1 ${getSeverityColor(
                                        result.severity
                                    )}`}
                                >
                                    {getSeverityIcon(result.severity)}
                                    {result.severity}
                                </Badge>
                                <Badge variant="outline" className="text-xs">
                                    Confidence: {result.confidence}
                                </Badge>
                            </>
                        )}

                        {isPlantCare(result) && (
                            <Badge
                                variant="outline"
                                className={`text-xs ${getDifficultyColor(
                                    result.care_difficulty
                                )}`}
                            >
                                {result.care_difficulty} Care
                            </Badge>
                        )}
                    </div>
                )}
            </CardHeader>

            <CardContent className="space-y-6">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                    <TabsList className="w-full justify-start overflow-x-auto">
                        <TabsTrigger value="basic">Basic</TabsTrigger>
                        <TabsTrigger value="actions">Actions</TabsTrigger>
                        <TabsTrigger value="detailed">Detailed</TabsTrigger>
                    </TabsList>

                    <TabsContent value="basic" className="mt-4 space-y-4">
                        {isImageAnalysis(result) && (
                            <div className="grid gap-3">
                                <div className="p-3 bg-muted/50 rounded-lg">
                                    <div className="text-xs font-medium text-muted-foreground mb-1">
                                        Plant
                                    </div>
                                    <div className="text-sm leading-relaxed">
                                        {result.plant_identification}
                                    </div>
                                </div>
                                <div className="p-3 bg-muted/50 rounded-lg">
                                    <div className="text-xs font-medium text-muted-foreground mb-1">
                                        Main Issue
                                    </div>
                                    <div className="text-sm leading-relaxed">
                                        {result.primary_issue}
                                    </div>
                                </div>
                            </div>
                        )}

                        {isSymptomsAnalysis(result) && (
                            <div className="p-3 bg-muted/50 rounded-lg">
                                <div className="text-xs font-medium text-muted-foreground mb-1">
                                    Likely Condition
                                </div>
                                <div className="text-sm leading-relaxed">
                                    {result.likely_condition}
                                </div>
                            </div>
                        )}

                        {isPlantCare(result) && (
                            <div className="p-3 rounded-lg border bg-muted/40 text-sm text-muted-foreground">
                                Quick overview shown above. Use the Actions and Detailed tabs for full care guidance.
                            </div>
                        )}
                    </TabsContent>

                    <TabsContent value="actions" className="mt-4 space-y-4">
                        {isImageAnalysis(result) && (
                            <>
                                <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-3">
                                        🚨 Immediate Action Required
                                    </h4>
                                    <MarkdownViewer
                                        content={result.immediate_action}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                                <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-3">
                                        💊 Treatment Plan
                                    </h4>
                                    <MarkdownViewer
                                        content={result.treatment}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                                <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-green-800 dark:text-green-200 mb-3">
                                        🛡️ Prevention Strategies
                                    </h4>
                                    <MarkdownViewer
                                        content={result.prevention}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                            </>
                        )}

                        {isSymptomsAnalysis(result) && (
                            <>
                                <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-3">
                                        🚨 Immediate Action Required
                                    </h4>
                                    <MarkdownViewer
                                        content={result.immediate_action}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                                <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-3">
                                        💊 Treatment Steps
                                    </h4>
                                    <MarkdownViewer
                                        content={result.treatment_steps}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                                <div className="p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg">
                                    <h4 className="text-sm font-semibold text-purple-800 dark:text-purple-200 mb-3">
                                        👀 What to Monitor
                                    </h4>
                                    <MarkdownViewer
                                        content={result.what_to_watch}
                                        compact
                                        className="prose prose-sm max-w-none text-sm"
                                    />
                                </div>
                            </>
                        )}

                        {isPlantCare(result) && (
                            <>
                                <div className="space-y-4">
                                    <h4 className="text-sm font-semibold">
                                        🌱 Essential Care Requirements
                                    </h4>
                                    <div className="grid gap-4">
                                        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
                                            <div className="text-sm font-semibold text-amber-800 dark:text-amber-200 mb-2">
                                                ☀️ Light Requirements
                                            </div>
                                            <MarkdownViewer
                                                content={result.essential_care.light}
                                                compact
                                                className="prose prose-sm max-w-none text-sm text-amber-700 dark:text-amber-300"
                                            />
                                        </div>
                                        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                                            <div className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
                                                💧 Watering Guidelines
                                            </div>
                                            <MarkdownViewer
                                                content={result.essential_care.water}
                                                compact
                                                className="prose prose-sm max-w-none text-sm text-blue-700 dark:text-blue-300"
                                            />
                                        </div>
                                        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                                            <div className="text-sm font-semibold text-green-800 dark:text-green-200 mb-2">
                                                🌿 Soil Requirements
                                            </div>
                                            <MarkdownViewer
                                                content={result.essential_care.soil}
                                                compact
                                                className="prose prose-sm max-w-none text-sm text-green-700 dark:text-green-300"
                                            />
                                        </div>
                                    </div>
                                </div>
                                {result.key_tips && result.key_tips.length > 0 && (
                                    <div className="space-y-3">
                                        <h4 className="text-sm font-semibold">
                                            💡 Expert Tips
                                        </h4>
                                        <div className="space-y-3">
                                            {result.key_tips.map((tip, index) => (
                                                <div
                                                    key={index}
                                                    className="p-3 bg-muted/30 rounded-lg border-l-4 border-primary"
                                                >
                                                    <MarkdownViewer
                                                        content={tip}
                                                        compact
                                                        className="prose prose-sm max-w-none text-sm"
                                                    />
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                                {result.common_problems && result.common_problems.length > 0 && (
                                    <div className="space-y-3">
                                        <h4 className="text-sm font-semibold">
                                            ⚠️ Common Problems & Solutions
                                        </h4>
                                        <div className="space-y-3">
                                            {result.common_problems.map((problem, index) => (
                                                <div
                                                    key={index}
                                                    className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
                                                >
                                                    <MarkdownViewer
                                                        content={problem}
                                                        compact
                                                        className="prose prose-sm max-w-none text-sm text-red-800 dark:text-red-200"
                                                    />
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </>
                        )}
                    </TabsContent>

                    <TabsContent value="detailed" className="mt-4 pt-1">
                        <h4 className="text-sm font-semibold mb-3">Detailed Analysis</h4>
                        <MarkdownViewer
                            content={detailedContent}
                            className="prose prose-sm max-w-none"
                        />
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
}
