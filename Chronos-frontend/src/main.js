import PrimeVue from 'primevue/config';
import { createApp } from 'vue';
import App from './App.vue';
import Aura from '@primeuix/themes/aura';
import Nora from '@primeuix/themes/nora';
import Material from '@primeuix/themes/material';
import ToastService from 'primevue/toastservice';

import router from '@/router/index.js'
import store from '@/store';
import 'primeicons/primeicons.css'
import Ripple from 'primevue/ripple';
import "./assets/main.css";
import { definePreset } from '@primeuix/themes';

const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{slate.50}',
            100: '{slate.100}',
            200: '{slate.200}',
            300: '{slate.300}',
            400: '{slate.400}',
            500: '{slate.500}',
            600: '{slate.600}',
            700: '{slate.700}',
            800: '{slate.800}',
            900: '{slate.900}',
            950: '{slate.950}'
        }
    }
});

const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: MyPreset
    },
    options: {
        cssLayer: {
            name: 'primevue',
            order: 'theme, base, primevue'
        }
    },
    ripple: true,
    inputStyle: 'filled'
});
app.use(router)
app.use(store)
app.use(ToastService);

//app.directive('ripple', Ripple);


app.mount('#app')