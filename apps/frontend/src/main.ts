import { createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";
import ToastService from "primevue/toastservice";
import ConfirmationService from "primevue/confirmationservice";

import App from "./App.vue";
import { router } from "./router";
import "primeicons/primeicons.css";
import "./styles/tokens.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: "p",
      darkModeSelector: ".p-dark",
      cssLayer: false,
    },
  },
  ripple: true,
  locale: {
    accept: "Sim",
    reject: "Não",
    firstDayOfWeek: 0,
  },
});
app.use(ToastService);
app.use(ConfirmationService);

app.mount("#app");
