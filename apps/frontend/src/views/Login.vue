<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useAuthStore } from "@/stores/auth";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Button from "primevue/button";
import Card from "primevue/card";

const email = ref("");
const password = ref("");
const loading = ref(false);

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();
const toast = useToast();

async function submit(): Promise<void> {
  if (!email.value || !password.value) return;
  loading.value = true;
  try {
    await auth.login(email.value, password.value);
    const next = (route.query.next as string) || "/";
    router.push(next);
  } catch (e) {
    toast.add({
      severity: "error",
      summary: "Falha no login",
      detail: e instanceof Error ? e.message : "Erro inesperado",
      life: 4000,
    });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="login">
    <Card class="login-card">
      <template #title>
        Entrar
      </template>
      <template #content>
        <form
          class="form"
          @submit.prevent="submit"
        >
          <label class="field">
            <span>E-mail</span>
            <InputText
              v-model="email"
              type="email"
              autocomplete="email"
              required
            />
          </label>
          <label class="field">
            <span>Senha</span>
            <Password
              v-model="password"
              :feedback="false"
              toggle-mask
              required
            />
          </label>
          <Button
            type="submit"
            label="Entrar"
            :loading
            icon="pi pi-sign-in"
          />
        </form>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.login { min-height: 100vh; display: grid; place-items: center; padding: 1rem; }
.login-card { width: 100%; max-width: 420px; }
.form { display: grid; gap: 1rem; }
.field { display: grid; gap: .35rem; }
</style>
