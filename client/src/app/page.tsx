import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Bot, Scan, FileText, Sprout, ArrowRight, Heart, Shield } from 'lucide-react'

const HomePage = async () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
            {/* Hero Section */}
            <div className="container mx-auto px-4 py-16 pt-20 mt-8">
                <div className="text-center space-y-8 max-w-4xl mx-auto">
                    <div className="flex items-center justify-center gap-3 mb-8">
                        <div className="flex items-center justify-center size-16 bg-primary text-primary-foreground rounded-2xl">
                            <Bot className="size-8" />
                        </div>
                        <div className="text-left">
                            <h1 className="text-4xl md:text-6xl font-bold text-foreground">
                                Leaf Disease
                            </h1>
                            <h2 className="text-2xl md:text-3xl font-semibold text-primary">
                                Detection AI
                            </h2>
                        </div>
                    </div>

                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                        Keep your plants healthy with AI-powered disease detection, symptom analysis, 
                        and personalized care recommendations. Upload photos or describe symptoms 
                        to get instant expert guidance.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
                        <Link href="/analysis">
                            <Button size="lg" className="text-lg px-8 py-6">
                                Start Analysis
                                <ArrowRight className="size-5 ml-2" />
                            </Button>
                        </Link>
                    </div>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto mt-20">
                    <Card className="p-6 text-center hover:shadow-lg transition-shadow">
                        <div className="flex items-center justify-center size-12 bg-primary/10 text-primary rounded-xl mx-auto mb-4">
                            <Scan className="size-6" />
                        </div>
                        <h3 className="text-lg font-semibold mb-2">Image Analysis</h3>
                        <p className="text-muted-foreground text-sm">
                            Upload clear photos of affected plant leaves for AI-powered disease detection and comprehensive diagnosis.
                        </p>
                    </Card>

                    <Card className="p-6 text-center hover:shadow-lg transition-shadow">
                        <div className="flex items-center justify-center size-12 bg-primary/10 text-primary rounded-xl mx-auto mb-4">
                            <FileText className="size-6" />
                        </div>
                        <h3 className="text-lg font-semibold mb-2">Symptom Analysis</h3>
                        <p className="text-muted-foreground text-sm">
                            Describe symptoms you&apos;ve observed and get expert analysis based on your detailed descriptions.
                        </p>
                    </Card>

                    <Card className="p-6 text-center hover:shadow-lg transition-shadow">
                        <div className="flex items-center justify-center size-12 bg-primary/10 text-primary rounded-xl mx-auto mb-4">
                            <Sprout className="size-6" />
                        </div>
                        <h3 className="text-lg font-semibold mb-2">Care Guidelines</h3>
                        <p className="text-muted-foreground text-sm">
                            Get comprehensive care instructions and maintenance tips for keeping your plants healthy and thriving.
                        </p>
                    </Card>
                </div>

                {/* Benefits Section */}
                <div className="mt-20 text-center">
                    <h3 className="text-2xl font-bold mb-12">Why Choose Our AI Plant Doctor?</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
                        <div className="flex flex-col items-center space-y-3">
                            <Shield className="size-8 text-primary" />
                            <h4 className="font-semibold">Expert Accuracy</h4>
                            <p className="text-muted-foreground text-sm">
                                Powered by advanced AI models trained on extensive plant pathology data
                            </p>
                        </div>
                        <div className="flex flex-col items-center space-y-3">
                            <Heart className="size-8 text-primary" />
                            <h4 className="font-semibold">Plant Care Focus</h4>
                            <p className="text-muted-foreground text-sm">
                                Comprehensive care recommendations tailored to your specific plant needs
                            </p>
                        </div>
                        <div className="flex flex-col items-center space-y-3">
                            <Bot className="size-8 text-primary" />
                            <h4 className="font-semibold">24/7 Availability</h4>
                            <p className="text-muted-foreground text-sm">
                                Get instant analysis and recommendations whenever you need them
                            </p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default HomePage;
