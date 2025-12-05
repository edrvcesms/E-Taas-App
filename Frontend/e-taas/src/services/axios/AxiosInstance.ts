import axios, { type AxiosInstance } from "axios";

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
  }
  return instance;
};