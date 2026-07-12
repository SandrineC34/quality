<script setup>
import { ref } from "vue";
import { ChevronDown, ChevronRight } from "lucide-vue-next";
import { UI } from "../../../dashboard/components/ui";
import { ACTIONS_TABLE_COLUMNS } from "../../constants/suiviActions";
import { formatDate } from "../../../../utils/";
import {
  getActionSuiviStatutClass,
  getEfficaciteClass,
  displayStatut,
} from "../../utils/suiviActions";

defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

defineEmits(["edit", "delete"]);

const expanded = ref(new Set());

function toggleExpand(id, event) {
  event.stopPropagation();
  const next = new Set(expanded.value);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  expanded.value = next;
}
</script>

<template>
  <div :class="[UI.card, 'overflow-x-auto']">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-slate-200">
          <th class="w-8"></th>
          <th
            v-for="col in ACTIONS_TABLE_COLUMNS"
            :key="col"
            class="text-left px-4 py-3 font-semibold text-slate-500 uppercase text-xs tracking-wide whitespace-nowrap"
          >
            {{ col }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="ACTIONS_TABLE_COLUMNS.length + 1" class="text-center px-4 py-10 text-slate-400">
            Chargement…
          </td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="ACTIONS_TABLE_COLUMNS.length + 1" class="text-center px-4 py-10 text-slate-400">
            Aucune action. Cliquez sur « Ajouter une action ».
          </td>
        </tr>
        <template v-for="item in items" :key="item._id">
          <tr
            class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer"
            @click="$emit('edit', item)"
          >
            <td class="px-2 py-3">
              <button class="text-slate-400 hover:text-slate-600" @click="toggleExpand(item._id, $event)">
                <component :is="expanded.has(item._id) ? ChevronDown : ChevronRight" class="w-4 h-4" />
              </button>
            </td>
            <td class="px-4 py-3 font-medium text-slate-900 whitespace-nowrap">{{ item.numero_ref }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_creation) }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              {{ item.origine }}<span v-if="item.origine_ref" class="text-slate-400"> ({{ item.origine_ref }})</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.type_action || "-" }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.description }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.responsable }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_prevue) }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="[UI.badge, getActionSuiviStatutClass(displayStatut(item))]">
                {{ displayStatut(item) }}
              </span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_cloture) }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="[UI.badge, getEfficaciteClass(item.resultat_efficacite)]">
                {{ item.resultat_efficacite || "Non évaluée" }}
              </span>
            </td>
          </tr>
          <tr v-if="expanded.has(item._id)" class="bg-slate-50">
            <td :colspan="ACTIONS_TABLE_COLUMNS.length + 1" class="px-4 py-3">
              <div class="grid grid-cols-2 gap-4 bg-white border border-slate-200 rounded-lg p-4 text-sm">
                <div>
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">Éléments de preuve</p>
                  <p class="text-slate-700 whitespace-pre-line">{{ item.preuves || "-" }}</p>
                </div>
                <div>
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">Priorité</p>
                  <p class="text-slate-700">{{ item.priorite || "-" }}</p>
                </div>
                <div>
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">
                    Critères de validation de l'efficacité
                  </p>
                  <p class="text-slate-700 whitespace-pre-line">{{ item.criteres_efficacite || "-" }}</p>
                </div>
                <div>
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">Date de mesure de l'efficacité</p>
                  <p class="text-slate-700">{{ formatDate(item.date_mesure_efficacite) }}</p>
                </div>
                <div class="col-span-2">
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">Commentaire sur l'efficacité</p>
                  <p class="text-slate-700 whitespace-pre-line">{{ item.commentaire_efficacite || "-" }}</p>
                </div>
                <div>
                  <p class="font-semibold text-slate-500 uppercase text-xs mb-1">Validé par</p>
                  <p class="text-slate-700">{{ item.valide_par || "-" }}</p>
                </div>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
