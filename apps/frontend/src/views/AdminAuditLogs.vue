<script setup lang="ts">
import { onMounted, ref } from "vue";
import AppShell from "@/components/AppShell.vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Tag from "primevue/tag";
import { useToast } from "primevue/usetoast";
import { api } from "@/api/client";

interface AuditEvent {
  id: string; ts: string; actor: Record<string, unknown>;
  action: string; entity: Record<string, unknown>;
  before?: Record<string, unknown> | null;
  after?: Record<string, unknown> | null;
  outcome: string; reason?: string | null;
  requestId?: string | null; traceId?: string | null;
  prevHash?: string | null; hash: string;
}

const items = ref<AuditEvent[]>([]);
const loading = ref(false);
const action = ref<string>("");
const q = ref<string>("");
const toast = useToast();

async function load(): Promise<void> {
  loading.value = true;
  try {
    const params = new URLSearchParams();
    if (action.value) params.set("action", action.value);
    if (q.value) params.set("q", q.value);
    const res = await api<{ items: AuditEvent[] }>(`/admin/audit-logs?${params}`);
    items.value = res.items;
  } finally {
    loading.value = false;
  }
}

async function verify(): Promise<void> {
  const res = await api<{ ok: boolean; checked: number }>("/admin/audit-logs/verify");
  toast.add({
    severity: res.ok ? "success" : "error",
    summary: res.ok ? "Cadeia íntegra" : "Cadeia comprometida",
    detail: `${res.checked} eventos verificados`,
    life: 4000,
  });
}

onMounted(load);
</script>

<template>
  <AppShell>
    <h1>Auditoria</h1>
    <p class="muted">
      Trilha imutável de ações do usuário (append-only, hash chain).
      Para erros técnicos do sistema, ver <RouterLink to="/admin/logs">/admin/logs</RouterLink>.
    </p>

    <div class="filters">
      <InputText v-model="action" placeholder="action (ex.: auth.login)" />
      <InputText v-model="q" placeholder="Buscar (reason)" />
      <Button icon="pi pi-refresh" label="Atualizar" @click="load" />
      <Button icon="pi pi-shield" label="Verificar integridade" severity="secondary" @click="verify" />
    </div>

    <DataTable :value="items" :loading data-key="id" striped-rows>
      <Column field="ts" header="Quando">
        <template #body="{ data }">{{ new Date(data.ts).toLocaleString() }}</template>
      </Column>
      <Column header="Ator">
        <template #body="{ data }">{{ data.actor?.email ?? data.actor?.userId ?? "—" }}</template>
      </Column>
      <Column field="action" header="Ação" />
      <Column header="Entidade">
        <template #body="{ data }">{{ data.entity?.type }}/{{ data.entity?.id }}</template>
      </Column>
      <Column field="outcome" header="Resultado">
        <template #body="{ data }">
          <Tag :severity="data.outcome === 'ok' ? 'success' : 'danger'" :value="data.outcome" />
        </template>
      </Column>
      <Column field="reason" header="Motivo" />
      <Column header="Hash">
        <template #body="{ data }"><code class="hash">{{ data.hash.slice(0, 12) }}…</code></template>
      </Column>
    </DataTable>
  </AppShell>
</template>

<style scoped>
.muted { color: var(--p-text-muted-color); }
.filters { display: flex; gap: .5rem; flex-wrap: wrap; margin: 1rem 0; }
.hash { font-family: ui-monospace, SFMono-Regular, monospace; font-size: .85em; }
</style>
