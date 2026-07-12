<script setup>
/* Décrit la fenêtre où planifier ou modifier un audit interne / revue de processus */

import { reactive, watch } from "vue";
import { X } from "lucide-vue-next";
import { UI } from "../../dashboard/components/ui";
import { PROCESSUS, STATUTS_AUDIT } from "../constants/audits";
import { emptyAudit } from "../utils/audits";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  initialData: { type: Object, default: null },
  error: { type: String, default: null },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const form = reactive(emptyAudit());

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      const source = props.initialData ? { ...props.initialData } : emptyAudit();
      Object.assign(form, emptyAudit(), source);
    }
  }
);

function close() {
  emit("update:modelValue", false);
}

function handleSubmit() {
  const payload = { ...form };
  payload.date_realisation = payload.date_realisation || null;
  payload.date_cloture = payload.date_cloture || null;
  payload.prochain_audit = payload.prochain_audit || null;
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
          {{ initialData ? "Modifier l'audit" : "Planifier un audit" }}
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

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Processus audité</label>
            <select v-model="form.processus" required :class="UI.select">
              <option value="" disabled>Sélectionner...</option>
              <option v-for="p in PROCESSUS" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
          <div>
            <label :class="UI.label">Auditeur</label>
            <input v-model="form.auditeur" type="text" required :class="UI.input" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Date planifiée</label>
            <input v-model="form.date_planifiee" type="date" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Statut</label>
            <select v-model="form.statut" :class="UI.select">
              <option v-for="s in STATUTS_AUDIT" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>

        <div>
          <label :class="UI.label">Périmètre / objectif de l'audit</label>
          <textarea
            v-model="form.perimetre"
            rows="2"
            placeholder="Ex : conformité aux procédures, suivi des actions précédentes..."
            :class="UI.textarea"
          ></textarea>
        </div>

        <div>
          <label :class="UI.label">Date de réalisation</label>
          <input v-model="form.date_realisation" type="date" :class="UI.input + ' max-w-xs'" />
        </div>

        <div>
          <label :class="UI.label">Écarts / constats</label>
          <textarea
            v-model="form.constats"
            rows="3"
            placeholder="Synthèse des constats, écarts relevés, points forts..."
            :class="UI.textarea"
          ></textarea>
        </div>

        <div>
          <label :class="UI.label">Référence du rapport d'audit</label>
          <input v-model="form.rapport_reference" type="text" :class="UI.input" />
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Date de clôture de l'audit</label>
            <input v-model="form.date_cloture" type="date" :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Prochain audit prévu</label>
            <input v-model="form.prochain_audit" type="date" :class="UI.input" />
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
