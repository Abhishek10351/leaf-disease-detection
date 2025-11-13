import { AxiosError } from 'axios';
import api from '@/app/utils/api';
import {
  ImageUploadResponse,
  AnalysisResponse,
  CareResponse,
  ImageAnalysisRequest,
  SymptomsAnalysisRequest,
  PlantCareRequest,
  UploadedImage,
  AnalysisHistory
} from '@/types/analysis';

export class AnalysisService {
  /**
   * Upload an image for analysis
   */
  static async uploadImage(file: File): Promise<ImageUploadResponse> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await api.post<ImageUploadResponse>('/analysis/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Upload failed';
      throw new Error(message);
    }
  }

  /**
   * Analyze an uploaded image by ID
   */
  static async analyzeImage(request: ImageAnalysisRequest): Promise<AnalysisResponse> {
    try {
      const response = await api.post<AnalysisResponse>('/analysis/analyze', request);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Analysis failed';
      throw new Error(message);
    }
  }

  /**
   * Analyze symptoms without an image
   */
  static async analyzeSymptoms(request: SymptomsAnalysisRequest): Promise<AnalysisResponse> {
    try {
      const response = await api.post<AnalysisResponse>('/analysis/symptoms', request);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Analysis failed';
      throw new Error(message);
    }
  }

  /**
   * Get care tips for a plant type
   */
  static async getCareTips(request: PlantCareRequest): Promise<CareResponse> {
    try {
      const response = await api.post<CareResponse>('/analysis/care-tips', request);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Failed to get care tips';
      throw new Error(message);
    }
  }

  /**
   * Get list of uploaded images
   */
  static async getUploadedImages(limit = 20, skip = 0): Promise<{
    images: UploadedImage[];
    total: number;
    skip: number;
    limit: number;
  }> {
    try {
      const response = await api.get('/analysis/images', {
        params: { limit, skip }
      });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Failed to fetch images';
      throw new Error(message);
    }
  }

  /**
   * Get analysis history
   */
  static async getAnalysisHistory(
    limit = 20,
    skip = 0,
    analysisType?: string
  ): Promise<{
    history: AnalysisHistory[];
    total: number;
    skip: number;
    limit: number;
  }> {
    try {
      const response = await api.get('/analysis/history', {
        params: { limit, skip, analysis_type: analysisType }
      });
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Failed to fetch history';
      throw new Error(message);
    }
  }

  /**
   * Delete an uploaded image
   */
  static async deleteImage(imageId: string): Promise<void> {
    try {
      await api.delete(`/analysis/images/${imageId}`);
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Failed to delete image';
      throw new Error(message);
    }
  }

  /**
   * Delete an analysis from history
   */
  static async deleteAnalysis(analysisId: string): Promise<void> {
    try {
      await api.delete(`/analysis/history/${analysisId}`);
    } catch (error) {
      const axiosError = error as AxiosError;
      const message = (axiosError.response?.data as any)?.detail || axiosError.message || 'Failed to delete analysis';
      throw new Error(message);
    }
  }
}