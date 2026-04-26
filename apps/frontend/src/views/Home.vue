<script setup lang="ts">
import AppShell from "@/components/AppShell.vue";
import Card from "primevue/card";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
</script>

<template>
  <AppShell>
    <h1>Bem-vindo</h1>
    <p>Você está autenticado como <strong>{{ auth.role }}</strong>.</p>
    <div class="cards">
      <Card>
        <template #title>Manual</template>
        <template #content>Documentação do produto, sempre embutida.</template>
      </Card>
      <Card v-if="auth.hasAnyRole(['admin', 'operator'])">
        <template #title>Logs técnicos</template>
        <template #content>Erros, latência e requisições do sistema.</template>
      </Card>
      <Card v-if="auth.hasAnyRole(['admin', 'auditor'])">
        <template #title>Auditoria</template>
        <template #content>Trilha imutável das ações dos usuários.</template>
      </Card>
    </div>
  </AppShell>
</template>

<style scoped>
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
</style>
