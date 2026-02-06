export interface LoginCredentials {
  email: string;
  password: string;
  equipmentId: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  equipmentId?: string;
  user?: {
    email: string;
    id?: string;
    name?: string;
  };
  error?: string;
  token?: string;
}

export interface LoginFormData {
  email: string;
  password: string;
}