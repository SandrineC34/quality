<script setup>
import Sidebar from "./layouts/Sidebar.vue";
</script>

<template>
  <div class="flex min-h-screen bg-slate-50">
    <Sidebar />
    <main class="flex-1 px-10 py-8">
      <router-view />
    </main>
  </div>
</template>
