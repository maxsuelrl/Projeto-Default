<script setup lang="ts">
import Menubar from "primevue/menubar";
import Button from "primevue/button";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import { computed } from "vue";

const auth = useAuthStore();
const router = useRouter();

const items = computed(() => {
  const base = [
    { label: "Início", icon: "pi pi-home", command: () => router.push("/") },
    { label: "Manual", icon: "pi pi-book", command: () => router.push("/manual") },
  ];
  if (auth.hasAnyRole(["admin", "operator"])) {
    base.push({ label: "Logs", icon: "pi pi-list", command: () => router.push("/admin/logs") });
  }
  if (auth.hasAnyRole(["admin", "auditor"])) {
    base.push({
      label: "Auditoria",
      icon: "pi pi-shield",
      command: () => router.push("/admin/audit-logs"),
    });
  }
  return base;
});

function logout(): void {
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <div class="shell">
    <Menubar :model="items">
      <template #end>
        <Button icon="pi pi-sign-out" text severity="secondary" label="Sair" @click="logout" />
      </template>
    </Menubar>
    <main class="content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.shell { min-height: 100vh; display: flex; flex-direction: column; }
.content { flex: 1; padding: 1.5rem; max-width: 1400px; margin: 0 auto; width: 100%; }
</style>
