<script setup>
/* Décrit la fenêtre où créer ou modifier un indicateur qualité */

import { computed, reactive, watch } from "vue";
import { X } from "lucide-vue-next";
import { UI } from "../../constants/ui";
import { FREQUENCES, METHODES_CALCUL, SENS_CIBLE } from "../../constants/indicateurs";
import {
  emptyIndicateurForm,
  getPeriodeLabels,
  resizeValeurs,
  computeResultatAnnuel,
  computeEcart,
  computeStatut,
} from "../../utils/indicateurs";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  initialData: { type: Object, default: null },
  error: { type: String, default: null },
});

const emit = defineEmits(["update:modelValue", "submit"]);

const form = reactive(emptyIndicateurForm());

watch(
  () => props.modelValue,
  (open) => {
    if (open) {
      const source = props.initialData ? { ...props.initialData } : emptyIndicateurForm();
      // Copie pour ne pas modifier l'item du tableau tant que non enregistré
      source.valeurs = resizeValeurs(source.valeurs || [], source.frequence || "Mensuelle");
      Object.assign(form, source);
    }
  }
);

// Quand la fréquence change, on redimensionne les relevés en conservant les valeurs déjà saisies
watch(
  () => form.frequence,
  (frequence) => {
    form.valeurs = resizeValeurs(form.valeurs, frequence);
  }
);

const periodeLabels = computed(() => getPeriodeLabels(form.frequence));

// Aperçu du calcul en direct, avant enregistrement
const resultatAnnuel = computed(() => computeResultatAnnuel(form.valeurs, form.methode_calcul));
const ecartCible = computed(() => computeEcart(resultatAnnuel.value, Number(form.cible), form.sens_cible));
const statut = computed(() => computeStatut(ecartCible.value, Number(form.cible)));

function close() {
  emit("update:modelValue", false);
}

function handleSubmit() {
  const payload = {
    ...form,
    cible: form.cible === "" || form.cible === null ? null : Number(form.cible),
    valeurs: form.valeurs.map((v) => (v === "" || v === null || v === undefined ? null : Number(v))),
    resultat_annuel: resultatAnnuel.value,
    ecart_cible: ecartCible.value,
    statut: statut.value,
  };
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
          {{ initialData ? "Modifier l'indicateur" : "Nouvel indicateur" }}
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

        <div class="grid grid-cols-3 gap-5">
          <div>
            <label :class="UI.label">Processus impacté</label>
            <input v-model="form.processus" type="text" required :class="UI.input" placeholder="ex: Management" />
          </div>
          <div>
            <label :class="UI.label">Référence interne</label>
            <input v-model="form.reference_interne" type="text" :class="UI.input" placeholder="ex: IND-001" />
          </div>
          <div>
            <label :class="UI.label">Référence ISO 9001</label>
            <input v-model="form.reference_iso" type="text" :class="UI.input" placeholder="ex: 8.2 / 9.1.2" />
          </div>
        </div>

        <div>
          <label :class="UI.label">Description de l'indicateur</label>
          <textarea v-model="form.description" required rows="2" :class="UI.textarea"></textarea>
        </div>

        <div class="grid grid-cols-4 gap-5">
          <div>
            <label :class="UI.label">Unité</label>
            <input v-model="form.unite" type="text" :class="UI.input" placeholder="%, Nb..." />
          </div>
          <div>
            <label :class="UI.label">Cible</label>
            <input v-model="form.cible" type="number" step="any" required :class="UI.input" />
          </div>
          <div>
            <label :class="UI.label">Sens souhaité</label>
            <select v-model="form.sens_cible" :class="UI.select">
              <option v-for="s in SENS_CIBLE" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div>
            <label :class="UI.label">Méthode d'agrégation</label>
            <select v-model="form.methode_calcul" :class="UI.select">
              <option v-for="m in METHODES_CALCUL" :key="m" :value="m">{{ m }}</option>
            </select>
          </div>
        </div>

        <div>
          <label :class="UI.label">Fréquence de collecte</label>
          <select v-model="form.frequence" :class="UI.select + ' max-w-xs'">
            <option v-for="f in FREQUENCES" :key="f" :value="f">{{ f }}</option>
          </select>
        </div>

        <!-- Relevés périodiques : le nombre de champs affichés dépend de la fréquence choisie -->
        <div>
          <label :class="UI.label">Relevés ({{ periodeLabels.length }} période(s))</label>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="(label, idx) in periodeLabels" :key="label">
              <label :class="UI.labelSm">{{ label }}</label>
              <input v-model="form.valeurs[idx]" type="number" step="any" :class="UI.input" />
            </div>
          </div>
        </div>

        <!-- Aperçu du calcul, à titre indicatif avant enregistrement -->
        <div class="grid grid-cols-3 gap-5 bg-slate-50 border border-slate-200 rounded-lg p-4">
          <div>
            <p :class="UI.labelSm">Résultat annuel</p>
            <p class="font-semibold text-slate-900">{{ resultatAnnuel ?? "-" }}</p>
          </div>
          <div>
            <p :class="UI.labelSm">Écart vs cible</p>
            <p class="font-semibold text-slate-900">{{ ecartCible ?? "-" }}</p>
          </div>
          <div>
            <p :class="UI.labelSm">Statut</p>
            <p class="font-semibold text-slate-900">{{ statut ?? "-" }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-5">
          <div>
            <label :class="UI.label">Responsable</label>
            <input v-model="form.responsable" type="text" :class="UI.input" />
          </div>
        </div>

        <div>
          <label :class="UI.label">Commentaires</label>
          <textarea v-model="form.commentaires" rows="2" :class="UI.textarea"></textarea>
        </div>

        <div class="flex justify-end gap-3 pt-2">
          <button type="button" :class="UI.btnSecondary" @click="close">Annuler</button>
          <button type="submit" :class="UI.btnPrimary">Enregistrer</button>
        </div>
      </form>
    </div>
  </div>
</template>
