"use client";

import { Badge } from "@/components/ui/badge";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { MarkdownViewer } from "@/components/ui/markdown-viewer";
import {
    Clock,
    Bot,
    AlertCircle,
    CheckCircle,
    AlertTriangle,
    XCircle,
} from "lucide-react";
import { AnalysisResponse, CareResponse } from "@/types/analysis";

interface AnalysisResultViewerProps {
    result: AnalysisResponse | CareResponse;
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

export function AnalysisResultViewer({
    result,
    title,
    showMetadata = true,
}: AnalysisResultViewerProps) {
    const isAnalysis = "analysis" in result;
    const isCare = "care_tips" in result;

    const content = isAnalysis ? result.analysis : result.care_tips;
    const analysisType = isAnalysis ? result.analysis_type : "care";

    return (
        <Card className="w-full">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Bot className="h-5 w-5 text-primary" />
                        <CardTitle className="text-lg">
                            {title ||
                                (isAnalysis
                                    ? "Analysis Results"
                                    : "Care Instructions")}
                        </CardTitle>
                    </div>
                    {showMetadata && (
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <Clock className="h-4 w-4" />
                            {new Date(result.timestamp).toLocaleString()}
                        </div>
                    )}
                </div>

                {isAnalysis && result.summary && (
                    <CardDescription className="text-base">
                        {result.summary}
                    </CardDescription>
                )}

                {isCare && result.quick_overview && (
                    <CardDescription className="text-base">
                        {result.quick_overview}
                    </CardDescription>
                )}                {showMetadata && (
                    <div className="flex flex-wrap items-center gap-2 mt-3">
                        <Badge variant="outline" className="text-xs">
                            {result.model_used}
                        </Badge>

                        <Badge
                            variant="secondary"
                            className="text-xs capitalize"
                        >
                            {analysisType}
                        </Badge>

                        {isAnalysis && result.severity && (
                            <Badge
                                variant="outline"
                                className={`text-xs flex items-center gap-1 ${getSeverityColor(
                                    result.severity
                                )}`}
                            >
                                {getSeverityIcon(result.severity)}
                                {result.severity}
                            </Badge>
                        )}

                        {isCare && result.care_difficulty && (
                            <Badge
                                variant="outline"
                                className={`text-xs ${getDifficultyColor(
                                    result.care_difficulty
                                )}`}
                            >
                                {result.care_difficulty} Care
                            </Badge>
                        )}

                        {isAnalysis && result.confidence && (
                            <Badge variant="outline" className="text-xs">
                                {result.confidence}
                            </Badge>
                        )}

                        {isCare && result.plant_type && (
                            <Badge
                                variant="outline"
                                className="text-xs capitalize"
                            >
                                {result.plant_type}
                            </Badge>
                        )}
                    </div>
                )}
            </CardHeader>

            <CardContent className="space-y-6">
                {/* Quick Overview for Analysis */}
                {isAnalysis && (
                    <div className="space-y-4">
                        {(result.plant_identification ||
                            result.primary_issue ||
                            result.likely_condition) && (
                            <div className="grid gap-3">
                                {result.plant_identification && (
                                    <div className="flex items-center gap-2 p-3 bg-muted/50 rounded-lg">
                                        <span className="text-sm font-medium text-muted-foreground">
                                            Plant:
                                        </span>
                                        <span className="text-sm">
                                            {result.plant_identification}
                                        </span>
                                    </div>
                                )}
                                {(result.primary_issue ||
                                    result.likely_condition) && (
                                    <div className="flex items-center gap-2 p-3 bg-muted/50 rounded-lg">
                                        <span className="text-sm font-medium text-muted-foreground">
                                            Issue:
                                        </span>
                                        <span className="text-sm">
                                            {result.primary_issue ||
                                                result.likely_condition}
                                        </span>
                                    </div>
                                )}
                            </div>
                        )}

                        {result.immediate_action && (
                            <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                                <h4 className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 mb-3">
                                    🚨 Immediate Action Required
                                </h4>
                                <div className="text-sm text-yellow-700 dark:text-yellow-300 whitespace-pre-line leading-relaxed">
                                    {result.immediate_action}
                                </div>
                            </div>
                        )}

                        {(result.treatment || result.treatment_steps) && (
                            <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                                <h4 className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-3">
                                    💊 Treatment Plan
                                </h4>
                                <div className="text-sm text-blue-700 dark:text-blue-300 whitespace-pre-line leading-relaxed">
                                    {result.treatment || result.treatment_steps}
                                </div>
                            </div>
                        )}

                        {result.prevention && (
                            <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                                <h4 className="text-sm font-semibold text-green-800 dark:text-green-200 mb-3">
                                    🛡️ Prevention Strategies
                                </h4>
                                <div className="text-sm text-green-700 dark:text-green-300 whitespace-pre-line leading-relaxed">
                                    {result.prevention}
                                </div>
                            </div>
                        )}

                        {result.what_to_watch && (
                            <div className="p-4 bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg">
                                <h4 className="text-sm font-semibold text-purple-800 dark:text-purple-200 mb-3">
                                    👀 What to Monitor
                                </h4>
                                <div className="text-sm text-purple-700 dark:text-purple-300 whitespace-pre-line leading-relaxed">
                                    {result.what_to_watch}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* Quick Overview for Care Tips */}
                {isCare && (
                    <div className="space-y-4">
                        {result.quick_overview && (
                            <div className="p-3 bg-muted/50 rounded-lg">
                                <p className="text-sm">
                                    {result.quick_overview}
                                </p>
                            </div>
                        )}

                        {result.essential_care && (
                            <div className="space-y-4">
                                <h4 className="text-sm font-semibold">
                                    🌱 Essential Care Requirements
                                </h4>
                                <div className="grid gap-4">
                                    {result.essential_care.light && (
                                        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg">
                                            <div className="text-sm font-semibold text-amber-800 dark:text-amber-200 mb-2">
                                                ☀️ Light Requirements
                                            </div>
                                            <div className="text-sm text-amber-700 dark:text-amber-300 leading-relaxed">
                                                {result.essential_care.light}
                                            </div>
                                        </div>
                                    )}
                                    {result.essential_care.water && (
                                        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                                            <div className="text-sm font-semibold text-blue-800 dark:text-blue-200 mb-2">
                                                💧 Watering Guidelines
                                            </div>
                                            <div className="text-sm text-blue-700 dark:text-blue-300 leading-relaxed">
                                                {result.essential_care.water}
                                            </div>
                                        </div>
                                    )}
                                    {result.essential_care.soil && (
                                        <div className="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                                            <div className="text-sm font-semibold text-green-800 dark:text-green-200 mb-2">
                                                🌿 Soil Requirements
                                            </div>
                                            <div className="text-sm text-green-700 dark:text-green-300 leading-relaxed">
                                                {result.essential_care.soil}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

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
                                            <div className="text-sm leading-relaxed">
                                                {tip}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {result.common_problems &&
                            result.common_problems.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-sm font-semibold">
                                        ⚠️ Common Problems & Solutions
                                    </h4>
                                    <div className="space-y-3">
                                        {result.common_problems.map(
                                            (problem, index) => (
                                                <div
                                                    key={index}
                                                    className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
                                                >
                                                    <div className="text-sm text-red-800 dark:text-red-200 leading-relaxed">
                                                        {problem}
                                                    </div>
                                                </div>
                                            )
                                        )}
                                    </div>
                                </div>
                            )}
                    </div>
                )}

                {/* Detailed Analysis */}
                <div className="pt-4 border-t">
                    <h4 className="text-sm font-semibold mb-3">
                        Detailed Analysis
                    </h4>
                    <MarkdownViewer
                        content={content}
                        className="prose prose-sm max-w-none"
                    />
                </div>
            </CardContent>
        </Card>
    );
}
