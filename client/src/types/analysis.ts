export interface ImageUploadResponse {
  image_id: string;
  filename: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
}

// Image Analysis Response (matches ImageAnalysisLLMResponse from backend)
export interface ImageAnalysisResponse {
  plant_identification: string;
  health_status: string;
  confidence: string;
  primary_issue: string;
  quick_summary: string;
  immediate_action: string;
  treatment: string;
  prevention: string;
  detailed_analysis: string;
}

// Symptoms Analysis Response (matches SymptomsAnalysisLLMResponse from backend)
export interface SymptomsAnalysisResponse {
  likely_condition: string;
  severity: string;
  confidence: string;
  quick_summary: string;
  immediate_action: string;
  treatment_steps: string;
  what_to_watch: string;
  detailed_analysis: string;
}

export interface EssentialCare {
  light: string;
  water: string;
  soil: string;
}

export interface PlantCareResponse {
  care_difficulty: string;
  quick_overview: string;
  essential_care: EssentialCare;
  key_tips: string[];
  common_problems: string[];
  detailed_guide: string;
}

export interface ImageAnalysisRequest {
  image_id: string;
}

export interface SymptomsAnalysisRequest {
  symptoms_description: string;
  plant_type?: string;
}

export interface PlantCareRequest {
  plant_type: string;
}

export interface UploadedImage {
  image_id: string;
  filename: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
}

export interface AnalysisHistory {
  id: string;
  analysis_type: "image" | "symptoms" | "care";
  timestamp: string;
  request_data: any;
  preview?: string;
}