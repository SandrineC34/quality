import { defineStore } from "pinia";
import apiClient from "../../../services/apiClient";

export const useSuiviActionsStore = defineStore("suiviActions", {
  state: () => ({
    items: [],
    loading: false,
    error: null,
    search: "",
    statut: "Tous les statuts",
  }),
  actions: {
    async fetchAll() {
      this.loading = true;
      this.error = null;
      try {
        const params = {};
        if (this.search) params.search = this.search;
        if (this.statut && this.statut !== "Tous les statuts") params.statut = this.statut;
        const { data } = await apiClient.get("/actions", { params });
        this.items = data;
      } catch (err) {
        this.error = "Impossible de charger les actions.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async create(payload) {
      const { data } = await apiClient.post("/actions", payload);
      this.items.unshift(data);
      return data;
    },
    async update(id, payload) {
      const { data } = await apiClient.put(`/actions/${id}`, payload);
      const idx = this.items.findIndex((i) => i._id === id);
      if (idx !== -1) this.items[idx] = data;
      return data;
    },
    async remove(id) {
      await apiClient.delete(`/actions/${id}`);
      this.items = this.items.filter((i) => i._id !== id);
    },
  },
});
