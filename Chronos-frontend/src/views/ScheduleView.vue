<template>
    <div class="schedule-wrapper">
      <div class="card" style="overflow: hidden; height: 100%;">
        <Splitter style="height: 100%;">
          <SplitterPanel class="flex" :size="16" :minSize="10">
            <div class="border-white w-full h-full">
              <Menu :model="items" style="--p-menu-border-color: transparent;" />
            </div>
          </SplitterPanel>
          <SplitterPanel class="flex items-center justify-center" :size="84">
            Panel 2
          </SplitterPanel>
        </Splitter>
      </div>
    </div>
  </template>
  
  <script setup>
  import Menu from 'primevue/menu';
  import Splitter from 'primevue/splitter';
  import SplitterPanel from 'primevue/splitterpanel';
  import { ref } from "vue";
  const items = ref([
      { label: 'New', icon: 'pi pi-plus' },
      { label: 'Search', icon: 'pi pi-search' }
  ]);
  </script>
  
  <style scoped>
  .schedule-wrapper {
    /* Adjust 56px to your navbar height */
    height: calc(100vh - 8vh);
    overflow: hidden;
  }
  .card {
    height: 100%;
    overflow: hidden;
  }
  </style>