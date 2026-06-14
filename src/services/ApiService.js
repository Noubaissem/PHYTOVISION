import axios from 'axios';

const BASE_URL = "http://localhost:8000/api";

const ApiService = {

  analyseImage: async (imageFile, zone) => {
    const formData = new FormData();
    formData.append("file", imageFile);
    if (zone) {
      formData.append("zone", zone);
    }
    const response = await axios.post(
      `${BASE_URL}/analyse`,
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );
    return response.data;
  },

  getDiagnostics: async () => {
    const response = await axios.get(`${BASE_URL}/diagnostics`);
    return response.data;
  },

  getDashboard: async () => {
    const response = await axios.get(`${BASE_URL}/dashboard`);
    return response.data;
  },

  getEpidemiologie: async () => {
    const response = await axios.get(`${BASE_URL}/epidemiologie`);
    return response.data;
  }
};

export default ApiService;