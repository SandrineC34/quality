<script setup>
import { reactive, watch } from "vue";
import { X, Plus, Trash2 } from "lucide-vue-next";

const SOURCES = ["Audit interne", "Client", "Fournisseur", "Réclamation", "Interne"];
const SERVICES = ["Management", "Production", "Qualité", "Achats", "Logistique", "RH", "Commercial"];
const GRAVITES = ["Mineure", "Majeure", "Critique"];
const STATUTS = ["Ouverte", "En cours", "Clôturée"];

const ACTION_STATUTS = ["À faire", "En cours", "Abandonnée", "Reportée"];

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  initialData: { type: Object, default: null },
  error: { type: String, default: null },
});

const emit = defineEmits(["update:modelValue", "submit"]);

function emptyAction() {
  return { description: "", pilote: "", date_cloture: "", statut: "À faire" };
}

function emptyForm() {
  return {
    date: new Date().toISOString().slice(0, 10),
    source: "Audit interne",
    service_impacte: "Management",
    pilote: "",
    description: "",
    gravite: "Majeure",
    statut: "En cours",
    analyse_causes: "",
    actions_correctives: [],
    date_cloture: "",
  };
}

const form = reactive(emptyForm());

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      const source = props.initialData ? { ...props.initialData } : emptyForm();
      // Copie profonde pour ne pas modifier item du tableau tant que non enregistré,
      // et on remplit les valeurs manquantes de chaque action (null -> "")
      source.actions_correctives = (source.actions_correctives || []).map((a) => ({
        description: a.description || "",
        pilote: a.pilote || "",
        date_cloture: a.date_cloture || "",
        statut: a.statut || "À faire",
      }));
      Object.assign(form, source);
    }
  }
);

function addAction() {
  form.actions_correctives.push(emptyAction());
}

function removeAction(index) {
  form.actions_correctives.splice(index, 1);
}

function close() {
  emit("update:modelValue", false);
}

function handleSubmit() {
  const payload = { ...form };
  if (!payload.date_cloture) payload.date_cloture = null;
  payload.actions_correctives = form.actions_correctives.map((a) => ({
    ...a,
    date_cloture: a.date_cloture || null,
  }));
  emit("submit", payload);
}
</script>

<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-900">
          {{ initialData ? "Modifier la non-conformité" : "Nouvelle non-conformité" }}
        </h2>
        <button class="text-slate-400 hover:text-slate-600" @click="close">
          <X class="w-5 h-5" />
        </button>
      </div>

      <form class="space-y-5" @submit.prevent="handleSubmit">
        <p
          v-if="error"
          class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-3 py-2"
        >
          {{ error }}
        </p>
        <div class="grid grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Date</label>
            <input
              v-model="form.date"
              type="date"
              required
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Source</label>
            <select
              v-model="form.source"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option v-for="s in SOURCES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Service impacté</label>
            <select
              v-model="form.service_impacte"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option v-for="s in SERVICES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Pilote</label>
            <input
              v-model="form.pilote"
              type="text"
              placeholder="Nom du Pilote"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Description</label>
          <textarea
            v-model="form.description"
            required
            rows="2"
            class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Gravité</label>
            <select
              v-model="form.gravite"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option v-for="g in GRAVITES" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Statut</label>
            <select
              v-model="form.statut"
              class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option v-for="s in STATUTS" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Analyse des causes</label>
          <textarea
            v-model="form.analyse_causes"
            rows="2"
            class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
          ></textarea>
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="block text-sm font-medium text-slate-700">Actions correctives</label>
            <button
              type="button"
              class="flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
              @click="addAction"
            >
              <Plus class="w-4 h-4" />
              Ajouter une action
            </button>
          </div>

          <p v-if="form.actions_correctives.length === 0" class="text-sm text-slate-400 italic">
            Aucune action corrective pour l'instant.
          </p>

          <div
            v-for="(action, index) in form.actions_correctives"
            :key="index"
            class="border border-slate-200 rounded-lg p-4 mb-3 space-y-3"
          >
            <div class="flex items-start justify-between gap-3">
              <textarea
                v-model="action.description"
                rows="2"
                placeholder="Description de l'action corrective"
                class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
              ></textarea>
              <button
                type="button"
                class="text-slate-400 hover:text-red-600 shrink-0 mt-1"
                title="Supprimer cette action"
                @click="removeAction(index)"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <div>
                <label class="block text-xs font-medium text-slate-500 mb-1">Pilote de l'action</label>
                <input
                  v-model="action.pilote"
                  type="text"
                  placeholder="Nom du pilote"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-500 mb-1">Date de clôture</label>
                <input
                  v-model="action.date_cloture"
                  type="date"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-500 mb-1">Statut</label>
                <select
                  v-model="action.statut"
                  class="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option v-for="s in ACTION_STATUTS" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-slate-700 mb-1">Date de clôture</label>
          <input
            v-model="form.date_cloture"
            type="date"
            class="w-full max-w-xs border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button
            type="button"
            class="px-4 py-2 rounded-lg border border-slate-300 text-sm font-medium text-slate-700 hover:bg-slate-50"
            @click="close"
          >
            Annuler
          </button>
          <button
            type="submit"
            class="px-4 py-2 rounded-lg bg-slate-900 text-sm font-medium text-white hover:bg-slate-800"
          >
            Enregistrer
          </button>
        </div>
      </form>
    </div>
  </div>
</template>