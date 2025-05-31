import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "/api";

export const fetchPredictions = async () => {
  const res = await axios.get(`${API_BASE}/predictions`);
  return res.data;
};

export const runPrediction = async () => {
  return await axios.post(`${API_BASE}/predict`);
};