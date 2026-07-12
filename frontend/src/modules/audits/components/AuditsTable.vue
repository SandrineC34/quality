<script setup>
import { UI } from "../../dashboard/components/ui";
import { AUDITS_TABLE_COLUMNS } from "../constants/audits";
import { formatDate } from "../../../utils/";
import { getAuditStatutClass } from "../utils/audits";

defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});

defineEmits(["edit", "delete"]);
</script>

<template>
  <div :class="[UI.card, 'overflow-x-auto']">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-slate-200">
          <th
            v-for="col in AUDITS_TABLE_COLUMNS"
            :key="col"
            class="text-left px-4 py-3 font-semibold text-slate-500 uppercase text-xs tracking-wide whitespace-nowrap"
          >
            {{ col }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="AUDITS_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Chargement…
          </td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="AUDITS_TABLE_COLUMNS.length" class="text-center px-4 py-10 text-slate-400">
            Aucun audit planifié. Cliquez sur « Planifier un audit ».
          </td>
        </tr>
        <tr
          v-for="item in items"
          :key="item._id"
          class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer"
          @click="$emit('edit', item)"
        >
          <td class="px-4 py-3 font-medium text-slate-900 whitespace-nowrap">{{ item.numero_ref }}</td>
          <td class="px-4 py-3 whitespace-nowrap">{{ item.processus }}</td>
          <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_planifiee) }}</td>
          <td class="px-4 py-3 whitespace-nowrap">{{ item.auditeur }}</td>
          <td class="px-4 py-3 max-w-xs truncate">{{ item.perimetre || "-" }}</td>
          <td class="px-4 py-3 whitespace-nowrap">
            <span :class="[UI.badge, getAuditStatutClass(item.statut)]">{{ item.statut }}</span>
          </td>
          <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_realisation) }}</td>
          <td class="px-4 py-3 max-w-xs truncate">{{ item.constats || "-" }}</td>
          <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.date_cloture) }}</td>
          <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(item.prochain_audit) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
