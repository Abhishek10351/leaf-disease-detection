import { AxiosError } from 'axios';
import api from '@/app/utils/api';
import {
  ImageUploadResponse,
  ImageAnalysisResponse,
  SymptomsAnalysisResponse,
  PlantCareResponse,
  ImageAnalysisRequest,
  ImageAnalysisTranslationRequest,
  SymptomsAnalysisRequest,
  PlantCareRequest,
  UploadedImage,
  AnalysisHistory
} from '@/types/analysis';

type ApiErrorResponse = {
  detail?: string;
  message?: string;
};

const getErrorMessage = (error: unknown, fallback: string): string => {
  const axiosError = error as AxiosError<ApiErrorResponse>;
  return axiosError.response?.data?.detail || axiosError.response?.data?.message || axiosError.message || fallback;
};

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
      throw new Error(getErrorMessage(error, 'Upload failed'));
    }
  }

  /**
   * Analyze an uploaded image by ID
   */
  static async analyzeImage(request: ImageAnalysisRequest): Promise<ImageAnalysisResponse> {
    try {
      const response = await api.post<ImageAnalysisResponse>('/analysis/analyze', request);
      return response.data;
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Analysis failed'));
    }
  }

  /**
   * Translate a previously generated image analysis response
   */
  static async translateImageAnalysis(
    request: ImageAnalysisTranslationRequest
  ): Promise<ImageAnalysisResponse> {
    try {
      const response = await api.post<ImageAnalysisResponse>('/analysis/translate-image', request);
      return response.data;
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Translation failed'));
    }
  }

  /**
   * Analyze symptoms without an image
   */
  static async analyzeSymptoms(request: SymptomsAnalysisRequest): Promise<SymptomsAnalysisResponse> {
    try {
      const response = await api.post<SymptomsAnalysisResponse>('/analysis/symptoms', request);
      return response.data;
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Analysis failed'));
    }
  }

  /**
   * Get care tips for a plant type
   */
  static async getCareTips(request: PlantCareRequest): Promise<PlantCareResponse> {
    try {
      const response = await api.post<PlantCareResponse>('/analysis/care-tips', request);
      return response.data;
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Failed to get care tips'));
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
      throw new Error(getErrorMessage(error, 'Failed to fetch images'));
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
      throw new Error(getErrorMessage(error, 'Failed to fetch history'));
    }
  }

  /**
   * Get detailed analysis history item by ID
   */
  static async getAnalysisDetail(analysisId: string): Promise<AnalysisHistory> {
    try {
      const response = await api.get<AnalysisHistory>(`/analysis/history/${analysisId}`);
      return response.data;
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Failed to fetch analysis detail'));
    }
  }

  /**
   * Delete an uploaded image
   */
  static async deleteImage(imageId: string): Promise<void> {
    try {
      await api.delete(`/analysis/images/${imageId}`);
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Failed to delete image'));
    }
  }

  /**
   * Delete an analysis from history
   */
  static async deleteAnalysis(analysisId: string): Promise<void> {
    try {
      await api.delete(`/analysis/history/${analysisId}`);
    } catch (error) {
      throw new Error(getErrorMessage(error, 'Failed to delete analysis'));
    }
  }
}