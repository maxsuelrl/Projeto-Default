<script setup lang="ts">
import { onMounted, ref } from "vue";
import AppShell from "@/components/AppShell.vue";
import InputText from "primevue/inputtext";
import { api } from "@/api/client";

interface Section { id: string; title: string; order: string; }

const sections = ref<Section[]>([]);
const query = ref("");
const active = ref<string | null>(null);

const content: Record<string, string> = {
  "primeiros-passos":
    "Bem-vindo ao Projeto-Padrão. Este produto foi gerado a partir de um template versionado. Use o menu lateral para navegar.",
  "funcionalidades":
    "Cada release atualiza esta seção com as funcionalidades disponíveis. Em ambiente de produção, o conteúdo MDX é versionado em apps/frontend/src/manual/.",
  "atalhos":
    "Atalhos de teclado: G + L (logs), G + A (auditoria), / (busca).",
  "faq": "Perguntas frequentes serão listadas aqui.",
  "solucao-de-problemas": "Em caso de erro, abra o /admin/logs e procure pelo seu requestId.",
  "glossario": "Termos do domínio.",
  "privacidade":
    "Tratamento de dados pessoais conforme docs/PRIVACY-LGPD.md. Você pode exercer seus direitos do art. 18 em /me.",
  "suporte": "Contato do suporte: definido pelo projeto.",
};

onMounted(async () => {
  sections.value = await api<Section[]>("/manual/sections");
  active.value = sections.value[0]?.id ?? null;
});
</script>

<template>
  <AppShell>
    <header class="head">
      <h1>Manual</h1>
      <InputText
        v-model="query"
        placeholder="Buscar..."
        class="search"
      />
    </header>
    <div class="layout">
      <aside class="toc">
        <ul>
          <li
            v-for="s in sections"
            :key="s.id"
          >
            <button
              :class="{ active: active === s.id }"
              type="button"
              @click="active = s.id"
            >
              {{ s.title }}
            </button>
          </li>
        </ul>
      </aside>
      <article class="article">
        <h2 v-if="active">
          {{ sections.find(s => s.id === active)?.title }}
        </h2>
        <p v-if="active">
          {{ content[active] }}
        </p>
        <p v-else>
          Selecione uma seção.
        </p>
      </article>
    </div>
  </AppShell>
</template>

<style scoped>
.head { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.search { min-width: 240px; }
.layout { display: grid; grid-template-columns: 220px 1fr; gap: 2rem; margin-top: 1rem; }
.toc ul { list-style: none; padding: 0; margin: 0; display: grid; gap: .25rem; }
.toc button {
  width: 100%; text-align: left; background: transparent; border: 1px solid transparent;
  padding: .5rem .75rem; border-radius: 6px; cursor: pointer; color: inherit;
}
.toc button.active, .toc button:hover { background: var(--p-content-hover-background); }
.article { line-height: 1.6; }
@media (max-width: 720px) { .layout { grid-template-columns: 1fr; } }
</style>
