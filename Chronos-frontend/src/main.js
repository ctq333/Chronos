import PrimeVue from 'primevue/config';
import { createApp } from 'vue';
import App from './App.vue';
import Aura from '@primeuix/themes/aura';
import Nora from '@primeuix/themes/nora';
import Material from '@primeuix/themes/material';

import router from '@/router/index.js'
import 'primeicons/primeicons.css'
import Ripple from 'primevue/ripple';
import "./assets/main.css";

const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Aura
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

//app.directive('ripple', Ripple);


app.mount('#app')