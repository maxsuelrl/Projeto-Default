<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { onMounted } from "vue";
import Toast from "primevue/toast";
import ConfirmDialog from "primevue/confirmdialog";

const auth = useAuthStore();

onMounted(() => {
  auth.hydrate();
});
</script>

<template>
  <Toast />
  <ConfirmDialog />
  <RouterView />
</template>
