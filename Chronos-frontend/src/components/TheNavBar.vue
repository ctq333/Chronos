<template>
    <div class="card sticky" style="top: 0; z-index: 1000;">
        <Menubar :model="items">
        <template #start>
            <div class="w-10 h-10" width="35" height="40" fill="none">
                <router-link to="/"><img src="/logo.jpeg" alt="Logo" id="logo" /></router-link>
            </div>
        </template>

            <template #item="{ item, props, hasSubmenu, root }">
                <router-link
                    :to="item.url"
                    v-ripple
                    class="flex align-items-center"
                    v-bind="props.action"
                    style="text-decoration: none;"
                >
                    <span v-if="item.icon" :class="item.icon" />
                    <span class="ml-2">{{ item.label }}</span>
                    <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                    <i v-if="hasSubmenu" :class="['pi pi-angle-down', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
                </router-link>
            </template>

            <template #end>
                <div class="flex align-items-center gap-2">
                    
                    <div v-if="isLoggedIn">
                        <Button icon="pi pi-sign-out" severity="info" aria-label="User" label="Logout" @click="logout"></Button>
                    </div>
                    <div v-else>
                        <router-link to="/login">
                            <Button icon="pi pi-sign-in" severity="info" label="Login" aria-label="User"></Button>
                        </router-link>
                    </div>
                </div>
            </template>
        </Menubar>
    </div>
</template>

<script setup>
import { ref, computed, watchEffect } from "vue";
import { useRouter } from "vue-router";
import store from '@/store';
import Menubar from 'primevue/menubar';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Badge from 'primevue/badge';

// --- Search ---
const searchQuery = ref('');
const router = useRouter();
const isLoggedIn = store.getters.isLogin;
function onSearch() {
    if (searchQuery.value) {
        router.push({ path: '/search/' + searchQuery.value });
    }
}

// --- Logout ---
function logout() {
    store.dispatch('logout')
    router.push("/login")
}

// --- Menu Items (Auto-generated from your routes) ---
const items = computed(() => {
    const baseItems = [
        { label: 'Home', icon: 'pi pi-home', url: '/' },
        { label: 'Schedule', icon: 'pi pi-calendar', url: '/schedule' },
        { label: 'Tasks', icon: 'pi pi-list', url: '/tasks' },
        { label: 'Weekly Report', icon: 'pi pi-chart-bar', url: '/weekreport' },
        { label: 'Monthly Report', icon: 'pi pi-chart-line', url: '/monthreport' },
        { label: 'Incoming Events', icon: 'pi pi-bell', url: '/incomingevent' },
        { label: 'About', icon: 'pi pi-info-circle', url: '/about' },
    ];

    // Add admin entry only if admin is logged in
    if (store.getters.isAdmin) {
        baseItems.splice(1, 0, { label: 'Admin', icon: 'pi pi-cog', url: '/admin' });
    }

    // Hide Login/Signup if already logged in
    if (store.getters.isLogin) {
        return baseItems.filter(item => item.url !== '/login' && item.url !== '/signup');
    }
    return baseItems;
});
</script>

<style scoped>
#logo {
    height: 2.5rem;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
}
</style>