// Cliente HTTP enxuto baseado em fetch. Inclui token, request id e
// erros tipados — sem axios pra manter o bundle pequeno.

const BASE = import.meta.env.VITE_API_URL ?? "/api";

export class ApiError extends Error {
  status: number;
  body: unknown;
  constructor(status: number, message: string, body?: unknown) {
    super(message);
    this.status = status;
    this.body = body;
  }
}

function getToken(): string | null {
  return localStorage.getItem("auth.token");
}

function newRequestId(): string {
  return crypto.randomUUID();
}

export async function api<T>(
  path: string,
  init: RequestInit & { auth?: boolean } = {},
): Promise<T> {
  const headers = new Headers(init.headers ?? {});
  headers.set("X-Request-Id", newRequestId());
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (init.auth !== false) {
    const t = getToken();
    if (t) headers.set("Authorization", `Bearer ${t}`);
  }

  const res = await fetch(`${BASE}${path}`, { ...init, headers });
  const text = await res.text();
  const body = text ? safeJson(text) : null;

  if (!res.ok) {
    throw new ApiError(res.status, (body as { detail?: string })?.detail ?? res.statusText, body);
  }
  return body as T;
}

function safeJson(s: string): unknown {
  try {
    return JSON.parse(s);
  } catch {
    return s;
  }
}
