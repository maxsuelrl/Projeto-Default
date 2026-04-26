import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { api } from "@/api/client";

interface JwtPayload {
  sub: string;
  role: string;
  exp: number;
}

function decodeJwt(token: string): JwtPayload | null {
  try {
    const [, payload] = token.split(".");
    return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/"))) as JwtPayload;
  } catch {
    return null;
  }
}

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(null);
  const userId = ref<string | null>(null);
  const role = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value);

  function hasAnyRole(roles: string[]): boolean {
    return !!role.value && roles.includes(role.value);
  }

  function hydrate(): void {
    const stored = localStorage.getItem("auth.token");
    if (!stored) return;
    const payload = decodeJwt(stored);
    if (!payload || payload.exp * 1000 < Date.now()) {
      localStorage.removeItem("auth.token");
      return;
    }
    token.value = stored;
    userId.value = payload.sub;
    role.value = payload.role;
  }

  async function login(email: string, password: string): Promise<void> {
    const res = await api<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      auth: false,
    });
    localStorage.setItem("auth.token", res.access_token);
    hydrate();
  }

  function logout(): void {
    localStorage.removeItem("auth.token");
    token.value = null;
    userId.value = null;
    role.value = null;
  }

  return { token, userId, role, isAuthenticated, hasAnyRole, hydrate, login, logout };
});
