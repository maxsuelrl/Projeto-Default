import { describe, expect, it, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useAuthStore } from "@/stores/auth";

function fakeJwt(payload: Record<string, unknown>): string {
  const enc = (o: unknown) =>
    btoa(JSON.stringify(o)).replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");
  return `${enc({ alg: "HS256" })}.${enc(payload)}.sig`;
}

describe("auth store", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    localStorage.clear();
  });

  it("hidrata do localStorage quando token é válido", () => {
    const exp = Math.floor(Date.now() / 1000) + 3600;
    localStorage.setItem("auth.token", fakeJwt({ sub: "u1", role: "admin", exp }));
    const auth = useAuthStore();
    auth.hydrate();
    expect(auth.isAuthenticated).toBe(true);
    expect(auth.role).toBe("admin");
    expect(auth.hasAnyRole(["admin", "auditor"])).toBe(true);
  });

  it("descarta token expirado", () => {
    localStorage.setItem(
      "auth.token",
      fakeJwt({ sub: "u1", role: "admin", exp: Math.floor(Date.now() / 1000) - 10 }),
    );
    const auth = useAuthStore();
    auth.hydrate();
    expect(auth.isAuthenticated).toBe(false);
    expect(localStorage.getItem("auth.token")).toBeNull();
  });
});
