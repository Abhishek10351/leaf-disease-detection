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
}

export interface CareResponse {
  care_tips: string;
  plant_type: string;
  model_used: string;
  timestamp: string;
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