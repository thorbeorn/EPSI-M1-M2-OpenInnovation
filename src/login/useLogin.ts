import { useState, useEffect } from 'react';
import type { LoginCredentials, LoginResponse, LoginFormData } from './types';

export const useLogin = () => {
  const [equipmentId, setEquipmentId] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEquipmentId = async () => {
      try {
        const id = await window.electron.invoke('get-equipment-id');
        setEquipmentId(id);
      } catch (err) {
        console.error('Erreur lors de la récupération de l\'equipment ID:', err);
        setError('Impossible de récupérer l\'ID de l\'équipement');
      }
    };

    fetchEquipmentId();
  }, []);

  const login = async (formData: LoginFormData): Promise<LoginResponse> => {
    setIsLoading(true);
    setError(null);

    try {
      const credentials: LoginCredentials = {
        email: formData.email,
        password: formData.password,
        equipmentId: equipmentId
      };

      const response: LoginResponse = await window.electron.invoke('login-attempt', credentials);

      if (!response.success) {
        setError(response.message || 'Échec de la connexion');
      }

      setIsLoading(false);
      return response;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur inconnue';
      setError(errorMessage);
      setIsLoading(false);
      
      return {
        success: false,
        message: errorMessage
      };
    }
  };

  return {
    equipmentId,
    isLoading,
    error,
    login,
    clearError: () => setError(null)
  };
};