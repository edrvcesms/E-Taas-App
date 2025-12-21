import axios, { type AxiosInstance } from "axios";
import { refreshToken } from "../auth/Token";

export const createApiInstance = (baseUrl: string, withCredentials?: boolean | undefined): AxiosInstance => {
  const instance: AxiosInstance = axios.create({
    baseURL: baseUrl,
    withCredentials: withCredentials
  });
  
  if (withCredentials) {
    instance.interceptors.request.use(async (config) => {
      config.withCredentials = true;
      return config;
    }); 

    instance.interceptors.response.use(response => response, async (error) => {
      if (error.response && error.response.status === 401) {
        try {
          const refreshed = await refreshToken();
          if (refreshed.statusCode !== 200) {
            return Promise.reject(error);
          }
          const originalRequest = error.config;
          originalRequest._retry = true;
          return instance(originalRequest);
        } catch (refreshError) {
          return Promise.reject(refreshError);
        }
      }
      return Promise.reject(error);
    });
  }
  return instance;
};