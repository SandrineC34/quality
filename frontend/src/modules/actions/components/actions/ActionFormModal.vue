<script setup>
/* Décrit la fenêtre où créer ou modifier une action de suivi */

import { reactive, watch } from "vue";
import { X } from "lucide-vue-next";
import { UI } from "../../../dashboard/components/ui";
import {
  ORIGINES,
  TYPES_ACTION,
  PRIORITES,
  STATUTS_ACTION,
  RESULTATS_EFFICACITE,
} from "../../constants/suiviActions";
import { emptySuiviAction } from "../../utils/suiviActions";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  initialData: { type: Object, default: null },
  error: { type: String, default: null },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const form = reactive(emptySuiviAction());

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      const source = props.initialData ? { ...props.initialData } : emptySuiviAction();
      Object.assign(form, emptySuiviAction(), source);
    }
  }
);

function close() {
  emit("update:modelValue", false);
}

function handleSubmit() {
  const payload = { ...form };
  payload.date_cloture = payload.date_cloture || null;
  payload.date_mesure_efficacite = payload.date_mesure_efficacite || null;
  emit("submit", payload);
}
</script>

<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
    @click.self="close">
    <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-900">
          {{ initialData ? "Modifier l'action" : "Nouvelle action de suivi" }}
        </h2>
        <button class="text-slate-400 hover:text-slate-600" @click="close">
          <X class="w-5 h-5" />
        </button>
      </div>

      <form class="space-y-5" @submit.prevent="handleSubmit">
        <p
          v-if="error"
          class="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-3 py-2">
          {{ error }}
        </p>

        <!-- Origine et identification -->
        <div class="grid grid-cols-3 gap-5">
          <div>
            <label :class="UI.label">Date de création</label>
            <input v-model="form.date_creation" type="date" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Origine</label>
            <select v-model="form.origine" required :class="UI.select">
              <option value="" disabled>Sélectionner...</option>
              <option v-for="o in ORIGINES" :key="o" :value="o">{{ o }}</option>
            </select>
          </div>
          <div>
            <label :class="UI.label">Référence de l'origine</label>
            <input
              v-model="form.origine_ref"
              type="text"
              placeholder="Ex : NC-2026-014, revue du 10/03..."
              :class="UI.input"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Type d'action</label>
            <select v-model="form.type_action" :class="UI.select">
              <option value="" disabled>Sélectionner...</option>
              <option v-for="t in TYPES_ACTION" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <div>
            <label :class="UI.label">Priorité</label>
            <select v-model="form.priorite" :class="UI.select">
              <option value="" disabled>Sélectionner...</option>
              <option v-for="p in PRIORITES" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
        </div>

        <div>
          <label :class="UI.label">Descriptif complet de l'action</label>
          <textarea v-model="form.description" required rows="3" :class="UI.textarea"></textarea>
        </div>

        <!-- Responsable et échéance -->
        <div class="grid grid-cols-3 gap-5">
          <div>
            <label :class="UI.label">Responsable</label>
            <input v-model="form.responsable" type="text" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Date prévisionnelle</label>
            <input v-model="form.date_prevue" type="date" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Statut</label>
            <select v-model="form.statut" :class="UI.select">
              <option v-for="s in STATUTS_ACTION" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <div>
          <label :class="UI.label">Date de clôture</label>
          <input v-model="form.date_cloture" type="date" :class="UI.input + ' max-w-xs'" />
        </div>

        <div>
          <label :class="UI.label">Éléments de preuve</label>
          <textarea
            v-model="form.preuves"
            rows="2"
            placeholder="Documents, photos, comptes-rendus..."
            :class="UI.textarea"
          ></textarea>
        </div>

        <!-- Efficacité -->
        <div class="border-t border-slate-200 pt-5">
          <p class="text-sm font-semibold text-slate-700 mb-3">Évaluation de l'efficacité</p>

          <div class="mb-4">
            <label :class="UI.label">Critères permettant de valider l'efficacité</label>
            <textarea
              v-model="form.criteres_efficacite"
              rows="2"
              placeholder="Ex : absence de récurrence sur 3 mois, indicateur X < seuil..."
              :class="UI.textarea"
            ></textarea>
          </div>

          <div class="grid grid-cols-3 gap-5 mb-4">
            <div>
              <label :class="UI.label">Date de mesure de l'efficacité</label>
              <input v-model="form.date_mesure_efficacite" type="date" :class="UI.input" />
            </div>
            <div>
              <label :class="UI.label">Résultat de la validation</label>
              <select v-model="form.resultat_efficacite" :class="UI.select">
                <option v-for="r in RESULTATS_EFFICACITE" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>
            <div>
              <label :class="UI.label">Validé par</label>
              <input v-model="form.valide_par" type="text" :class="UI.input" />
            </div>
          </div>

          <div>
            <label :class="UI.label">Commentaire</label>
            <textarea v-model="form.commentaire_efficacite" rows="2" :class="UI.textarea"></textarea>
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button type="button" :class="UI.btnSecondary" @click="close">Annuler</button>
          <button type="submit" :class="UI.btnPrimary">Enregistrer</button>
        </div>
      </form>
    </div>
  </div>
</template>
