<script setup>
import { onMounted, ref } from "vue";
import { Plus, Search } from "lucide-vue-next";
import { useNonConformitesStore } from "../stores/nonConformites";
import NCTable from "../components/ncs/NCTable.vue";
import NCFormModal from "../components/ncs/NCFormModal.vue";

const store = useNonConformitesStore();
const showModal = ref(false);
const editingItem = ref(null);

const STATUTS = ["Tous les statuts", "Ouverte", "En cours", "Clôturée"];

onMounted(() => store.fetchAll());

function openCreate() {
  editingItem.value = null;
  showModal.value = true;
}

function openEdit(item) {
  editingItem.value = item;
  showModal.value = true;
}

const submitError = ref(null);

async function handleSubmit(payload) {
  submitError.value = null;
  try {
    if (editingItem.value) {
      await store.update(editingItem.value._id, payload);
    } else {
      await store.create(payload);
    }
    showModal.value = false;
  } catch (err) {
    console.error(err);
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) {
      // Erreur de validation FastAPI : tableau d'objets {loc, msg, ...}
      submitError.value = detail.map((d) => `${d.loc?.at(-1)}: ${d.msg}`).join(" / ");
    } else if (typeof detail === "string") {
      submitError.value = detail;
    } else if (err.response) {
      submitError.value = `Erreur serveur (${err.response.status}). Voir la console pour le détail.`;
    } else {
      submitError.value =
        "Impossible de contacter le backend (réseau/CORS). Vérifiez qu'il tourne sur le port 8001.";
    }
  }
}

let searchTimeout;
function onSearchInput() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => store.fetchAll(), 300);
}
</script>

<template>
  <div>
    <p class="text-xs font-semibold text-red-600 uppercase tracking-wide mb-1">Registre qualité</p>
    <div class="flex items-start justify-between mb-1">
      <h1 class="text-3xl font-bold text-slate-900">Non-conformités</h1>
      <button
        class="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-slate-900 text-white text-sm font-medium hover:bg-slate-800"
        @click="openCreate"
      >
        <Plus class="w-4 h-4" />
        Ajouter une NC
      </button>
      
    </div>
    <p class="text-slate-500 text-sm mb-6">Saisie, suivi et traitement des non-conformités du SMQ</p>

    <!--Barre de recherche rattache à backens/routers/Non_conformity.py-->
    <div class="flex gap-4 mb-4">
      <div class="relative flex-1">
        <Search class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          v-model="store.search"
          type="text"
          placeholder="Rechercher (réf, description, service...)"
          class="w-full border border-slate-300 rounded-lg pl-9 pr-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="onSearchInput"
        />
      </div>
      <select
        v-model="store.statut"
        class="border border-slate-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 min-w-[180px]"
        @change="store.fetchAll()"
      >
        <option v-for="s in STATUTS" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <NCTable :items="store.items" :loading="store.loading" @edit="openEdit" />

    <NCFormModal
      v-model="showModal"
      :initial-data="editingItem"
      :error="submitError"
      @submit="handleSubmit"
    />
  </div>
</template>
