import { createRouter, createWebHistory, type RouteLocationNormalized } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const Login = () => import("@/views/Login.vue");
const Home = () => import("@/views/Home.vue");
const Manual = () => import("@/views/Manual.vue");
const AdminLogs = () => import("@/views/AdminLogs.vue");
const AdminAuditLogs = () => import("@/views/AdminAuditLogs.vue");
const NotFound = () => import("@/views/NotFound.vue");
const Forbidden = () => import("@/views/Forbidden.vue");

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "login", component: Login, meta: { public: true } },
    { path: "/", name: "home", component: Home, meta: { requiresAuth: true } },
    { path: "/manual", name: "manual", component: Manual, meta: { requiresAuth: true } },
    {
      path: "/admin/logs",
      name: "admin-logs",
      component: AdminLogs,
      meta: { requiresAuth: true, roles: ["admin", "operator"] },
    },
    {
      path: "/admin/audit-logs",
      name: "admin-audit-logs",
      component: AdminAuditLogs,
      meta: { requiresAuth: true, roles: ["admin", "auditor"] },
    },
    { path: "/forbidden", name: "forbidden", component: Forbidden, meta: { public: true } },
    { path: "/:pathMatch(.*)*", name: "not-found", component: NotFound, meta: { public: true } },
  ],
});

router.beforeEach((to: RouteLocationNormalized) => {
  const auth = useAuthStore();
  if (to.meta.public) return true;
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login", query: { next: to.fullPath } };
  }
  if (to.meta.roles && !auth.hasAnyRole(to.meta.roles as string[])) {
    return { name: "forbidden" };
  }
  return true;
});
