import PrimeVue from 'primevue/config';
import { createApp } from 'vue';
import App from './App.vue';
import Aura from '@primeuix/themes/aura';
import router from '@/router/index.js'
import 'primeicons/primeicons.css'
import Ripple from 'primevue/ripple';

const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(router)

//app.directive('ripple', Ripple);


app.mount('#app')