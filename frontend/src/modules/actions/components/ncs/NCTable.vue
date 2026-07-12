<script setup>
import { ref } from "vue";
import { ChevronDown, ChevronRight } from "lucide-vue-next";
import StatusBadge from "./StatusBadge.vue";
import { UI } from "../../../dashboard/components/ui";
import { NC_TABLE_COLUMNS } from "../../constants/nonConformites";
import { formatDate } from "../../../../utils";
import { getActionStatutClass } from "../../utils/nonConformites";

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
          <th
            v-for="col in NC_TABLE_COLUMNS"
            :key="col"
            class="text-left px-4 py-3 font-semibold text-slate-500 uppercase text-xs tracking-wide whitespace-nowrap"
          >
            {{ col }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="NC_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Chargement…
          </td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="NC_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Aucune non-conformité. Cliquez sur « Ajouter une NC ».
          </td>
        </tr>
        <template v-for="item in items" :key="item._id">
          <tr
            class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer"
            @click="$emit('edit', item)"
          >
            <td class="px-4 py-3 font-medium text-slate-900 whitespace-nowrap">{{ item.numero_ref }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date) }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.source }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.service_impacte }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.description }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.gravite }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.action_curative || "-" }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.analyse_causes || "-" }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <button
                v-if="(item.actions_correctives || []).length > 0"
                class="flex items-center gap-1 text-blue-600 hover:text-blue-700 font-medium"
                @click="toggleExpand(item._id, $event)"
              >
                <component :is="expanded.has(item._id) ? ChevronDown : ChevronRight" class="w-4 h-4" />
                {{ item.actions_correctives.length }} action(s)
              </button>
              <span v-else class="text-slate-400">-</span>
            </td>
            <!--<td class="px-4 py-3 whitespace-nowrap">{{ item.pilote || "-" }}</td>-->
            <td class="px-4 py-3 whitespace-nowrap"><StatusBadge :statut="item.statut" /></td>
            <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_cloture) }}</td>
          </tr>
          <tr v-if="expanded.has(item._id)" class="bg-slate-50">
            <td :colspan="NC_TABLE_COLUMNS.length" class="px-4 py-3">
              <table class="w-full text-sm bg-white border border-slate-200 rounded-lg overflow-hidden">
                <thead>
                  <tr class="bg-slate-100 border-b border-slate-200">
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Descriptif de l'action corrective</th>
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Pilote</th>                   
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Échéance</th>                    
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Efficacité</th>
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Date de clôture</th>
                    <th class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs">Statut</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(action, idx) in item.actions_correctives"
                    :key="idx"
                    class="border-b border-slate-100 last:border-0"
                  >
                    <td class="px-3 py-2 max-w-md">{{ action.description || "-" }}</td>
                    <td class="px-3 py-2 whitespace-nowrap">{{ action.pilote || "-" }}</td>
                    <td class="px-3 py-2 whitespace-nowrap">{{ formatDate(action.date_objectif) }}</td>
                    <td class="px-3 py-2 max-w-md">{{ action.efficacite || "-" }}</td>
                    <td class="px-3 py-2 whitespace-nowrap">{{ formatDate(action.date_cloture) }}</td>
                    <td class="px-3 py-2 whitespace-nowrap">
                      <span :class="[UI.badge, getActionStatutClass(action.statut)]">
                        {{ action.statut }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
