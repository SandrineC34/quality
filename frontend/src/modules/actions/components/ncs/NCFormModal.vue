<script setup>
/* Décrit la fenêtre où créer ou modifier une non-conformité */

import { reactive, watch } from "vue";
import { X, Plus, Trash2 } from "lucide-vue-next";
import { UI } from "../../../dashboard/components/ui";
import {
  SOURCES,
  SERVICES,
  GRAVITES,
  STATUTS,
  ACTION_STATUTS,
} from "../../constants/nonConformites";
import { emptyAction, emptyNCForm } from "../../utils/nonConformites";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  initialData: { type: Object, default: null },
  error: { type: String, default: null },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const form = reactive(emptyNCForm());

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      const source = props.initialData ? { ...props.initialData } : emptyNCForm();
      // Copie profonde pour ne pas modifier item du tableau tant que non enregistré,
      // et on remplit les valeurs manquantes de chaque action (null -> "")
      source.actions_correctives = (source.actions_correctives || []).map((a) => ({
        description: a.description || "",
        pilote: a.pilote || "",
        date_objectif: a.date_objectif || "",
        date_cloture: a.date_cloture || "",
        efficacite: a.efficacite || a.Efficacité || "",
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
  if (!payload.date_action_curative) payload.date_action_curative = null;
  payload.actions_correctives = form.actions_correctives.map((a) => ({
    ...a,
    date_objectif: a.date_objectif || null,
    date_cloture: a.date_cloture || null,
  }));
  emit("submit", payload);
}
</script>

<!-- Affichage du tableau recapitulatifs des non conformité -->
<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
    @click.self="close">
    <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-900">
          {{ initialData ? "Modifier la non-conformité" : "Nouvelle non-conformité" }}
        </h2>
        <button class="text-slate-400 hover:text-slate-600" @click="close">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Formulaire de saisie nouvelle non conformité  -->
      <form class="space-y-5" @submit.prevent="handleSubmit">
        <p
          v-if="error"
          class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-3 py-2">
          {{ error }}
        </p>

        <div class="grid grid-cols-3 gap-5">
          <div>
            <label :class="UI.label">Date de Détection</label>
            <input v-model="form.date" type="date" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Canal de détection</label>
            <select v-model="form.source" :class="UI.select">
              <option v-for="s in SOURCES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>

          <div>
            <label :class="UI.label">Processus impacté</label>
            <select v-model="form.service_impacte" :class="UI.select">
              <option v-for="s in SERVICES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          
        </div>

      
        <div>
          <label :class="UI.label">Description de  l'anomalie</label>
          <textarea v-model="form.description" required rows="2" :class="UI.textarea"></textarea>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Gravité</label>
            <select v-model="form.gravite" :class="UI.select">
              <option v-for="g in GRAVITES" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
          <div>
            <label :class="UI.label">Statut</label>
            <select v-model="form.statut" :class="UI.select">
              <option v-for="s in STATUTS" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <div>
          <label :class="UI.label">Analyse des causes</label>
          <textarea v-model="form.analyse_causes" rows="2" :class="UI.textarea"></textarea>
        </div>

        <div class="grid grid-cols-3 gap-5">
          <div class="col-span-2">
            <label :class="UI.label">Actions curatives (correction immédiate de l'anomalie)</label>
            <textarea v-model="form.action_curative" rows="2" :class="UI.textarea"></textarea>
          </div>
          <div>
            <label :class="UI.label">Date de réalisation</label>
            <input v-model="form.date_action_curative" type="date" :class="UI.input" />
          </div>
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label :class="UI.label + ' mb-0'">Action corrective/préventive</label>
            <button
              type="button"
              class="flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
              @click="addAction"
            >
              <Plus class="w-4 h-4" />
              Ajouter une action corrective/préventive
            </button>
          </div>
        </div>

        <p v-if="form.actions_correctives.length === 0" class="text-sm text-slate-400 italic">
          Aucune action pour l'instant.
        </p>

        <!-- Formulaire secondaire : contenu de l'action corrective -->
        <div
          v-for="(action, index) in form.actions_correctives"
          :key="index"
          class="border border-slate-200 rounded-lg p-4 mb-3 space-y-3">
          <div class="flex items-start justify-between gap-3">
            <textarea
              v-model="action.description"
              rows="2"
              placeholder="Description de l'action corrective"
              :class="UI.textarea"
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
              <label :class="UI.labelSm">Pilote / Responsable</label>
              <input v-model="action.pilote" type="text" :class="UI.input" />
            </div>
            <div>
              <label :class="UI.labelSm">Date d'échéance</label>
              <input v-model="action.date_objectif" type="date" :class="UI.input" />
            </div>
            <div>
              <label :class="UI.labelSm">Statut</label>
              <select v-model="action.statut" :class="UI.select">
                <option v-for="s in ACTION_STATUTS" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="col-span-2">
              <label :class="UI.labelSm">Évaluation de l'efficacité</label>
              <input v-model="action.efficacite" type="text" placeholder="Ex: Efficace, À réévaluer..." :class="UI.input" />
            </div>
            <div>
              <label :class="UI.labelSm">Date de clôture</label>
              <input v-model="action.date_cloture" type="date" :class="UI.input" />
            </div>
          </div>
              
           

    </div>

        <div>
          <label :class="UI.label">Date de clôture</label>
          <input v-model="form.date_cloture" type="date" :class="UI.input + ' max-w-xs'" />
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button type="button" :class="UI.btnSecondary" @click="close">Annuler</button>
          <button type="submit" :class="UI.btnPrimary">Enregistrer</button>
        </div>
      </form>
    </div>
  </div>
</template>
