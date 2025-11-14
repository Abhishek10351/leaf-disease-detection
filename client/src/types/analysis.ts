export interface ImageUploadResponse {
  image_id: string;
  filename: string;
  file_size: number;
  content_type: string;
  uploaded_at: string;
}

export interface AnalysisResponse {
  analysis: string;
  model_used: string;
  confidence?: string;
  timestamp: string;
  analysis_type: string;
  summary?: string;
  severity?: string;
  // New structured fields
  plant_identification?: string;
  primary_issue?: string;
  immediate_action?: string;
  treatment?: string;
  prevention?: string;
  likely_condition?: string;
  treatment_steps?: string;
  what_to_watch?: string;
}

export interface CareResponse {
  care_tips: string;
  plant_type: string;
  model_used: string;
  timestamp: string;
  care_difficulty?: string;
  seasonal_care?: string;
  // New structured fields
  quick_overview?: string;
  essential_care?: {
    light?: string;
    water?: string;
    soil?: string;
  };
  key_tips?: string[];
  common_problems?: string[];
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