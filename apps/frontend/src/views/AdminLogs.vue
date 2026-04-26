<script setup lang="ts">
import { onMounted, ref } from "vue";
import AppShell from "@/components/AppShell.vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Select from "primevue/select";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Tag from "primevue/tag";
import { api } from "@/api/client";

interface TechLog {
  id: string; ts: string; level: string; service: string; env: string;
  category: string; event: string; message: string; traceId?: string | null;
  userId?: string | null; requestId?: string | null; route?: string | null;
  method?: string | null; status?: number | null; latencyMs?: number | null;
  outcome?: string | null;
}

const items = ref<TechLog[]>([]);
const loading = ref(false);
const level = ref<string | null>(null);
const category = ref<string | null>(null);
const q = ref<string>("");

const levels = ["debug", "info", "warning", "error", "fatal"].map(v => ({ label: v, value: v }));
const categories = ["app", "security", "integration", "job"].map(v => ({ label: v, value: v }));

function levelSeverity(l: string): "secondary" | "info" | "warn" | "danger" | "contrast" {
  switch (l) {
    case "debug": return "secondary";
    case "info": return "info";
    case "warning": return "warn";
    case "error":
    case "fatal": return "danger";
    default: return "contrast";
  }
}

async function load(): Promise<void> {
  loading.value = true;
  try {
    const params = new URLSearchParams();
    if (level.value) params.set("level", level.value);
    if (category.value) params.set("category", category.value);
    if (q.value) params.set("q", q.value);
    const res = await api<{ items: TechLog[] }>(`/admin/logs?${params}`);
    items.value = res.items;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <AppShell>
    <h1>Logs técnicos</h1>
    <p class="muted">Erros, latência e requisições. Para ações do usuário, ver <RouterLink to="/admin/audit-logs">/admin/audit-logs</RouterLink>.</p>

    <div class="filters">
      <Select v-model="level" :options="levels" option-label="label" option-value="value" placeholder="Nível" show-clear />
      <Select v-model="category" :options="categories" option-label="label" option-value="value" placeholder="Categoria" show-clear />
      <InputText v-model="q" placeholder="Buscar (mensagem)" />
      <Button icon="pi pi-refresh" label="Atualizar" @click="load" />
    </div>

    <DataTable :value="items" :loading data-key="id" striped-rows>
      <Column field="ts" header="Quando">
        <template #body="{ data }">{{ new Date(data.ts).toLocaleString() }}</template>
      </Column>
      <Column field="level" header="Nível">
        <template #body="{ data }"><Tag :severity="levelSeverity(data.level)" :value="data.level" /></template>
      </Column>
      <Column field="service" header="Serviço" />
      <Column field="event" header="Evento" />
      <Column field="message" header="Mensagem" />
      <Column field="latencyMs" header="ms" />
      <Column field="status" header="HTTP" />
    </DataTable>
  </AppShell>
</template>

<style scoped>
.muted { color: var(--p-text-muted-color); }
.filters { display: flex; gap: .5rem; flex-wrap: wrap; margin: 1rem 0; }
</style>
