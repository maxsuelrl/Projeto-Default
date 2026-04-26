<script setup lang="ts">
import Button from "primevue/button";
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div class="page">
    <h1>403</h1>
    <p>Você não tem permissão para acessar esta área.</p>
    <Button icon="pi pi-home" label="Voltar" @click="router.push('/')" />
  </div>
</template>

<style scoped>
.page { min-height: 100vh; display: grid; place-items: center; gap: 1rem; }
</style>
