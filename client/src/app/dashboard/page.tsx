"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/lib/redux/hooks";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ImageAnalysis } from "@/components/analysis/image-analysis";
import { SymptomsAnalysis } from "@/components/analysis/symptoms-analysis";
import { CareTips } from "@/components/analysis/care-tips";
import { AnalysisHistory } from "@/components/analysis/analysis-history";
import {
    Scan,
    FileText,
    Sprout,
    History,
    User,
    Shield,
    Mail,
} from "lucide-react";

export default function Dashboard() {
    const router = useRouter();
    const { isAuthenticated, user, isLoading, token } = useAppSelector(
        (state) => state.auth
    );
    const [activeTab, setActiveTab] = useState("image");

    useEffect(() => {
        if (!isAuthenticated && !token) {
            router.push("/auth/login");
            return;
        }
    }, [isAuthenticated, token, router]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Loading...</p>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null; // Will redirect to login
    }

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h1 className="text-3xl font-bold text-foreground">
                                Plant Disease Detection
                            </h1>
                            <p className="text-muted-foreground">
                                Analyze your plants and get expert care
                                recommendations using AI
                            </p>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                            <span>Online</span>
                        </div>
                    </div>

                    {/* User Info Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        <Card>
                            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">
                                    Welcome Back!
                                </CardTitle>
                                <User className="h-4 w-4 ml-auto text-primary" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold">
                                    {user?.name || "User"}
                                </div>
                                <CardDescription>
                                    You're successfully logged in
                                </CardDescription>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">
                                    Account Status
                                </CardTitle>
                                <Shield className="h-4 w-4 ml-auto text-primary" />
                            </CardHeader>
                            <CardContent>
                                <div className="flex items-center gap-2 mb-1">
                                    <Badge
                                        variant={
                                            user?.is_active
                                                ? "default"
                                                : "secondary"
                                        }
                                    >
                                        {user?.is_active
                                            ? "Active"
                                            : "Inactive"}
                                    </Badge>
                                </div>
                                <CardDescription>
                                    Role:{" "}
                                    {user?.is_superuser ? "Admin" : "User"}
                                </CardDescription>
                            </CardContent>
                        </Card>

                        <Card>
                            <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">
                                    Email
                                </CardTitle>
                                <Mail className="h-4 w-4 ml-auto text-primary" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-sm font-mono">
                                    {user?.email || "Not available"}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* Main Analysis Interface */}
                <Tabs
                    value={activeTab}
                    onValueChange={setActiveTab}
                    className="space-y-6"
                >
                    <TabsList className="grid w-full grid-cols-4">
                        <TabsTrigger
                            value="image"
                            className="flex items-center gap-2"
                        >
                            <Scan className="size-4" />
                            Image Analysis
                        </TabsTrigger>
                        <TabsTrigger
                            value="symptoms"
                            className="flex items-center gap-2"
                        >
                            <FileText className="size-4" />
                            Symptoms
                        </TabsTrigger>
                        <TabsTrigger
                            value="care"
                            className="flex items-center gap-2"
                        >
                            <Sprout className="size-4" />
                            Care Tips
                        </TabsTrigger>
                        <TabsTrigger
                            value="history"
                            className="flex items-center gap-2"
                        >
                            <History className="size-4" />
                            History
                        </TabsTrigger>
                    </TabsList>

                    <TabsContent value="image" className="space-y-6">
                        <ImageAnalysis />
                    </TabsContent>

                    <TabsContent value="symptoms" className="space-y-6">
                        <SymptomsAnalysis />
                    </TabsContent>

                    <TabsContent value="care" className="space-y-6">
                        <CareTips />
                    </TabsContent>

                    <TabsContent value="history" className="space-y-6">
                        <AnalysisHistory />
                    </TabsContent>
                </Tabs>

                {/* Quick Actions */}
                <Card className="mt-8">
                    <CardHeader>
                        <CardTitle>Quick Actions</CardTitle>
                        <CardDescription>
                            Common tasks and navigation
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex flex-wrap gap-4">
                            <Button
                                variant="outline"
                                onClick={() => router.push("/")}
                            >
                                Go to Home
                            </Button>
                            <Button onClick={() => window.location.reload()}>
                                Refresh Page
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
