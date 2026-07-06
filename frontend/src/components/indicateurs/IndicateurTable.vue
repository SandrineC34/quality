<script setup>
import { ref } from "vue";
import { ChevronDown, ChevronRight } from "lucide-vue-next";
import { UI } from "../../constants/ui";
import { INDICATEUR_TABLE_COLUMNS } from "../../constants/indicateurs";
import { getStatutClass, getPeriodeLabels } from "../../utils/indicateurs";

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
            v-for="col in INDICATEUR_TABLE_COLUMNS"
            :key="col"
            class="text-left px-4 py-3 font-semibold text-slate-500 uppercase text-xs tracking-wide whitespace-nowrap"
          >
            {{ col }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="INDICATEUR_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Chargement…
          </td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="INDICATEUR_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Aucun indicateur. Cliquez sur « Ajouter un indicateur ».
          </td>
        </tr>
        <template v-for="item in items" :key="item._id">
          <tr class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer" @click="$emit('edit', item)">
            <td class="px-4 py-3 whitespace-nowrap">{{ item.processus }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.reference_interne || "-" }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.reference_iso || "-" }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.description }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.unite }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.cible }}</td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.frequence }}</td>
            <!-- Clic sur le résultat annuel : ouvre le détail des relevés de la période -->
            <td class="px-4 py-3 whitespace-nowrap">
              <button
                class="flex items-center gap-1 text-blue-600 hover:text-blue-700 font-medium"
                @click="toggleExpand(item._id, $event)"
              >
                <component :is="expanded.has(item._id) ? ChevronDown : ChevronRight" class="w-4 h-4" />
                {{ item.resultat_annuel ?? "-" }}
              </button>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.ecart_cible ?? "-" }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="[UI.badge, getStatutClass(item.statut)]">{{ item.statut || "-" }}</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">{{ item.responsable || "-" }}</td>
            <td class="px-4 py-3 max-w-xs truncate">{{ item.commentaires || "-" }}</td>
          </tr>
          <tr v-if="expanded.has(item._id)" class="bg-slate-50">
            <td :colspan="INDICATEUR_TABLE_COLUMNS.length" class="px-4 py-3">
              <table class="w-full text-sm bg-white border border-slate-200 rounded-lg overflow-hidden">
                <thead>
                  <tr class="bg-slate-100 border-b border-slate-200">
                    <th
                      v-for="label in getPeriodeLabels(item.frequence)"
                      :key="label"
                      class="text-left px-3 py-2 font-semibold text-slate-500 uppercase text-xs"
                    >
                      {{ label }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td
                      v-for="(label, idx) in getPeriodeLabels(item.frequence)"
                      :key="label"
                      class="px-3 py-2 whitespace-nowrap"
                    >
                      {{ (item.valeurs || [])[idx] ?? "-" }}
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
