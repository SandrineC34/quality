<script setup>
import { onMounted, ref } from "vue";
import { Plus, Search } from "lucide-vue-next";
import { useSuiviActionsStore } from "../stores/suiviActions";
import ActionsTable from "../components/actions/ActionsTable.vue";
import ActionFormModal from "../components/actions/ActionFormModal.vue";
import { UI, SEARCH_DEBOUNCE_MS } from "../../dashboard/components/ui";
import { STATUT_FILTER_OPTIONS } from "../constants/suiviActions";
import { debounce, extractApiErrorMessage } from "../../../utils";

const store = useSuiviActionsStore();
const showModal = ref(false);
const editingItem = ref(null);
const submitError = ref(null);

onMounted(() => store.fetchAll());

function openCreate() {
  editingItem.value = null;
  showModal.value = true;
}

function openEdit(item) {
  editingItem.value = item;
  showModal.value = true;
}

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
    submitError.value = extractApiErrorMessage(err);
  }
}

const onSearchInput = debounce(() => store.fetchAll(), SEARCH_DEBOUNCE_MS);
</script>

<template>
  <div>
    <p :class="UI.pageEyebrow">Registre qualité</p>
    <div class="flex items-start justify-between mb-1">
      <h1 :class="UI.pageTitle">Suivi des actions</h1>
      <button
        :class="[UI.btnPrimary, 'flex items-center gap-2 py-2.5']"
        @click="openCreate"
      >
        <Plus class="w-4 h-4" />
        Ajouter une action
      </button>
    </div>
    <p :class="UI.pageSubtitle">
      Suivi des actions correctives, préventives et d'amélioration, quelle que soit leur origine
      (non-conformités, revues de direction, audits...)
    </p>

    <!-- Barre de recherche rattachée à backend/routers/actions -->
    <div class="flex gap-4 mb-4">
      <div class="relative flex-1">
        <Search class="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          v-model="store.search"
          type="text"
          placeholder="Rechercher (réf, description, responsable...)"
          :class="UI.input + ' pl-9'"
          @input="onSearchInput"
        />
      </div>
      <select
        v-model="store.statut"
        :class="UI.select + ' min-w-[180px]'"
        @change="store.fetchAll()"
      >
        <option v-for="s in STATUT_FILTER_OPTIONS" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <ActionsTable :items="store.items" :loading="store.loading" @edit="openEdit" />

    <ActionFormModal
      v-model="showModal"
      :initial-data="editingItem"
      :error="submitError"
      @submit="handleSubmit"
    />
  </div>
</template>
