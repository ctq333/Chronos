<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router'
import TheNavBar from '@/components/TheNavBar.vue';
import Button from 'primevue/button';

const route = useRoute()

</script>

<template>
  <div class="app-layout">
    <TheNavBar v-if="!route.meta.hideNavBar" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh; /* ensures the layout fills the viewport */
  /*overflow: hidden;  prevent unwanted scroll */
}

.main-content {
  flex: 1 1 0%;
  min-height: 0; /* very important for flex children to avoid overflow */
  /*overflow: hidden;  prevents main-content from scrolling */
  /*background: #fafbfc;*/
}
</style>
